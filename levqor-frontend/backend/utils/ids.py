import secrets

def generate_gdpr_reference():
    return secrets.token_hex(8)
