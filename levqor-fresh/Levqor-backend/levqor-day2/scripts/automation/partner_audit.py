"""
Automated Partner Audit Job
Runs quarterly audits on all verified partners
"""
from modules.governance.audit import run_full_audit
from modules.governance.review_cycle import generate_review_report, send_review_notifications
from datetime import datetime

def run_quarterly_audit():
    """
    Run quarterly partner audit
    Checks compliance, sends notifications, and logs to Notion
    """
    print("=" * 60)
    print(f"🔍 PARTNER AUDIT - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # Run full audit
    audit_summary = run_full_audit()
    
    print(f"\n✅ Audited {audit_summary['total_partners_audited']} partners")
    print(f"   Compliant: {audit_summary['compliant']}")
    print(f"   Issues found: {audit_summary['issues_found']}")
    
    # Generate review cycle report
    review_report = generate_review_report()
    
    if review_report['partners_due_for_review'] > 0:
        print(f"\n📋 {review_report['partners_due_for_review']} partners due for review")
        
        if review_report['most_overdue']:
            print(f"   Most overdue: {review_report['most_overdue']['name']} ({review_report['most_overdue']['days_overdue']} days)")
        
        # Send review notifications
        sent = send_review_notifications()
        print(f"   Sent {sent} review notifications")
    else:
        print("\n✅ All partners up to date on reviews")
    
    print("=" * 60)
    
    return {
        "audit": audit_summary,
        "review_cycle": review_report
    }

if __name__ == "__main__":
    run_quarterly_audit()
