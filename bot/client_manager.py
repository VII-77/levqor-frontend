"""
Client Management & Revenue Tracking System
Manages clients, pricing tiers, revenue calculations, invoice generation, and delivery.
Integrates with existing Notion API and Gmail systems.
"""

import os
import datetime
import io
from typing import Optional, Dict, Any
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from bot.notion_api import get_notion_client


def get_client_db_id() -> str:
    """Get Client Database ID from environment."""
    return os.getenv("NOTION_CLIENT_DB_ID", "")


def create_client(
    name: str, 
    email: str, 
    rate_usd_per_min: float = 5.0,
    notes: str = ""
) -> tuple[int, dict]:
    """
    Create a new client in Notion Clients database.
    
    Args:
        name: Client name
        email: Client email address
        rate_usd_per_min: Billing rate in USD per minute (default: $5/min)
        notes: Additional notes about the client
        
    Returns:
        tuple: (status_code, response_dict)
    """
    notion = get_notion_client()
    client_db_id = get_client_db_id()
    
    if not client_db_id:
        return 400, {"error": "NOTION_CLIENT_DB_ID not configured"}
    
    try:
        properties = {
            "Client Name": {"title": [{"text": {"content": name}}]},
            "Email": {"email": email},
            "Rate USD/min": {"number": rate_usd_per_min},
            "Active": {"checkbox": True}
        }
        
        if notes:
            properties["Notes"] = {"rich_text": [{"text": {"content": notes}}]}
        
        response = notion.pages.create(
            parent={"database_id": client_db_id},
            properties=properties
        )
        
        return 200, {"success": True, "client_id": response["id"], "name": name}
    
    except Exception as e:
        return 500, {"error": str(e)}


