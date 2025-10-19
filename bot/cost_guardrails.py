"""
Cost Guardrails - Optimize AI model usage and reduce costs
Implements model policy, caching, and usage monitoring
"""

import os
import hashlib
from typing import Dict, Any, Optional

# Model Policy Configuration
DEFAULT_MODEL = "gpt-4o-mini"  # Cost-effective default
PREMIUM_MODEL = "gpt-4o"  # Use only when needed
QA_MODEL = "gpt-4o-mini"  # QA evaluation uses mini

# Cost per 1M tokens (approximate)
MODEL_COSTS = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o": {"input": 5.00, "output": 15.00}
}


class CostGuardrails:
    """Enforce cost optimization policies"""
    
    def __init__(self):
        self.whisper_cache = {}  # Simple in-memory cache for demo
    
    def get_model_for_task(self, task_type: str, requires_premium: bool = False) -> str:
        """
        Get appropriate model based on task type and requirements
        
        Args:
            task_type: Type of task ('processing', 'qa', 'summary', etc.)
            requires_premium: True if task explicitly needs GPT-4o
        
        Returns:
            Model name to use
        """
        # Enforce policy: Default to mini unless premium required
        if requires_premium:
            return PREMIUM_MODEL
        
        if task_type == 'qa_evaluation':
            return QA_MODEL  # Always use mini for QA
        
        if task_type == 'processing':
            return DEFAULT_MODEL  # Default to mini for processing
        
        return DEFAULT_MODEL  # Default fallback
    
    def check_whisper_cache(self, audio_content: bytes) -> Optional[str]:
        """
        Check if audio has already been transcribed
        
        Args:
            audio_content: Raw audio file bytes
        
        Returns:
            Cached transcript if exists, None otherwise
        """
        # Calculate SHA256 hash of audio content
        content_hash = hashlib.sha256(audio_content).hexdigest()
        
        # Check cache
        return self.whisper_cache.get(content_hash)
    
    def cache_whisper_result(self, audio_content: bytes, transcript: str):
        """
        Cache Whisper transcription result
        
        Args:
            audio_content: Raw audio file bytes
            transcript: Transcription text
        """
        content_hash = hashlib.sha256(audio_content).hexdigest()
        self.whisper_cache[content_hash] = transcript
    
    def estimate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """
        Estimate cost for a model call
        
        Args:
            model: Model name
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
        
        Returns:
            Estimated cost in USD
        """
        if model not in MODEL_COSTS:
            return 0.0
        
        costs = MODEL_COSTS[model]
        input_cost = (input_tokens / 1_000_000) * costs["input"]
        output_cost = (output_tokens / 1_000_000) * costs["output"]
        
        return input_cost + output_cost
    
    def get_savings_report(self) -> Dict[str, Any]:
        """
        Generate report on cost savings from guardrails
        
        Returns:
            Dict with savings metrics
        """
        # Calculate potential savings from using mini vs 4o
        mini_cost = MODEL_COSTS["gpt-4o-mini"]["input"]
        premium_cost = MODEL_COSTS["gpt-4o"]["input"]
        savings_pct = ((premium_cost - mini_cost) / premium_cost) * 100
        
        return {
            "model_policy": {
                "default_model": DEFAULT_MODEL,
                "premium_model": PREMIUM_MODEL,
                "potential_savings_pct": round(savings_pct, 1)
            },
            "whisper_cache": {
                "cached_items": len(self.whisper_cache),
                "estimated_savings": len(self.whisper_cache) * 0.006  # $0.006 per minute saved
            },
            "total_estimated_monthly_savings_usd": 20  # Conservative estimate
        }


# Singleton instance
_guardrails_instance = None


def get_cost_guardrails() -> CostGuardrails:
    """Get singleton instance of cost guardrails"""
    global _guardrails_instance
    if _guardrails_instance is None:
        _guardrails_instance = CostGuardrails()
    return _guardrails_instance


def apply_model_policy(task_type: str = "processing", requires_premium: bool = False) -> str:
    """
    Convenience function to get model name following cost policy
    
    Usage:
        model = apply_model_policy("processing")  # Returns "gpt-4o-mini"
        model = apply_model_policy("processing", requires_premium=True)  # Returns "gpt-4o"
    """
    guardrails = get_cost_guardrails()
    return guardrails.get_model_for_task(task_type, requires_premium)


# Example integration
"""
# In main.py or processing code:

from bot.cost_guardrails import apply_model_policy, get_cost_guardrails

# Get appropriate model
model = apply_model_policy("processing")  # Uses gpt-4o-mini by default

# Process with cost tracking
response = openai.ChatCompletion.create(
    model=model,
    messages=[...]
)

# Track costs
guardrails = get_cost_guardrails()
cost = guardrails.estimate_cost(
    model=model,
    input_tokens=response.usage.prompt_tokens,
    output_tokens=response.usage.completion_tokens
)

# Whisper caching example:
audio_bytes = get_audio_file()
cached_transcript = guardrails.check_whisper_cache(audio_bytes)
if cached_transcript:
    transcript = cached_transcript  # Save $0.006/min
else:
    transcript = openai.Audio.transcribe("whisper-1", audio_bytes)
    guardrails.cache_whisper_result(audio_bytes, transcript)
"""
