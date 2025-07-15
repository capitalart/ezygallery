"""Management Suite dashboard and module routing."""
from __future__ import annotations

import os
from flask import Blueprint, render_template, session, abort
from routes import utils

ADMIN_USER = os.getenv("ADMIN_USER", "robbie")

bp = Blueprint("management", __name__, url_prefix="/admin/management")


@bp.before_request
def restrict() -> None:
    """Limit access to the configured admin user."""
    if session.get("user") != ADMIN_USER:
        abort(403)


@bp.route("/")
def dashboard() -> str:
    """Render the Management Suite landing page."""
    return render_template("management_suite/index.html", menu=utils.get_menu())
