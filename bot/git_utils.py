import subprocess
import os
from typing import Tuple

def get_git_info() -> Tuple[str, str, bool]:
    """Get Git commit, branch, and dirty status. Works in both dev and deployment."""
    
    commit = None
    branch = None
    
    # Try git commands first
    try:
        commit = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], 
            stderr=subprocess.DEVNULL,
            timeout=5
        ).decode().strip()
    except:
        pass
    
    # Try environment variables if git failed
    if not commit:
        commit = os.getenv('GIT_COMMIT', None) or os.getenv('REPL_SLUG', None)
    
    # Final fallback
    if not commit:
        try:
            with open('.git/HEAD', 'r') as f:
                ref = f.read().strip()
                if ref.startswith('ref: '):
                    ref_path = ref[5:]
                    with open(f'.git/{ref_path}', 'r') as ref_file:
                        commit = ref_file.read().strip()
                else:
                    commit = ref
        except:
            commit = "deployed"
    
    # Get branch
    try:
        branch = subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
            stderr=subprocess.DEVNULL,
            timeout=5
        ).decode().strip()
    except:
        try:
            with open('.git/HEAD', 'r') as f:
                ref = f.read().strip()
                if ref.startswith('ref: refs/heads/'):
                    branch = ref.split('/')[-1]
                else:
                    branch = "main"
        except:
            branch = os.getenv('GIT_BRANCH', 'production')
    
    # Check if working tree is dirty
    try:
        result = subprocess.run(
            ['git', 'diff', '--quiet'], 
            capture_output=True,
            timeout=5
        )
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
