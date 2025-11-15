"""
Stripe Integration Health Check
Verifies Stripe API connectivity and configured prices
"""

from flask import Blueprint, jsonify
import os
import time
import logging

logger = logging.getLogger("levqor.stripe_check")

stripe_check_bp = Blueprint("stripe_check", __name__, url_prefix="/api/stripe")


@stripe_check_bp.route("/check", methods=["GET"])
def stripe_check():
    """
    GET /api/stripe/check
    
    Returns comprehensive Stripe integration health check:
    - API key presence
    - Account retrieval
    - Configured price IDs verification
    
    Returns:
        200: All checks passed
        500: One or more checks failed (with detailed errors)
    """
    ts = int(time.time())
    
    checks = {
        "backend_alive": True,
        "stripe_api_key_present": False,
        "account_retrieved": False,
        "prices": {},
    }
    errors = []
    
    # Check for Stripe API key
    secret = os.getenv("STRIPE_SECRET_KEY", "").strip()
    
    if not secret:
        errors.append("STRIPE_SECRET_KEY missing from environment")
        logger.warning("stripe_check: STRIPE_SECRET_KEY not configured")
    else:
        checks["stripe_api_key_present"] = True
        
        # Only import stripe if we have a key
        try:
            import stripe
            stripe.api_key = secret
            
            # 1) Account retrieval check
            try:
                acct = stripe.Account.retrieve()
                checks["account_retrieved"] = True
                checks["account_id"] = acct.get("id", "unknown")
                checks["account_charges_enabled"] = bool(acct.get("charges_enabled"))
                
                if not acct.get("charges_enabled"):
                    errors.append("Stripe account has charges_enabled=false")
                    logger.warning(f"stripe_check: Account {acct.get('id')} charges disabled")
                
                logger.info(f"stripe_check: Account {acct.get('id')} retrieved successfully")
                
            except stripe.error.AuthenticationError as e:
                errors.append(f"stripe_account_auth_error: Invalid API key")
                logger.error(f"stripe_check: Authentication failed: {e}")
            except stripe.error.APIConnectionError as e:
                errors.append(f"stripe_account_connection_error: Cannot reach Stripe API")
                logger.error(f"stripe_check: Connection error: {e}")
            except Exception as e:
                errors.append(f"stripe_account_error: {type(e).__name__}")
                logger.error(f"stripe_check: Account retrieval failed: {e}")
            
            # 2) Price ID checks (only check env vars that exist)
            price_envs = [
                "STRIPE_PRICE_GROWTH",
                "STRIPE_PRICE_GROWTH_YEAR",
                "STRIPE_PRICE_BUSINESS",
                "STRIPE_PRICE_BUSINESS_YEAR",
                "STRIPE_PRICE_PRO",
                "STRIPE_PRICE_PRO_YEAR",
                "STRIPE_PRICE_STARTER",
                "STRIPE_PRICE_STARTER_YEAR",
                "STRIPE_PRICE_DFY_STARTER",
                "STRIPE_PRICE_DFY_PROFESSIONAL",
                "STRIPE_PRICE_DFY_ENTERPRISE",
                "STRIPE_PRICE_ADDON_PRIORITY_SUPPORT",
                "STRIPE_PRICE_ADDON_SLA_99_9",
                "STRIPE_PRICE_ADDON_WHITE_LABEL",
            ]
            
            for env_name in price_envs:
                price_id = os.getenv(env_name, "").strip()
                
                if not price_id:
                    # Not configured, skip (not an error)
                    continue
                
                price_result = {
                    "found": False,
                    "env_name": env_name,
                    "price_id": price_id
                }
                
                try:
                    price = stripe.Price.retrieve(price_id)
                    price_result["found"] = True
                    price_result["id"] = price.get("id")
                    price_result["currency"] = price.get("currency")
                    price_result["unit_amount"] = price.get("unit_amount")
                    price_result["active"] = price.get("active", False)
                    
                    if not price.get("active"):
                        errors.append(f"price_inactive: {env_name} ({price_id})")
                        logger.warning(f"stripe_check: Price {env_name}={price_id} is inactive")
                    
                    logger.debug(f"stripe_check: Price {env_name}={price_id} verified")
                    
                except stripe.error.InvalidRequestError as e:
                    errors.append(f"price_not_found: {env_name} ({price_id})")
                    logger.error(f"stripe_check: Price {env_name}={price_id} not found: {e}")
                except Exception as e:
                    errors.append(f"price_error: {env_name} ({price_id}) - {type(e).__name__}")
                    logger.error(f"stripe_check: Price {env_name}={price_id} check failed: {e}")
                
                checks["prices"][env_name] = price_result
        
        except ImportError:
            errors.append("stripe_module_not_installed")
            logger.error("stripe_check: stripe module not installed")
        except Exception as e:
            errors.append(f"stripe_initialization_error: {type(e).__name__}")
            logger.error(f"stripe_check: Initialization failed: {e}")
    
    # Determine HTTP status code
    status_code = 200 if not errors else 500
    
    response = {
        "ok": len(errors) == 0,
        "ts": ts,
        "checks": checks,
        "errors": errors,
    }
    
    if errors:
        logger.warning(f"stripe_check: Failed with {len(errors)} error(s): {errors}")
    else:
        logger.info("stripe_check: All checks passed")
    
    return jsonify(response), status_code
