"""
Sales Engine Database Models
Tables for leads, DFY orders, and sales automation
"""

from app import db
from datetime import datetime

class Lead(db.Model):
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(50), nullable=True)
    business_type = db.Column(db.String(100), nullable=True)
    problem = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(500), default='')
    score = db.Column(db.Integer, default=0)
    last_contact = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LeadActivity(db.Model):
    __tablename__ = 'lead_activity'
    
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class DFYOrder(db.Model):
    __tablename__ = 'dfy_orders'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(255), nullable=False)
    customer_email = db.Column(db.String(255), nullable=False)
    tier = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='NEW')
    deadline = db.Column(db.DateTime, nullable=True)
    revisions_left = db.Column(db.Integer, default=1)
    files_url = db.Column(db.Text, nullable=True)
    final_package_url = db.Column(db.Text, nullable=True)
    upgraded_from = db.Column(db.Integer, nullable=True)
    checklist_status = db.Column(db.String(50), default='PENDING')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DFYActivity(db.Model):
    __tablename__ = 'dfy_activity'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('dfy_orders.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class UpsellLog(db.Model):
    __tablename__ = 'upsell_log'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('dfy_orders.id'), nullable=False)
    email_type = db.Column(db.String(50), nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='SENT')
