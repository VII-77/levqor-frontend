#!/usr/bin/env python3
"""
EchoPilot Development Environment Checker
Validates local development setup and dependencies
"""

import os
import sys
import subprocess
from pathlib import Path

# Colors
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

checks_passed = 0
checks_failed = 0
checks_warned = 0

def success(msg):
    global checks_passed
    print(f"{GREEN}✓{NC} {msg}")
    checks_passed += 1

def fail(msg):
    global checks_failed
    print(f"{RED}✗{NC} {msg}")
    checks_failed += 1

def warn(msg):
    global checks_warned
    print(f"{YELLOW}⚠{NC} {msg}")
    checks_warned += 1

def info(msg):
    print(f"{BLUE}ℹ{NC} {msg}")

def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        success(f"Python {version.major}.{version.minor}.{version.micro}")
    else:
        fail(f"Python 3.8+ required (found {version.major}.{version.minor}.{version.micro})")

def check_dependencies():
    """Check Python dependencies"""
    required = [
        'flask',
        'notion-client',
        'openai',
        'google-api-python-client',
        'gunicorn',
        'schedule',
        'python-dotenv'
    ]
    
    import pkg_resources
    
    for package in required:
        try:
            pkg_resources.get_distribution(package)
            success(f"Package: {package}")
        except pkg_resources.DistributionNotFound:
            fail(f"Package missing: {package}")

def check_env_vars():
    """Check required environment variables"""
    required = {
        'SESSION_SECRET': 'Security: Session secret key',
        'DASHBOARD_KEY': 'Security: Dashboard authentication',
        'HEALTH_TOKEN': 'Health: Health endpoint token',
    }
    
    optional = {
        'NOTION_TOKEN': 'Notion API access',
        'AI_INTEGRATIONS_OPENAI_API_KEY': 'OpenAI API access',
        'TELEGRAM_BOT_TOKEN': 'Telegram notifications',
        'STRIPE_SECRET_KEY': 'Payment processing',
        'DATABASE_URL': 'PostgreSQL connection',
    }
    
    for var, desc in required.items():
        if os.getenv(var):
            success(f"ENV: {var} ({desc})")
        else:
            fail(f"ENV missing: {var} ({desc})")
    
    for var, desc in optional.items():
        if os.getenv(var):
            success(f"ENV: {var} ({desc})")
        else:
            warn(f"ENV optional: {var} ({desc})")

def check_directories():
    """Check required directories"""
    dirs = [
        'logs',
        'templates',
        'static',
        'bot',
        'scripts',
        'docs',
        'configs'
    ]
    
    for dir_name in dirs:
        if Path(dir_name).is_dir():
            success(f"Directory: {dir_name}/")
        else:
            fail(f"Directory missing: {dir_name}/")

def check_config_files():
    """Check required config files"""
    files = [
        'run.py',
        'bot/config.py',
        'configs/flags.json',
        'replit.md'
    ]
    
    for file_name in files:
        if Path(file_name).is_file():
            success(f"Config: {file_name}")
        else:
            fail(f"Config missing: {file_name}")

def check_git():
    """Check git status"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            success("Git: Repository initialized")
            
            if result.stdout.strip():
                warn("Git: Uncommitted changes detected")
            else:
                success("Git: Working tree clean")
        else:
            warn("Git: Not a git repository")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        warn("Git: Command not available")

def check_database():
    """Check database connectivity"""
    db_url = os.getenv('DATABASE_URL')
    
    if not db_url:
        warn("Database: DATABASE_URL not set")
        return
    
    try:
        import psycopg2
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s', ('public',))
        table_count = cur.fetchone()[0]
        conn.close()
        
        success(f"Database: Connected ({table_count} tables)")
    except ImportError:
        warn("Database: psycopg2 not installed (optional)")
    except Exception as e:
        fail(f"Database: Connection failed - {str(e)}")

def check_port():
    """Check if default port is available"""
    import socket
    
    port = 5000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.bind(('0.0.0.0', port))
        sock.close()
        success(f"Port {port}: Available")
    except OSError:
        warn(f"Port {port}: Already in use")

def check_disk_space():
    """Check disk space"""
    import shutil
    
    total, used, free = shutil.disk_usage('/')
    free_gb = free // (2**30)
    
    if free_gb >= 5:
        success(f"Disk space: {free_gb}GB free")
    elif free_gb >= 1:
        warn(f"Disk space: {free_gb}GB free (low)")
    else:
        fail(f"Disk space: {free_gb}GB free (critical)")

def main():
    print()
    print("=" * 50)
    print("  EchoPilot Development Environment Check")
    print("=" * 50)
    print()
    
    info("Checking Python...")
    check_python()
    
    print()
    info("Checking dependencies...")
    check_dependencies()
    
    print()
    info("Checking environment variables...")
    check_env_vars()
    
    print()
    info("Checking directory structure...")
    check_directories()
    
    print()
    info("Checking config files...")
    check_config_files()
    
    print()
    info("Checking git...")
    check_git()
    
    print()
    info("Checking database...")
    check_database()
    
    print()
    info("Checking system...")
    check_port()
    check_disk_space()
    
    # Summary
    print()
    print("=" * 50)
    print("  Summary")
    print("=" * 50)
    print(f"{GREEN}Passed:  {checks_passed}{NC}")
    print(f"{YELLOW}Warnings: {checks_warned}{NC}")
    print(f"{RED}Failed:   {checks_failed}{NC}")
    print("=" * 50)
    print()
    
    if checks_failed == 0:
        print(f"{GREEN}✓ Development environment ready!{NC}")
        return 0
    else:
        print(f"{RED}✗ Fix {checks_failed} issue(s) before continuing{NC}")
        return 1

if __name__ == '__main__':
    exit(main())
