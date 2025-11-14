#!/usr/bin/env python3
"""
High-Risk Workflow Audit Script
Scans all existing workflows for prohibited content
Does NOT delete - only reports for manual review
"""
import os
import sys
import sqlite3
from datetime import datetime

# Add parent directory to path to import compliance modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compliance.high_risk_firewall import contains_high_risk_content


def audit_workflows():
    """
    Scan all workflows in the database for high-risk content
    
    Returns:
        dict with 'total', 'blocked', 'allowed', 'details'
    """
    db_path = os.environ.get('DATABASE_PATH', 'levqor.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all workflows (adjust table name if different)
        cursor.execute("""
            SELECT id, name, description, config, created_at
            FROM jobs
            ORDER BY created_at DESC
        """)
        
        workflows = cursor.fetchall()
        
        if not workflows:
            print("ℹ️  No workflows found in database")
            return {'total': 0, 'blocked': 0, 'allowed': 0, 'details': []}
        
        results = {
            'total': len(workflows),
            'blocked': 0,
            'allowed': 0,
            'details': []
        }
        
        print(f"\n🔍 Scanning {len(workflows)} workflows for high-risk content...\n")
        print("=" * 80)
        
        for workflow in workflows:
            wf_id, name, description, config, created_at = workflow
            
            # Combine all text fields for scanning
            combined_text = " ".join(filter(None, [
                str(name) if name else "",
                str(description) if description else "",
                str(config) if config else ""
            ]))
            
            # Check for high-risk content
            is_blocked, matched_terms = contains_high_risk_content(combined_text)
            
            if is_blocked:
                results['blocked'] += 1
                status = "🚫 BLOCKED"
                color = "\033[91m"  # Red
            else:
                results['allowed'] += 1
                status = "✅ OK"
                color = "\033[92m"  # Green
            
            reset_color = "\033[0m"
            
            # Print result
            print(f"{color}{status}{reset_color} | ID: {wf_id}")
            print(f"  Name: {name or '(No name)'}")
            
            if is_blocked:
                print(f"  ⚠️  Matched terms: {', '.join(matched_terms[:5])}")
                if len(matched_terms) > 5:
                    print(f"     (and {len(matched_terms) - 5} more...)")
            
            if description:
                desc_preview = description[:100]
                if len(description) > 100:
                    desc_preview += "..."
                print(f"  Description: {desc_preview}")
            
            print(f"  Created: {datetime.fromtimestamp(created_at).strftime('%Y-%m-%d %H:%M:%S') if created_at else 'Unknown'}")
            print("-" * 80)
            
            # Store details
            results['details'].append({
                'id': wf_id,
                'name': name,
                'blocked': is_blocked,
                'matched_terms': matched_terms if is_blocked else [],
                'created_at': created_at
            })
        
        conn.close()
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 AUDIT SUMMARY")
        print("=" * 80)
        print(f"Total workflows scanned: {results['total']}")
        print(f"✅ Allowed: {results['allowed']} ({results['allowed']/results['total']*100:.1f}%)")
        print(f"🚫 Blocked: {results['blocked']} ({results['blocked']/results['total']*100:.1f}%)")
        print("=" * 80)
        
        if results['blocked'] > 0:
            print(f"\n⚠️  {results['blocked']} workflow(s) contain prohibited content")
            print("   These workflows were created before blocking was enforced")
            print("   Recommendation: Review manually and contact users if needed")
        else:
            print("\n✅ All workflows are compliant - no action needed")
        
        return results
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return None


def export_blocked_workflows(results, filename='blocked_workflows_audit.txt'):
    """
    Export blocked workflows to a text file for review
    
    Args:
        results: Results dict from audit_workflows()
        filename: Output filename
    """
    if not results or results['blocked'] == 0:
        return
    
    try:
        with open(filename, 'w') as f:
            f.write("HIGH-RISK WORKFLOW AUDIT REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Total workflows scanned: {results['total']}\n")
            f.write(f"Blocked workflows: {results['blocked']}\n\n")
            
            f.write("BLOCKED WORKFLOWS:\n")
            f.write("-" * 80 + "\n")
            
            for detail in results['details']:
                if detail['blocked']:
                    f.write(f"\nWorkflow ID: {detail['id']}\n")
                    f.write(f"Name: {detail['name']}\n")
                    f.write(f"Matched terms: {', '.join(detail['matched_terms'])}\n")
                    f.write(f"Created: {datetime.fromtimestamp(detail['created_at']).strftime('%Y-%m-%d %H:%M:%S') if detail['created_at'] else 'Unknown'}\n")
                    f.write("-" * 80 + "\n")
        
        print(f"\n📄 Blocked workflows exported to: {filename}")
        
    except Exception as e:
        print(f"❌ Failed to export blocked workflows: {e}")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("HIGH-RISK WORKFLOW AUDIT")
    print("Levqor Compliance Scanner v1.0")
    print("=" * 80 + "\n")
    
    results = audit_workflows()
    
    if results and results['blocked'] > 0:
        export_blocked_workflows(results)
    
    print("\n✅ Audit complete\n")
