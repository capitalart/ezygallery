"""SQLAlchemy model for tracking upload and analysis events."""

from __future__ import annotations

import datetime as _dt

from . import db


class UploadEvent(db.Model):
    """Record timing information for uploads and analysis."""

    __tablename__ = "upload_events"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=True)
    upload_id = db.Column(db.String, nullable=False, unique=True)
    filename = db.Column(db.String, nullable=False)
    upload_start_time = db.Column(db.DateTime(timezone=True), nullable=False)
    upload_end_time = db.Column(db.DateTime(timezone=True), nullable=False)
    analysis_start_time = db.Column(db.DateTime(timezone=True), nullable=True)
    analysis_end_time = db.Column(db.DateTime(timezone=True), nullable=True)
    status = db.Column(
        db.String,
        nullable=False,
        default="started",
    )
    error_msg = db.Column(db.Text, nullable=True)
    session_id = db.Column(db.String, nullable=True)
    ip_address = db.Column(db.String, nullable=True)
    user_agent = db.Column(db.String, nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True), default=_dt.datetime.utcnow, nullable=False
    )

    def upload_duration_ms(self) -> float | None:
        """Return upload duration in milliseconds if available."""

        if self.upload_start_time and self.upload_end_time:
            delta = self.upload_end_time - self.upload_start_time
            return delta.total_seconds() * 1000
        return None

    def analysis_duration_ms(self) -> float | None:
        """Return analysis duration in milliseconds if available."""

        if self.analysis_start_time and self.analysis_end_time:
            delta = self.analysis_end_time - self.analysis_start_time
            return delta.total_seconds() * 1000
        return None


