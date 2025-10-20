"""
AI Quality Management System (Boss Mode Phase 8)
- Centralized prompt templates
- Evaluation harness
- Version tracking
"""

import json
from datetime import datetime
from pathlib import Path

# ===== Prompt Templates =====
PROMPT_TEMPLATES = {
    "brief_processing_v1": {
        "version": "1.0",
        "created": "2025-10-15",
        "system": "You are an AI assistant that processes project briefs and generates detailed outputs.",
        "user_template": "Process this brief:\n\n{brief_text}\n\nProvide a detailed response.",
        "model": "gpt-4o",
        "temperature": 0.7,
        "max_tokens": 2000
    },
    "qa_evaluation_v1": {
        "version": "1.0",
        "created": "2025-10-15",
        "system": "You are a quality assurance evaluator. Score outputs on clarity, accuracy, completeness, and tone.",
        "user_template": "Evaluate this output:\n\n{output}\n\nProvide scores (0-100) for: clarity, accuracy, completeness, professional_tone",
        "model": "gpt-4o-mini",
        "temperature": 0.3,
        "max_tokens": 500
    },
    "code_generation_v1": {
        "version": "1.0",
        "created": "2025-10-20",
        "system": "You are an expert software engineer. Generate clean, production-ready code.",
        "user_template": "Generate code for:\n\n{requirements}\n\nLanguage: {language}\nFramework: {framework}",
        "model": "gpt-4o",
        "temperature": 0.5,
        "max_tokens": 3000
    }
}

def get_prompt(template_name, **variables):
    """Get a prompt template with variable substitution"""
    if template_name not in PROMPT_TEMPLATES:
        raise ValueError(f"Unknown prompt template: {template_name}")
    
    template = PROMPT_TEMPLATES[template_name]
    
    user_prompt = template["user_template"].format(**variables)
    
    return {
        "system": template["system"],
        "user": user_prompt,
        "model": template["model"],
        "temperature": template["temperature"],
        "max_tokens": template["max_tokens"],
        "version": template["version"]
    }

# ===== Evaluation Harness =====
def evaluate_output(output, expected_criteria=None):
    """
    Evaluate AI output quality
    Returns scores and overall pass/fail
    """
    if expected_criteria is None:
        expected_criteria = {
            "clarity": 80,
            "accuracy": 80,
            "completeness": 80,
            "professional_tone": 80
        }
    
    # Simplified evaluation - in production, use GPT-4o-mini
    scores = {
        "clarity": min(100, len(output) / 10),  # Placeholder logic
        "accuracy": 85,  # Would use actual evaluation
        "completeness": 90,
        "professional_tone": 85
    }
    
    overall_score = sum(scores.values()) / len(scores)
    passed = all(scores[k] >= v for k, v in expected_criteria.items())
    
    return {
        "scores": scores,
        "overall_score": overall_score,
        "passed": passed,
        "threshold": expected_criteria,
        "evaluated_at": datetime.utcnow().isoformat() + "Z"
    }

# ===== Version Tracking =====
def log_prompt_usage(template_name, input_vars, output, scores=None):
    """Log prompt usage for auditing and improvement"""
    log_path = Path(__file__).parent.parent / "logs" / "ndjson" / "prompt_usage.ndjson"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    entry = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "template": template_name,
        "version": PROMPT_TEMPLATES.get(template_name, {}).get("version", "unknown"),
        "input_length": sum(len(str(v)) for v in input_vars.values()),
        "output_length": len(output) if output else 0,
        "scores": scores
    }
    
    try:
        with open(log_path, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    except:
        pass

def get_prompt_stats():
    """Aggregate prompt usage statistics"""
    log_path = Path(__file__).parent.parent / "logs" / "ndjson" / "prompt_usage.ndjson"
    
    if not log_path.exists():
        return {"total_uses": 0, "by_template": {}}
    
    stats = {"total_uses": 0, "by_template": {}}
    
    try:
        with open(log_path) as f:
            for line in f:
                entry = json.loads(line)
                stats["total_uses"] += 1
                
                template = entry.get("template", "unknown")
                if template not in stats["by_template"]:
                    stats["by_template"][template] = {"count": 0, "avg_score": 0}
                
                stats["by_template"][template]["count"] += 1
                
                if entry.get("scores"):
                    scores = entry["scores"]
                    avg = sum(scores.values()) / len(scores) if scores else 0
                    stats["by_template"][template]["avg_score"] = avg
    except:
        pass
    
    return stats
