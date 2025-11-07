import logging
import json
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """
    JSON log formatter for structured logging
    """
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        if hasattr(record, 'user_id'):
            log_data["user_id"] = record.user_id
        
        if hasattr(record, 'request_id'):
            log_data["request_id"] = record.request_id
        
        if hasattr(record, 'duration_ms'):
            log_data["duration_ms"] = record.duration_ms
        
        return json.dumps(log_data)

def setup_json_logging():
    """
    Configure JSON logging with 24h rotation for api.log and queue.log
    """
    os.makedirs("logs", exist_ok=True)
    
    api_handler = TimedRotatingFileHandler(
        filename="logs/api.log",
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8"
    )
    api_handler.setFormatter(JSONFormatter())
    api_handler.setLevel(logging.INFO)
    
    queue_handler = TimedRotatingFileHandler(
        filename="logs/queue.log",
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8"
    )
    queue_handler.setFormatter(JSONFormatter())
    queue_handler.setLevel(logging.INFO)
    
    api_logger = logging.getLogger("levqor.api")
    api_logger.addHandler(api_handler)
    api_logger.setLevel(logging.INFO)
    
    queue_logger = logging.getLogger("levqor.queue")
    queue_logger.addHandler(queue_handler)
    queue_logger.setLevel(logging.INFO)
    
    logging.info("✅ Structured JSON logging configured (api.log, queue.log with 24h rotation)")
    
    return {
        "api": api_logger,
        "queue": queue_logger
    }

def log_api_request(logger, method, path, status_code, duration_ms, user_id=None):
    """
    Log API request in structured format
    """
    extra = {
        'duration_ms': duration_ms,
        'user_id': user_id
    }
    logger.info(f"{method} {path} -> {status_code}", extra=extra)

def log_queue_job(logger, job_id, job_type, status, duration_ms=None, error=None):
    """
    Log queue job execution
    """
    extra = {
        'duration_ms': duration_ms
    }
    if error:
        logger.error(f"Job {job_id} ({job_type}) failed: {error}", extra=extra)
    else:
        logger.info(f"Job {job_id} ({job_type}) completed: {status}", extra=extra)
