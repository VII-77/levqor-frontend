#!/usr/bin/env python3
"""
Phase 42: AI-driven Revenue Intelligence
Analyzes live revenue trends & forecasts using GPT-4o-mini
"""
import os
import sys
import json
from datetime import datetime, timedelta

# Add bot to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def get_revenue_data():
    """Extract revenue from payment logs"""
    try:
        payments = []
        log_file = 'logs/payments_live.ndjson'
        
        if not os.path.exists(log_file):
            return []
        
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    if 'amount' in entry:
                        payments.append(entry['amount'])
                except:
                    continue
        
        return payments
    except:
        return []

def analyze_revenue():
    """Analyze revenue trends with AI"""
    try:
        from openai import OpenAI
        
        client = OpenAI(
            api_key=os.getenv('AI_INTEGRATIONS_OPENAI_API_KEY'),
            base_url=os.getenv('AI_INTEGRATIONS_OPENAI_BASE_URL')
        )
        
        payments = get_revenue_data()
        
        if len(payments) < 2:
            return {
                "ok": True,
                "trend": "insufficient_data",
                "ai_advice": "Need more payment data to analyze trends"
            }
        
        # Calculate recent trend
        recent = payments[-10:] if len(payments) >= 10 else payments
        previous = payments[-20:-10] if len(payments) >= 20 else payments[:len(payments)//2]
        
        recent_total = sum(recent)
        previous_total = sum(previous) if previous else 1
        
        change_pct = ((recent_total - previous_total) / max(previous_total, 1)) * 100
        trend_word = "increase" if change_pct > 0 else "decrease"
        
        # Get AI advice
        prompt = f"""Revenue Analysis:
- Recent total: ${recent_total:.2f}
- Previous period: ${previous_total:.2f}
- Change: {change_pct:+.1f}%
- Trend: {trend_word}

Provide 3 specific, actionable strategic recommendations for this revenue trend."""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        
        advice = response.choices[0].message.content
        
        # Log analysis
        log_entry = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "event": "revenue_intelligence",
            "recent_total": recent_total,
            "change_pct": change_pct,
            "trend": trend_word,
            "ai_advice": advice
        }
        
        os.makedirs('logs', exist_ok=True)
        with open('logs/revenue_intelligence.ndjson', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        return {
            "ok": True,
            "trend": f"{trend_word} of {abs(change_pct):.1f}%",
            "recent_total": recent_total,
            "change_pct": change_pct,
            "ai_advice": advice
        }
    
    except Exception as e:
        return {"ok": False, "error": str(e)}

if __name__ == "__main__":
    result = analyze_revenue()
    print(json.dumps(result, indent=2))
