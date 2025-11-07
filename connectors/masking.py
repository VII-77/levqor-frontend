def mask(s: str) -> str:
    """Mask sensitive string: keep first 4, last 2, else ****"""
    if not s or len(s) <= 6:
        return "****"
    return f"{s[:4]}****{s[-2:]}"
