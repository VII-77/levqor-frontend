"""
Error Event Model
Stores all frontend and backend errors for in-house monitoring (Sentry replacement)
"""

from app import db
from datetime import datetime


class ErrorEvent(db.Model):
    __tablename__ = 'error_events'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    source = db.Column(db.String(50), nullable=False, index=True)
    service = db.Column(db.String(100), nullable=False, index=True)
    path_or_screen = db.Column(db.String(500), nullable=True)
    user_email = db.Column(db.String(255), nullable=True, index=True)
    severity = db.Column(db.String(20), nullable=False, default='error', index=True)
    message = db.Column(db.Text, nullable=False)
    stack = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'source': self.source,
            'service': self.service,
            'path_or_screen': self.path_or_screen,
            'user_email': self.user_email,
            'severity': self.severity,
            'message': self.message,
            'stack': self.stack
        }
