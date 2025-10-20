#!/usr/bin/env python3
"""
Predictive Maintenance - AI-based risk forecasting
Predicts system failures within 24h and creates Notion tickets
"""
import json
import os
import psutil
import requests
from datetime import datetime, timezone, timedelta
from pathlib import Path
import statistics

OPENAI_API_KEY = os.getenv('AI_INTEGRATIONS_OPENAI_API_KEY', '')
OPENAI_BASE_URL = os.getenv('AI_INTEGRATIONS_OPENAI_BASE_URL', 'https://api.openai.com/v1')

def collect_historical_metrics(hours=24):
    """Collect historical system metrics"""
    metrics = {
        "cpu_samples": [],
        "memory_samples": [],
        "disk_samples": [],
        "error_count": 0,
        "webhook_failures": 0,
        "payment_failures": 0
    }
    
    # Current system metrics
    cpu = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    
    metrics["cpu_samples"].append(cpu)
    metrics["memory_samples"].append(memory)
    metrics["disk_samples"].append(disk)
    
    # Count recent errors
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    
    try:
        with open('logs/production_alerts.ndjson', 'r') as f:
            for line in f:
                try:
                    alert = json.loads(line)
                    if 'ts' in alert:
                        ts = datetime.fromisoformat(alert['ts'].replace('Z', '+00:00'))
                        if ts > cutoff:
                            if alert.get('severity') in ['CRITICAL', 'ERROR']:
                                metrics["error_count"] += 1
                            if 'webhook' in alert.get('event', '').lower():
                                metrics["webhook_failures"] += 1
                except:
                    continue
    except:
        pass
    
    try:
        with open('logs/finance.ndjson', 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get('event') == 'payment_failed':
                        if 'ts' in entry:
                            ts = datetime.fromisoformat(entry['ts'].replace('Z', '+00:00'))
                            if ts > cutoff:
                                metrics["payment_failures"] += 1
                except:
                    continue
    except:
        pass
    
    return metrics

def predict_risks_with_ai(metrics):
    """Use AI to predict potential failures"""
    if not OPENAI_API_KEY:
        return {
            "risk_level": "UNKNOWN",
            "predicted_failures": [],
            "note": "OpenAI API key not configured"
        }
    
    # Calculate averages
    cpu_avg = statistics.mean(metrics["cpu_samples"]) if metrics["cpu_samples"] else 0
    memory_avg = statistics.mean(metrics["memory_samples"]) if metrics["memory_samples"] else 0
    disk_avg = statistics.mean(metrics["disk_samples"]) if metrics["disk_samples"] else 0
    
    # Build prompt for AI
    prompt = f"""Analyze these system metrics and predict potential failures within 24 hours:

CPU Usage: {cpu_avg:.1f}%
Memory Usage: {memory_avg:.1f}%
Disk Usage: {disk_avg:.1f}%
Recent Errors (24h): {metrics['error_count']}
Webhook Failures (24h): {metrics['webhook_failures']}
Payment Failures (24h): {metrics['payment_failures']}

Based on these metrics, assess:
1. Overall risk level (LOW, MEDIUM, HIGH, CRITICAL)
2. Specific component failure predictions
3. Recommended preventive actions

Respond in JSON format:
{{
  "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
  "predicted_failures": ["component1", "component2"],
  "recommendations": ["action1", "action2"],
  "confidence": 0-100
}}
"""
    
    try:
        headers = {
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'gpt-4o-mini',
            'messages': [
                {'role': 'system', 'content': 'You are a predictive maintenance AI analyzing system metrics.'},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.3,
            'response_format': {'type': 'json_object'}
        }
        
        response = requests.post(
            f'{OPENAI_BASE_URL}/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            prediction = json.loads(result['choices'][0]['message']['content'])
            return prediction
        else:
            return {
                "risk_level": "UNKNOWN",
                "predicted_failures": [],
                "note": f"AI prediction failed: HTTP {response.status_code}"
            }
    except Exception as e:
        return {
            "risk_level": "UNKNOWN",
            "predicted_failures": [],
            "error": str(e)
        }

def create_notion_ticket(failure_type, risk_level):
    """Create Notion ticket for predicted failure"""
    # This would integrate with Notion API
    # For now, log to file
    ticket = {
        "ts": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "type": "predictive_maintenance_ticket",
        "failure_type": failure_type,
        "risk_level": risk_level,
        "status": "open",
        "created_by": "predictive_maintenance_ai"
    }
    
    os.makedirs('logs', exist_ok=True)
    with open('logs/maintenance_tickets.ndjson', 'a') as f:
        f.write(json.dumps(ticket) + '\n')
    
    return ticket

def run_predictive_maintenance():
    """Run predictive maintenance analysis"""
    maintenance_ts = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    print(f"[{maintenance_ts}] Running predictive maintenance...")
    
    # Collect metrics
    metrics = collect_historical_metrics(hours=24)
    
    # Predict risks with AI
    prediction = predict_risks_with_ai(metrics)
    
    # Build maintenance entry
    maintenance_entry = {
        "ts": maintenance_ts,
        "metrics": metrics,
        "prediction": prediction,
        "tickets_created": []
    }
    
    print(f"   Risk Level: {prediction.get('risk_level', 'UNKNOWN')}")
    print(f"   Predicted Failures: {len(prediction.get('predicted_failures', []))}")
    
    # Create tickets for high-risk failures
    if prediction.get('risk_level') in ['HIGH', 'CRITICAL']:
        for failure in prediction.get('predicted_failures', []):
            ticket = create_notion_ticket(failure, prediction['risk_level'])
            maintenance_entry["tickets_created"].append(ticket)
            print(f"   🎫 Created ticket for: {failure}")
    
    # Write to log
    with open('logs/predictive_maintenance.ndjson', 'a') as f:
        f.write(json.dumps(maintenance_entry) + '\n')
    
    return maintenance_entry

if __name__ == '__main__':
    result = run_predictive_maintenance()
    print(json.dumps(result, indent=2))
