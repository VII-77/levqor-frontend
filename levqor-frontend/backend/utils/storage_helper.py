"""
Storage Helper Utility
File storage for DFY deliverables
"""

import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

STORAGE_ROOT = os.path.join(os.getcwd(), 'storage', 'dfy')

def save_file(order_id, file_data, filename):
    """
    Save file to storage
    
    Args:
        order_id: DFY order ID
        file_data: File content (bytes)
        filename: File name
    
    Returns:
        str: File URL/path
    """
    order_dir = os.path.join(STORAGE_ROOT, str(order_id))
    os.makedirs(order_dir, exist_ok=True)
    
    file_path = os.path.join(order_dir, filename)
    
    with open(file_path, 'wb') as f:
        f.write(file_data)
    
    logger.info(f"File saved: {file_path}")
    
    return f"/storage/dfy/{order_id}/{filename}"


def get_file_url(order_id, filename):
    """Get file URL"""
    return f"/storage/dfy/{order_id}/{filename}"


def list_files(order_id):
    """List all files for order"""
    order_dir = os.path.join(STORAGE_ROOT, str(order_id))
    
    if not os.path.exists(order_dir):
        return []
    
    files = []
    for filename in os.listdir(order_dir):
        file_path = os.path.join(order_dir, filename)
        if os.path.isfile(file_path):
            files.append({
                'filename': filename,
                'url': get_file_url(order_id, filename),
                'size': os.path.getsize(file_path)
            })
    
    return files
