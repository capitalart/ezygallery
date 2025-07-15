"""Admin routes for miscellaneous tools and configuration panels."""

from __future__ import annotations

import subprocess
import os
from flask import Blueprint, render_template, abort, session, flash, redirect, url_for
from flask import request, jsonify
import login_bypass_toggle as login_bypass
import no_cache_toggle
from routes import utils
from pathlib import Path
import json

# --- SECTION: Blueprint setup ---

bp = Blueprint("admin_routes", __name__, url_prefix="/admin")

ADMIN_USER = os.getenv("ADMIN_USER", "robbie")


@bp.before_request
def restrict_admin():
    if session.get("user") != ADMIN_USER:
        flash("Admin access required", "warning")
        return redirect(url_for("auth.login", next=request.url))


@bp.route("/admin-all")
def admin_all():
    """Unified admin console containing all sections."""
    if session.get("user") != ADMIN_USER:
        abort(403)
    categories = [p.stem for p in OPTIONS_DIR.glob("*.json")]
    try:
        result = subprocess.run(
            ["git", "log", "-10", "--oneline", "--decorate"],
            capture_output=True,
            text=True,
            check=True,
        )
        log_lines = result.stdout.strip().splitlines()
    except Exception as exc:  # pragma: no cover - git failure
        log_lines = [f"Error retrieving git log: {exc}"]
    sessions_data = all_sessions()
    return render_template("admin/admin_all.html",
        categories=categories,
        log_lines=log_lines,
        sessions=sessions_data,
        remaining=login_bypass.remaining_str(),
        active=login_bypass.is_enabled(),
        cache_status=no_cache_toggle.is_enabled(),
        cache_remaining=no_cache_toggle.remaining_str(),
        menu=utils.get_menu(),
    )


# --- SECTION: Debug Git log ---

@bp.route("/debug/git-log")
def git_log() -> str:
    """Render last 10 git commits for authenticated admins."""
    if session.get("user") != ADMIN_USER:
        abort(403)
    return admin_all()


# --- SECTION: Prompt Options Editor ---

OPTIONS_DIR = Path('config/ai_prompt_options')

@bp.route('/prompt-options')
def prompt_options_editor():
    """Display list of available prompt option categories."""
    if session.get('user') != ADMIN_USER:
        abort(403)
    return redirect(url_for('admin_routes.admin_all') + '#prompt-options')


@bp.route('/prompt-options/<category>', methods=['POST'])
def save_prompt_options(category: str):
    """Persist updated JSON for a prompt options category."""
    if session.get('user') != ADMIN_USER:
        abort(403)
    file = OPTIONS_DIR / f"{category}.json"
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({'status': 'error', 'message': 'Invalid JSON'}), 400
    file.parent.mkdir(parents=True, exist_ok=True)
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    return jsonify({'status': 'ok', 'message': 'Saved'})


# --- SECTION: Security Controls ---


@bp.route('/security', methods=['GET', 'POST'])
def security():
    """Toggle login bypass for the development environment."""
    if session.get('user') != ADMIN_USER:
        abort(403)
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'enable':
            seconds = int(request.form.get('duration', '0'))
            login_bypass.enable(seconds / 3600)
            flash(f'Login bypass enabled for {login_bypass.remaining_str()}', 'success')
        elif action == 'disable':
            login_bypass.disable()
            flash('Login bypass disabled', 'success')
        return redirect(url_for('admin_routes.admin_all') + '#security')
    return redirect(url_for('admin_routes.admin_all') + '#security')


# --- SECTION: Login Bypass Toggle ---


@bp.route('/login-bypass', methods=['GET', 'POST'])
def login_bypass_panel():
    """Admin panel for temporary login bypass."""
    if session.get('user') != ADMIN_USER:
        abort(403)
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'enable':
            login_bypass.enable()
            flash('Login bypass enabled for 2 hours', 'success')
        elif action == 'disable':
            login_bypass.disable()
            flash('Login bypass disabled', 'success')
        return redirect(url_for('admin_routes.admin_all') + '#login-bypass')
    return redirect(url_for('admin_routes.admin_all') + '#login-bypass')


# --- SECTION: Active Sessions ---

from routes.session_tracker import all_sessions, remove_session


@bp.route('/sessions', methods=['GET', 'POST'])
def active_sessions():
    """View and optionally revoke active user sessions."""
    if session.get('user') != ADMIN_USER:
        abort(403)
    if request.method == 'POST':
        user = request.form.get('username')
        sid = request.form.get('session_id')
        if user and sid:
            remove_session(user, sid)
            flash('Session revoked', 'success')
        return redirect(url_for('admin_routes.admin_all') + '#sessions')
    return redirect(url_for('admin_routes.admin_all') + '#sessions')


# --- SECTION: Cache Control ---


@bp.route('/cache-control', methods=['GET', 'POST'])
def cache_control():
    """Manually enable or disable the global no-cache flag."""
    if session.get('user') != ADMIN_USER:
        abort(403)
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'enable':
            no_cache_toggle.enable()
            flash('Forced no-cache enabled for 2 hours', 'success')
        elif action == 'disable':
            no_cache_toggle.disable()
            flash('Forced no-cache disabled', 'success')
        return redirect(url_for('admin_routes.admin_all') + '#cache-control')
    return redirect(url_for('admin_routes.admin_all') + '#cache-control')


@bp.route('/user-management')
def user_management():
    """Placeholder page for admin user management."""
    if session.get('user') != ADMIN_USER:
        abort(403)
    return redirect(url_for('admin_routes.admin_all') + '#user-management')


@bp.route('/dashboard')
def dashboard():
    """Simple admin dashboard placeholder."""
    return redirect(url_for('admin_routes.admin_all') + '#dashboard')


@bp.route('/settings')
def settings():
    """Placeholder settings page."""
    return redirect(url_for('admin_routes.admin_all') + '#settings')


@bp.route('/login-disabled')
def login_disabled():
    """Inform admin users that login has been disabled."""
    if session.get('user') != ADMIN_USER:
        abort(403)
    return render_template('admin/login-disabled.html', menu=utils.get_menu())


@bp.route('/logs')
def view_logs():
    """Display log entries with basic filtering."""
    if session.get('user') != ADMIN_USER:
        abort(403)
    from models import LogEntry
    level = request.args.get('level')
    user = request.args.get('user')
    query = LogEntry.query.order_by(LogEntry.timestamp.desc())
    if level:
        query = query.filter_by(level=level)
    if user:
        query = query.filter_by(user_id=user)
    entries = query.limit(200).all()
    return render_template('admin/logs.html', entries=entries, menu=utils.get_menu())
