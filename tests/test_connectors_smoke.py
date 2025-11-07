import os
import pytest
import requests

BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")


@pytest.mark.skipif(not os.environ.get("RESEND_API_KEY"), reason="RESEND_API_KEY not set")
def test_email_send():
    """Test email connector (always test if configured)"""
    response = requests.post(
        f"{BASE_URL}/actions/email.send",
        json={
            "to": "support@levqor.ai",
            "subject": "Smoke Test",
            "text": "This is a smoke test email from automated tests."
        },
        timeout=15
    )
    
    assert response.status_code in [200, 402], f"Expected 200 or 402, got {response.status_code}: {response.text}"
    
    if response.status_code == 200:
        data = response.json()
        assert data.get("status") == "sent", f"Expected status='sent', got {data}"


@pytest.mark.skipif(not os.environ.get("SLACK_WEBHOOK_URL"), reason="SLACK_WEBHOOK_URL not set")
def test_slack_send():
    """Test Slack connector if configured"""
    response = requests.post(
        f"{BASE_URL}/actions/slack.send",
        json={
            "text": "Smoke test from Levqor connectors"
        },
        timeout=15
    )
    
    assert response.status_code in [200, 402], f"Expected 200 or 402, got {response.status_code}: {response.text}"
    
    if response.status_code == 200:
        data = response.json()
        assert data.get("status") == "sent"


@pytest.mark.skipif(not os.environ.get("NOTION_API_KEY"), reason="NOTION_API_KEY not set")
def test_notion_create():
    """Test Notion connector if configured"""
    database_id = os.environ.get("NOTION_TEST_DATABASE_ID")
    if not database_id:
        pytest.skip("NOTION_TEST_DATABASE_ID not set")
    
    response = requests.post(
        f"{BASE_URL}/actions/notion.create",
        json={
            "database_id": database_id,
            "props": {
                "Name": {
                    "title": [{"text": {"content": "Smoke Test"}}]
                }
            }
        },
        timeout=15
    )
    
    assert response.status_code in [200, 402]
    
    if response.status_code == 200:
        data = response.json()
        assert data.get("status") == "created"
        assert "id" in data


@pytest.mark.skipif(
    not (os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON") and os.environ.get("GOOGLE_SHEETS_SPREADSHEET_ID")),
    reason="Google Sheets env vars not set"
)
def test_sheets_append():
    """Test Google Sheets connector if configured"""
    response = requests.post(
        f"{BASE_URL}/actions/sheets.append",
        json={
            "range": "Sheet1!A1:C1",
            "values": [["Smoke Test", "2025-01-07", "OK"]]
        },
        timeout=15
    )
    
    assert response.status_code in [200, 402]
    
    if response.status_code == 200:
        data = response.json()
        assert data.get("status") == "appended"


@pytest.mark.skipif(not os.environ.get("TELEGRAM_BOT_TOKEN"), reason="TELEGRAM_BOT_TOKEN not set")
def test_telegram_send():
    """Test Telegram connector if configured"""
    chat_id = os.environ.get("TELEGRAM_CHAT_ID_DEFAULT")
    if not chat_id:
        pytest.skip("TELEGRAM_CHAT_ID_DEFAULT not set")
    
    response = requests.post(
        f"{BASE_URL}/actions/telegram.send",
        json={
            "text": "Smoke test from Levqor connectors"
        },
        timeout=15
    )
    
    assert response.status_code in [200, 402]
    
    if response.status_code == 200:
        data = response.json()
        assert data.get("status") == "sent"


def test_health():
    """Test actions health endpoint (always runs)"""
    response = requests.get(f"{BASE_URL}/actions/health", timeout=5)
    
    assert response.status_code == 200
    data = response.json()
    
    assert "connectors" in data
    assert "configured" in data
    assert "total" in data
    assert data["total"] == 5
    
    for connector in ["slack", "notion", "sheets", "telegram", "email"]:
        assert connector in data["connectors"]
