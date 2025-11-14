from datetime import datetime
from app import db

class DSARRequest(db.Model):
    __tablename__ = "dsar_requests"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(255), nullable=False)

    status = db.Column(db.String(50), nullable=False, default="pending")
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    export_filename = db.Column(db.String(255), nullable=True)
    export_bytes_size = db.Column(db.BigInteger, nullable=True)
    request_ip = db.Column(db.String(255), nullable=True)

    last_error = db.Column(db.Text, nullable=True)
    request_source = db.Column(db.String(50), default="account")
    gdpr_reference_id = db.Column(db.String(64), nullable=True, unique=True)
