"""
DSAR Security Layer
Handles download tokens and OTP generation/verification for secure data access
"""
import secrets
import hashlib
import hmac
from time import time


def create_download_token_and_otp(salt_secret="levqor-dsar"):
    """
    Generate a secure download token and one-time passcode
    
    Returns:
        tuple: (download_token: str, otp: str, otp_hash: str)
    """
    # Generate cryptographically secure download token (32 bytes = 256 bits)
    download_token = secrets.token_urlsafe(32)
    
    # Generate 6-digit OTP
    otp = str(secrets.randbelow(1000000)).zfill(6)
    
    # Hash the OTP with HMAC-SHA256
    otp_hash = hashlib.pbkdf2_hmac(
        'sha256',
        otp.encode('utf-8'),
        salt_secret.encode('utf-8'),
        100000  # 100k iterations
    ).hex()
    
    return download_token, otp, otp_hash


def verify_otp(otp_input, otp_hash_stored, salt_secret="levqor-dsar"):
    """
    Verify an OTP against its stored hash
    
    Args:
        otp_input: The OTP entered by the user
        otp_hash_stored: The hash stored in the database
        salt_secret: Salt for hashing (should match creation)
    
    Returns:
        bool: True if OTP is valid, False otherwise
    """
    if not otp_input or not otp_hash_stored:
        return False
    
    # Hash the input OTP
    otp_hash_input = hashlib.pbkdf2_hmac(
        'sha256',
        otp_input.encode('utf-8'),
        salt_secret.encode('utf-8'),
        100000
    ).hex()
    
    # Constant-time comparison to prevent timing attacks
    return hmac.compare_digest(otp_hash_input, otp_hash_stored)


def verify_download_token_and_otp(db_connection, token, otp_input):
    """
    Verify both token and OTP, check expiry
    
    Returns:
        tuple: (export_dict or None, error_reason or None)
    """
    now = time()
    
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT id, user_id, storage_path, download_token_expires_at, 
               otp_hash, otp_expires_at, downloaded_at
        FROM dsar_exports
        WHERE download_token = ?
    """, (token,))
    
    row = cursor.fetchone()
    
    if not row:
        return None, "INVALID_TOKEN"
    
    export_id, user_id, storage_path, token_expires_at, otp_hash, otp_expires_at, downloaded_at = row
    
    # Check if token expired
    if now > token_expires_at:
        return None, "TOKEN_EXPIRED"
    
    # Check if OTP expired
    if now > otp_expires_at:
        return None, "OTP_EXPIRED"
    
    # Verify OTP
    if not verify_otp(otp_input, otp_hash):
        return None, "INVALID_OTP"
    
    # Optional: Check if already downloaded (one-time use)
    # Uncomment if you want strict one-time downloads
    # if downloaded_at:
    #     return None, "ALREADY_DOWNLOADED"
    
    return {
        "export_id": export_id,
        "user_id": user_id,
        "storage_path": storage_path
    }, None
