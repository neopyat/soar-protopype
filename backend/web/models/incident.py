from datetime import datetime

from web.extensions import db


class Incident(db.Model):
    __tablename__ = "incidents"

    id = db.Column(db.Integer, primary_key=True)

    type = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.String(100), nullable=True)

    severity = db.Column(db.String(20), default="low")
    status = db.Column(db.String(20), default="open")

    mitre = db.Column(db.String(50), nullable=True)

    raw_log = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)