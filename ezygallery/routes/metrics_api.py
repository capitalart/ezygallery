"""API endpoints providing simple metrics for front-end widgets."""

from __future__ import annotations

import statistics
from flask import Blueprint, jsonify

from models import db, UploadEvent

bp = Blueprint("metrics", __name__, url_prefix="/api")


@bp.get("/metrics")
def metrics() -> "tuple[str, int]":
    """Return median upload and analysis times in milliseconds."""

    events = UploadEvent.query.all()
    upload_times = [e.upload_duration_ms() for e in events if e.upload_duration_ms()]
    analysis_times = [
        e.analysis_duration_ms() for e in events if e.analysis_duration_ms()
    ]

    median_upload = statistics.median(upload_times) if upload_times else 0
    median_analysis = statistics.median(analysis_times) if analysis_times else 0

    data = {
        "overall": {
            "median_upload_ms": median_upload,
            "median_analysis_ms": median_analysis,
        }
    }

    # Additional stats such as averages or percentiles can be added using
    # SQLAlchemy queries with ``func.avg`` or Postgres ``percentile_cont``.

    return jsonify(data)

