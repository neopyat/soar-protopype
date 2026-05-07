from web.extensions import db


class Incident(db.Model):
    __tablename__ = "incidents"

    id = db.Column(db.String, primary_key=True)

    type = db.Column(db.String(100), nullable=False)

    ip = db.Column(db.String(100))

    severity = db.Column(db.String(20))

    timestamp = db.Column(db.Float)

    status = db.Column(db.String(20))

    mitre = db.Column(db.String(50))

    threat = db.Column(db.String(50))