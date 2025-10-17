import os
import json
import base64
import hmac
import hashlib
import time
import requests
import stripe

STRIPE_KEY = os.getenv("STRIPE_SECRET_KEY", "").strip()
STRIPE_WH_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "").strip()
PAYPAL_ID = os.getenv("PAYPAL_CLIENT_ID", "").strip()
PAYPAL_SEC = os.getenv("PAYPAL_SECRET", "").strip()
PAYPAL_LIVE = os.getenv("PAYPAL_LIVE", "true").lower() == "true"

CURRENCY = os.getenv("PAYMENT_CURRENCY", "USD").upper()
SUCCESS_URL = os.getenv("PAYMENT_SUCCESS_URL", "https://example.com/success")
CANCEL_URL = os.getenv("PAYMENT_CANCEL_URL", "https://example.com/cancel")
BRAND_NAME = os.getenv("PAYMENT_BRAND_NAME", "EchoPilot AI")


def stripe_create_checkout(amount_usd: float, job_id: str, client_email: str = None):
    if not STRIPE_KEY:
        raise RuntimeError("STRIPE_SECRET_KEY missing")
    stripe.api_key = STRIPE_KEY
    cents = int(round(amount_usd * 100))
    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": CURRENCY.lower(),
                "unit_amount": cents,
                "product_data": {"name": f"{BRAND_NAME} Job {job_id}"}
            },
            "quantity": 1
        }],
        customer_email=client_email or None,
        success_url=f"{SUCCESS_URL}?job={job_id}&status=success",
        cancel_url=f"{CANCEL_URL}?job={job_id}&status=cancel",
        metadata={"job_id": job_id}
    )
    return {
        "provider": "stripe",
        "amount": amount_usd,
        "currency": CURRENCY,
        "url": session.url,
        "id": session.id
    }


def stripe_parse_webhook(payload: bytes, sig_header: str):
    if not STRIPE_WH_SECRET:
        raise RuntimeError("STRIPE_WEBHOOK_SECRET missing")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WH_SECRET)
        typ = event["type"]
        data = event["data"]["object"]
        job_id = (data.get("metadata") or {}).get("job_id") or \
                 (data.get("payment_link") or {}).get("metadata", {}).get("job_id")
        status = None
        if typ in ("checkout.session.completed", "payment_intent.succeeded"):
            status = "Paid"
        elif typ in ("payment_intent.payment_failed", "checkout.session.expired"):
            status = "Cancelled"
        return {
            "ok": True,
            "provider": "stripe",
            "type": typ,
            "job_id": job_id,
            "status": status
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _paypal_base():
    host = "https://api-m.paypal.com" if PAYPAL_LIVE else "https://api-m.sandbox.paypal.com"
    return host


def paypal_token():
    auth = base64.b64encode(f"{PAYPAL_ID}:{PAYPAL_SEC}".encode()).decode()
    r = requests.post(
        _paypal_base() + "/v1/oauth2/token",
        headers={"Authorization": f"Basic {auth}"},
        data={"grant_type": "client_credentials"},
        timeout=20
    )
    r.raise_for_status()
    return r.json()["access_token"]


def paypal_create_order(amount_usd: float, job_id: str):
    token = paypal_token()
    body = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "reference_id": job_id,
            "amount": {"currency_code": CURRENCY, "value": f"{amount_usd:.2f}"},
            "description": f"{BRAND_NAME} Job {job_id}"
        }],
        "application_context": {
            "brand_name": BRAND_NAME,
            "return_url": f"{SUCCESS_URL}?job={job_id}&status=success",
            "cancel_url": f"{CANCEL_URL}?job={job_id}&status=cancel",
            "shipping_preference": "NO_SHIPPING",
            "user_action": "PAY_NOW"
        }
    }
    r = requests.post(
        _paypal_base() + "/v2/checkout/orders",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=body,
        timeout=20
    )
    r.raise_for_status()
    data = r.json()
    approve = next((l["href"] for l in data["links"] if l["rel"] == "approve"), None)
    return {
        "provider": "paypal",
        "amount": amount_usd,
        "currency": CURRENCY,
        "url": approve,
        "id": data["id"]
    }


def paypal_capture(order_id: str):
    token = paypal_token()
    r = requests.post(
        _paypal_base() + f"/v2/checkout/orders/{order_id}/capture",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        timeout=20
    )
    r.raise_for_status()
    return r.json()


def paypal_parse_webhook(body: dict):
    event_type = body.get("event_type")
    resource = body.get("resource", {})
    job_id = (resource.get("purchase_units") or [{}])[0].get("reference_id")
    status = None
    if event_type in ("CHECKOUT.ORDER.APPROVED", "PAYMENT.CAPTURE.COMPLETED"):
        status = "Paid"
    elif event_type in ("CHECKOUT.ORDER.CANCELLED", "PAYMENT.CAPTURE.DENIED"):
        status = "Cancelled"
    return {
        "ok": True,
        "provider": "paypal",
        "type": event_type,
        "job_id": job_id,
        "status": status
    }


def create_payment_link(amount_usd: float, job_id: str, client_email: str = None):
    if STRIPE_KEY:
        return stripe_create_checkout(amount_usd, job_id, client_email)
    elif PAYPAL_ID and PAYPAL_SEC:
        return paypal_create_order(amount_usd, job_id)
    else:
        raise RuntimeError("No payment provider configured")


def is_payment_configured():
    return bool(STRIPE_KEY or (PAYPAL_ID and PAYPAL_SEC))
