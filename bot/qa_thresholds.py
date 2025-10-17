from typing import Dict, Optional
from bot.constants import QC_PASS_THRESHOLD

QA_DEFAULTS = {
    'Research': 95,
    'Drafting': 90,
    'Data-transform': 92,
    'Transcription': 88,
    'Other': 95
}

def get_qa_threshold(task_type: str, custom_target: Optional[float] = None) -> int:
    if custom_target is not None and custom_target > 0:
        return int(custom_target)
    
    return QC_PASS_THRESHOLD

def extract_task_type(properties: Dict) -> str:
    if 'Task Type' in properties:
        select_prop = properties['Task Type'].get('select')
        if select_prop:
            return select_prop.get('name', 'Other')
    return 'Other'

def extract_qa_target(properties: Dict) -> Optional[float]:
    if 'QA Target' in properties:
        number_prop = properties['QA Target'].get('number')
        if number_prop is not None:
            return number_prop
    return None
