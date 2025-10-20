#!/usr/bin/env python3
"""
AI Ops Brain - Phase 40
Autonomous operational intelligence and improvement suggestions
"""
import os
import glob
import json
from datetime import datetime
from openai import OpenAI

def analyze_operations():
    """Use AI to analyze logs and suggest improvements"""
    # Initialize OpenAI client
    client = OpenAI(
        api_key=os.getenv("AI_INTEGRATIONS_OPENAI_API_KEY"),
        base_url=os.getenv("AI_INTEGRATIONS_OPENAI_BASE_URL")
    )
    
    # Gather context from recent logs
    context_lines = []
    summary_files = sorted(glob.glob("logs/*COMPLETE*.txt") + glob.glob("logs/PHASE*.txt"))
    
    for summary_file in summary_files[-5:]:  # Last 5 summary files
        try:
            with open(summary_file, "r") as f:
                context_lines.append(f"=== {os.path.basename(summary_file)} ===")
                context_lines.append(f.read()[:2000])  # First 2000 chars
        except:
            continue
    
    if not context_lines:
        context_lines = ["No operational summaries available yet."]
    
    context = "\n\n".join(context_lines)
    
    # Ask AI for operational insights
    system_prompt = """You are the EchoPilot Ops Brain, an AI system that analyzes operational data 
and suggests concrete improvements. Provide 3 specific, actionable recommendations based on the logs."""
    
    user_prompt = f"""Analyze these operational summaries:

{context}

Provide exactly 3 specific improvements we should implement next. Focus on:
1. Performance optimization
2. Cost reduction
3. User experience enhancement

Format each as: "Priority X: [Action] - [Expected Impact]"
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=400,
            temperature=0.7
        )
        
        plan = response.choices[0].message.content
        
        result = {
            "ok": True,
            "ts": datetime.utcnow().isoformat() + "Z",
            "plan": plan,
            "model": "gpt-4o-mini",
            "context_files": len(summary_files[-5:])
        }
        
        # Save to ops brain log
        os.makedirs("logs", exist_ok=True)
        brain_file = f"logs/ops_brain_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(brain_file, "w") as f:
            json.dump(result, f, indent=2)
        
        return result
        
    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
            "ts": datetime.utcnow().isoformat() + "Z"
        }

if __name__ == "__main__":
    result = analyze_operations()
    print(json.dumps(result, indent=2))
