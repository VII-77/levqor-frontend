"""
Performance optimization utilities for Boss Mode
- HTTP caching
- LRU cache
- Response compression
"""

from functools import lru_cache, wraps
from flask import request, make_response
import time

# ===== HTTP Caching =====
def cache_control(max_age=3600, public=True):
    """Add Cache-Control headers to response"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            response = make_response(f(*args, **kwargs))
            
            visibility = "public" if public else "private"
            response.headers['Cache-Control'] = f'{visibility}, max-age={max_age}'
            response.headers['ETag'] = f'"{hash(str(response.get_data()))}"'
            
            # Check If-None-Match for 304 responses
            if_none_match = request.headers.get('If-None-Match')
            if if_none_match and if_none_match == response.headers.get('ETag'):
                response.status_code = 304
                response.set_data(b'')
            
            return response
        return wrapped
    return decorator

def no_cache(f):
    """Disable caching for sensitive endpoints"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        response = make_response(f(*args, **kwargs))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    return wrapped

# ===== Memory Caching =====
@lru_cache(maxsize=128)
def cached_computation(key):
    """Example of LRU cached computation"""
    # Expensive operation here
    return f"result_{key}"

def clear_caches():
    """Clear all LRU caches"""
    cached_computation.cache_clear()

# ===== Performance Monitoring =====
def track_performance(metric_name):
    """Decorator to track endpoint performance"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            start = time.time()
            result = f(*args, **kwargs)
            duration_ms = (time.time() - start) * 1000
            
            # Log slow requests (>500ms)
            if duration_ms > 500:
                print(f"⚠️ Slow request: {metric_name} took {duration_ms:.0f}ms")
            
            return result
        return wrapped
    return decorator
