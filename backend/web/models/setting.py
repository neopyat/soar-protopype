from datetime import datetime

from web.extensions import db


class Setting(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)

    debug = db.Column(db.Boolean, default=True)
    ml_enabled = db.Column(db.Boolean, default=True)
    blocking = db.Column(db.Boolean, default=False)

    loop_interval = db.Column(db.Integer, default=2)
    siem = db.Column(db.String(50), default="none")

    updated_at = db.Column(db.DateTime, default=datetime.utcnow)