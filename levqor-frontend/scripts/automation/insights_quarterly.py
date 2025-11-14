#!/usr/bin/env python3
"""
Automated Quarterly Insights Report Generation
Generates and uploads insights PDF to Google Drive
"""
import requests
import os
from datetime import datetime

def run():
    """Generate quarterly insights report"""
    api_base = os.environ.get("PUBLIC_API", "https://api.levqor.ai")
    
    try:
        print(f"🔄 Generating quarterly insights report at {datetime.utcnow().isoformat()}")
        
        response = requests.post(
            f"{api_base}/api/insights/report",
            timeout=60
        )
        
        response.raise_for_status()
        data = response.json()
        
        drive_link = data.get("drive_link", "")
        print(f"✅ Insights report generated successfully")
        print(f"📊 Drive Link: {drive_link}")
        print(f"📈 Revenue: ${data.get('kpis', {}).get('revenue', {}).get('total', 0):,.2f}")
        print(f"🔌 API Calls: {data.get('kpis', {}).get('api_usage', {}).get('calls', 0):,}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to generate insights report: {e}")
        return False

if __name__ == "__main__":
    run()
