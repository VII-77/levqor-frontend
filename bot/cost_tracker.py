import os
import time


def now_s():
    """Get current timestamp in seconds"""
    return time.time()


def seconds_since(t0):
    """Calculate seconds elapsed since timestamp t0"""
    try:
        return round(max(0, time.time() - float(t0)), 3)
    except:
        return 0.0


def _parse_price(key, default):
    """Parse price from environment variable"""
    return float(os.getenv(key, default))


def read_price_env():
    """Read OpenAI pricing from environment variables with defaults"""
    return {
        "IN_1K": _parse_price("COST_GPT_IN_PER_1K_USD", "0.0025"),  # GPT-4o: $2.50 per 1M input = $0.0025 per 1K
        "OUT_1K": _parse_price("COST_GPT_OUT_PER_1K_USD", "0.01"),  # GPT-4o: $10 per 1M output = $0.01 per 1K
        "WHISPER_MIN": _parse_price("COST_WHISPER_PER_MIN_USD", "0.006"),  # Whisper: $0.006 per minute
    }


def estimate_cost(usage: dict | None = None, audio_seconds: float | None = None):
    """
    Calculate cost based on token usage and audio processing time.
    
    Args:
        usage: Dict with 'prompt_tokens' and 'completion_tokens' from OpenAI API
        audio_seconds: Duration of audio processed in seconds
        
    Returns:
        tuple: (cost in USD, total tokens used)
    """
    prices = read_price_env()
    cost = 0.0
    tokens = 0
    
    if usage:
        prompt_tokens = int(usage.get("prompt_tokens", 0))
        completion_tokens = int(usage.get("completion_tokens", 0))
        tokens = prompt_tokens + completion_tokens
        
        # Calculate cost based on token counts
        cost += (prompt_tokens / 1000) * prices["IN_1K"]
        cost += (completion_tokens / 1000) * prices["OUT_1K"]
    
    if audio_seconds and audio_seconds > 0:
        # Convert seconds to minutes for Whisper pricing
        cost += (audio_seconds / 60.0) * prices["WHISPER_MIN"]
    
    return round(cost, 6), tokens
