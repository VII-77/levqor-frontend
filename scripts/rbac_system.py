#!/usr/bin/env python3
"""Phase 81: RBAC System - Role-Based Access Control"""
import os, sys, json, hashlib
from datetime import datetime

DEFAULT_ADMIN_EMAIL = os.getenv('DEFAULT_ADMIN_EMAIL', 'admin@echopilot.ai')
RBAC_SECRET = os.getenv('RBAC_SECRET', 'default-rbac-secret')

ROLES = {
    'admin': ['read', 'write', 'delete', 'manage_users', 'billing'],
    'user': ['read', 'write'],
    'viewer': ['read']
}

def load_users():
    if os.path.exists('data/rbac_users.json'):
        with open('data/rbac_users.json', 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    os.makedirs('data', exist_ok=True)
    with open('data/rbac_users.json', 'w') as f:
        json.dump(users, f, indent=2)

def create_user(email, role='user'):
    users = load_users()
    if email in users:
        return {"ok": False, "error": "User already exists"}
    
    users[email] = {
        "role": role,
        "created": datetime.utcnow().isoformat() + "Z",
        "active": True
    }
    save_users(users)
    return {"ok": True, "user": users[email]}

def check_permission(email, permission):
    users = load_users()
    if email not in users:
        return False
    role = users[email].get('role', 'viewer')
    return permission in ROLES.get(role, [])

def initialize_rbac():
    users = load_users()
    if not users:
        create_user(DEFAULT_ADMIN_EMAIL, 'admin')
    return {"ok": True, "users": len(users)}

if __name__ == "__main__":
    result = initialize_rbac()
    print(json.dumps(result, indent=2))
