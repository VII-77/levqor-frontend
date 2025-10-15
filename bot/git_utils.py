import subprocess
import os
from typing import Tuple

def get_git_info() -> Tuple[str, str, bool]:
    try:
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], stderr=subprocess.DEVNULL).decode().strip()
    except:
        commit = "no-git"
    
    try:
        branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stderr=subprocess.DEVNULL).decode().strip()
    except:
        branch = "unknown"
    
    try:
        result = subprocess.run(['git', 'diff', '--quiet'], capture_output=True)
        is_dirty = result.returncode != 0
    except:
        is_dirty = False
    
    return commit, branch, is_dirty

def check_git_clean() -> bool:
    allow_dirty = os.getenv('ALLOW_DIRTY', 'false').lower() == 'true'
    _, _, is_dirty = get_git_info()
    
    if is_dirty and not allow_dirty:
        raise Exception("Working tree is dirty. Set ALLOW_DIRTY=true to override.")
    
    return True
