#!/usr/bin/env python3
"""
AI Command Console - Natural language command interpreter for admin operations
Uses GPT-4o-mini with function calling to execute admin commands
"""
import json
import os
import sys
import requests
import subprocess
from datetime import datetime, timezone

OPENAI_API_KEY = os.getenv('AI_INTEGRATIONS_OPENAI_API_KEY', '')
OPENAI_BASE_URL = os.getenv('AI_INTEGRATIONS_OPENAI_BASE_URL', 'https://api.openai.com/v1')

SYSTEM_PROMPT = """You are EchoPilot Supervisor AI - a command interpreter for managing autonomous enterprise systems.

Your role:
- Maintain full operational awareness of EchoPilot systems
- Execute admin commands safely and accurately
- Alert Boss (Fahad) if anomalies exceed thresholds
- Always log all actions to logs/ai_console.ndjson

Available commands:
- show system status: Display current system health
- restart scheduler: Restart the scheduler process
- run audit: Execute final audit script
- analyze payments: Show payment metrics
- summarize kpis: Display key performance indicators
- forecast risk: Run predictive maintenance
- check slo: Show SLO compliance status
- view logs [logfile]: Show recent log entries

Safety rules:
- Never execute destructive commands without confirmation
- Log all actions
- Refuse unsafe operations
- Provide clear explanations

Respond in JSON format with:
{
  "command": "command_name",
  "action": "what you will do",
  "parameters": {},
  "requires_confirmation": true/false
}
"""

def execute_command(command, parameters=None):
    """Execute admin command"""
    parameters = parameters or {}
    result = {"command": command, "success": False}
    
    try:
        if command == "show_system_status":
            output = subprocess.check_output(['python3', 'scripts/telemetry_collector.py'], text=True)
            result["output"] = json.loads(output)
            result["success"] = True
        
        elif command == "run_audit":
            output = subprocess.check_output(['python3', 'scripts/final_audit.py'], text=True)
            result["output"] = output
            result["success"] = True
        
        elif command == "analyze_payments":
            with open('logs/finance.ndjson', 'r') as f:
                lines = f.readlines()[-20:]
            result["output"] = [json.loads(line) for line in lines if line.strip()]
            result["success"] = True
        
        elif command == "summarize_kpis":
            with open('logs/slo_report.json', 'r') as f:
                slo_data = json.load(f)
            result["output"] = {
                "slo_status": slo_data.get('overall_status'),
                "availability": slo_data.get('slos', {}).get('availability', {}),
                "latency": slo_data.get('slos', {}).get('p95_latency', {}),
                "webhooks": slo_data.get('slos', {}).get('webhook_success', {})
            }
            result["success"] = True
        
        elif command == "check_slo":
            with open('logs/slo_report.json', 'r') as f:
                result["output"] = json.load(f)
            result["success"] = True
        
        elif command == "forecast_risk":
            output = subprocess.check_output(['python3', 'scripts/predictive_maintenance.py'], text=True)
            result["output"] = output
            result["success"] = True
        
        elif command == "view_logs":
            logfile = parameters.get('logfile', 'logs/scheduler.log')
            with open(logfile, 'r') as f:
                lines = f.readlines()[-50:]
            result["output"] = lines
            result["success"] = True
        
        elif command == "restart_scheduler":
            result["output"] = "Restart scheduler command received (not implemented for safety)"
            result["success"] = False
            result["reason"] = "Requires manual intervention"
        
        else:
            result["output"] = f"Unknown command: {command}"
            result["success"] = False
    
    except Exception as e:
        result["error"] = str(e)
        result["success"] = False
    
    return result

def interpret_command(user_input):
    """Use AI to interpret natural language command"""
    if not OPENAI_API_KEY:
        return {
            "error": "OpenAI API key not configured",
            "command": None
        }
    
    try:
        headers = {
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'gpt-4o-mini',
            'messages': [
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': user_input}
            ],
            'temperature': 0.1,
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
            interpretation = json.loads(result['choices'][0]['message']['content'])
            return interpretation
        else:
            return {
                "error": f"AI interpretation failed: HTTP {response.status_code}",
                "command": None
            }
    except Exception as e:
        return {
            "error": str(e),
            "command": None
        }

def log_console_action(user_input, interpretation, execution_result):
    """Log AI console action"""
    log_entry = {
        "ts": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "user_input": user_input,
        "interpretation": interpretation,
        "execution": execution_result
    }
    
    os.makedirs('logs', exist_ok=True)
    with open('logs/ai_console.ndjson', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

def main():
    """Main AI command console"""
    print("="*80)
    print("EchoPilot Supervisor AI - Command Console")
    print("="*80)
    print()
    
    if len(sys.argv) > 1:
        # Command from args
        user_input = ' '.join(sys.argv[1:])
        print(f"Command: {user_input}")
        print()
    else:
        # Interactive mode
        print("Enter command (or 'exit' to quit):")
        user_input = input("> ").strip()
        
        if user_input.lower() in ['exit', 'quit']:
            return
    
    # Interpret command with AI
    print("🧠 Interpreting command...")
    interpretation = interpret_command(user_input)
    
    if interpretation.get('error'):
        print(f"❌ Error: {interpretation['error']}")
        return
    
    print(f"   Command: {interpretation.get('command', 'unknown')}")
    print(f"   Action: {interpretation.get('action', 'unknown')}")
    
    # Check if confirmation required
    if interpretation.get('requires_confirmation', False):
        print()
        print("⚠️  This command requires confirmation. Proceed? (y/n)")
        confirm = input("> ").strip().lower()
        if confirm != 'y':
            print("Command cancelled.")
            return
    
    # Execute command
    print()
    print("⚙️  Executing...")
    execution_result = execute_command(
        interpretation.get('command'),
        interpretation.get('parameters', {})
    )
    
    if execution_result['success']:
        print("✅ Success!")
        if execution_result.get('output'):
            if isinstance(execution_result['output'], dict):
                print(json.dumps(execution_result['output'], indent=2))
            else:
                print(execution_result['output'])
    else:
        print(f"❌ Failed: {execution_result.get('error', 'Unknown error')}")
    
    # Log action
    log_console_action(user_input, interpretation, execution_result)
    print()
    print("📝 Action logged to logs/ai_console.ndjson")

if __name__ == '__main__':
    main()
