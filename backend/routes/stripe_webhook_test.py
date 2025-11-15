"""
Temporary debug route to verify Stripe webhook payload reaches backend.
This MUST NOT alter any production logic.
"""

from flask import Blueprint, jsonify, request
import logging

log = logging.getLogger("levqor.stripe_webhook_test")

bp = Blueprint("stripe_webhook_test", __name__)


@bp.route("/webhook-test", methods=["POST"])
def webhook_test():
    """
    Temporary debug route to verify Stripe webhook payload reaches backend.
    Returns the received payload for verification.
    """
    data = request.json or {}
    log.info(f"stripe_webhook_test: Received payload: {data}")
    return jsonify({"received": True, "payload": data}), 200


@bp.route("/webhook-test", methods=["GET"])
def webhook_test_health():
    """Health check for test endpoint"""
    return jsonify({"ok": True, "message": "Stripe webhook test endpoint ready"}), 200
