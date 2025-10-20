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
    truncate_text,
    safe_int_conversion
)
from bot.cost_tracker import estimate_cost, now_s, seconds_since
from bot.notion_api import NotionClientWrapper
from bot.google_drive_client import GoogleDriveClientWrapper
from bot.qa_thresholds import get_qa_threshold, extract_task_type, extract_qa_target
from bot.alerting import AlertManager
# Metrics now handled via API endpoints

try:
    from bot.payments import create_payment_link, is_payment_configured
    PAYMENTS_AVAILABLE = True
except ImportError:
    PAYMENTS_AVAILABLE = False
    create_payment_link = None  # type: ignore
    is_payment_configured = None  # type: ignore
    print("[Processor] Payment module not available")

try:
    from bot.client_manager import (
        calculate_revenue, generate_invoice_pdf, 
        deliver_invoice_email, is_client_system_configured
    )
    CLIENT_SYSTEM_AVAILABLE = True
except ImportError:
    CLIENT_SYSTEM_AVAILABLE = False
    calculate_revenue = None  # type: ignore
    generate_invoice_pdf = None  # type: ignore
    deliver_invoice_email = None  # type: ignore
    is_client_system_configured = None  # type: ignore
    print("[Processor] Client management module not available")

class TaskProcessor:
    def __init__(self, commit: str = "unknown", alert_manager: Optional[AlertManager] = None, cost_guardrails: Optional[Dict] = None):
        self.openai_client = OpenAI(
            api_key=config.OPENAI_API_KEY,
            base_url=config.OPENAI_BASE_URL,
            timeout=OPENAI_TIMEOUT_SECONDS
        )
        self.notion = NotionClientWrapper()
        self.gdrive = GoogleDriveClientWrapper()
        self.commit = commit
        self.alert_manager = alert_manager or AlertManager()
        self.cost_guardrails = cost_guardrails or {}
    
    def _create_payment_link(self, job_name: str, cost: float, client_email: Optional[str] = None) -> Optional[Dict]:
        """Create payment link if payment provider is configured"""
        if not PAYMENTS_AVAILABLE:
            return None
        
        try:
            if not is_payment_configured():
                return None
            
            amount = cost * 3.0
            payment_info = create_payment_link(amount, job_name, client_email or "")
            print(f"[Payment] Created {payment_info['provider']} link for {job_name}: ${amount:.2f}")
            return payment_info
        except Exception as e:
            print(f"[Payment] Error creating payment link: {e}")
            return None
    
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
        task_name = extract_notion_property(properties, 'Job Name', 'title') or \
                   extract_notion_property(properties, 'Task Name', 'title') or 'Unnamed Task'
        task_description = extract_notion_property(properties, 'Description', 'rich_text') or ''
        return task_name, task_description
    
    def extract_client_info(self, properties: Dict) -> tuple[Optional[str], Optional[str], float]:
        """
        Extract client information from task properties.
        Returns: (client_id, client_email, rate_per_min)
        """
        import os
        
        client_id = None
        client_email = None
        default_rate = float(os.getenv("DEFAULT_RATE_USD_PER_MIN", "5.0"))
        
        if "Client" in properties and properties["Client"].get("relation"):
            relations = properties["Client"]["relation"]
            if relations and len(relations) > 0:
                client_id = relations[0].get("id")
        
        if "Client Email" in properties:
            client_email = properties["Client Email"].get("email")
        
        rate = default_rate
        if "Client Rate USD/min" in properties and properties["Client Rate USD/min"].get("number") is not None:
            rate = properties["Client Rate USD/min"]["number"]
        
        return client_id, client_email, rate
    
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
            
            # Use improved cost tracking
            usage = {"prompt_tokens": tokens_in, "completion_tokens": tokens_out}
            cost, total_tokens = estimate_cost(usage, audio_seconds=None)
            
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
        
        payment_info = self._create_payment_link(task_name, cost)
        
        job_data = {
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
        }
        
        if payment_info:
            job_data['payment_link'] = payment_info['url']
            job_data['payment_status'] = 'Unpaid'
        
        try:
            self.notion.log_completed_job(job_data)
        except Exception as e:
            print(f"Warning: Could not log to Job Log database: {e}")
        
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
        
        notion_client = self.notion.get_client()
        task = notion_client.pages.retrieve(page_id=task_id)
        properties = task.get('properties', {})
        client_id, client_email, client_rate = self.extract_client_info(properties)
        
        payment_info = self._create_payment_link(task_name, cost, client_email)
        
        job_data = {
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
        }
        
        if payment_info:
            job_data['payment_link'] = payment_info['url']
            job_data['payment_status'] = 'Unpaid'
        
        if CLIENT_SYSTEM_AVAILABLE:
            try:
                if is_client_system_configured():
                    duration_minutes = duration_ms / 60000.0
                    revenue = calculate_revenue(duration_minutes, client_rate, cost)
                    
                    job_data['client_rate_per_min'] = client_rate
                    job_data['gross_usd'] = revenue['gross']
                    job_data['profit_usd'] = revenue['profit']
                    job_data['margin_percent'] = revenue['margin_percent']
                    
                    if client_email:
                        try:
                            client_name = extract_notion_property(properties, 'Client Name', 'title') or task_name
                            pdf_bytes = generate_invoice_pdf(
                                client_name=client_name,
                                job_id=task_id,
                                duration_minutes=duration_minutes,
                                rate_per_min=client_rate,
                                ai_cost=cost,
                                gross=revenue['gross'],
                                profit=revenue['profit'],
                                margin_percent=revenue['margin_percent'],
                                job_description=task_name
                            )
                            
                            deliver_invoice_email(
                                client_email=client_email,
                                client_name=client_name,
                                job_id=task_id,
                                gross=revenue['gross'],
                                profit=revenue['profit'],
                                pdf_bytes=pdf_bytes
                            )
                        except Exception as e:
                            print(f"[Client] Invoice delivery failed: {e}")
            except Exception as e:
                print(f"[Client] Revenue tracking failed: {e}")
        
        try:
            self.notion.log_completed_job(job_data)
        except Exception as e:
            print(f"Warning: Could not log to Job Log database: {e}")
        
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
        
        return {
            'success': False,
            'task_name': task_name,
            'error': error_msg
        }
