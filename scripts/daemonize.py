#!/usr/bin/env python3
"""
Daemonize helper for EchoPilot scheduler
Properly detaches exec_scheduler.py as a background daemon.
"""

import os
import sys
import subprocess
from pathlib import Path

def daemonize():
    """
    Launch exec_scheduler.py as a detached background process.
    Returns the child PID.
    
    NOTE: We do NOT use os.setsid() because it causes the process to exit
    immediately in the Replit environment. Simple background detachment works.
    """
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    scheduler_out = log_dir / 'scheduler.out'
    pid_file = log_dir / 'scheduler.pid'
    
    # Open log file for stdout/stderr
    outfile = open(scheduler_out, 'a')
    
    # Launch exec_scheduler.py detached
    # NOTE: In Replit environment, ANY session detachment (setsid or start_new_session)
    # causes the process to exit immediately. Simple background process works fine.
    process = subprocess.Popen(
        [sys.executable, 'scripts/exec_scheduler.py'],
        stdout=outfile,
        stderr=outfile,
        stdin=subprocess.DEVNULL,
        close_fds=True
        # NO session management - causes exit in Replit
    )
    
    child_pid = process.pid
    
    # Write PID to file
    pid_file.write_text(str(child_pid))
    
    print(f"✅ Scheduler daemonized (PID: {child_pid})")
    print(f"   Logs: {scheduler_out}")
    
    return child_pid

if __name__ == '__main__':
    pid = daemonize()
    sys.exit(0)
