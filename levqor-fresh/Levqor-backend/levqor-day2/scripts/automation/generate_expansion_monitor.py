#!/usr/bin/env python3
"""
Generate EXPANSION-MONITOR.md
Auto-generated weekly report summarizing all expansion modules:
- Revenue by product
- Usage metrics
- Uptime & health
- Spend & margins
Commits file to repo every Friday
"""
import os
import sys
import requests
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


def collect_expansion_data():
    """Collect all expansion metrics"""
    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "week_ending": datetime.utcnow().date().isoformat(),
        "uptime": get_uptime_metrics(),
        "revenue": get_revenue_metrics(),
        "costs": get_cost_metrics(),
        "expansion": get_expansion_products(),
    }
    
    return data


def get_uptime_metrics():
    """Get uptime from public metrics"""
    try:
        response = requests.get("https://api.levqor.ai/public/metrics", timeout=10)
        
        if response.status_code == 200:
            metrics = response.json()
            return {
                "7d_percent": metrics.get("uptime_rolling_7d", 0.0),
                "30d_percent": metrics.get("uptime_rolling_30d", 0.0),
                "status": "healthy" if metrics.get("uptime_rolling_7d", 0) > 99.0 else "degraded",
            }
    except Exception as e:
        print(f"⚠️  Uptime metrics error: {str(e)}")
    
    return {"7d_percent": 0.0, "30d_percent": 0.0, "status": "unknown"}


def get_revenue_metrics():
    """Get revenue from Stripe"""
    stripe_key = os.getenv("STRIPE_SECRET_KEY", "").strip()
    
    if not stripe_key:
        return {"total": 0.0, "integrity": 0.0, "templates": 0.0, "api": 0.0}
    
    try:
        headers = {"Authorization": f"Bearer {stripe_key}"}
        week_ago = int((datetime.utcnow() - timedelta(days=7)).timestamp())
        params = {"created[gte]": week_ago, "limit": 100}
        
        response = requests.get(
            "https://api.stripe.com/v1/charges",
            headers=headers,
            params=params,
        )
        
        if response.status_code == 200:
            data = response.json()
            charges = data.get("data", [])
            paid_charges = [c for c in charges if c.get("paid")]
            
            total = sum(c["amount"] for c in paid_charges) / 100
            
            # Filter by product type
            integrity = sum(
                c["amount"] for c in paid_charges
                if "integrity" in c.get("description", "").lower()
            ) / 100
            
            templates = sum(
                c["amount"] for c in paid_charges
                if "template" in c.get("description", "").lower()
            ) / 100
            
            api = sum(
                c["amount"] for c in paid_charges
                if "api" in c.get("description", "").lower()
            ) / 100
            
            return {
                "total": total,
                "integrity": integrity,
                "templates": templates,
                "api": api,
            }
    except Exception as e:
        print(f"⚠️  Revenue metrics error: {str(e)}")
    
    return {"total": 0.0, "integrity": 0.0, "templates": 0.0, "api": 0.0}


def get_cost_metrics():
    """Get cost breakdown"""
    # Placeholder - would pull from cost_collector data
    return {
        "replit": 0.0,
        "stripe_fees": 0.0,
        "vercel": 0.0,
        "total": 0.0,
    }


def get_expansion_products():
    """Get expansion product metrics"""
    return {
        "integrity_runs": 0,  # From Notion DB
        "template_downloads": 0,  # From Notion DB
        "api_users": 0,  # From database
        "white_label_leads": 0,  # From Notion DB
    }


def generate_markdown_report(data):
    """Generate markdown report"""
    revenue = data["revenue"]
    costs = data["costs"]
    net_margin = revenue["total"] - costs["total"]
    margin_percent = (net_margin / revenue["total"] * 100) if revenue["total"] > 0 else 0
    
    report = f"""# Levqor Expansion Monitor
**Week Ending:** {data['week_ending']}  
**Generated:** {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}

---

## 📊 Overview

| Metric | Value | Status |
|--------|-------|--------|
| **7-Day Uptime** | {data['uptime']['7d_percent']:.2f}% | {data['uptime']['status'].upper()} |
| **Weekly Revenue** | ${revenue['total']:.2f} | {'🟢' if revenue['total'] > 0 else '⚪'} |
| **Net Margin** | ${net_margin:.2f} ({margin_percent:.1f}%) | {'🟢' if net_margin > 0 else '🔴'} |

---

## 💰 Revenue Breakdown

| Product | Revenue |
|---------|---------|
| **Integrity Pack** | ${revenue['integrity']:.2f} |
| **Template Packs** | ${revenue['templates']:.2f} |
| **API Tier** | ${revenue['api']:.2f} |
| **Total** | **${revenue['total']:.2f}** |

---

## 💸 Cost Breakdown

| Category | Cost |
|----------|------|
| Replit | ${costs['replit']:.2f} |
| Stripe Fees | ${costs['stripe_fees']:.2f} |
| Vercel | ${costs['vercel']:.2f} |
| **Total Costs** | **${costs['total']:.2f}** |

**Net Margin:** ${net_margin:.2f} ({margin_percent:.1f}%)

---

## 🚀 Expansion Products

| Product | Activity |
|---------|----------|
| Integrity Runs | {data['expansion']['integrity_runs']} |
| Template Downloads | {data['expansion']['template_downloads']} |
| API Users | {data['expansion']['api_users']} |
| White-Label Leads | {data['expansion']['white_label_leads']} |

---

## 🎯 Week-over-Week Trends

*Coming soon: Historical comparison charts*

---

## ⚡ Quick Actions

- [ ] Review failed integrity checks (if any)
- [ ] Follow up on white-label leads
- [ ] Analyze high-cost days
- [ ] Update pricing if margin < 30%

---

## 📝 Notes

Auto-generated by `scripts/automation/generate_expansion_monitor.py`  
Next update: {(datetime.utcnow() + timedelta(days=7)).strftime('%Y-%m-%d')}

---

**Status Legend:**
- 🟢 Healthy / Positive
- ⚪ Neutral / No data
- 🔴 Issue / Negative
"""
    
    return report


def write_report_to_file(report, filename="reports/EXPANSION-MONITOR.md"):
    """Write report to file"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w') as f:
        f.write(report)
    
    print(f"✅ Report written to: {filename}")
    return filename


def commit_to_repo(filename):
    """Commit report to git repo"""
    # Note: In production, this would use git commands to commit
    # For now, just print instructions
    print("\nℹ️  To commit this report to your repo:")
    print(f"   git add {filename}")
    print(f"   git commit -m 'Weekly expansion monitor - {datetime.utcnow().strftime('%Y-%m-%d')}'")
    print(f"   git push")


if __name__ == "__main__":
    print(f"📊 Generating Expansion Monitor - {datetime.utcnow().isoformat()}")
    
    # Collect data
    data = collect_expansion_data()
    
    # Generate report
    report = generate_markdown_report(data)
    
    # Write to file
    filename = write_report_to_file(report)
    
    # Show commit instructions
    commit_to_repo(filename)
    
    print("\n✅ Expansion monitor generated successfully")
    exit(0)
