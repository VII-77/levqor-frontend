import time
import hashlib
from openai import OpenAI, OpenAIError, APITimeoutError, RateLimitError
from typing import Dict, Optional
from datetime import datetime
from bot import config
from bot.constants import (
    MODEL_GPT4O, MODEL_GPT4O_MINI,
    TEMP_PROCESSING, TEMP_QA_SCORING,
    MAX_TOKENS_PROCESSING, MAX_TOKENS_QA,
    OPENAI_TIMEOUT_SECONDS,
    QA_SCORE_MIN, QA_SCORE_MAX,
    NOTION_RICH_TEXT_LIMIT, JOB_RESULT_PREVIEW_LIMIT,
    QA_CONTENT_EVALUATION_LIMIT
)
from bot.utils import (
    extract_notion_property, 
    retry_on_failure, 
    calculate_cost, 
    truncate_text,
    safe_int_conversion
)
from bot.notion_api import NotionClientWrapper
from bot.google_drive_client import GoogleDriveClientWrapper
from bot.qa_thresholds import get_qa_threshold, extract_task_type, extract_qa_target
from bot.alerting import AlertManager
from bot.metrics import MetricsCollector

class TaskProcessor:
    def __init__(self, commit: str = "unknown", alert_manager: Optional[AlertManager] = None, metrics: Optional[MetricsCollector] = None):
        self.openai_client = OpenAI(
            api_key=config.OPENAI_API_KEY,
            base_url=config.OPENAI_BASE_URL,
            timeout=OPENAI_TIMEOUT_SECONDS
        )
        self.notion = NotionClientWrapper()
        self.gdrive = GoogleDriveClientWrapper()
        self.commit = commit
        self.alert_manager = alert_manager or AlertManager()
        self.metrics = metrics or MetricsCollector()
    
    @retry_on_failure(max_retries=2)
    def calculate_qa_score(self, content: str, criteria: Optional[Dict] = None) -> int:
        """
        Calculate quality assurance score for content
        Uses GPT-4o-mini with retry logic for reliability
        """
        try:
            truncated_content = truncate_text(content, QA_CONTENT_EVALUATION_LIMIT, "...")
            
            prompt = f"""
            Evaluate the following content on a scale of 0-100 based on quality criteria:
            - Clarity and coherence (30 points)
            - Accuracy and relevance (30 points)
            - Completeness (20 points)
            - Professional tone (20 points)
            
            Content: {truncated_content}
            
            Respond with ONLY a number between 0-100.
            """
            
            response = self.openai_client.chat.completions.create(
                model=MODEL_GPT4O_MINI,
                messages=[
                    {"role": "system", "content": "You are a quality assurance evaluator. Respond only with a number."},
                    {"role": "user", "content": prompt}
                ],
                temperature=TEMP_QA_SCORING,
                max_tokens=MAX_TOKENS_QA
            )
            
            score_text = response.choices[0].message.content
            if not score_text:
                return QA_SCORE_MIN
            
            score = safe_int_conversion(score_text.strip(), QA_SCORE_MIN)
            return min(max(score, QA_SCORE_MIN), QA_SCORE_MAX)
            
        except (RateLimitError, APITimeoutError) as e:
            print(f"OpenAI API error in QA scoring: {type(e).__name__} - {e}")
            raise
        except OpenAIError as e:
            print(f"OpenAI error calculating QA score: {e}")
            return QA_SCORE_MIN
        except Exception as e:
            print(f"Unexpected error calculating QA score: {e}")
            return QA_SCORE_MIN
    
    @retry_on_failure(max_retries=2)
    def process_with_ai(self, task_description: str, task_type: str = "general") -> tuple[str, int, int]:
        """
        Process task using AI with retry logic
        Returns: (result_text, tokens_in, tokens_out)
        """
        try:
            prompt = f"Task: {task_description}\n\nPlease complete this task professionally and thoroughly."
            
            response = self.openai_client.chat.completions.create(
                model=MODEL_GPT4O,
                messages=[
                    {"role": "system", "content": "You are EchoPilot, an AI automation assistant. Complete tasks accurately and professionally."},
                    {"role": "user", "content": prompt}
                ],
                temperature=TEMP_PROCESSING,
                max_tokens=MAX_TOKENS_PROCESSING
            )
            
            result = response.choices[0].message.content
            if not result:
                raise Exception("AI returned empty response")
            
            tokens_in = response.usage.prompt_tokens if response.usage else 0
            tokens_out = response.usage.completion_tokens if response.usage else 0
            
            return result, tokens_in, tokens_out
            
        except (RateLimitError, APITimeoutError) as e:
            raise Exception(f"OpenAI API error: {type(e).__name__} - {str(e)}")
        except OpenAIError as e:
            raise Exception(f"OpenAI processing error: {str(e)}")
        except Exception as e:
            raise Exception(f"AI processing failed: {str(e)}")
    
    def generate_idempotency_key(self, job_id: str, stage: str) -> str:
        """Generate idempotency key for safe retries"""
        return hashlib.sha256(f"{job_id}{stage}".encode()).hexdigest()
    
    def extract_task_properties(self, properties: Dict) -> tuple[str, str]:
        """Extract task name and description from Notion properties"""
        task_name = extract_notion_property(properties, 'Task Name', 'title') or 'Unnamed Task'
        task_description = extract_notion_property(properties, 'Description', 'rich_text') or ''
        return task_name, task_description
    
    def process_task(self, task: Dict) -> Dict:
        """
        Process a single task with comprehensive error handling and logging
        """
        start_time = time.time()
        task_id = task['id']
        properties = task.get('properties', {})
        
        task_name, task_description = self.extract_task_properties(properties)
        task_type = extract_task_type(properties)
        custom_qa_target = extract_qa_target(properties)
        qa_threshold = get_qa_threshold(task_type, custom_qa_target)
        
        try:
            self.notion.log_activity(
                task_name=task_name,
                status="Processing",
                message=f"Started processing task: {task_name}",
                details=f"Type: {task_type}, QA Threshold: {qa_threshold}",
                commit=self.commit
            )
            
            self.notion.update_page(
                page_id=task_id,
                properties={"Status": {"select": {"name": "Processing"}}}
            )
            
            result, tokens_in, tokens_out = self.process_with_ai(task_description, task_type)
            
            qa_score = self.calculate_qa_score(result)
            
            duration_ms = int((time.time() - start_time) * 1000)
            cost = calculate_cost(tokens_in, tokens_out)
            
            if qa_score < qa_threshold:
                return self._handle_qa_failure(
                    task_id, task_name, task_type, qa_score, qa_threshold,
                    cost, duration_ms, tokens_in, tokens_out
                )
            else:
                return self._handle_success(
                    task_id, task_name, task_type, result, qa_score, qa_threshold,
                    cost, duration_ms, tokens_in, tokens_out
                )
            
        except Exception as e:
            return self._handle_processing_error(
                task_id, task_name, task_type, str(e), 
                int((time.time() - start_time) * 1000)
            )
    
    def _handle_qa_failure(self, task_id: str, task_name: str, task_type: str, 
                          qa_score: int, qa_threshold: int, cost: float, 
                          duration_ms: int, tokens_in: int, tokens_out: int) -> Dict:
        """Handle task that needs human review due to low QA score"""
        failure_note = f"QA score {qa_score} below threshold {qa_threshold}"
        self.alert_manager.record_failure(task_name, task_type)
        self.metrics.record_failure(failure_note)
        
        self.notion.update_page(
            page_id=task_id,
            properties={
                "Status": {"select": {"name": "Waiting Human"}},
                "Trigger": {"checkbox": False}
            }
        )
        
        self.notion.log_activity(
            task_name=task_name,
            status="Review",
            message=f"Task needs human review: {task_name}",
            details=failure_note,
            commit=self.commit
        )
        
        try:
            self.notion.log_completed_job({
                'job_name': task_name,
                'qa_score': qa_score,
                'cost': cost,
                'status': 'Waiting Human',
                'notes': failure_note,
                'commit': self.commit,
                'task_type': task_type,
                'duration_ms': duration_ms,
                'tokens_in': tokens_in,
                'tokens_out': tokens_out
            })
        except Exception as e:
            print(f"Warning: Could not log to Job Log database: {e}")
        
        self.metrics.record_job({
            'timestamp': datetime.now(),
            'success': False,
            'error': failure_note,
            'qa_score': qa_score,
            'duration_ms': duration_ms,
            'cost': cost
        })
        
        return {
            'success': False,
            'task_name': task_name,
            'qa_score': qa_score,
            'error': failure_note
        }
    
    def _handle_success(self, task_id: str, task_name: str, task_type: str, 
                       result: str, qa_score: int, qa_threshold: int, cost: float,
                       duration_ms: int, tokens_in: int, tokens_out: int) -> Dict:
        """Handle successful task completion"""
        self.alert_manager.reset_failures(task_name)
        
        truncated_result = truncate_text(result, NOTION_RICH_TEXT_LIMIT, "")
        
        self.notion.update_page(
            page_id=task_id,
            properties={
                "Status": {"select": {"name": "Done"}},
                "Trigger": {"checkbox": False},
                "Result Summary": {"rich_text": [{"text": {"content": truncated_result}}]}
            }
        )
        
        self.notion.log_activity(
            task_name=task_name,
            status="Success",
            message=f"Completed task: {task_name}",
            details=f"QA Score: {qa_score}, Cost: ${cost:.4f}, Duration: {duration_ms}ms",
            commit=self.commit
        )
        
        result_preview = truncate_text(result, JOB_RESULT_PREVIEW_LIMIT, "...")
        
        try:
            self.notion.log_completed_job({
                'job_name': task_name,
                'qa_score': qa_score,
                'cost': cost,
                'status': 'Done',
                'notes': f"Result: {result_preview}",
                'commit': self.commit,
                'task_type': task_type,
                'duration_ms': duration_ms,
                'tokens_in': tokens_in,
                'tokens_out': tokens_out
            })
        except Exception as e:
            print(f"Warning: Could not log to Job Log database: {e}")
        
        self.metrics.record_job({
            'timestamp': datetime.now(),
            'success': True,
            'qa_score': qa_score,
            'duration_ms': duration_ms,
            'cost': cost
        })
        
        return {
            'success': True,
            'task_name': task_name,
            'qa_score': qa_score,
            'cost': cost,
            'duration_ms': duration_ms
        }
    
    def _handle_processing_error(self, task_id: str, task_name: str, 
                                 task_type: str, error_msg: str, 
                                 duration_ms: int) -> Dict:
        """Handle processing errors"""
        self.alert_manager.record_failure(task_name, task_type)
        self.metrics.record_failure(error_msg)
        
        self.notion.update_page(
            page_id=task_id,
            properties={
                "Status": {"select": {"name": "Failed"}},
                "Trigger": {"checkbox": False}
            }
        )
        
        self.notion.log_activity(
            task_name=task_name,
            status="Error",
            message=f"Failed to process task: {task_name}",
            details=error_msg,
            commit=self.commit
        )
        
        self.metrics.record_job({
            'timestamp': datetime.now(),
            'success': False,
            'error': error_msg,
            'duration_ms': duration_ms,
            'cost': 0
        })
        
        return {
            'success': False,
            'task_name': task_name,
            'error': error_msg
        }
