import os

MAX_AUDIO_MINUTES = int(os.getenv("MAX_AUDIO_MINUTES", "240"))  # 4 hours default
MAX_FILE_MB = int(os.getenv("MAX_FILE_MB", "1536"))  # 1.5 GB default


def validate_file_size(file_path):
    """
    Validate file size is within limits
    
    Args:
        file_path: Path to file
    
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}"
        
        size_bytes = os.path.getsize(file_path)
        size_mb = size_bytes / (1024 * 1024)
        
        if size_mb > MAX_FILE_MB:
            return False, f"File too large: {size_mb:.1f} MB > {MAX_FILE_MB} MB limit"
        
        return True, f"File size OK: {size_mb:.1f} MB"
        
    except Exception as e:
        return False, f"Error checking file size: {e}"


def validate_audio_duration(duration_seconds):
    """
    Validate audio duration is within limits
    
    Args:
        duration_seconds: Audio duration in seconds
    
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        duration_minutes = duration_seconds / 60.0
        
        if duration_minutes > MAX_AUDIO_MINUTES:
            return False, f"Audio too long: {duration_minutes:.1f} min > {MAX_AUDIO_MINUTES} min limit"
        
        return True, f"Duration OK: {duration_minutes:.1f} min"
        
    except Exception as e:
        return False, f"Error checking duration: {e}"


def validate_media(file_path, duration_seconds=None):
    """
    Validate media file meets size and duration limits
    
    Args:
        file_path: Path to media file
        duration_seconds: Optional audio duration in seconds
    
    Returns:
        tuple: (is_valid, error_message)
    
    Raises:
        ValueError: If validation fails
    """
    # Check file size
    is_valid, message = validate_file_size(file_path)
    if not is_valid:
        raise ValueError(message)
    
    print(f"[MediaValidation] {message}")
    
    # Check duration if provided
    if duration_seconds is not None:
        is_valid, message = validate_audio_duration(duration_seconds)
        if not is_valid:
            raise ValueError(message)
        
        print(f"[MediaValidation] {message}")
    
    return True, "Media validation passed"
