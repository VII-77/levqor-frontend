"""
Utility functions for EchoPilot
Helper functions for cleaner code and better maintainability
"""

from typing import Dict, Optional, Any
import time
from functools import wraps
from bot.constants import RETRY_DELAY_SECONDS, RETRY_BACKOFF_MULTIPLIER, MAX_RETRIES

def extract_notion_property(properties: Dict, property_name: str, property_type: str = 'title') -> str:
    """
    Safely extract a property value from Notion page properties
    
    Args:
        properties: Notion properties dict
        property_name: Name of the property to extract
        property_type: Type of property ('title', 'rich_text', 'select', etc.)
    
    Returns:
        Extracted string value or empty string if not found
    """
    if property_name not in properties:
        return ""
    
    prop_data = properties[property_name]
    
    if property_type == 'title':
        title_list = prop_data.get('title', [])
        if title_list:
            return title_list[0].get('text', {}).get('content', '')
    
    elif property_type == 'rich_text':
        text_list = prop_data.get('rich_text', [])
        if text_list:
            return text_list[0].get('text', {}).get('content', '')
    
    elif property_type == 'select':
        select_obj = prop_data.get('select', {})
        if select_obj:
            return select_obj.get('name', '')
    
    elif property_type == 'number':
        return prop_data.get('number', 0)
    
    return ""


def retry_on_failure(max_retries: int = MAX_RETRIES, delay: float = RETRY_DELAY_SECONDS):
    """
    Decorator to retry a function on failure with exponential backoff
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries (doubles each retry)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception: Exception = Exception("Unknown error")
            current_delay = delay
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        print(f"Retry {attempt + 1}/{max_retries} for {func.__name__}: {e}")
                        time.sleep(current_delay)
                        current_delay *= RETRY_BACKOFF_MULTIPLIER
                    else:
                        print(f"All retries exhausted for {func.__name__}: {e}")
            
            raise last_exception
        
        return wrapper
    return decorator


def calculate_cost(tokens_in: int, tokens_out: int, 
                   input_rate: Optional[float] = None, output_rate: Optional[float] = None) -> float:
    """
    Calculate the cost of an AI operation based on token usage
    
    Args:
        tokens_in: Number of input tokens
        tokens_out: Number of output tokens
        input_rate: Cost per input token (defaults to GPT-4o rate)
        output_rate: Cost per output token (defaults to GPT-4o rate)
    
    Returns:
        Total cost in USD
    """
    from bot.constants import GPT4O_INPUT_TOKEN_COST, GPT4O_OUTPUT_TOKEN_COST
    
    actual_input_rate = input_rate if input_rate is not None else GPT4O_INPUT_TOKEN_COST
    actual_output_rate = output_rate if output_rate is not None else GPT4O_OUTPUT_TOKEN_COST
    
    return (tokens_in * actual_input_rate) + (tokens_out * actual_output_rate)


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length with optional suffix
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def safe_int_conversion(value: Any, default: int = 0) -> int:
    """
    Safely convert a value to integer with fallback
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
    
    Returns:
        Integer value or default
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default
