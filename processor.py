import os
from openai import OpenAI
from typing import Dict, Optional
import config
from notion_api import NotionClientWrapper
from google_drive_client import GoogleDriveClientWrapper  # type: ignore

class TaskProcessor:
    def __init__(self):
        self.openai_client = OpenAI(
            api_key=config.OPENAI_API_KEY,
            base_url=config.OPENAI_BASE_URL
        )
        self.notion = NotionClientWrapper()
        self.gdrive = GoogleDriveClientWrapper()
    
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
            
            score_text = response.choices[0].message.content.strip()
            score = int(score_text)
            return min(max(score, 0), 100)
        except Exception as e:
            print(f"Error calculating QA score: {e}")
            return 0
    
    def process_with_ai(self, task_description: str, task_type: str = "general") -> str:
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
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"AI processing failed: {str(e)}")
    
    def process_task(self, task: Dict) -> Dict:
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
        
        try:
            self.notion.log_activity(
                task_name=task_name,
                status="Processing",
                message=f"Started processing task: {task_name}"
            )
            
            self.notion.update_page(
                page_id=task_id,
                properties={"Status": {"select": {"name": "Processing"}}}
            )
            
            result = self.process_with_ai(task_description)
            
            qa_score = self.calculate_qa_score(result)
            
            cost = 0.02
            
            self.notion.update_page(
                page_id=task_id,
                properties={
                    "Status": {"select": {"name": "Completed"}},
                    "Trigger": {"checkbox": False}
                }
            )
            
            self.notion.log_activity(
                task_name=task_name,
                status="Success",
                message=f"Completed task: {task_name}",
                details=f"QA Score: {qa_score}, Cost: ${cost}"
            )
            
            self.notion.log_completed_job({
                'job_name': task_name,
                'qa_score': qa_score,
                'cost': cost,
                'status': 'Completed',
                'notes': f"Result: {result[:500]}..."
            })
            
            return {
                'success': True,
                'task_name': task_name,
                'qa_score': qa_score,
                'cost': cost
            }
            
        except Exception as e:
            error_msg = str(e)
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
                details=error_msg
            )
            
            return {
                'success': False,
                'task_name': task_name,
                'error': error_msg
            }
