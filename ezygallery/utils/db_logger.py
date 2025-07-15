from __future__ import annotations

"""Custom logging handler writing entries to the database."""

import logging
from flask import has_app_context, has_request_context, session, request
from models import db, LogEntry


class DBLogHandler(logging.Handler):
    """Logging handler that persists records to ``LogEntry``."""

    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover - side effects
        if not has_app_context():
            return
        try:
            entry = LogEntry(
                level=record.levelname,
                event_type=getattr(record, "event_type", record.name),
                message=record.getMessage(),
                details=getattr(record, "details", None),
                user_id=session.get("user") if has_request_context() else None,
                session_id=session.get("token") if has_request_context() else None,
                ip_address=request.remote_addr if has_request_context() else None,
            )
            db.session.add(entry)
            db.session.commit()
        except Exception:  # pragma: no cover - logging failure
            db.session.rollback()


def setup_logging(app) -> None:
    """Configure file and DB logging handlers on the given Flask app."""

    handler = DBLogHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    if app.logger.level > logging.INFO:
        app.logger.setLevel(logging.INFO)

