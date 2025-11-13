"""
Intelligence Monitor - Automated Intelligence Layer Execution
Runs all intelligence components on schedule
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from modules.auto_intel import collect_metrics, detect_anomalies, attempt_fix
from modules.decision_engine import analyze_trends
from modules.ai_advisor import generate_ai_insights
from modules.governance_ai import evaluate_risk
from modules.autoscale import check_load
from datetime import datetime

def run_intelligence_cycle():
    """
    Execute full intelligence monitoring cycle
    """
    print("=" * 60)
    print(f"🧠 INTELLIGENCE MONITOR - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # 1. Collect system metrics
    print("\n1️⃣ Collecting system metrics...")
    metrics = collect_metrics()
    
    # 2. Detect anomalies
    print("\n2️⃣ Detecting anomalies...")
    anomaly = detect_anomalies()
    
    if anomaly:
        print(f"   ⚠️ Anomaly detected: {anomaly['type']}")
        
        # 3. Attempt self-healing if needed
        print("\n3️⃣ Attempting self-heal...")
        attempt_fix(anomaly['type'], anomaly)
    else:
        print("   ✅ No anomalies detected")
    
    print("\n" + "=" * 60)
    print("✅ Intelligence cycle complete")
    print("=" * 60)

def run_weekly_analysis():
    """
    Execute weekly trend analysis and AI insights
    """
    print("=" * 60)
    print(f"📊 WEEKLY INTELLIGENCE ANALYSIS - {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 60)
    
    # 1. Analyze trends
    print("\n1️⃣ Analyzing trends...")
    trends = analyze_trends()
    print(f"   Generated {trends['recommendation_count']} recommendations")
    
    # 2. Generate AI insights
    print("\n2️⃣ Generating AI forecasts...")
    insights = generate_ai_insights()
    
    # 3. Evaluate governance risk
    print("\n3️⃣ Evaluating governance risk...")
    risk = evaluate_risk()
    print(f"   Risk Score: {risk['risk_score']}/100 ({risk['risk_level']})")
    
    print("\n" + "=" * 60)
    print("✅ Weekly analysis complete")
    print("=" * 60)
    
    return {
        "trends": trends,
        "insights": insights,
        "risk": risk
    }

def run_scaling_check():
    """
    Check system load and make scaling decisions
    """
    print("🔍 Checking system load...")
    load = check_load()
    
    if load.get('scaling_action'):
        print(f"   {load['scaling_action'].upper()}: {load.get('reason', 'N/A')}")
    else:
        print("   ✅ Load nominal - no scaling needed")
    
    return load

if __name__ == "__main__":
    run_intelligence_cycle()
