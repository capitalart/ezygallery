"""Admin management for the OpenAI system prompt."""
from __future__ import annotations

import os
import shutil
from datetime import datetime
from flask import Blueprint, render_template, request, session, abort, redirect, url_for, flash, jsonify

from routes import utils
import config
from utils.ai_services import call_openai_api

ADMIN_USER = os.getenv("ADMIN_USER", "robbie")
GUIDANCE_PATH = config.ONBOARDING_PATH
HISTORY_DIR = config.LOGS_DIR / "openai_guidance_versions"

bp = Blueprint("openai_guidance", __name__, url_prefix="/admin/openai-guidance")


@bp.before_request
def restrict() -> None:
    if session.get("user") != ADMIN_USER:
        abort(403)


@bp.route("/", methods=["GET", "POST"])
def manage() -> str:
    """View and edit the system prompt used for artwork analysis."""
    if request.method == "POST":
        text = request.form.get("guidance", "")
        GUIDANCE_PATH.write_text(text, encoding="utf-8")
        HISTORY_DIR.mkdir(parents=True, exist_ok=True)
        ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        (HISTORY_DIR / f"{ts}.txt").write_text(text, encoding="utf-8")
        flash("Guidance saved", "success")
        return redirect(url_for("openai_guidance.manage"))

    text = GUIDANCE_PATH.read_text(encoding="utf-8") if GUIDANCE_PATH.exists() else ""
    versions = sorted(HISTORY_DIR.glob("*.txt"), reverse=True)
    return render_template(
        "management_suite/openai_guidance.html",
        menu=utils.get_menu(),
        text=text,
        versions=[v.name for v in versions],
    )


@bp.route("/revert/<name>")
def revert(name: str) -> str:
    """Restore a previous version of the guidance prompt."""
    src = HISTORY_DIR / name
    if src.is_file():
        shutil.copy(src, GUIDANCE_PATH)
        flash(f"Reverted to {name}", "success")
    return redirect(url_for("openai_guidance.manage"))


@bp.post("/test")
def test_prompt() -> "json":
    """Send a test prompt to OpenAI and return the response."""
    prompt = request.form.get("prompt", "")
    result = call_openai_api(prompt)
    return jsonify({"result": result})
