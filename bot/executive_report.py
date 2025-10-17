import os
import io
import datetime
import statistics
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from bot.gmail_client import GmailClientWrapper
from bot.notion_api import NotionClientWrapper

def summarize_7d():
    """Summarize job data from last 7 days"""
    notion = NotionClientWrapper()
    
    # Query job log database (get all jobs, no filter)
    from bot import config
    if not config.JOB_LOG_DB_ID:
        raise ValueError("JOB_LOG_DB_ID not configured")
    all_data = notion.query_database(config.JOB_LOG_DB_ID)
    
    # Filter to last 7 days in Python
    import datetime as dt
    seven_days_ago = dt.datetime.now() - dt.timedelta(days=7)
    data = []
    
    for item in all_data:
        try:
            date_prop = item.get("properties", {}).get("Date", {}).get("date", {})
            if date_prop and date_prop.get("start"):
                item_date = dt.datetime.fromisoformat(date_prop["start"].replace("Z", "+00:00"))
                if item_date >= seven_days_ago:
                    data.append(item)
        except:
            # Include items with no date or parsing errors
            data.append(item)
    total = len(data)
    done = 0
    qa = []
    cost = []
    gross = []
    unpaid = 0
    by_client = {}
    
    for p in data:
        prop = p["properties"]
        st = prop.get("Status", {}).get("select", {}).get("name", "")
        if st == "Done":
            done += 1
        
        q = prop.get("QA Score", {}).get("number")
        if q is not None:
            qa.append(q)
        
        c = prop.get("Cost USD", {}).get("number")
        cost.append(c or 0)
        
        g = prop.get("Gross USD", {}).get("number")
        gross.append(g or 0)
        
        pay = prop.get("Payment Status", {}).get("select", {}).get("name", "")
        if pay == "Unpaid":
            unpaid += 1
        
        client = prop.get("Client", {}).get("relation", [])
        cname = ("Client:" + client[0]["id"][-6:]) if client else "Client:Unknown"
        by_client[cname] = by_client.get(cname, 0) + (g or 0)
    
    avg_qa = round(statistics.mean([x for x in qa if isinstance(x, (int, float))]), 2) if qa else 0
    sum_cost = round(sum(cost), 2)
    sum_gross = round(sum(gross), 2)
    margin = round(((sum_gross - sum_cost) / sum_gross * 100), 1) if sum_gross > 0 else 0.0
    top = sorted(by_client.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        "total": total,
        "done": done,
        "avg_qa": avg_qa,
        "sum_cost": sum_cost,
        "sum_gross": sum_gross,
        "margin_pct": margin,
        "unpaid": unpaid,
        "top_clients": top
    }

def build_pdf(summary: dict) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%MZ")
    
    y = 820
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "EchoPilot — Daily Executive Report")
    y -= 22
    
    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Generated: {ts}")
    y -= 30
    
    lines = [
        f"Jobs (7d): {summary['total']}  |  Done: {summary['done']}",
        f"Avg QA: {summary['avg_qa']}   |  Gross (7d): ${summary['sum_gross']:.2f}  |  Cost: ${summary['sum_cost']:.2f}  |  Margin: {summary['margin_pct']}%",
        f"Unpaid invoices: {summary['unpaid']}",
        "Top Clients (by Gross):"
    ]
    
    for L in lines:
        c.drawString(40, y, L)
        y -= 18
    
    for name, amt in summary["top_clients"]:
        c.drawString(60, y, f"• {name} — ${amt:.2f}")
        y -= 16
    
    y -= 8
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(40, y, "Notes: Data from Notion Job Log (last 7 days). For details, open the EchoPilot Dashboard.")
    
    c.showPage()
    c.save()
    buf.seek(0)
    return buf.getvalue()

def email_pdf(pdf_bytes, summary):
    """Send executive report via Gmail API (no SMTP credentials needed)"""
    to = os.getenv("ALERT_TO")
    if not to:
        print("⚠️ No ALERT_TO email configured, skipping email send")
        return False
    
    # Use Gmail API via Replit Connector
    gmail = GmailClientWrapper()
    
    body = (
        f"Jobs(7d): {summary['total']}  Done: {summary['done']}  "
        f"Avg QA: {summary['avg_qa']}  Gross: ${summary['sum_gross']:.2f}  "
        f"Cost: ${summary['sum_cost']:.2f}  Margin: {summary['margin_pct']}%  "
        f"Unpaid: {summary['unpaid']}\n\n"
        f"See attached PDF for full executive report."
    )
    
    subject = f"[EchoPilot] Daily Executive Report — {datetime.date.today().isoformat()}"
    
    success = gmail.send_email_with_attachment(
        to_email=to,
        subject=subject,
        body=body,
        attachment_data=pdf_bytes,
        attachment_filename="EchoPilot_Daily_Executive_Report.pdf",
        attachment_mimetype="application/pdf"
    )
    
    if success:
        print(f"✅ Executive report sent to {to}")
    else:
        print(f"❌ Failed to send executive report to {to}")
    
    return success

def run_exec_report():
    """Generate and email daily executive report"""
    print("[ExecReport] Generating executive report...")
    s = summarize_7d()
    print(f"[ExecReport] Summary: {s['total']} jobs, {s['done']} done, ${s['sum_gross']:.2f} gross")
    
    pdf = build_pdf(s)
    print(f"[ExecReport] PDF generated ({len(pdf)} bytes)")
    
    email_pdf(pdf, s)
    
    return s

if __name__ == "__main__":
    print(run_exec_report())
