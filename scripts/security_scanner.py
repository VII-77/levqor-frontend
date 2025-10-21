#!/usr/bin/env python3
"""
EchoPilot Security Scanner (Phase 114)
Runs pip-audit, checks for secrets, and generates SBOM
"""

import os
import sys
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

def log_event(event_type, details=None):
    """Log scanner events"""
    log_entry = {
        'ts': datetime.utcnow().isoformat() + 'Z',
        'event_type': event_type,
        'details': details or {}
    }
    
    log_file = Path('logs/security_scanner.ndjson')
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')

def run_pip_audit():
    """Run pip-audit to check for vulnerabilities"""
    try:
        # First check if pip-audit is installed
        check_install = subprocess.run(
            ['pip-audit', '--version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if check_install.returncode != 0:
            # pip-audit not installed, install it
            subprocess.run(
                ['pip', 'install', '--quiet', 'pip-audit'],
                capture_output=True,
                timeout=60
            )
        
        # Run pip-audit in JSON format
        result = subprocess.run(
            ['pip-audit', '--format=json'],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # pip-audit exits with non-zero if vulnerabilities found
        if result.stdout:
            try:
                audit_data = json.loads(result.stdout)
                vulnerabilities = audit_data.get('dependencies', [])
                
                return {
                    'status': 'ok',
                    'vulnerabilities': len(vulnerabilities),
                    'findings': vulnerabilities[:10],  # Limit output
                    'exit_code': result.returncode
                }
            except json.JSONDecodeError:
                # Fallback to text output
                return {
                    'status': 'ok',
                    'vulnerabilities': 0,
                    'raw_output': result.stdout[:500],
                    'exit_code': result.returncode
                }
        else:
            return {
                'status': 'ok',
                'vulnerabilities': 0,
                'message': 'No vulnerabilities found',
                'exit_code': result.returncode
            }
            
    except subprocess.TimeoutExpired:
        log_event('pip_audit_timeout', {})
        return {
            'status': 'timeout',
            'error': 'pip-audit timed out after 120s'
        }
    except Exception as e:
        log_event('pip_audit_error', {'error': str(e)})
        return {
            'status': 'error',
            'error': str(e)
        }

def scan_for_secrets():
    """Scan codebase for accidentally committed secrets"""
    secret_patterns = [
        (r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\']([a-zA-Z0-9_-]{20,})["\']', 'API Key'),
        (r'(?i)(password|passwd|pwd)\s*[=:]\s*["\']([^"\']{8,})["\']', 'Password'),
        (r'(?i)(secret|token)\s*[=:]\s*["\']([a-zA-Z0-9_-]{20,})["\']', 'Secret/Token'),
        (r'(?i)(AKIA[0-9A-Z]{16})', 'AWS Access Key'),
        (r'(?i)(ghp_[a-zA-Z0-9]{36})', 'GitHub Personal Access Token'),
    ]
    
    findings = []
    exclude_patterns = [
        'node_modules/',
        '__pycache__/',
        '.git/',
        'venv/',
        '.ndjson',
        '.log'
    ]
    
    try:
        for file_path in Path('.').rglob('*.py'):
            # Skip excluded paths
            if any(exc in str(file_path) for exc in exclude_patterns):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                for pattern, secret_type in secret_patterns:
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        # Filter out false positives (comments, documentation)
                        line_context = content[max(0, match.start()-50):match.end()+50]
                        if '#' in line_context or 'example' in line_context.lower():
                            continue
                        
                        findings.append({
                            'file': str(file_path),
                            'type': secret_type,
                            'line': content[:match.start()].count('\n') + 1,
                            'context': line_context.strip()[:100]
                        })
            except Exception as e:
                continue
        
        return findings
        
    except Exception as e:
        log_event('secret_scan_error', {'error': str(e)})
        return []

def generate_sbom():
    """Generate Software Bill of Materials"""
    try:
        result = subprocess.run(
            ['pip', 'list', '--format=json'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            return {'error': 'Failed to list packages'}
        
        packages = json.loads(result.stdout)
        
        sbom = {
            'format': 'echopilot-sbom-v1',
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'components': [
                {
                    'name': pkg['name'],
                    'version': pkg['version'],
                    'type': 'python-package'
                }
                for pkg in packages
            ],
            'metadata': {
                'python_version': sys.version.split()[0],
                'platform': sys.platform
            }
        }
        
        # Save SBOM
        sbom_file = Path('logs/sbom.json')
        with open(sbom_file, 'w') as f:
            json.dump(sbom, f, indent=2)
        
        return {
            'status': 'ok',
            'file': str(sbom_file),
            'components': len(sbom['components'])
        }
        
    except Exception as e:
        log_event('sbom_error', {'error': str(e)})
        return {
            'status': 'error',
            'error': str(e)
        }

def run_security_scan():
    """Main security scanner routine"""
    try:
        print("Running security scan...")
        
        # Run pip audit
        print("\n1. Checking dependencies...")
        pip_result = run_pip_audit()
        
        # Scan for secrets
        print("2. Scanning for secrets...")
        secret_findings = scan_for_secrets()
        
        # Generate SBOM
        print("3. Generating SBOM...")
        sbom_result = generate_sbom()
        
        # Build report
        report = {
            'ts': datetime.utcnow().isoformat() + 'Z',
            'pip_audit': pip_result,
            'secret_scan': {
                'findings': len(secret_findings),
                'issues': secret_findings[:10]  # Limit output
            },
            'sbom': sbom_result,
            'status': 'ok'
        }
        
        # Log full scan
        log_event('security_scan_complete', report)
        
        # Save report
        report_file = Path('logs/security_report.json')
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✓ Security scan complete. Report: {report_file}")
        print(json.dumps({
            'dependencies': pip_result.get('count', 0),
            'secret_findings': len(secret_findings),
            'sbom_components': sbom_result.get('components', 0)
        }, indent=2))
        
        return 0
        
    except Exception as e:
        log_event('scan_error', {'error': str(e)})
        print(f"Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(run_security_scan())