def get_client_by_id(client_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve client information from Notion by client ID.
    
    Args:
        client_id: Notion page ID of the client
        
    Returns:
        dict with client info or None if not found
    """
    notion = get_notion_client()
    
    try:
        page = notion.pages.retrieve(page_id=client_id)
        props = page.get("properties", {})
        
        return {
            "id": client_id,
            "name": _extract_title(props.get("Client Name", {})),
            "email": props.get("Email", {}).get("email", ""),
            "rate": props.get("Rate USD/min", {}).get("number", 5.0),
            "active": props.get("Active", {}).get("checkbox", True)
        }
    
    except Exception as e:
        print(f"❌ Failed to retrieve client {client_id}: {e}")
        return None


def _extract_title(title_property: dict) -> str:
    """Extract text from Notion title property."""
    title_array = title_property.get("title", [])
    if title_array and len(title_array) > 0:
        return title_array[0].get("text", {}).get("content", "")
    return ""


def calculate_revenue(
    duration_minutes: float,
    client_rate_per_min: float,
    ai_cost_usd: float
) -> Dict[str, float]:
    """
    Calculate revenue metrics for a job.
    
    Args:
        duration_minutes: Job duration in minutes
        client_rate_per_min: Client's billing rate (USD/min)
        ai_cost_usd: AI processing cost in USD
        
    Returns:
        dict with gross, profit, and margin_percent
    """
    gross = round(duration_minutes * client_rate_per_min, 4)
    profit = round(gross - ai_cost_usd, 4)
    margin_percent = round((profit / gross * 100), 1) if gross > 0 else 0
    
    return {
        "gross": gross,
        "profit": profit,
        "margin_percent": margin_percent
    }


def generate_invoice_pdf(
    client_name: str,
    job_id: str,
    duration_minutes: float,
    rate_per_min: float,
    ai_cost: float,
    gross: float,
    profit: float,
    margin_percent: float,
    job_description: str = ""
) -> bytes:
    """
    Generate PDF invoice for a completed job.
    
    Args:
        client_name: Name of the client
        job_id: Notion job ID (truncated for display)
        duration_minutes: Job duration in minutes
        rate_per_min: Client's billing rate
        ai_cost: AI processing cost
        gross: Gross revenue
        profit: Net profit
        margin_percent: Profit margin percentage
        job_description: Optional job description
        
    Returns:
        bytes: PDF file content
    """
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    
    pdf.setFont("Helvetica-Bold", 16)
    y = 800
    pdf.drawString(50, y, "EchoPilot AI - Invoice")
    
    pdf.setFont("Helvetica", 10)
    y -= 20
    pdf.drawString(50, y, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    
    pdf.setFont("Helvetica", 12)
    y -= 40
    pdf.drawString(50, y, f"Client: {client_name}")
    
    y -= 25
    pdf.drawString(50, y, f"Job ID: ...{job_id[-8:]}")
    
    if job_description:
        y -= 25
        pdf.drawString(50, y, f"Description: {job_description[:60]}")
    
    y -= 40
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Job Details")
    
    pdf.setFont("Helvetica", 11)
    y -= 25
    pdf.drawString(70, y, f"Duration: {duration_minutes:.2f} minutes")
    
    y -= 20
    pdf.drawString(70, y, f"Rate: ${rate_per_min:.2f} USD/minute")
    
    y -= 30
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Financial Summary")
    
    pdf.setFont("Helvetica", 11)
    y -= 25
    pdf.drawString(70, y, f"Gross Revenue: ${gross:.2f} USD")
    
    y -= 20
    pdf.drawString(70, y, f"AI Processing Cost: ${ai_cost:.4f} USD")
    
    y -= 20
    pdf.drawString(70, y, f"Net Profit: ${profit:.2f} USD")
    
    y -= 20
    pdf.drawString(70, y, f"Profit Margin: {margin_percent:.1f}%")
    
    y -= 50
    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawString(50, y, "Thank you for using EchoPilot AI Automation Services!")
    
    y -= 60
    pdf.setFont("Helvetica", 8)
    pdf.drawString(50, y, "Questions? Contact us via your automation portal.")
    pdf.drawString(50, y - 15, "This is an automated invoice generated by EchoPilot AI.")
    
    pdf.showPage()
    pdf.save()
    
    buffer.seek(0)
    return buffer.getvalue()


def deliver_invoice_email(
    client_email: str,
    client_name: str,
    job_id: str,
    gross: float,
    profit: float,
    pdf_bytes: bytes
) -> bool:
    """
    Send invoice PDF via Gmail (using existing gmail_client).
    
    Args:
        client_email: Recipient email address
        client_name: Client name
        job_id: Job ID (truncated for display)
        gross: Gross revenue
        profit: Net profit
        pdf_bytes: PDF file content
        
    Returns:
        bool: True if sent successfully
    """
    try:
        from bot.gmail_client import send_email_with_attachment
        
        subject = f"[EchoPilot AI] Invoice - Job #{job_id[-8:]}"
        
        body = f"""Hello {client_name},

Your EchoPilot AI automation job has been completed successfully!

Job Summary:
• Job ID: ...{job_id[-8:]}
• Gross Revenue: ${gross:.2f} USD
• Net Profit: ${profit:.2f} USD

Please find your detailed invoice attached.

Thank you for using EchoPilot AI!

---
This is an automated message from EchoPilot AI.
"""
        
        result = send_email_with_attachment(
            to_email=client_email,
            subject=subject,
            body=body,
            attachment_data=pdf_bytes,
            attachment_filename="echopilot_invoice.pdf",
            attachment_mimetype="application/pdf"
        )
        
        if result:
            print(f"✅ Invoice delivered to {client_email}")
            return True
        else:
            print(f"❌ Failed to deliver invoice to {client_email}")
            return False
            
    except Exception as e:
        print(f"❌ Invoice delivery error: {e}")
        return False


def is_client_system_configured() -> bool:
    """Check if client system is configured."""
    return bool(get_client_db_id())


CLIENT_SYSTEM_AVAILABLE = is_client_system_configured()

print(f"💼 Client Management System: {'✅ Configured' if CLIENT_SYSTEM_AVAILABLE else '⚠️  Not configured (optional)'}")
