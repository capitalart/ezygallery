from __future__ import annotations

"""SQLAlchemy model for application log entries."""

import datetime as _dt
from . import db


class LogEntry(db.Model):
    """Record of an event or error for admin visibility."""

    __tablename__ = "log_entries"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), default=_dt.datetime.utcnow, nullable=False)
    level = db.Column(db.String(50), nullable=False)
    event_type = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    details = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.String, nullable=True)
    session_id = db.Column(db.String, nullable=True)
    ip_address = db.Column(db.String, nullable=True)

