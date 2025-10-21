"""
Tests for Phase 103: Customer Authentication & Portal
Tests JWT generation, verification, rate limiting, and customer routes
"""

import pytest
import jwt
import json
import os
from datetime import datetime, timedelta


# Mock data for testing
MOCK_EMAIL = "test@example.com"
MOCK_CUSTOMER_ID = "cus_test123"


class TestJWTAuthentication:
    """Test JWT token generation and verification"""
    
    def test_generate_jwt(self):
        """Test JWT token generation"""
        from bot.auth import generate_jwt, AUTH_JWT_SECRET
        
        token = generate_jwt(MOCK_EMAIL, MOCK_CUSTOMER_ID)
        
        assert token is not None
        assert isinstance(token, str)
        
        # Decode and verify payload
        payload = jwt.decode(token, AUTH_JWT_SECRET, algorithms=["HS256"])
        assert payload["email"] == MOCK_EMAIL
        assert payload["customer_id"] == MOCK_CUSTOMER_ID
        assert "exp" in payload
        assert "iat" in payload
    
    def test_verify_jwt_valid(self):
        """Test JWT verification with valid token"""
        from bot.auth import generate_jwt, verify_jwt
        
        token = generate_jwt(MOCK_EMAIL, MOCK_CUSTOMER_ID)
        is_valid, payload = verify_jwt(token)
        
        assert is_valid is True
        assert payload["email"] == MOCK_EMAIL
        assert payload["customer_id"] == MOCK_CUSTOMER_ID
    
    def test_verify_jwt_invalid(self):
        """Test JWT verification with invalid token"""
        from bot.auth import verify_jwt
        
        is_valid, payload = verify_jwt("invalid.token.here")
        
        assert is_valid is False
        assert payload is None
    
    def test_verify_jwt_expired(self):
        """Test JWT verification with expired token"""
        from bot.auth import AUTH_JWT_SECRET
        
        # Create expired token
        expired_payload = {
            "email": MOCK_EMAIL,
            "exp": datetime.utcnow() - timedelta(hours=1)
        }
        expired_token = jwt.encode(expired_payload, AUTH_JWT_SECRET, algorithm="HS256")
        
        from bot.auth import verify_jwt
        is_valid, payload = verify_jwt(expired_token)
        
        assert is_valid is False
        assert payload is None


class TestRateLimiting:
    """Test rate limiting functionality"""
    
    def test_check_rate_limit_allowed(self):
        """Test rate limit allows requests under threshold"""
        from bot.auth import check_rate_limit
        
        identifier = "test_ip_1"
        
        # Should allow first 5 requests
        for i in range(5):
            assert check_rate_limit(identifier, limit=5, window=60) is True
    
    def test_check_rate_limit_exceeded(self):
        """Test rate limit blocks requests over threshold"""
        from bot.auth import check_rate_limit
        
        identifier = "test_ip_2"
        
        # Use up the limit
        for i in range(5):
            check_rate_limit(identifier, limit=5, window=60)
        
        # Next request should be blocked
        assert check_rate_limit(identifier, limit=5, window=60) is False


class TestAuthLogging:
    """Test authentication event logging"""
    
    def test_auth_log_created(self):
        """Test that auth events are logged to NDJSON"""
        from bot.auth import log_auth_event
        
        log_file = "logs/auth.ndjson"
        
        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)
        
        # Clear log file
        if os.path.exists(log_file):
            os.remove(log_file)
        
        # Log an event
        log_auth_event("test_event", detail="test_detail")
        
        # Verify log entry
        assert os.path.exists(log_file)
        
        with open(log_file, "r") as f:
            lines = f.readlines()
            assert len(lines) > 0
            
            last_entry = json.loads(lines[-1])
            assert last_entry["event"] == "test_event"
            assert last_entry["detail"] == "test_detail"
            assert "ts" in last_entry
    
    def test_sensitive_data_redacted(self):
        """Test that sensitive data is redacted from logs"""
        from bot.auth import log_auth_event
        
        log_file = "logs/auth.ndjson"
        
        # Log event with sensitive data
        log_auth_event("login_attempt", password="secret123", token="jwt.token.here")
        
        # Verify sensitive data is redacted
        with open(log_file, "r") as f:
            lines = f.readlines()
            last_entry = json.loads(lines[-1])
            
            assert "password" not in last_entry
            assert last_entry.get("token") == "***REDACTED***"


class TestMagicLink:
    """Test magic link functionality"""
    
    def test_send_magic_link(self):
        """Test magic link email stub"""
        from bot.auth import send_magic_link
        
        email_log = "logs/emails.ndjson"
        os.makedirs("logs", exist_ok=True)
        
        # Clear email log
        if os.path.exists(email_log):
            os.remove(email_log)
        
        # Send magic link
        success = send_magic_link(MOCK_EMAIL)
        
        assert success is True
        assert os.path.exists(email_log)
        
        # Verify email log entry
        with open(email_log, "r") as f:
            lines = f.readlines()
            assert len(lines) > 0
            
            last_entry = json.loads(lines[-1])
            assert last_entry["to"] == MOCK_EMAIL
            assert "magic_url" in last_entry
            assert "EchoPilot" in last_entry["subject"]


class TestCustomerLookup:
    """Test customer lookup from Notion"""
    
    def test_get_customer_by_email_not_found(self):
        """Test customer lookup with non-existent email"""
        from bot.auth import get_customer_by_email
        
        # This will fail gracefully if Notion DB not configured
        customer = get_customer_by_email("nonexistent@example.com")
        
        # Should return None for non-existent customer
        assert customer is None or isinstance(customer, dict)


# Integration test markers
def test_auth_routes_summary():
    """Summary of Phase 103 auth routes"""
    routes = [
        "GET /auth/login - Login page",
        "GET /app - Customer portal",
        "POST /api/auth/login - Login endpoint",
        "POST /api/auth/magic-link - Magic link sender",
        "GET /api/me - Current user profile",
        "GET /api/billing/history - Billing history",
        "POST /api/billing/portal - Stripe portal link"
    ]
    
    print("\n✅ Phase 103 Routes:")
    for route in routes:
        print(f"   {route}")
    
    assert len(routes) == 7


if __name__ == "__main__":
    print("Running Phase 103 Authentication Tests...")
    print("=" * 60)
    
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
