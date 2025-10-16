import time
import hashlib
from openai import OpenAI
from typing import Dict, Optional
from datetime import datetime
from bot import config
from bot.notion_api import NotionClientWrapper
from bot.google_drive_client import GoogleDriveClientWrapper
from bot.qa_thresholds import get_qa_threshold, extract_task_type, extract_qa_target
from bot.alerting import AlertManager
from bot.metrics import MetricsCollector

class TaskProcessor:
    def __init__(self, commit: str = "unknown", alert_manager: Optional[AlertManager] = None, metrics: Optional[MetricsCollector] = None):
        self.openai_client = OpenAI(
            api_key=config.OPENAI_API_KEY,
            base_url=config.OPENAI_BASE_URL
        )
        self.notion = NotionClientWrapper()
        self.gdrive = GoogleDriveClientWrapper()
        self.commit = commit
        self.alert_manager = alert_manager or AlertManager()
        self.metrics = metrics or MetricsCollector()
    
    def calculate_qa_score(self, content: str, criteria: Optional[Dict] = None) -> int:
        try:
            prompt = f"""
            Evaluate the following content on a scale of 0-100 based on quality criteria:
            - Clarity and coherence (30 points)
            - Accuracy and relevance (30 points)
            - Completeness (20 points)
            - Professional tone (20 points)
            
            Content: {content[:1000]}
            
            Respond with ONLY a number between 0-100.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a quality assurance evaluator. Respond only with a number."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=10
            )
            
            score_text = response.choices[0].message.content
            if not score_text:
                return 0
            score = int(score_text.strip())
            return min(max(score, 0), 100)
        except Exception as e:
            print(f"Error calculating QA score: {e}")
            return 0
    
    def process_with_ai(self, task_description: str, task_type: str = "general") -> tuple[str, int, int]:
        try:
            prompt = f"Task: {task_description}\n\nPlease complete this task professionally and thoroughly."
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are EchoPilot, an AI automation assistant. Complete tasks accurately and professionally."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            result = response.choices[0].message.content
            if not result:
                raise Exception("AI returned empty response")
            
            tokens_in = response.usage.prompt_tokens if response.usage else 0
            tokens_out = response.usage.completion_tokens if response.usage else 0
            
            return result, tokens_in, tokens_out
        except Exception as e:
            raise Exception(f"AI processing failed: {str(e)}")
    
    def generate_idempotency_key(self, job_id: str, stage: str) -> str:
        return hashlib.sha256(f"{job_id}{stage}".encode()).hexdigest()
    
    def process_task(self, task: Dict) -> Dict:
        start_time = time.time()
        task_id = task['id']
        properties = task.get('properties', {})
        
        task_name = ""
        if 'Task Name' in properties:
            title_prop = properties['Task Name'].get('title', [])
            if title_prop:
                task_name = title_prop[0].get('text', {}).get('content', 'Unnamed Task')
        
        task_description = ""
        if 'Description' in properties:
            desc_prop = properties['Description'].get('rich_text', [])
            if desc_prop:
                task_description = desc_prop[0].get('text', {}).get('content', '')
        
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
            cost = (tokens_in * 0.00001 + tokens_out * 0.00003)
            
            if qa_score < qa_threshold:
                status = "Failed"
                failure_note = f"QA score {qa_score} below threshold {qa_threshold}"
                self.alert_manager.record_failure(task_name, task_type)
                self.metrics.record_failure(failure_note)
                
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
                    message=f"QA score below threshold: {task_name}",
                    details=failure_note,
                    commit=self.commit
                )
                
                try:
                    self.notion.log_completed_job({
                        'job_name': task_name,
                        'qa_score': qa_score,
                        'cost': cost,
                        'status': 'Failed',
                        'notes': failure_note,
                        'commit': self.commit,
                        'task_type': task_type,
                        'duration_ms': duration_ms,
                        'tokens_in': tokens_in,
                        'tokens_out': tokens_out
                    })
                except Exception as e:
                    print(f"Warning: Could not log to Job Log database: {e}")
                
                job_metrics = {
                    'timestamp': datetime.now(),
                    'success': False,
                    'error': failure_note,
                    'qa_score': qa_score,
                    'duration_ms': duration_ms,
                    'cost': cost
                }
                self.metrics.record_job(job_metrics)
                
                return {
                    'success': False,
                    'task_name': task_name,
                    'qa_score': qa_score,
                    'error': failure_note
                }
            
            else:
                self.alert_manager.reset_failures(task_name)
                
                self.notion.update_page(
                    page_id=task_id,
                    properties={
                        "Status": {"select": {"name": "Completed"}},
                        "Trigger": {"checkbox": False},
                        "Result Summary": {"rich_text": [{"text": {"content": result[:2000]}}]}
                    }
                )
                
                self.notion.log_activity(
                    task_name=task_name,
                    status="Success",
                    message=f"Completed task: {task_name}",
                    details=f"QA Score: {qa_score}, Cost: ${cost:.4f}, Duration: {duration_ms}ms",
                    commit=self.commit
                )
                
                try:
                    self.notion.log_completed_job({
                        'job_name': task_name,
                        'qa_score': qa_score,
                        'cost': cost,
                        'status': 'Completed',
                        'notes': f"Result: {result[:500]}...",
                        'commit': self.commit,
                        'task_type': task_type,
                        'duration_ms': duration_ms,
                        'tokens_in': tokens_in,
                        'tokens_out': tokens_out
                    })
                except Exception as e:
                    print(f"Warning: Could not log to Job Log database: {e}")
                
                job_metrics = {
                    'timestamp': datetime.now(),
                    'success': True,
                    'qa_score': qa_score,
                    'duration_ms': duration_ms,
                    'cost': cost
                }
                self.metrics.record_job(job_metrics)
                
                return {
                    'success': True,
                    'task_name': task_name,
                    'qa_score': qa_score,
                    'cost': cost,
                    'duration_ms': duration_ms
                }
            
        except Exception as e:
            error_msg = str(e)
            duration_ms = int((time.time() - start_time) * 1000)
            
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
            
            job_metrics = {
                'timestamp': datetime.now(),
                'success': False,
                'error': error_msg,
                'duration_ms': duration_ms,
                'cost': 0
            }
            self.metrics.record_job(job_metrics)
            
            return {
                'success': False,
                'task_name': task_name,
                'error': error_msg
            }
