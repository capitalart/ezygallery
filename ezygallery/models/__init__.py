"""Database initialization and model imports.

This package exposes the ``db`` SQLAlchemy instance and core models for the
application. Importing :mod:`models` ensures all tables are registered with
Flask before migrations or runtime usage.
"""

from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .upload_event import UploadEvent  # noqa: E402  -- model registration
from .log_entry import LogEntry  # noqa: E402  -- model registration

__all__ = ["db", "UploadEvent", "LogEntry"]

