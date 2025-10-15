import time
from typing import Dict, List, Tuple
from bot.notion_api import NotionClientWrapper

QUEUE_SCHEMA = {
    'Task Name': 'title',
    'Description': 'rich_text',
    'Trigger': 'checkbox',
    'Status': 'select',
    'Task Type': 'select',
    'QA Target': 'number'
}

LOG_SCHEMA = {
    'Task': 'title',
    'Status': 'select',
    'Message': 'rich_text',
    'Details': 'rich_text',
    'Timestamp': 'date',
    'Commit': 'rich_text'
}

JOB_LOG_SCHEMA = {
    'Job Name': 'title',
    'QA Score': 'number',
    'Cost': 'number',
    'Status': 'select',
    'Notes': 'rich_text',
    'Timestamp': 'date',
    'Commit': 'rich_text',
    'Task Type': 'select',
    'Duration (ms)': 'number',
    'Tokens In': 'number',
    'Tokens Out': 'number'
}

class SchemaValidator:
    def __init__(self, notion: NotionClientWrapper):
        self.notion = notion
    
    def validate_and_repair_schema(self, database_id: str, expected_schema: Dict[str, str], db_name: str) -> Tuple[bool, List[str], List[str]]:
        changes = []
        errors = []
        
        try:
            client = self.notion.get_client()
            db = client.databases.retrieve(database_id=database_id)
            existing_props = db.get('properties', {})
            
            for prop_name, prop_type in expected_schema.items():
                if prop_name not in existing_props:
                    try:
                        if prop_type == 'select':
                            prop_def = {'select': {'options': []}}
                        elif prop_type == 'number':
                            prop_def = {'number': {'format': 'number'}}
                        elif prop_type == 'rich_text':
                            prop_def = {'rich_text': {}}
                        elif prop_type == 'checkbox':
                            prop_def = {'checkbox': {}}
                        elif prop_type == 'date':
                            prop_def = {'date': {}}
                        elif prop_type == 'title':
                            continue
                        else:
                            prop_def = {prop_type: {}}
                        
                        client.databases.update(
                            database_id=database_id,
                            properties={prop_name: prop_def}
                        )
                        changes.append(f"Added {prop_name} ({prop_type}) to {db_name}")
                        time.sleep(0.3)
                    except Exception as e:
                        errors.append(f"Failed to add {prop_name} to {db_name}: {str(e)}")
                else:
                    existing_type = existing_props[prop_name].get('type')
                    if existing_type != prop_type and prop_type != 'title':
                        errors.append(f"Type mismatch in {db_name}: {prop_name} is {existing_type}, expected {prop_type}")
            
            return len(errors) == 0, changes, errors
        
        except Exception as e:
            errors.append(f"Schema validation failed for {db_name}: {str(e)}")
            return False, changes, errors
    
    def validate_all_schemas(self, queue_id: str, log_id: str, job_id: str) -> Dict:
        all_changes = []
        all_errors = []
        
        ok1, changes1, errors1 = self.validate_and_repair_schema(queue_id, QUEUE_SCHEMA, "Queue")
        all_changes.extend(changes1)
        all_errors.extend(errors1)
        
        ok2, changes2, errors2 = self.validate_and_repair_schema(log_id, LOG_SCHEMA, "Log")
        all_changes.extend(changes2)
        all_errors.extend(errors2)
        
        ok3, changes3, errors3 = self.validate_and_repair_schema(job_id, JOB_LOG_SCHEMA, "Job Log")
        all_changes.extend(changes3)
        all_errors.extend(errors3)
        
        return {
            'schema_ok': ok1 and ok2 and ok3,
            'changed_properties': all_changes,
            'errors': all_errors
        }
