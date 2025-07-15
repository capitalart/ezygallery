# 🧠 EzyGallery Code Snapshot — EZYGALLERY-15-JUL-2025-02-46PM


---
## 📄 `config.py`

```py
class Config:
    SECRET_KEY = 'change-me'
    FORCE_NOCACHE = False

```

---
## 📄 `test-codex-snapshot-commit.sh`

```sh
#!/bin/bash

# ============================================================
# 🧠 EzyGallery Snapshot Test Commit Script — Robbie Mode™
# ------------------------------------------------------------
# Adds dummy content to verify Codex snapshot tracking works.
# ============================================================

set -euo pipefail

echo "📄 Updating templates/about.html..."
mkdir -p templates
cat <<EOF > templates/about.html
<!-- templates/about.html -->
{% extends "base.html" %}
{% block title %}About EzyGallery{% endblock %}
{% block content %}
  <div class="container">
    <h1>About EzyGallery</h1>
    <p>This site is built by artists, for artists — using AI tools, Flask, and heaps of 💚 from Robbie.</p>
    <p>Codex-friendly? You bet! Every snapshot is documented so Codex knows exactly where to look.</p>
  </div>
{% endblock %}
EOF

echo "📝 Updating ezy.py with Codex awareness..."
cat <<EOF > ezy.py
# ezy.py - Main app bootstrap
# Updated: 12 July 2025 — Added Codex snapshot awareness 💚
EOF

echo "📘 Updating README.md..."
cat <<EOF > README.md
# 🖼️ EzyGallery

EzyGallery is a modular, AI-assisted art platform built by Robbie Custance — where every artwork tells a story and every snapshot is logged for Codex.

## Codex Snapshot Integration

All development snapshots live in the \`reports/\` directory.

> "Build it like Robbie — back it like a legend." 💾
EOF

echo "📂 Adding updated files to Git..."
git add templates/about.html ezy.py README.md

# ✅ FIXED: Safe snapshot directory detection using find instead of ls
LATEST_SNAPSHOT_DIR=$(find reports/ -maxdepth 1 -type d -name "EZYGALLERY-*" -printf "%T@ %p\n" | sort -n | tail -n 1 | cut -d' ' -f2-)

if [[ -n "$LATEST_SNAPSHOT_DIR" && -d "$LATEST_SNAPSHOT_DIR" ]]; then
  echo "🗂️ Tracking latest snapshot folder: $LATEST_SNAPSHOT_DIR"
  git add "$LATEST_SNAPSHOT_DIR"
else
  echo "⚠️ No snapshot folder found under /reports/, skipping snapshot add."
fi

echo "✅ Committing changes..."
git commit -m "Test commit: Snapshot tracking + dummy updates for Codex validation"

echo "🚀 Pushing to origin/master..."
git push origin master

echo "🎉 All done, Robbie! Codex snapshot files now part of Git and pushed up 💚"

```

---
## 📄 `git-update-push.sh`

```sh
#!/bin/bash

# ==============================================================================
# EzyGallery.com — Git Update + Commit + Push + Backup (Robbie Mode™ Edition)
# ------------------------------------------------------------------------------
# Usage:
#   ./git-update-push.sh --full-auto     # Does everything (commit, backup, cloud)
#   ./git-update-push.sh --just git      # Just git add/commit/push (skip backup)
#   ./git-update-push.sh --no-zip        # Skip local zip backup
#   ./git-update-push.sh --no-cloud      # Skip rclone upload to Google Drive
#   ./git-update-push.sh --no-retention  # Skip cloud retention cleanup
#   ./git-update-push.sh --no-git        # Skip git add/commit/push
#
#   🔥 Will also run ezygallery-total-rundown.py if present
#   🔥 Will cache-bust static folder to force refresh on Flask
# ==============================================================================

set -euo pipefail

# ============= 🔧 CONFIGURATION ================
LOG_DIR="git-update-push-logs"
BACKUP_DIR="backups"
NOW=$(date '+%Y-%m-%d-%H-%M-%p')
LOG_FILE="$LOG_DIR/git-update-push-${NOW}.log"
BACKUP_ZIP="$BACKUP_DIR/${NOW}_backup.zip"
DIFF_RAW="$BACKUP_DIR/diff-raw.txt"
DIFF_REPORT="$BACKUP_DIR/backup-diff-REPORT.md"
COMMIT_MSG_FILE=".codex-commit-msg.txt"
GDRIVE_REMOTE="gdrive"
GDRIVE_FOLDER="ezygallery-backups"

# ============= 📁 PREP ================
mkdir -p "$LOG_DIR" "$BACKUP_DIR"

# ============= 🔄 FLAGS ================
AUTO_MODE=false
ENABLE_ZIP=true
ENABLE_CLOUD=true
ENABLE_RETENTION=true
ENABLE_GIT=true
JUST_GIT=false

for arg in "$@"; do
  case $arg in
    --auto|--full-auto) AUTO_MODE=true ;;
    --no-zip)           ENABLE_ZIP=false ;;
    --no-cloud)         ENABLE_CLOUD=false ;;
    --no-retention)     ENABLE_RETENTION=false ;;
    --no-git)           ENABLE_GIT=false ;;
    --just|--just-git)  JUST_GIT=true ;;
    *) echo "❌ Unknown option: $arg"; exit 1 ;;
  esac
done

# ============= 📜 LOG FUNCTION ================
log() {
  local msg="$1"
  local ts
  ts=$(date '+%Y-%m-%d %H:%M:%S')
  echo "[$ts] $msg" | tee -a "$LOG_FILE"
}

log "=== 🟢 EzyGallery Git + Backup Script Started ==="

# ============= 📁 GIT STATUS & COMMIT ================
log "📂 Checking git status..."
git status | tee -a "$LOG_FILE"

log "➕ Staging all changes..."
git add . 2>>"$LOG_FILE"

if $AUTO_MODE; then
  if [[ -s "$COMMIT_MSG_FILE" ]]; then
    commit_msg=$(cat "$COMMIT_MSG_FILE")
    log "📝 Using Codex commit message: $commit_msg"
  else
    commit_msg="Auto commit: Preparing for Codex upgrade"
    log "📝 Using fallback commit message: $commit_msg"
  fi
else
  read -rp "📝 Enter commit message: " commit_msg
fi

log "✅ Committing changes..."
git commit -m "$commit_msg" 2>>"$LOG_FILE" || log "⚠️ Nothing to commit."
[[ -s "$COMMIT_MSG_FILE" ]] && rm -f "$COMMIT_MSG_FILE"

# ============= 🚫 JUST GIT? ================
if $JUST_GIT; then
  log "⏹️ JUST GIT MODE: Skipping all backup & cloud steps."
  exit 0
fi

# ============= 💥 FORCE CACHE-BUST STATIC FILES ================
if [ -d static ]; then
  log "♻️ Touching static files for cache bust..."
  find static -type f -exec touch {} +
fi

# ============= 🧠 TOTAL RUNDOWN REPORT ================
if [ -f "./ezygallery-total-rundown.py" ]; then
  log "🧠 Running ezygallery-total-rundown.py..."
  python3 ezygallery-total-rundown.py >> "$LOG_FILE" 2>&1 || log "⚠️ Rundown script failed."
else
  log "ℹ️ No total rundown script found."
fi

# ============= 📦 BACKUP ZIP ================
if $ENABLE_ZIP; then
  log "📦 Creating ZIP backup..."
  zip -r "$BACKUP_ZIP" . \
    -x ".git/*" "*.git*" "__pycache__/*" "node_modules/*" "venv/*" "outputs/*" "inputs/*" ".cache/*" ".pytest_cache/*" ".mypy_cache/*" "$BACKUP_DIR/*" "$LOG_DIR/*" "*.DS_Store" "*.pyc" "*.pyo" ".env" "*.sqlite3" >> "$LOG_FILE"
  log "✅ ZIP created: $BACKUP_ZIP"
else
  log "⏭️ Skipping ZIP backup (flag --no-zip)"
fi

# ============= 📄 DIFF REPORT ================
log "📄 Generating markdown diff report..."
git diff --name-status HEAD~1 HEAD > "$DIFF_RAW"
{
  echo "# 🗂️ Diff Report — $(date '+%Y-%m-%d %H:%M %p')"
  echo "Backup file: \`$BACKUP_ZIP\`"
  echo ""
  echo "## 📂 Changed Files:"
  if [[ -s "$DIFF_RAW" ]]; then
    cat "$DIFF_RAW"
  else
    echo "_No changes since last commit_"
  fi
} > "$DIFF_REPORT"
log "✅ Markdown diff report saved: $DIFF_REPORT"

# ============= 🔄 GIT PUSH ================
if $ENABLE_GIT; then
  log "🔄 Pulling latest changes with --rebase --autostash..."
  git pull origin main --rebase --autostash 2>>"$LOG_FILE" || {
    log "❌ git pull --rebase failed. Please resolve manually."
    exit 1
  }
  log "🚀 Pushing to origin/main..."
  git push origin main 2>>"$LOG_FILE" || {
    log "❌ git push failed."
    exit 2
  }
else
  log "⏭️ Skipping Git pull/push (flag --no-git)"
fi

# ============= ☁️ RCLONE UPLOAD ================
if $ENABLE_CLOUD; then
  log "☁️ Uploading to Google Drive ($GDRIVE_REMOTE:$GDRIVE_FOLDER)..."
  if command -v rclone >/dev/null 2>&1; then
    rclone copy "$BACKUP_ZIP" "$GDRIVE_REMOTE:$GDRIVE_FOLDER" >> "$LOG_FILE" 2>&1 \
      && log "✅ Upload complete." \
      || log "❌ Upload failed."
  else
    log "⚠️ rclone not found — skipping cloud upload."
  fi
else
  log "⏭️ Skipping cloud upload (flag --no-cloud)"
fi

# ============= 🧹 CLOUD RETENTION ================
if $ENABLE_RETENTION && $ENABLE_CLOUD; then
  log "🧹 Cleaning up old cloud backups..."
  if command -v rclone >/dev/null 2>&1 && command -v jq >/dev/null 2>&1; then
    OLD_FILES=$(rclone lsjson "$GDRIVE_REMOTE:$GDRIVE_FOLDER" \
      | jq -r '.[] | select(.IsDir == false) | "\(.ModTime) \(.Path)"' \
      | sort \
      | head -n -30 | cut -d' ' -f2-)
    if [[ -n "$OLD_FILES" ]]; then
      while IFS= read -r file; do
        log "🗑️ Deleting old: $file"
        rclone delete "$GDRIVE_REMOTE:$GDRIVE_FOLDER/$file" >> "$LOG_FILE" 2>&1 || true
      done <<< "$OLD_FILES"
      log "✅ Cleanup complete."
    else
      log "ℹ️ Nothing to clean up."
    fi
  else
    log "⚠️ jq or rclone missing — skipping retention."
  fi
else
  log "⏭️ Skipping retention (flag --no-retention or --no-cloud)"
fi

# ============= 🎉 DONE ================
log "🎉 All done, Robbie! Git, ZIP, Flask cache-bust, rundown, cloud and cleanup complete. 💚"

```

---
## 📄 `ezygallery-total-rundown.py`

```py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================
# 🧠 EzyGallery Total Rundown v1.0
# 🔍 Developer Snapshot + Backup Generator
# ➕ Supports git logging, env metadata, pip checks, zip reports
# ➕ Logs stored in DEV_LOGS_DIR/snapshot-YYYY-MM-DD-HHMMSS.log
# 
# Usage:
#   python3 ezygallery-total-rundown.py
#   python3 ezygallery-total-rundown.py --no-zip
#   python3 ezygallery-total-rundown.py --skip-git --skip-env
# =============================================================

import os
import sys
import datetime
import subprocess
import zipfile
import py_compile
import traceback
import argparse
from pathlib import Path
from typing import Generator

# =========================
# 🔧 Configuration
# =========================

DEV_LOGS_DIR = Path("dev_logs")
DEV_LOGS_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".py", ".sh", ".jsx", ".txt", ".html", ".js", ".css"}
EXCLUDED_EXTENSIONS = {".json"}
EXCLUDED_FOLDERS = {"venv", ".git", ".idea", ".vscode", "backups", "__pycache__", "node_modules"}
EXCLUDED_FILES = {".DS_Store"}

LOG_PATH = DEV_LOGS_DIR / f"snapshot-{datetime.datetime.now():%Y-%m-%d-%H%M%S}.log"

# =========================
# 🧾 Logging Functions
# =========================

def log(msg: str):
    print(msg)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now():[%Y-%m-%d %H:%M:%S]} {msg}\n")

def log_error(msg: str):
    print(f"\033[91m{msg}\033[0m")
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now():[%Y-%m-%d %H:%M:%S]} ERROR: {msg}\n")

# =========================
# 📅 Timestamp & Folder
# =========================

def get_timestamp() -> str:
    return datetime.datetime.now().strftime("EZYGALLERY-%d-%b-%Y-%I-%M%p").upper()

def create_reports_folder() -> Path:
    folder = Path("reports") / get_timestamp()
    folder.mkdir(parents=True, exist_ok=True)
    log(f"📁 Report folder created: {folder}")
    return folder

# =========================
# 📁 File Inclusion Rules
# =========================

def get_included_files() -> Generator[Path, None, None]:
    for path in Path(".").rglob("*"):
        if (
            path.is_file() and
            path.suffix in ALLOWED_EXTENSIONS and
            path.suffix not in EXCLUDED_EXTENSIONS and
            path.name not in EXCLUDED_FILES and
            not any(part in EXCLUDED_FOLDERS for part in path.parts)
        ):
            try:
                path.stat()
                yield path
            except Exception:
                continue

# =========================
# 🧾 Markdown Code Snapshot
# =========================

def gather_code_snapshot(folder: Path) -> Path:
    md_path = folder / f"report_code_snapshot_{folder.name.lower()}.md"
    with open(md_path, "w", encoding="utf-8") as md:
        md.write(f"# 🧠 EzyGallery Code Snapshot — {folder.name}\n\n")
        for file in get_included_files():
            rel = file.relative_to(Path("."))
            log(f"📄 Including: {rel}")
            md.write(f"\n---\n## 📄 `{rel}`\n\n```{file.suffix[1:]}\n")
            try:
                with open(file, "r", encoding="utf-8") as f:
                    md.write(f.read())
            except Exception as e:
                md.write(f"[Error: {e}]")
            md.write("\n```\n")
    return md_path

# =========================
# 📊 File Summary Markdown
# =========================

def generate_file_summary(folder: Path):
    summary_path = folder / "file_summary.md"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("# 📊 File Summary\n\n| File | Size (KB) | Last Modified |\n|------|-----------|----------------|\n")
        for file in get_included_files():
            try:
                size = round(file.stat().st_size / 1024, 1)
                mtime = datetime.datetime.fromtimestamp(file.stat().st_mtime)
                rel = file.relative_to(Path("."))
                f.write(f"| `{rel}` | {size} KB | {mtime:%Y-%m-%d %H:%M} |\n")
            except Exception:
                continue

# =========================
# ✅ Python Syntax Validator
# =========================

def validate_python_files():
    log("🧪 Validating Python files...")
    for file in get_included_files():
        if file.suffix == ".py":
            try:
                py_compile.compile(file, doraise=True)
                log(f"✅ OK: {file}")
            except py_compile.PyCompileError as e:
                log_error(f"❌ {file}: {e.msg}")

# =========================
# 📘 Git Snapshot Generator
# =========================

def log_git_status(folder: Path):
    path = folder / "git_snapshot.txt"
    try:
        with open(path, "w", encoding="utf-8") as f:
            subprocess.run(["git", "status"], stdout=f, stderr=subprocess.STDOUT, check=False)
            f.write("\n")
            subprocess.run(["git", "log", "-1"], stdout=f, stderr=subprocess.STDOUT, check=False)
            f.write("\n")
            subprocess.run(["git", "diff", "--stat"], stdout=f, stderr=subprocess.STDOUT, check=False)
        log(f"📘 Git snapshot saved: {path}")
    except Exception as e:
        log_error(f"Git snapshot failed: {e}")

# =========================
# 📚 Environment Info Dump
# =========================

def log_environment_details(folder: Path):
    path = folder / "env_metadata.txt"
    try:
        with open(path, "w", encoding="utf-8") as f:
            subprocess.run(["python3", "--version"], stdout=f, check=False)
            f.write("\n")
            if sys.platform != "win32":
                subprocess.run(["uname", "-a"], stdout=f, check=False)
            f.write("\n")
            subprocess.run(["pip", "freeze"], stdout=f, check=False)
        log(f"📚 Environment metadata written: {path}")
    except Exception as e:
        log_error(f"Environment metadata failed: {e}")

# =========================
# 🔍 Pip Sanity Check
# =========================

def show_dependency_issues():
    log("🔍 Checking pip dependencies...")
    try:
        subprocess.run(["pip", "check"], check=False)
        subprocess.run(["pip", "list", "--outdated"], check=False)
    except Exception as e:
        log_error(f"Pip checks failed: {e}")

# =========================
# 📦 Zip Report Folder
# =========================

def zip_report_folder(folder: Path) -> Path:
    zip_path = folder.with_suffix(".zip")
    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for file in folder.rglob("*"):
                z.write(file, file.relative_to(folder.parent))
        log(f"📦 Zip archive created: {zip_path}")
        return zip_path
    except Exception as e:
        log_error(f"Zipping failed: {e}")
        return zip_path

# =========================
# 🚀 Argument Parser
# =========================

def parse_args():
    parser = argparse.ArgumentParser(description="EzyGallery Dev Snapshot Tool")
    parser.add_argument("--no-zip", action="store_true", help="Skip creating .zip archive")
    parser.add_argument("--skip-env", action="store_true", help="Skip environment metadata logging")
    parser.add_argument("--skip-validate", action="store_true", help="Skip Python validation")
    parser.add_argument("--skip-git", action="store_true", help="Skip Git snapshot")
    parser.add_argument("--skip-pip-check", action="store_true", help="Skip pip check + outdated")
    return parser.parse_args()

# =========================
# 🧠 Main Snapshot Runner
# =========================

def main():
    args = parse_args()
    log("🚀 Running EzyGallery Dev Snapshot...")

    try:
        # 🔨 1. Create report output folder
        folder = create_reports_folder()

        # 📸 2. Gather codebase as Markdown snapshot
        gather_code_snapshot(folder)

        # 📊 3. Create file summary
        generate_file_summary(folder)

        # 🧪 4. Optional: Validate .py syntax
        if not args.skip_validate:
            validate_python_files()

        # 🌐 5. Optional: Dump environment details
        if not args.skip_env:
            log_environment_details(folder)

        # 🔧 6. Optional: Git status snapshot
        if not args.skip_git:
            log_git_status(folder)

        # 🔍 7. Optional: Pip dependency health check
        if not args.skip_pip_check:
            show_dependency_issues()

        # 📦 8. Optional: Create ZIP archive of reports
        if not args.no_zip:
            zip_report_folder(folder)

        # 📥 9. Auto-add report folder to Git for Codex usage
        try:
            subprocess.run(["git", "add", str(folder)], check=True)
            commit_msg = f"🧠 Add dev snapshot: {folder.name}"
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            log(f"📥 Git commit added for: {folder.name}")
        except subprocess.CalledProcessError as e:
            log_error(f"⚠️ Failed to commit snapshot to Git: {e}")

        log("✅ Snapshot complete — nice one Robbie! 💚")

    except Exception as e:
        log_error(f"💥 Snapshot failed: {traceback.format_exc()}")

# =========================
# 🏁 Entry Point
# =========================

if __name__ == "__main__":
    main()

```

---
## 📄 `requirements.txt`

```txt
annotated-types==0.7.0
anyio==4.9.0
blinker==1.9.0
certifi==2025.6.15
charset-normalizer==3.4.2
click==8.2.1
distro==1.9.0
Flask==3.1.1
Flask-SQLAlchemy==3.1.1
greenlet==3.2.3
gunicorn==23.0.0
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
jiter==0.10.0
joblib==1.5.1
markdown-it-py==3.0.0
MarkupSafe==3.0.2
mdurl==0.1.2
numpy==2.3.1
openai==1.93.0
opencv-python==4.11.0.86
packaging==25.0
pandas==2.3.0
pillow==11.2.1
pydantic==2.11.7
pydantic_core==2.33.2
Pygments==2.19.2
python-dateutil==2.9.0.post0
python-dotenv==1.1.1
pytz==2025.2
requests==2.32.4
rich==14.0.0
scikit-learn==1.7.0
scipy==1.16.0
six==1.17.0
sniffio==1.3.1
SQLAlchemy==2.0.41
threadpoolctl==3.6.0
tqdm==4.67.1
typing-inspection==0.4.1
typing_extensions==4.14.0
tzdata==2025.2
urllib3==2.5.0
Werkzeug==3.1.3

```

---
## 📄 `app.py`

```py
"""Main application entry point for the EzyGallery Flask site.

This module bootstraps the Flask app, registers all blueprints and
provides global context processors. It also includes a generic route
for serving simple flatpage templates so that any ``.html`` file placed
in ``templates/`` can be accessed without additional routing logic.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from flask import Flask, abort, render_template, url_for

from routes import register_blueprints
import config

app = Flask(__name__)
app.config.from_object(config.Config)
register_blueprints(app)


def _static_url(filename: str) -> str:
    """Generate a cache-busted URL for static assets."""
    if app.config.get("FORCE_NOCACHE"):
        version = int(datetime.utcnow().timestamp())
        return url_for("static", filename=filename, v=version)
    return url_for("static", filename=filename)


@app.context_processor
def inject_global_tools() -> dict[str, object]:
    """Inject helper functions and page listings into all templates."""

    def available_pages() -> list[dict[str, str]]:
        pages: list[dict[str, str]] = []
        template_dir = Path(app.template_folder or "templates")
        for tpl in template_dir.glob("*.html"):
            name = tpl.stem
            if name in {"base", "layout"}:
                continue
            url = url_for("flatpage", page_name=name)
            pages.append({"name": name.replace("_", " ").title(), "url": url})
        return pages

    return {
        "static_url": _static_url,
        "available_pages": available_pages(),
    }


@app.route("/toggle-nocache")
def toggle_nocache() -> str:
    """Flip the FORCE_NOCACHE flag for cache busting during development."""
    app.config["FORCE_NOCACHE"] = not app.config.get("FORCE_NOCACHE", False)
    return f"FORCE_NOCACHE = {app.config['FORCE_NOCACHE']}"


@app.route("/<page_name>")
def flatpage(page_name: str):
    """Serve simple templates directly from the ``templates`` folder."""
    template_file = f"{page_name}.html"
    template_path = Path(app.template_folder or "templates") / template_file
    if template_path.is_file():
        return render_template(template_file)
    abort(404)


if __name__ == "__main__":  # pragma: no cover - manual launch
    app.run(host="0.0.0.0", port=8080, debug=True)

```

---
## 📄 `create_db.py`

```py
"""Utility to initialize the SQLite database schema."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.artwork import Base, Artwork

DB_URL = 'sqlite:///app.db'

def init_db(url: str = DB_URL):
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    # Uncomment the lines below to add a sample entry
    # with Session() as session:
    #     sample = Artwork(title='Sample Artwork', seo_filename='sample-artwork')
    #     session.add(sample)
    #     session.commit()

if __name__ == '__main__':
    init_db()
    print('Database initialized.')

```

---
## 📄 `templates/upload.html`

```html
{% extends "base.html" %}
{% block content %}
<h1>Upload</h1>
<p>Coming soon...</p>
{% endblock %}

```

---
## 📄 `templates/docs.html`

```html
{% extends "base.html" %}
{% block content %}
<h1>Docs</h1>
<p>Coming soon...</p>
{% endblock %}

```

---
## 📄 `templates/account.html`

```html
{% extends 'layout.html' %}
{% block content %}
<h1>Account Placeholder</h1>
{% endblock %}

```

---
## 📄 `templates/terms.html`

```html
{% extends 'layout.html' %}
{% block title %}Terms & Conditions{% endblock %}
{% block content %}
<section class="container mx-auto p-6 space-y-6">
  <h1 class="text-3xl font-bold mb-4">Terms &amp; Conditions</h1>
  <p>
    All artwork here is digital and protected by copyright. Mate, don’t steal
    stuff, and we won’t either. Each listing you purchase grants you a licence
    for personal or exclusive use as noted.
  </p>
  <p>
    We offer limited editions for certain pieces. Listings are capped at
    500 characters so you know exactly what you’re getting.
  </p>
  <p>
    By using this site you agree to follow these terms and respect the artists
    who share their stories here.
  </p>
</section>
<footer class="container mx-auto p-6 text-center space-x-4">
  <a href="{{ url_for('flatpage', page_name='index') }}">Back to Home</a>
  <span>|</span>
  <a href="{{ url_for('flatpage', page_name='upload') }}">Upload</a>
  <span>|</span>
  <a href="{{ url_for('flatpage', page_name='gallery') }}">Gallery</a>
</footer>
{% endblock %}

```

---
## 📄 `templates/cart.html`

```html
{% extends 'layout.html' %}
{% block content %}
<h1>Cart Placeholder</h1>
{% endblock %}

```

---
## 📄 `templates/art_detail.html`

```html
{% extends 'layout.html' %}
{% block content %}
<h1>Artwork Detail Placeholder</h1>
{% endblock %}

```

---
## 📄 `templates/checkout.html`

```html
{% extends 'layout.html' %}
{% block content %}
<h1>Checkout Placeholder</h1>
{% endblock %}

```

---
## 📄 `templates/about.html`

```html
{% extends 'layout.html' %}
{% block title %}About EzyGallery{% endblock %}
{% block content %}
<section class="container mx-auto p-6 space-y-6">
  <h1 class="text-3xl font-bold mb-4">About EzyGallery</h1>
  <p>
    Born from the creative drive of Robbie Custance, an Aboriginal artist who
    turned digital to share culture with the world, EzyGallery mixes art and
    automation so every artist can shine.
  </p>
  <p>
    What started as a few mockups on a dusty laptop is now a platform powering
    uploads, AI listings and exports to places like Sellbrite. The goal? Help
    artists tell their stories and keep their voice strong—without selling out
    or drowning in admin.
  </p>
  <img src="{{ static_url('img/placeholder.jpg') }}" alt="Artwork placeholder"
       class="w-full rounded shadow">
  <blockquote class="border-l-4 pl-4 italic">
    "Tech moves fast, but culture runs deep. We reckon both can work together."
  </blockquote>
  <p>
    With a focus on ethical scale and smart automation, we weave
    art-tech fusion that keeps creativity front and centre.
  </p>
</section>
<footer class="container mx-auto p-6 text-center space-x-4">
  <a href="{{ url_for('flatpage', page_name='index') }}">Back to Home</a>
  <span>|</span>
  <a href="{{ url_for('flatpage', page_name='upload') }}">Upload</a>
  <span>|</span>
  <a href="{{ url_for('flatpage', page_name='gallery') }}">Gallery</a>
</footer>
{% endblock %}

```

---
## 📄 `templates/gallery_page.html`

```html
{% extends 'base.html' %}
{% block title %}Gallery - EzyGallery{% endblock %}
{% block content %}
<div class="container py-4">
  <h1 class="mb-3">High-Quality Art Prints: Framed &amp; Recessed</h1>
  <p>Explore our curated collection of modern art prints perfect for any space.</p>
  <div class="row row-cols-1 row-cols-md-2 g-4 my-4">
    <div class="col">
      <a href="/gallery/foil-art" class="text-decoration-none">
        <div class="card h-100">
          <img src="{{ url_for('static', filename='img/placeholder1.jpg') }}" class="card-img-top" alt="Foil Art Prints">
          <div class="card-body text-center">
            <h3 class="card-title">New: Foil Art Prints</h3>
          </div>
        </div>
      </a>
    </div>
    <div class="col">
      <a href="/gallery/collage" class="text-decoration-none">
        <div class="card h-100">
          <img src="{{ url_for('static', filename='img/placeholder2.jpg') }}" class="card-img-top" alt="Collage Sets">
          <div class="card-body text-center">
            <h3 class="card-title">New: Collage Sets</h3>
          </div>
        </div>
      </a>
    </div>
  </div>
  <div class="row row-cols-1 row-cols-md-3 g-4">
    {% for i in range(1,4) %}
    <div class="col">
      <div class="card h-100 text-center">
        <img src="{{ url_for('static', filename='img/artwork' ~ i ~ '.jpg') }}" class="card-img-top" alt="Artwork {{ i }}">
        <div class="card-body">
          <h5 class="card-title">Artwork {{ i }}</h5>
          <p class="card-text"><span class="fw-bold">$44.00</span> <del>$55</del> 20% Off</p>
          <p class="card-text small text-muted">Customize: ✓ Frame, ✓ Size</p>
        </div>
      </div>
    </div>
    {% endfor %}
  </div>
</div>
{% endblock %}

```

---
## 📄 `templates/contact.html`

```html
{% extends 'base.html' %}
{% block title %}Contact - EzyGallery{% endblock %}
{% block content %}
<h2>Contact</h2>
<p>Contact us at <a href="mailto:info@example.com">info@example.com</a>.</p>
{% endblock %}

```

---
## 📄 `templates/artist_profile.html`

```html
{% extends 'layout.html' %}
{% block content %}
<h1>Artist Profile Placeholder</h1>
{% endblock %}

```

---
## 📄 `templates/gallery.html`

```html
{% extends 'layout.html' %}
{% block title %}Artwork Gallery{% endblock %}
{% block content %}
<section class="container mx-auto p-6">
  <h1 class="text-3xl font-bold mb-6">Artwork Gallery</h1>
  <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
    {% set titles = [
      'Wattle Dreaming',
      'Ocean Eyes',
      'Tracks of Fire',
      'Desert Whispers',
      'Rain Song',
      'Midnight Gum',
      'Coastal Flow',
      'Sunlit Path',
      'Earth Echo'
    ] %}
    {% for title in titles[:9] %}
    <figure class="relative group bg-gray-100 rounded shadow overflow-hidden">
      <img src="{{ static_url('img/placeholder.jpg') }}" alt="{{ title }}"
           class="w-full h-auto">
      <figcaption class="absolute inset-0 flex flex-col items-center justify-center bg-black bg-opacity-50 opacity-0 group-hover:opacity-100 transition">
        <h3 class="text-white mb-2">{{ title }}</h3>
        <div class="space-x-2">
          <a href="#" class="px-2 py-1 bg-white text-sm">View Details</a>
          <a href="#" class="px-2 py-1 bg-white text-sm">Add to Export</a>
        </div>
      </figcaption>
    </figure>
    {% endfor %}
  </div>
</section>
<footer class="container mx-auto p-6 text-center space-x-4">
  <a href="{{ url_for('flatpage', page_name='index') }}">Back to Home</a>
  <span>|</span>
  <a href="{{ url_for('flatpage', page_name='upload') }}">Upload</a>
  <span>|</span>
  <a href="{{ url_for('flatpage', page_name='about') }}">About</a>
</footer>
{% endblock %}

```

---
## 📄 `templates/privacy.html`

```html
{% extends 'layout.html' %}
{% block title %}Privacy Policy{% endblock %}
{% block content %}
<section class="container mx-auto p-6 space-y-6">
  <h1 class="text-3xl font-bold mb-4">Privacy Policy</h1>
  <p>
    We keep things simple: no sneaky tracking beyond what helps the site run.
    Anything you upload stays private until you choose to share it.
  </p>
  <p>
    We do lean on a few mates like OpenAI and Sellbrite to power our tools,
    so your data may pass through their services—but only to make your life
    easier here on EzyGallery.
  </p>
  <p>Got questions? Email us at <a href="mailto:privacy@ezygallery.com">privacy@ezygallery.com</a>.</p>
</section>
<footer class="container mx-auto p-6 text-center space-x-4">
  <a href="{{ url_for('flatpage', page_name='index') }}">Back to Home</a>
  <span>|</span>
  <a href="{{ url_for('flatpage', page_name='upload') }}">Upload</a>
  <span>|</span>
  <a href="{{ url_for('flatpage', page_name='gallery') }}">Gallery</a>
</footer>
{% endblock %}

```

---
## 📄 `templates/room_preview.html`

```html
{% extends 'layout.html' %}
{% block content %}
<h1>Room Preview Placeholder</h1>
{% endblock %}

```

---
## 📄 `templates/index.html`

```html
{% extends "base.html" %}
{% block content %}
<h1>Home</h1>
<p>Coming soon...</p>
{% endblock %}

```

---
## 📄 `templates/artwork_detail.html`

```html
{% extends 'base.html' %}
{% block title %}{{ artwork.title }} - EzyGallery{% endblock %}
{% block content %}
<div class="container py-4">
  <a href="{{ url_for('gallery.gallery') }}" class="d-block mb-3">&larr; Back to Gallery</a>
  <div class="row">
    <div class="col-md-6 text-center mb-3">
      <img src="{{ url_for('static', filename='img/artwork1.jpg') }}" class="img-fluid" alt="{{ artwork.title }}">
    </div>
    <div class="col-md-6">
      <h1>{{ artwork.title }}</h1>
      <p class="h5 mb-3">
        <span class="fw-bold">${{ artwork.price }}</span>
        {% if artwork.discount_price %}<del>${{ artwork.discount_price }}</del>{% endif %}
      </p>
      <p class="mb-3">Customize your print with various frame and size options.</p>
      <h3>Mockups</h3>
      <ul>
        {% for i in range(1,11) %}
        <li>MU-{{ '%02d' % i }}</li>
        {% endfor %}
      </ul>
      <button class="btn btn-primary">Buy Print</button>
    </div>
  </div>
</div>
{% endblock %}

```

---
## 📄 `templates/base.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Ezy Gallery{% endblock %}</title>
    <link rel="stylesheet" href="{{ static_url('css/menu-style.css') }}">
</head>
<body>
    <div class="page-wrapper">
        <header class="site-header">
            <div class="header-content">
                <div class="header-left">
                    <img src="{{ static_url('icons/svg/light/palette-light.svg') }}" alt="Palette Icon" class="header-icon">
                    <a href="{{ url_for('flatpage', page_name='index') }}" class="logo">Ezy Gallery</a>
                </div>
                <div class="header-center">
                    <button id="menuToggle" class="menu-toggle">
                        <span>Menu</span>
                        <img src="{{ static_url('icons/svg/light/arrow-circle-down-light.svg') }}" alt="Open menu" class="header-icon arrow-icon">
                    </button>
                </div>
                <div class="header-right">
                    <a href="#" id="userAuthLink" class="header-icon-link">
                        <img id="userIcon" src="{{ static_url('icons/svg/light/user-circle-light.svg') }}" alt="User Icon" class="header-icon">
                    </a>
                    <button id="themeToggle" class="theme-toggle-btn">
                        <img id="themeIcon" src="{{ static_url('icons/svg/light/moon-light.svg') }}" alt="Theme Toggle Icon" class="header-icon">
                    </button>
                </div>
            </div>
        </header>

        <nav id="overlayMenu">
            <div class="overlay-header">
                <div class="header-content">
                    <div class="header-left">
                        <img src="{{ static_url('icons/svg/light/palette-light.svg') }}" alt="Palette Icon" class="header-icon">
                        <a href="{{ url_for('flatpage', page_name='index') }}" class="logo">Ezy Gallery</a>
                    </div>
                    <div class="header-center">
                        <button id="menuToggleOverlay" class="menu-toggle">
                            <span>Menu</span>
                            <img src="{{ static_url('icons/svg/light/arrow-circle-up-light.svg') }}" alt="Close menu" class="header-icon arrow-icon">
                        </button>
                    </div>
                    <div class="header-right">
                        <a href="#" id="userAuthLinkOverlay" class="header-icon-link">
                            <img id="userIconOverlay" src="{{ static_url('icons/svg/light/user-circle-light.svg') }}" alt="User Icon" class="header-icon">
                        </a>
                        <button id="themeToggleOverlay" class="theme-toggle-btn">
                            <img id="themeIconOverlay" src="{{ static_url('icons/svg/light/moon-light.svg') }}" alt="Theme Toggle Icon" class="header-icon">
                        </button>
                    </div>
                </div>
            </div>
            <div class="overlay-content">
                <div class="menu-columns">
                    <ul class="menu-column">
                        <li><a href="{{ url_for('flatpage', page_name='upload') }}">Upload</a></li>
                        <li><a href="{{ url_for('flatpage', page_name='gallery') }}">Gallery</a></li>
                        <li><a href="#">Finalised</a></li>
                        <li><a href="#">Exports</a></li>
                        <li><a href="#">Prompts</a></li>
                        <li><a href="{{ url_for('flatpage', page_name='docs') }}">Docs</a></li>
                        <li><a href="#">Admin</a></li>
                    </ul>
                    <ul class="menu-column">
                        <li><a href="#">GDWS Editor</a></li>
                        <li><a href="#">AIGW</a></li>
                        <li><a href="#">Privacy Policy</a></li>
                        <li><a href="#">Terms &amp; Limitations</a></li>
                        <li><a href="{{ url_for('flatpage', page_name='accessibility') }}">Accessibility</a></li>
                        <li><a href="{{ url_for('flatpage', page_name='contact') }}">Contact</a></li>
                        <li><a href="{{ url_for('flatpage', page_name='about') }}">About</a></li>
                    </ul>
                </div>
            </div>
        </nav>

        <main class="main-content">
            {% block content %}{% endblock %}
        </main>

        <footer class="site-footer">
            <div class="footer-content">
                <div class="footer-columns">
                    <div class="footer-col">
                        <h4>Ezy Gallery</h4>
                        <p>Aboriginal Australian art powered by next-gen automation &amp; heart.</p>
                    </div>
                    <div class="footer-col">
                        <h4>Menu</h4>
                        <ul>
                            <li><a href="{{ url_for('flatpage', page_name='index') }}">Home</a></li>
                            <li><a href="{{ url_for('flatpage', page_name='upload') }}">Upload</a></li>
                            <li><a href="{{ url_for('flatpage', page_name='gallery') }}">Gallery</a></li>
                            <li><a href="#">Finalised</a></li>
                            <li><a href="#">Exports</a></li>
                        </ul>
                    </div>
                    <div class="footer-col">
                        <h4>Company</h4>
                        <ul>
                            <li><a href="{{ url_for('flatpage', page_name='about') }}">About</a></li>
                            <li><a href="{{ url_for('flatpage', page_name='contact') }}">Contact</a></li>
                            <li><a href="#">Privacy Policy</a></li>
                            <li><a href="#">Terms &amp; Limitations</a></li>
                            <li><a href="{{ url_for('flatpage', page_name='accessibility') }}">Accessibility</a></li>
                        </ul>
                    </div>
                    <div class="footer-col">
                        <h4>Join our newsletter</h4>
                        <form class="newsletter-form">
                            <input type="email" placeholder="Your email" required>
                            <button type="submit" aria-label="Subscribe to newsletter">
                                <img src="{{ static_url('icons/svg/light/arrow-circle-up-light.svg') }}" class="header-icon" alt="Submit">
                            </button>
                        </form>
                    </div>
                </div>
                <div class="copyright-bar">
                    <p>© 2025 Robin Custance. All rights reserved.</p>
                </div>
            </div>
        </footer>
    </div>
    <script src="{{ static_url('js/menu-script.js') }}"></script>
</body>
</html>

```

---
## 📄 `templates/search.html`

```html
{% extends 'layout.html' %}
{% block content %}
<h1>Search Placeholder</h1>
{% endblock %}

```

---
## 📄 `templates/layout.html`

```html
{% extends 'base.html' %}
{% block content %}{% endblock %}

```

---
## 📄 `templates/intro.html`

```html
{% extends 'layout.html' %}
{% block title %}Welcome to EzyGallery{% endblock %}
{% block content %}
<section class="container mx-auto p-6 space-y-6 text-center">
  <h1 class="text-4xl font-bold mb-4">Your Story. Your Art. Your Gallery.</h1>
  <p>
    Aboriginal Australian art meets next-gen automation here at EzyGallery.
    We blend culture with clever tech so you can focus on creating.
  </p>
  <ul class="list-disc list-inside text-left max-w-xl mx-auto">
    <li>Upload once, store forever</li>
    <li>AI-crafted listings ready for the web</li>
    <li>Mockups sorted by room and vibe</li>
    <li>Export straight to your favourite marketplaces</li>
  </ul>
  <div class="space-x-4 mt-4">
    <a href="{{ url_for('flatpage', page_name='upload') }}" class="px-4 py-2 bg-blue-600 text-white rounded">Upload</a>
    <a href="{{ url_for('flatpage', page_name='gallery') }}" class="px-4 py-2 bg-green-600 text-white rounded">Gallery</a>
  </div>
</section>
<footer class="container mx-auto p-6 text-center space-x-4">
  <a href="{{ url_for('flatpage', page_name='index') }}">Back to Home</a>
  <span>|</span>
  <a href="{{ url_for('flatpage', page_name='about') }}">About</a>
  <span>|</span>
  <a href="{{ url_for('flatpage', page_name='privacy') }}">Privacy Policy</a>
</footer>
{% endblock %}

```

---
## 📄 `templates/login.html`

```html
{% extends 'layout.html' %}
{% block content %}
<h1>Login Placeholder</h1>
{% endblock %}

```

---
## 📄 `templates/accessibility.html`

```html
{% extends 'base.html' %}
{% block title %}Accessibility - EzyGallery{% endblock %}
{% block content %}
<div class="container py-4">
  <h1>Accessibility Commitment</h1>
  <p>EzyGallery strives to ensure our website is usable by everyone.</p>
  <h2>Accessibility Features</h2>
  <ul>
    <li>Captions for multimedia content</li>
    <li>Keyboard navigation support</li>
    <li>Logical heading structure</li>
    <li>Descriptive link text</li>
  </ul>
  <h2>Ongoing Process</h2>
  <p>We continually review and improve our site to meet WCAG 2.0 AA guidelines.</p>
  <h2>Contact Us</h2>
  <p>If you encounter issues, email <a href="mailto:accessibility@ezygallery.com">accessibility@ezygallery.com</a>.</p>
</div>
{% endblock %}

```

---
## 📄 `templates/components/add_to_cart_modal.html`

```html
<!-- Add to cart modal placeholder -->

```

---
## 📄 `templates/components/room_mockup_modal.html`

```html
<!-- Room mockup modal placeholder -->

```

---
## 📄 `templates/components/header.html`

```html
<header style="padding:10px;display:flex;justify-content:space-between;align-items:center;">
  <h1 style="margin:0;">EzyGallery</h1>
  <button id="theme-toggle">Toggle Theme</button>
</header>

```

---
## 📄 `templates/components/filterbar.html`

```html
<!-- Filterbar placeholder -->

```

---
## 📄 `templates/components/artist_card.html`

```html
<!-- Artist card placeholder -->

```

---
## 📄 `templates/components/sidebar.html`

```html
<!-- Sidebar placeholder -->

```

---
## 📄 `templates/components/artwork_grid.html`

```html
<!-- Artwork grid placeholder -->

```

---
## 📄 `templates/components/footer.html`

```html
<!-- Footer placeholder -->

```

---
## 📄 `models/order.py`

```py
# Order model placeholder

```

---
## 📄 `models/user.py`

```py
# User model placeholder

```

---
## 📄 `models/artist.py`

```py
# Artist model placeholder

```

---
## 📄 `models/__init__.py`

```py
# Model package

```

---
## 📄 `models/artwork.py`

```py
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class Artwork(Base):
    __tablename__ = 'artworks'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    seo_filename = Column(String(255), unique=True, nullable=False)
    artist_name = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    tags = Column(String(255))
    aspect_ratio = Column(String(50))
    primary_colour = Column(String(50))
    mockups_folder = Column(String(255))
    price = Column(Float)
    discount_price = Column(Float)
    status = Column(String(50), default='active')

    def __repr__(self):
        return f"<Artwork {self.seo_filename}>"

```

---
## 📄 `models/review.py`

```py
# Review model placeholder

```

---
## 📄 `menu-demo/main.html`

```html
<!DOCTYPE html>
<!-- The 'dark' class will be toggled on this html tag -->
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ezy Gallery</title>
      <!-- Favicons & Web Manifest -->
    <link rel="apple-touch-icon" sizes="180x180" href="{{ url_for('static', filename='favicons/apple-touch-icon.png') }}">
    <link rel="icon" type="image/png" sizes="32x32" href="{{ url_for('static', filename='favicons/favicon-32x32.png') }}">
    <link rel="icon" type="image/png" sizes="16x16" href="{{ url_for('static', filename='favicons/favicon-16x16.png') }}">
    <link rel="manifest" href="{{ url_for('static', filename='favicons/site.webmanifest') }}">
    <link rel="shortcut icon" href="{{ url_for('static', filename='favicons/favicon.ico') }}">
    <meta name="msapplication-TileColor" content="#ffffff">
    <meta name="theme-color" content="#ffffff">
    <!-- Android-specific -->
    <link rel="icon" type="image/png" sizes="192x192" href="{{ url_for('static', filename='favicons/android-chrome-192x192.png') }}">
    <link rel="icon" type="image/png" sizes="512x512" href="{{ url_for('static', filename='favicons/android-chrome-512x512.png') }}">
    <!-- Link to the external CSS file -->
    <link rel="stylesheet" href="static/css/style.css">
    
</head>
<body>
    <div class="page-wrapper">
        <!-- Header Section -->
        <header class="site-header">
            <div class="header-content">
                <div class="header-left">
                    <img src="static/icons/svg/light/palette-light.svg" alt="Palette Icon" class="header-icon">
                    <a href="#" class="logo">ART Narrator</a>
                </div>
                <div class="header-center">
                    <button id="menuToggle" class="menu-toggle">
                        <span>Menu</span>
                        <img src="static/icons/svg/light/arrow-circle-down-light.svg" alt="Open menu" class="header-icon arrow-icon">
                    </button>
                </div>
                <div class="header-right">
                    <a href="#" id="userAuthLink" class="header-icon-link">
                        <img id="userIcon" src="static/icons/svg/light/user-circle-light.svg" alt="User Icon" class="header-icon">
                    </a>
                    <button id="themeToggle" class="theme-toggle-btn">
                        <img id="themeIcon" src="static/icons/svg/light/moon-light.svg" alt="Theme Toggle Icon" class="header-icon">
                    </button>
                </div>
            </div>
        </header>

        <!-- Overlay Navigation Menu -->
        <nav id="overlayMenu">
            <!-- To remove the header from the dropdown menu, comment out or delete the entire 'overlay-header' div below -->
            <div class="overlay-header">
                <div class="header-content">
                     <div class="header-left">
                        <img src="static/icons/svg/light/palette-light.svg" alt="Palette Icon" class="header-icon">
                        <a href="#" class="logo">ART Narrator</a>
                    </div>
                    <div class="header-center">
                        <button id="menuToggleOverlay" class="menu-toggle">
                            <span>Menu</span>
                            <img src="static/icons/svg/light/arrow-circle-up-light.svg" alt="Close menu" class="header-icon arrow-icon">
                        </button>
                    </div>
                    <div class="header-right">
                         <a href="#" id="userAuthLinkOverlay" class="header-icon-link">
                            <img id="userIconOverlay" src="static/icons/svg/light/user-circle-light.svg" alt="User Icon" class="header-icon">
                        </a>
                        <button id="themeToggleOverlay" class="theme-toggle-btn">
                            <img id="themeIconOverlay" src="static/icons/svg/light/moon-light.svg" alt="Theme Toggle Icon" class="header-icon">
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="overlay-content">
                <div class="menu-columns">
                    <ul class="menu-column">
                        <li><a href="#">Upload</a></li>
                        <li><a href="#">Gallery</a></li>
                        <li><a href="#">Finalised</a></li>
                        <li><a href="#">Exports</a></li>
                        <li><a href="#">Prompts</a></li>
                        <li><a href="#">Docs</a></li>
                        <li><a href="#">Admin</a></li>
                    </ul>
                    <ul class="menu-column">
                        <li><a href="#">GDWS Editor</a></li>
                        <li><a href="#">AIGW</a></li>
                        <li><a href="#">Privacy Policy</a></li>
                        <li><a href="#">Terms & Limitations</a></li>
                        <li><a href="#">Accessibility</a></li>
                        <li><a href="#">Contact</a></li>
                        <li><a href="#">About</a></li>
                    </ul>
                </div>
            </div>
        </nav>

        <!-- Main Content of the page -->
        <main class="main-content">
            <h1>Main Content</h1>
            <p>This is the main content of the page. When you open the menu, this area will be covered by the overlay.</p>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor.</p>
        </main>

        <!-- Footer Section -->
        <footer class="site-footer">
            <div class="footer-content">
                <div class="footer-columns">
                    <div class="footer-col">
                        <h4>Ezy Gallery</h4>
                        <p>Aboriginal Australian art powered by next-gen automation & heart.</p>
                    </div>
                    <div class="footer-col">
                        <h4>Menu</h4>
                        <ul>
                            <li><a href="#">Home</a></li>
                            <li><a href="#">Upload</a></li>
                            <li><a href="#">Gallery</a></li>
                            <li><a href="#">Finalised</a></li>
                             <li><a href="#">Exports</a></li>
                        </ul>
                    </div>
                    <div class="footer-col">
                        <h4>Company</h4>
                        <ul>
                           <li><a href="#">About</a></li>
                           <li><a href="#">Contact</a></li>
                           <li><a href="#">Privacy Policy</a></li>
                           <li><a href="#">Terms & Limitations</a></li>
                           <li><a href="#">Accessibility</a></li>
                        </ul>
                    </div>
                    <div class="footer-col">
                        <h4>Join our newsletter</h4>
                        <form class="newsletter-form">
                            <input type="email" placeholder="Your email" required>
                            <button type="submit" aria-label="Subscribe to newsletter">
                                <img src="static/icons/svg/light/arrow-circle-up-light.svg" class="header-icon" alt="Submit">
                            </button>
                        </form>
                    </div>
                </div>
                <div class="copyright-bar">
                    <p>© 2025 Robin Custance. All rights reserved.</p>
                </div>
            </div>
        </footer>
    </div>

    <!-- Link to the external JavaScript file -->
    <script src="static/js/script.js"></script>

</body>
</html>
```

---
## 📄 `menu-demo/static/css/style.css`

```css
/* ==========================================================================
   File: style.css
   Purpose: Consolidated styles for ART Narrator.
   ========================================================================== */

/* --- [1] CSS Variables for Theming --- */
:root {
    --bg-color-light: #f9f9f6;
    --text-color-light: #0d0d0d;
    --border-color-light: #e0e0e0;
    --accent-color-light: #ed7214;
    --overlay-bg-light: rgba(249, 249, 246, 0.85);

    --bg-color-dark: #121212;
    --text-color-dark: #f0f0f0;
    --border-color-dark: #333;
    --accent-color-dark: #ed7214;
    --overlay-bg-dark: rgba(20, 20, 20, 0.85);
}

/* --- [2] Basic Body & Font Styles --- */
html, body {
    height: 100%;
}

body {
    margin: 0;
    font-family: monospace;
    background-color: var(--bg-color-light);
    color: var(--text-color-light);
    transition: background-color 0.3s ease, color 0.3s ease;
    display: flex;
    flex-direction: column;
}

html.dark body {
    background-color: var(--bg-color-dark);
    color: var(--text-color-dark);
}

.page-wrapper {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}

/* --- [3] Header Styles --- */
.site-header {
    padding: 1.5rem 2rem;
    border-bottom: 1px solid var(--border-color-light);
    position: relative;
    z-index: 1000;
}

html.dark .site-header {
    border-bottom-color: var(--border-color-dark);
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1600px;
    margin: 0 auto;
}

.header-left, .header-right {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex: 1;
}

.header-center {
    flex: 0 1 auto;
    text-align: center;
}

.header-right {
    justify-content: flex-end;
}

.logo, .cart, .menu-toggle {
    color: var(--text-color-light);
    text-decoration: none;
    font-weight: 500;
}

html.dark .logo, html.dark .cart, html.dark .menu-toggle {
    color: var(--text-color-dark);
}

.menu-toggle {
    background: none;
    border: 1px solid var(--text-color-light);
    padding: 0.5rem 1rem;
    cursor: pointer;
    border-radius: 20px;
    font-family: monospace;
    font-size: 1rem;
    transition: background-color 0.2s, color 0.2s;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}

html.dark .menu-toggle {
    border-color: var(--text-color-dark);
}

.menu-toggle:hover {
    background-color: var(--text-color-light);
    color: var(--bg-color-light);
}

html.dark .menu-toggle:hover {
    background-color: var(--text-color-dark);
    color: var(--bg-color-dark);
}

/* --- [4] Icon Styles --- */
.header-icon {
    width: 24px;
    height: 24px;
    vertical-align: middle;
}

.arrow-icon {
    width: 20px;
    height: 20px;
}

html.dark .header-icon {
    filter: invert(1);
}

.menu-toggle:hover .header-icon {
    filter: invert(1);
}
html.dark .menu-toggle:hover .header-icon {
    filter: none;
}


.header-icon-link, .theme-toggle-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: none;
    border: none;
    padding: 0.25rem;
    cursor: pointer;
    border-radius: 50%;
    transition: background-color 0.2s;
}

.header-icon-link:hover, .theme-toggle-btn:hover {
    background-color: rgba(0,0,0,0.05);
}

html.dark .header-icon-link:hover, html.dark .theme-toggle-btn:hover {
    background-color: rgba(255,255,255,0.1);
}


/* --- [5] Main Overlay Menu Styles --- */
#overlayMenu {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 999;
    visibility: hidden;
    opacity: 0;
    transition: opacity 0.4s cubic-bezier(0.25, 1, 0.5, 1), visibility 0.4s cubic-bezier(0.25, 1, 0.5, 1);
    background-color: var(--overlay-bg-light);
    -webkit-backdrop-filter: blur(15px);
    backdrop-filter: blur(15px);
    display: flex;
    align-items: center; /* Center content vertically */
    justify-content: center; /* Center content horizontally */
    overflow-y: auto;
}

html.dark #overlayMenu {
    background-color: var(--overlay-bg-dark);
}

#overlayMenu.is-active {
    visibility: visible;
    opacity: 1;
}

.overlay-header {
    position: absolute; /* Changed from fixed */
    top: 0;
    left: 0;
    width: 100%;
    padding: 1.5rem 2rem;
    box-sizing: border-box;
    z-index: 1001; /* Ensure header is on top of content */
}

.overlay-content {
    text-align: left;
    width: 90%;
    max-width: 1200px;
    padding: 6rem 0; /* Adjust padding to not be obscured by header */
}

/* --- [6] Two-Column Menu Layout --- */
.menu-columns {
    display: flex;
    justify-content: space-around;
    width: 100%;
    gap: 2rem;
}

.menu-column {
    list-style: none;
    padding: 0;
    margin: 0;
    flex: 1;
}

.overlay-content ul li {
    font-size: 3em;
    font-weight: 500;
    line-height: 1.4;
    margin: 0.5em 0;
    transform: translateY(20px);
    opacity: 0;
    transition: opacity 0.5s ease, transform 0.5s ease;
}

#overlayMenu.is-active .overlay-content ul li {
    transform: translateY(0);
    opacity: 1;
}

/* Staggered animation */
#overlayMenu.is-active .menu-column:nth-child(1) li:nth-child(1) { transition-delay: 0.25s; }
#overlayMenu.is-active .menu-column:nth-child(1) li:nth-child(2) { transition-delay: 0.30s; }
#overlayMenu.is-active .menu-column:nth-child(1) li:nth-child(3) { transition-delay: 0.35s; }
#overlayMenu.is-active .menu-column:nth-child(1) li:nth-child(4) { transition-delay: 0.40s; }
#overlayMenu.is-active .menu-column:nth-child(1) li:nth-child(5) { transition-delay: 0.45s; }
#overlayMenu.is-active .menu-column:nth-child(1) li:nth-child(6) { transition-delay: 0.50s; }
#overlayMenu.is-active .menu-column:nth-child(1) li:nth-child(7) { transition-delay: 0.55s; }

#overlayMenu.is-active .menu-column:nth-child(2) li:nth-child(1) { transition-delay: 0.27s; }
#overlayMenu.is-active .menu-column:nth-child(2) li:nth-child(2) { transition-delay: 0.32s; }
#overlayMenu.is-active .menu-column:nth-child(2) li:nth-child(3) { transition-delay: 0.37s; }
#overlayMenu.is-active .menu-column:nth-child(2) li:nth-child(4) { transition-delay: 0.42s; }
#overlayMenu.is-active .menu-column:nth-child(2) li:nth-child(5) { transition-delay: 0.47s; }
#overlayMenu.is-active .menu-column:nth-child(2) li:nth-child(6) { transition-delay: 0.52s; }
#overlayMenu.is-active .menu-column:nth-child(2) li:nth-child(7) { transition-delay: 0.57s; }

.overlay-content a {
    color: var(--text-color-light);
    text-decoration: none;
    transition: color 0.3s ease;
}

html.dark .overlay-content a {
    color: var(--text-color-dark);
}

.overlay-content a:hover {
    color: var(--accent-color-light);
}

html.dark .overlay-content a:hover {
    color: var(--accent-color-dark);
}

/* --- [7] Main Content & Footer Styles --- */
.main-content {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
    flex-grow: 1;
}

.site-footer {
    background-color: var(--bg-color-light);
    border-top: 1px solid var(--border-color-light);
    padding: 3rem 2rem;
    color: var(--text-color-light);
}

html.dark .site-footer {
    background-color: var(--bg-color-dark);
    border-top-color: var(--border-color-dark);
    color: var(--text-color-dark);
}

.footer-content {
    max-width: 1600px;
    margin: 0 auto;
}

.footer-columns {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.footer-col h4 {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 1rem;
}

.footer-col p {
    font-size: 0.9rem;
    line-height: 1.6;
    opacity: 0.8;
}

.footer-col ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.footer-col ul li {
    margin-bottom: 0.5rem;
}

.footer-col a {
    color: var(--text-color-light);
    text-decoration: none;
    opacity: 0.8;
    transition: opacity 0.2s;
}

html.dark .footer-col a {
    color: var(--text-color-dark);
}

.footer-col a:hover {
    opacity: 1;
    text-decoration: underline;
}

.newsletter-form {
    display: flex;
}

.newsletter-form input {
    flex-grow: 1;
    border: 1px solid var(--border-color-light);
    border-right: none;
    padding: 0.75rem;
    background: transparent;
    color: var(--text-color-light);
    font-family: monospace;
}
html.dark .newsletter-form input {
    border-color: var(--border-color-dark);
    color: var(--text-color-dark);
}

.newsletter-form button {
    background: transparent;
    border: 1px solid var(--border-color-light);
    padding: 0.5rem;
    cursor: pointer;
}
html.dark .newsletter-form button {
    border-color: var(--border-color-dark);
}

.copyright-bar {
    border-top: 1px solid var(--border-color-light);
    padding-top: 1.5rem;
    margin-top: 2rem;
    text-align: center;
    font-size: 0.8rem;
    opacity: 0.7;
}
html.dark .copyright-bar {
    border-top-color: var(--border-color-dark);
}

/* --- [8] Responsive Styles for Mobile --- */
@media (max-width: 768px) {
    .menu-columns {
        flex-direction: column;
        align-items: center;
        text-align: center;
        gap: 0;
    }
    .overlay-content ul li {
        font-size: clamp(1.5rem, 6vw, 2.5rem);
    }
}
```

---
## 📄 `menu-demo/static/js/script.js`

```js
/* ==========================================================================
   File: script.js
   Purpose: Handles interactive logic for the menu and theme toggling.
   ========================================================================== */

document.addEventListener("DOMContentLoaded", function () {
    const bodyTag = document.body;
    const htmlTag = document.documentElement;

    // === [ THEME TOGGLE LOGIC ] ===
    const themeToggle = document.getElementById("themeToggle");
    const themeToggleOverlay = document.getElementById("themeToggleOverlay");
    const themeIcon = document.getElementById("themeIcon");
    const themeIconOverlay = document.getElementById("themeIconOverlay");
    
    const userIcon = document.getElementById("userIcon");
    const userIconOverlay = document.getElementById("userIconOverlay");
    const userAuthLink = document.getElementById("userAuthLink");
    const userAuthLinkOverlay = document.getElementById("userAuthLinkOverlay");

    const icons = {
        sun: 'static/icons/svg/light/sun-light.svg',
        moon: 'static/icons/svg/light/moon-light.svg',
        user: 'static/icons/svg/light/user-circle-light.svg',
        userChecked: 'static/icons/svg/light/user-circle-check-light.svg'
    };

    const setTheme = (isDark) => {
        htmlTag.classList.toggle('dark', isDark);
        if (themeIcon) themeIcon.src = isDark ? icons.sun : icons.moon;
        if (themeIconOverlay) themeIconOverlay.src = isDark ? icons.sun : icons.moon;
        localStorage.setItem('darkMode', isDark);
    };

    const savedThemeIsDark = localStorage.getItem('darkMode') === 'true';
    setTheme(savedThemeIsDark);

    const toggleTheme = () => {
        const isCurrentlyDark = htmlTag.classList.contains('dark');
        setTheme(!isCurrentlyDark);
    };

    if (themeToggle) themeToggle.addEventListener('click', toggleTheme);
    if (themeToggleOverlay) themeToggleOverlay.addEventListener('click', toggleTheme);
    
    let isLoggedIn = false;
    const toggleLogin = (e) => {
        e.preventDefault();
        isLoggedIn = !isLoggedIn;
        if (userIcon) userIcon.src = isLoggedIn ? icons.userChecked : icons.user;
        if (userIconOverlay) userIconOverlay.src = isLoggedIn ? icons.userChecked : icons.user;
    };

    if (userAuthLink) userAuthLink.addEventListener('click', toggleLogin);
    if (userAuthLinkOverlay) userAuthLinkOverlay.addEventListener('click', toggleLogin);


    // === [ OVERLAY MENU LOGIC ] ===
    const menuToggle = document.getElementById("menuToggle");
    const menuToggleOverlay = document.getElementById("menuToggleOverlay");
    const overlayMenu = document.getElementById("overlayMenu");

    const openMenu = () => {
        if (!overlayMenu) return;
        overlayMenu.classList.add("is-active");
        bodyTag.style.overflow = 'hidden';
    };

    const closeMenu = () => {
        if (!overlayMenu) return;
        overlayMenu.classList.remove("is-active");
        bodyTag.style.overflow = '';
    };

    if (menuToggle) menuToggle.addEventListener("click", openMenu);
    if (menuToggleOverlay) menuToggleOverlay.addEventListener("click", closeMenu);

    if (overlayMenu) {
      overlayMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', closeMenu);
      });
        overlayMenu.addEventListener('click', (event) => {
            // This checks if the click was on the overlay background itself,
            // and NOT on any of its children (like the content or header).
            if (event.target === overlayMenu) {
                closeMenu();
            }
        });
    }

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && overlayMenu.classList.contains('is-active')) {
            closeMenu();
        }
    });
});
```

---
## 📄 `reports/EZYGALLERY-12-JUL-2025-03-20AM/env_metadata.txt`

```txt
Python 3.11.2
Linux art 6.1.0-37-cloud-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.140-1 (2025-05-22) x86_64 GNU/Linux
annotated-types==0.7.0
anyio==4.9.0
blinker==1.9.0
certifi==2025.6.15
charset-normalizer==3.4.2
click==8.2.1
distro==1.9.0
Flask==3.1.1
gunicorn==23.0.0
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
jiter==0.10.0
joblib==1.5.1
markdown-it-py==3.0.0
MarkupSafe==3.0.2
mdurl==0.1.2
numpy==2.3.1
openai==1.93.0
opencv-python==4.11.0.86
packaging==25.0
pandas==2.3.0
pillow==11.2.1
pydantic==2.11.7
pydantic_core==2.33.2
Pygments==2.19.2
python-dateutil==2.9.0.post0
python-dotenv==1.1.1
pytz==2025.2
requests==2.32.4
rich==14.0.0
scikit-learn==1.7.0
scipy==1.16.0
six==1.17.0
sniffio==1.3.1
threadpoolctl==3.6.0
tqdm==4.67.1
typing-inspection==0.4.1
typing_extensions==4.14.0
tzdata==2025.2
urllib3==2.5.0
Werkzeug==3.1.3



```

---
## 📄 `reports/EZYGALLERY-12-JUL-2025-03-20AM/git_snapshot.txt`

```txt
On branch master
Your branch is ahead of 'origin/master' by 1 commit.
  (use "git push" to publish your local commits)

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	reports/EZYGALLERY-12-JUL-2025-03-20AM/

nothing added to commit but untracked files present (use "git add" to track)
commit d8c0d03b7836e013f60465ee0643abdc82815dfe
Author: Robin Custance <robincustance@gmail.com>
Date:   Sat Jul 12 03:20:44 2025 +0930

    Auto commit: Preparing for Codex upgrade



```

---
## 📄 `reports/REPORTS-11-JUL-2025-05-31AM/env_metadata.txt`

```txt
Python 3.11.2
Linux art 6.1.0-37-cloud-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.140-1 (2025-05-22) x86_64 GNU/Linux
acme==4.1.1
annotated-types==0.7.0
anyio==4.9.0
blinker==1.9.0
certbot==4.1.1
certbot-nginx==4.1.1
certifi==2025.6.15
cffi==1.17.1
chardet==5.2.0
charset-normalizer==3.4.2
click==8.2.1
ConfigArgParse==1.7.1
configobj==5.0.9
cryptography==45.0.5
distro==1.9.0
Flask==3.1.1
gunicorn==23.0.0
h11==0.16.0
httpcore==1.0.9
httplib2==0.22.0
httpx==0.28.1
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
jiter==0.10.0
joblib==1.5.1
josepy==2.0.0
markdown-it-py==3.0.0
MarkupSafe==3.0.2
mdurl==0.1.2
numpy==2.2.6
openai==1.93.1
opencv-python==4.12.0.88
packaging==25.0
pandas==2.3.1
parsedatetime==2.6
pillow==11.3.0
pycparser==2.22
pycurl==7.45.6
pydantic==2.11.7
pydantic_core==2.33.2
Pygments==2.19.2
pyOpenSSL==25.1.0
pyparsing==3.2.3
pyRFC3339==2.0.1
python-dateutil==2.9.0.post0
python-debian==1.0.1
python-debianbts==4.1.1
python-dotenv==1.1.1
pytz==2025.2
PyYAML==6.0.2
requests==2.32.4
rich==14.0.0
scikit-learn==1.7.0
scipy==1.16.0
six==1.17.0
sniffio==1.3.1
threadpoolctl==3.6.0
tqdm==4.67.1
typing-inspection==0.4.1
typing_extensions==4.14.1
tzdata==2025.2
urllib3==2.5.0
Werkzeug==3.1.3
🐍 Python Version:

🖥️ Platform Info:

📦 Installed Packages:

```

---
## 📄 `reports/REPORTS-11-JUL-2025-05-31AM/git_snapshot.txt`

```txt
On branch master
Your branch is up to date with 'origin/master'.

nothing to commit, working tree clean
commit a3e04507079037e131b59891164720354730176e
Author: Robin Custance <robincustance@gmail.com>
Date:   Fri Jul 11 03:26:25 2025 +0930

    My next changes
🔧 Git Status:

🔁 Last Commit:

🧾 Diff Summary:

```

---
## 📄 `reports/EZYGALLERY-13-JUL-2025-02-45PM/env_metadata.txt`

```txt
Python 3.11.2
Linux art 6.1.0-37-cloud-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.140-1 (2025-05-22) x86_64 GNU/Linux
annotated-types==0.7.0
anyio==4.9.0
blinker==1.9.0
certifi==2025.6.15
charset-normalizer==3.4.2
click==8.2.1
distro==1.9.0
Flask==3.1.1
Flask-SQLAlchemy==3.1.1
greenlet==3.2.3
gunicorn==23.0.0
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
jiter==0.10.0
joblib==1.5.1
markdown-it-py==3.0.0
MarkupSafe==3.0.2
mdurl==0.1.2
numpy==2.3.1
openai==1.93.0
opencv-python==4.11.0.86
packaging==25.0
pandas==2.3.0
pillow==11.2.1
pydantic==2.11.7
pydantic_core==2.33.2
Pygments==2.19.2
python-dateutil==2.9.0.post0
python-dotenv==1.1.1
pytz==2025.2
requests==2.32.4
rich==14.0.0
scikit-learn==1.7.0
scipy==1.16.0
six==1.17.0
sniffio==1.3.1
SQLAlchemy==2.0.41
threadpoolctl==3.6.0
tqdm==4.67.1
typing-inspection==0.4.1
typing_extensions==4.14.0
tzdata==2025.2
urllib3==2.5.0
Werkzeug==3.1.3



```

---
## 📄 `reports/EZYGALLERY-13-JUL-2025-02-45PM/git_snapshot.txt`

```txt
On branch master
Your branch is up to date with 'origin/master'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	renamed:    ezy.py -> app.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	reports/EZYGALLERY-13-JUL-2025-02-45PM/

commit afde8e1b2020f3847a4886e0e4ff44db4cffd838
Merge: 7a8b983 7f5ab80
Author: Robin Custance <robincustance@gmail.com>
Date:   Sun Jul 13 06:50:11 2025 +0930

    Merge pull request #9 from capitalart/codex/reset-and-rebuild-frontend-layout-structure



```

---
## 📄 `reports/EZYGALLERY-12-JUL-2025-05-10AM/env_metadata.txt`

```txt
Python 3.11.2
Linux art 6.1.0-37-cloud-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.140-1 (2025-05-22) x86_64 GNU/Linux
annotated-types==0.7.0
anyio==4.9.0
blinker==1.9.0
certifi==2025.6.15
charset-normalizer==3.4.2
click==8.2.1
distro==1.9.0
Flask==3.1.1
Flask-SQLAlchemy==3.1.1
greenlet==3.2.3
gunicorn==23.0.0
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
jiter==0.10.0
joblib==1.5.1
markdown-it-py==3.0.0
MarkupSafe==3.0.2
mdurl==0.1.2
numpy==2.3.1
openai==1.93.0
opencv-python==4.11.0.86
packaging==25.0
pandas==2.3.0
pillow==11.2.1
pydantic==2.11.7
pydantic_core==2.33.2
Pygments==2.19.2
python-dateutil==2.9.0.post0
python-dotenv==1.1.1
pytz==2025.2
requests==2.32.4
rich==14.0.0
scikit-learn==1.7.0
scipy==1.16.0
six==1.17.0
sniffio==1.3.1
SQLAlchemy==2.0.41
threadpoolctl==3.6.0
tqdm==4.67.1
typing-inspection==0.4.1
typing_extensions==4.14.0
tzdata==2025.2
urllib3==2.5.0
Werkzeug==3.1.3



```

---
## 📄 `reports/EZYGALLERY-12-JUL-2025-05-10AM/git_snapshot.txt`

```txt
On branch master
Your branch is ahead of 'origin/master' by 7 commits.
  (use "git push" to publish your local commits)

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	reports/EZYGALLERY-12-JUL-2025-05-10AM/

nothing added to commit but untracked files present (use "git add" to track)
commit dbd254132a28230ee1616b27fdc029dc8c7b6fc2
Author: Robin Custance <robincustance@gmail.com>
Date:   Sat Jul 12 05:10:53 2025 +0930

    Auto commit: Preparing for Codex upgrade



```

---
## 📄 `reports/EZYGALLERY-11-JUL-2025-10-32PM/env_metadata.txt`

```txt
Python 3.11.2
Linux art 6.1.0-37-cloud-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.140-1 (2025-05-22) x86_64 GNU/Linux
annotated-types==0.7.0
anyio==4.9.0
blinker==1.9.0
certifi==2025.6.15
charset-normalizer==3.4.2
click==8.2.1
distro==1.9.0
Flask==3.1.1
gunicorn==23.0.0
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
jiter==0.10.0
joblib==1.5.1
markdown-it-py==3.0.0
MarkupSafe==3.0.2
mdurl==0.1.2
numpy==2.3.1
openai==1.93.0
opencv-python==4.11.0.86
packaging==25.0
pandas==2.3.0
pillow==11.2.1
pydantic==2.11.7
pydantic_core==2.33.2
Pygments==2.19.2
python-dateutil==2.9.0.post0
python-dotenv==1.1.1
pytz==2025.2
requests==2.32.4
rich==14.0.0
scikit-learn==1.7.0
scipy==1.16.0
six==1.17.0
sniffio==1.3.1
threadpoolctl==3.6.0
tqdm==4.67.1
typing-inspection==0.4.1
typing_extensions==4.14.0
tzdata==2025.2
urllib3==2.5.0
Werkzeug==3.1.3



```

---
## 📄 `reports/EZYGALLERY-11-JUL-2025-10-32PM/git_snapshot.txt`

```txt
On branch master
Your branch is ahead of 'origin/master' by 4 commits.
  (use "git push" to publish your local commits)

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	reports/EZYGALLERY-11-JUL-2025-10-32PM/

nothing added to commit but untracked files present (use "git add" to track)
commit a979763486b2336f944fc4925165abfa08273abc
Author: Robin Custance <robincustance@gmail.com>
Date:   Fri Jul 11 22:32:16 2025 +0930

    Auto commit: Preparing for Codex upgrade



```

---
## 📄 `reports/EZYGALLERY-12-JUL-2025-10-09PM/env_metadata.txt`

```txt
Python 3.11.2
Linux art 6.1.0-37-cloud-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.140-1 (2025-05-22) x86_64 GNU/Linux
annotated-types==0.7.0
anyio==4.9.0
blinker==1.9.0
certifi==2025.6.15
charset-normalizer==3.4.2
click==8.2.1
distro==1.9.0
Flask==3.1.1
Flask-SQLAlchemy==3.1.1
greenlet==3.2.3
gunicorn==23.0.0
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
jiter==0.10.0
joblib==1.5.1
markdown-it-py==3.0.0
MarkupSafe==3.0.2
mdurl==0.1.2
numpy==2.3.1
openai==1.93.0
opencv-python==4.11.0.86
packaging==25.0
pandas==2.3.0
pillow==11.2.1
pydantic==2.11.7
pydantic_core==2.33.2
Pygments==2.19.2
python-dateutil==2.9.0.post0
python-dotenv==1.1.1
pytz==2025.2
requests==2.32.4
rich==14.0.0
scikit-learn==1.7.0
scipy==1.16.0
six==1.17.0
sniffio==1.3.1
SQLAlchemy==2.0.41
threadpoolctl==3.6.0
tqdm==4.67.1
typing-inspection==0.4.1
typing_extensions==4.14.0
tzdata==2025.2
urllib3==2.5.0
Werkzeug==3.1.3



```

---
## 📄 `reports/EZYGALLERY-12-JUL-2025-10-09PM/git_snapshot.txt`

```txt
On branch master
Your branch is ahead of 'origin/master' by 13 commits.
  (use "git push" to publish your local commits)

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	reports/EZYGALLERY-12-JUL-2025-10-09PM/

nothing added to commit but untracked files present (use "git add" to track)
commit be76ed10d22d19b183131c07da891a9be8582810
Author: Robin Custance <robincustance@gmail.com>
Date:   Sat Jul 12 22:09:24 2025 +0930

    Auto commit: Preparing for Codex upgrade



```

---
## 📄 `reports/EZYGALLERY-12-JUL-2025-04-12AM/env_metadata.txt`

```txt
Python 3.11.2
Linux art 6.1.0-37-cloud-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.140-1 (2025-05-22) x86_64 GNU/Linux
annotated-types==0.7.0
anyio==4.9.0
blinker==1.9.0
certifi==2025.6.15
charset-normalizer==3.4.2
click==8.2.1
distro==1.9.0
Flask==3.1.1
gunicorn==23.0.0
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
jiter==0.10.0
joblib==1.5.1
markdown-it-py==3.0.0
MarkupSafe==3.0.2
mdurl==0.1.2
numpy==2.3.1
openai==1.93.0
opencv-python==4.11.0.86
packaging==25.0
pandas==2.3.0
pillow==11.2.1
pydantic==2.11.7
pydantic_core==2.33.2
Pygments==2.19.2
python-dateutil==2.9.0.post0
python-dotenv==1.1.1
pytz==2025.2
requests==2.32.4
rich==14.0.0
scikit-learn==1.7.0
scipy==1.16.0
six==1.17.0
sniffio==1.3.1
threadpoolctl==3.6.0
tqdm==4.67.1
typing-inspection==0.4.1
typing_extensions==4.14.0
tzdata==2025.2
urllib3==2.5.0
Werkzeug==3.1.3



```

---
## 📄 `reports/EZYGALLERY-12-JUL-2025-04-12AM/git_snapshot.txt`

```txt
On branch master
Your branch is ahead of 'origin/master' by 4 commits.
  (use "git push" to publish your local commits)

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	reports/EZYGALLERY-12-JUL-2025-04-12AM/

nothing added to commit but untracked files present (use "git add" to track)
commit fd0162fa9f80970d67bb06057e8543e23944dd48
Author: Robin Custance <robincustance@gmail.com>
Date:   Sat Jul 12 04:12:44 2025 +0930

    Auto commit: Preparing for Codex upgrade



```

---
## 📄 `reports/EZYGALLERY-12-JUL-2025-05-24AM/env_metadata.txt`

```txt
Python 3.11.2
Linux art 6.1.0-37-cloud-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.140-1 (2025-05-22) x86_64 GNU/Linux
annotated-types==0.7.0
anyio==4.9.0
blinker==1.9.0
certifi==2025.6.15
charset-normalizer==3.4.2
click==8.2.1
distro==1.9.0
Flask==3.1.1
Flask-SQLAlchemy==3.1.1
greenlet==3.2.3
gunicorn==23.0.0
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
jiter==0.10.0
joblib==1.5.1
markdown-it-py==3.0.0
MarkupSafe==3.0.2
mdurl==0.1.2
numpy==2.3.1
openai==1.93.0
opencv-python==4.11.0.86
packaging==25.0
pandas==2.3.0
pillow==11.2.1
pydantic==2.11.7
pydantic_core==2.33.2
Pygments==2.19.2
python-dateutil==2.9.0.post0
python-dotenv==1.1.1
pytz==2025.2
requests==2.32.4
rich==14.0.0
scikit-learn==1.7.0
scipy==1.16.0
six==1.17.0
sniffio==1.3.1
SQLAlchemy==2.0.41
threadpoolctl==3.6.0
tqdm==4.67.1
typing-inspection==0.4.1
typing_extensions==4.14.0
tzdata==2025.2
urllib3==2.5.0
Werkzeug==3.1.3



```

---
## 📄 `reports/EZYGALLERY-12-JUL-2025-05-24AM/git_snapshot.txt`

```txt
On branch master
Your branch is ahead of 'origin/master' by 9 commits.
  (use "git push" to publish your local commits)

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	reports/EZYGALLERY-12-JUL-2025-05-24AM/

nothing added to commit but untracked files present (use "git add" to track)
commit 0c33ffcfddf7c6d0c937023bb78a9bfa6f0f1a3e
Author: Robin Custance <robincustance@gmail.com>
Date:   Sat Jul 12 05:24:13 2025 +0930

    Auto commit: Preparing for Codex upgrade



```

---
## 📄 `reports/EZYGALLERY-12-JUL-2025-02-16AM/env_metadata.txt`

```txt
Python 3.11.2
Linux art 6.1.0-37-cloud-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.140-1 (2025-05-22) x86_64 GNU/Linux
annotated-types==0.7.0
anyio==4.9.0
blinker==1.9.0
certifi==2025.6.15
charset-normalizer==3.4.2
click==8.2.1
distro==1.9.0
Flask==3.1.1
gunicorn==23.0.0
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
jiter==0.10.0
joblib==1.5.1
markdown-it-py==3.0.0
MarkupSafe==3.0.2
mdurl==0.1.2
numpy==2.3.1
openai==1.93.0
opencv-python==4.11.0.86
packaging==25.0
pandas==2.3.0
pillow==11.2.1
pydantic==2.11.7
pydantic_core==2.33.2
Pygments==2.19.2
python-dateutil==2.9.0.post0
python-dotenv==1.1.1
pytz==2025.2
requests==2.32.4
rich==14.0.0
scikit-learn==1.7.0
scipy==1.16.0
six==1.17.0
sniffio==1.3.1
threadpoolctl==3.6.0
tqdm==4.67.1
typing-inspection==0.4.1
typing_extensions==4.14.0
tzdata==2025.2
urllib3==2.5.0
Werkzeug==3.1.3



```

---
## 📄 `reports/EZYGALLERY-12-JUL-2025-02-16AM/git_snapshot.txt`

```txt
On branch master
Your branch is ahead of 'origin/master' by 7 commits.
  (use "git push" to publish your local commits)

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	reports/EZYGALLERY-12-JUL-2025-02-16AM/

nothing added to commit but untracked files present (use "git add" to track)
commit ca5379d020ba190cb00bad90fcf6a64859ef2347
Author: Robin Custance <robincustance@gmail.com>
Date:   Sat Jul 12 02:16:28 2025 +0930

    Auto commit: Preparing for Codex upgrade



```

---
## 📄 `reports/REPORTS-11-JUL-2025-05-44AM/env_metadata.txt`

```txt
Python 3.11.2
Linux art 6.1.0-37-cloud-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.140-1 (2025-05-22) x86_64 GNU/Linux
acme==4.1.1
annotated-types==0.7.0
anyio==4.9.0
blinker==1.9.0
certbot==4.1.1
certbot-nginx==4.1.1
certifi==2025.6.15
cffi==1.17.1
chardet==5.2.0
charset-normalizer==3.4.2
click==8.2.1
ConfigArgParse==1.7.1
configobj==5.0.9
cryptography==45.0.5
distro==1.9.0
Flask==3.1.1
gunicorn==23.0.0
h11==0.16.0
httpcore==1.0.9
httplib2==0.22.0
httpx==0.28.1
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
jiter==0.10.0
joblib==1.5.1
josepy==2.0.0
markdown-it-py==3.0.0
MarkupSafe==3.0.2
mdurl==0.1.2
numpy==2.2.6
openai==1.93.1
opencv-python==4.12.0.88
packaging==25.0
pandas==2.3.1
parsedatetime==2.6
pillow==11.3.0
pycparser==2.22
pycurl==7.45.6
pydantic==2.11.7
pydantic_core==2.33.2
Pygments==2.19.2
pyOpenSSL==25.1.0
pyparsing==3.2.3
pyRFC3339==2.0.1
python-dateutil==2.9.0.post0
python-debian==1.0.1
python-debianbts==4.1.1
python-dotenv==1.1.1
pytz==2025.2
PyYAML==6.0.2
requests==2.32.4
rich==14.0.0
scikit-learn==1.7.0
scipy==1.16.0
six==1.17.0
sniffio==1.3.1
threadpoolctl==3.6.0
tqdm==4.67.1
typing-inspection==0.4.1
typing_extensions==4.14.1
tzdata==2025.2
urllib3==2.5.0
Werkzeug==3.1.3
🐍 Python Version:

🖥️ Platform Info:

📦 Installed Packages:

```

---
## 📄 `reports/REPORTS-11-JUL-2025-05-44AM/git_snapshot.txt`

```txt
On branch master
Your branch is ahead of 'origin/master' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
commit aeb42c129f6c6c009184adf0f5860fc818364d37
Author: Robin Custance <robincustance@gmail.com>
Date:   Fri Jul 11 05:44:54 2025 +0930

    Auto commit: Preparing for Codex upgrade
🔧 Git Status:

🔁 Last Commit:

🧾 Diff Summary:

```

---
## 📄 `reports/EZYGALLERY-12-JUL-2025-07-35PM/env_metadata.txt`

```txt
Python 3.11.2
Linux art 6.1.0-37-cloud-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.140-1 (2025-05-22) x86_64 GNU/Linux
annotated-types==0.7.0
anyio==4.9.0
blinker==1.9.0
certifi==2025.6.15
charset-normalizer==3.4.2
click==8.2.1
distro==1.9.0
Flask==3.1.1
Flask-SQLAlchemy==3.1.1
greenlet==3.2.3
gunicorn==23.0.0
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
jiter==0.10.0
joblib==1.5.1
markdown-it-py==3.0.0
MarkupSafe==3.0.2
mdurl==0.1.2
numpy==2.3.1
openai==1.93.0
opencv-python==4.11.0.86
packaging==25.0
pandas==2.3.0
pillow==11.2.1
pydantic==2.11.7
pydantic_core==2.33.2
Pygments==2.19.2
python-dateutil==2.9.0.post0
python-dotenv==1.1.1
pytz==2025.2
requests==2.32.4
rich==14.0.0
scikit-learn==1.7.0
scipy==1.16.0
six==1.17.0
sniffio==1.3.1
SQLAlchemy==2.0.41
threadpoolctl==3.6.0
tqdm==4.67.1
typing-inspection==0.4.1
typing_extensions==4.14.0
tzdata==2025.2
urllib3==2.5.0
Werkzeug==3.1.3



```

---
## 📄 `reports/EZYGALLERY-12-JUL-2025-07-35PM/git_snapshot.txt`

```txt
On branch master
Your branch is ahead of 'origin/master' by 11 commits.
  (use "git push" to publish your local commits)

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	reports/EZYGALLERY-12-JUL-2025-07-35PM/

nothing added to commit but untracked files present (use "git add" to track)
commit 385fe6324e547a586f3ea4d049b0a5870cf137ae
Author: Robin Custance <robincustance@gmail.com>
Date:   Sat Jul 12 19:35:28 2025 +0930

    Auto commit: Preparing for Codex upgrade



```

---
## 📄 `routes/account.py`

```py
from flask import Blueprint, render_template

account_bp = Blueprint('account', __name__, url_prefix='/account')

@account_bp.route('/')
def account():
    return render_template('account.html')

```

---
## 📄 `routes/accessibility.py`

```py
from flask import Blueprint, render_template

accessibility_bp = Blueprint('accessibility', __name__)

@accessibility_bp.route('/accessibility')
def accessibility():
    return render_template('accessibility.html')

```

---
## 📄 `routes/gallery.py`

```py
from flask import Blueprint, render_template

gallery_bp = Blueprint('gallery', __name__, url_prefix='/gallery')

@gallery_bp.route('/')
def gallery():
    return render_template('gallery.html')

```

---
## 📄 `routes/search.py`

```py
from flask import Blueprint, render_template

search_bp = Blueprint('search', __name__, url_prefix='/search')

@search_bp.route('/')
def search():
    return render_template('search.html')

```

---
## 📄 `routes/auth.py`

```py
from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login')
def login():
    return render_template('login.html')

```

---
## 📄 `routes/cart.py`

```py
from flask import Blueprint, render_template

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/')
def cart():
    return render_template('cart.html')

```

---
## 📄 `routes/info.py`

```py
from flask import Blueprint, render_template

info_bp = Blueprint('info', __name__, url_prefix='/info')

@info_bp.route('/')
def info():
    return 'Info placeholder'

```

---
## 📄 `routes/art.py`

```py
from flask import Blueprint, render_template, abort
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.artwork import Artwork, Base

art_bp = Blueprint('art', __name__, url_prefix='/artwork')

engine = create_engine('sqlite:///app.db')
Session = sessionmaker(bind=engine)

@art_bp.route('/<seo_filename>')
def artwork_detail(seo_filename):
    with Session() as session:
        artwork = session.query(Artwork).filter_by(seo_filename=seo_filename).first()
    if not artwork:
        abort(404)
    return render_template('artwork_detail.html', artwork=artwork)

```

---
## 📄 `routes/artist.py`

```py
from flask import Blueprint, render_template

artist_bp = Blueprint('artist', __name__, url_prefix='/artist')

@artist_bp.route('/<int:artist_id>')
def artist_profile(artist_id):
    return render_template('artist_profile.html', artist_id=artist_id)

```

---
## 📄 `routes/home.py`

```py
from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@home_bp.route('/home')
def index():
    """Display the main home page."""
    return render_template('index.html')

```

---
## 📄 `routes/__init__.py`

```py
from flask import Blueprint

home_bp = Blueprint('home', __name__)

def register_blueprints(app):
    from .home import home_bp as hb
    from .gallery import gallery_bp as gb
    from .art import art_bp as ab
    from .artist import artist_bp as arb
    from .cart import cart_bp as cb
    from .checkout import checkout_bp as cbp
    from .auth import auth_bp as authb
    from .account import account_bp as acb
    from .search import search_bp as sb
    from .info import info_bp as ib
    from .accessibility import accessibility_bp as acb2

    app.register_blueprint(hb)
    app.register_blueprint(gb)
    app.register_blueprint(ab)
    app.register_blueprint(arb)
    app.register_blueprint(cb)
    app.register_blueprint(cbp)
    app.register_blueprint(authb)
    app.register_blueprint(acb)
    app.register_blueprint(sb)
    app.register_blueprint(ib)
    app.register_blueprint(acb2)

```

---
## 📄 `routes/checkout.py`

```py
from flask import Blueprint, render_template

checkout_bp = Blueprint('checkout', __name__, url_prefix='/checkout')

@checkout_bp.route('/')
def checkout():
    return render_template('checkout.html')

```

---
## 📄 `ezygallery/config.py`

```py
"""Central configuration for the Ezy Gallery project.

This module defines all folder paths, filename templates, allowed
extensions, image sizes and other parameters used across the codebase.
Values can be overridden using environment variables of the same name.

Update paths here rather than hard-coding them elsewhere. All modules
should import settings from ``config`` so behaviour automatically adapts
when directory names or limits change. Every value can be overridden by an
environment variable of the same name which allows for per-user or
deployment specific customisation via ``.env`` files.

Critical folders are created on import. If creation fails an explicit
``RuntimeError`` is raised. Edit this file or set env vars to tweak folder
names, extensions or limits rather than updating code elsewhere.
"""

from __future__ import annotations

import os
from pathlib import Path

# --- Project Root -----------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
CONFIG_VERSION = "1.2.0"

# --- Database ---------------------------------------------------------------
DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR / "data"))
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
if not SQLALCHEMY_DATABASE_URI:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{(DATA_DIR / 'app.db').as_posix()}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# --- Input/Output Folders ---------------------------------------------------
ARTWORKS_INPUT_DIR = Path(
    os.getenv("ARTWORKS_INPUT_DIR", BASE_DIR / "inputs" / "artworks")
)
MOCKUPS_INPUT_DIR = Path(
    os.getenv("MOCKUPS_INPUT_DIR", BASE_DIR / "inputs" / "mockups")
)
MOCKUPS_CATEGORISED_DIR = Path(
    os.getenv("MOCKUPS_CATEGORISED_DIR", MOCKUPS_INPUT_DIR / "4x5-categorised")
)
ARTWORKS_PROCESSED_DIR = Path(
    os.getenv("ARTWORKS_PROCESSED_DIR", BASE_DIR / "outputs" / "processed")
)
ARTWORKS_FINALISED_DIR = Path(
    os.getenv("ARTWORKS_FINALISED_DIR", BASE_DIR / "outputs" / "finalised-artwork")
)
COMPOSITES_DIR = Path(os.getenv("COMPOSITES_DIR", BASE_DIR / "outputs" / "composites"))
SELECTIONS_DIR = Path(os.getenv("SELECTIONS_DIR", BASE_DIR / "outputs" / "selections"))
THUMBNAILS_DIR = Path(os.getenv("THUMBNAILS_DIR", BASE_DIR / "outputs" / "thumbnails"))
LOGS_DIR = Path(os.getenv("LOGS_DIR", BASE_DIR / "logs"))
DEV_LOGS_DIR = Path(os.getenv("DEV_LOGS_DIR", BASE_DIR / "dev-logs"))
PARSE_FAILURE_DIR = Path(os.getenv("PARSE_FAILURE_DIR", LOGS_DIR / "parse_failures"))
OPENAI_PROMPT_LOG_DIR = Path(
    os.getenv("OPENAI_PROMPT_LOG_DIR", LOGS_DIR / "openai_prompts")
)
OPENAI_RESPONSE_LOG_DIR = Path(
    os.getenv("OPENAI_RESPONSE_LOG_DIR", LOGS_DIR / "openai_responses")
)
GIT_LOG_DIR = Path(os.getenv("GIT_LOG_DIR", BASE_DIR / "git-update-push-logs"))
SCRIPTS_DIR = Path(os.getenv("SCRIPTS_DIR", BASE_DIR / "scripts"))
SIGNATURES_DIR = Path(os.getenv("SIGNATURES_DIR", BASE_DIR / "inputs" / "signatures"))
GENERIC_TEXTS_DIR = Path(os.getenv("GENERIC_TEXTS_DIR", BASE_DIR / "generic_texts"))
UPLOADS_TEMP_DIR = Path(os.getenv("UPLOADS_TEMP_DIR", BASE_DIR / "uploads_temp"))
COORDS_DIR = Path(os.getenv("COORDS_DIR", BASE_DIR / "inputs" / "Coordinates"))
TMP_DIR = Path(os.getenv("TMP_DIR", BASE_DIR / "tmp" / "ai_input_images"))
SELLBRITE_OUTPUT_DIR = Path(
    os.getenv("SELLBRITE_OUTPUT_DIR", BASE_DIR / "outputs" / "sellbrite")
)
AIGW_PROMPTS_DIR = Path(
    os.getenv("AIGW_PROMPTS_DIR", BASE_DIR / "outputs" / "aigw_prompts")
)
AIGW_OPTIONS_FILE = Path(
    os.getenv("AIGW_OPTIONS_FILE", BASE_DIR / "settings" / "aigw_options.json")
)
SELLBRITE_TEMPLATE_CSV = Path(
    os.getenv("SELLBRITE_TEMPLATE_CSV", BASE_DIR / "docs" / "csv_product_template.csv")
)
SELLBRITE_DEFAULT_QUANTITY = int(os.getenv("SELLBRITE_DEFAULT_QUANTITY", "1"))

# Additional general file locations
ONBOARDING_PATH = Path(
    os.getenv(
        "ONBOARDING_PATH",
        BASE_DIR
        / "settings"
        / "Master-Etsy-Listing-Description-Writing-Onboarding.txt",
    )
)
OUTPUT_JSON = Path(
    os.getenv("OUTPUT_JSON", BASE_DIR / "outputs" / "artwork_listing_master.json")
)
OUTPUT_PROCESSED_ROOT = ARTWORKS_PROCESSED_DIR

# Paths to helper scripts used by various workflows
ANALYZE_SCRIPT_PATH = Path(
    os.getenv("ANALYZE_SCRIPT_PATH", SCRIPTS_DIR / "analyze_artwork.py")
)
GENERATE_SCRIPT_PATH = Path(
    os.getenv("GENERATE_SCRIPT_PATH", SCRIPTS_DIR / "generate_composites.py")
)

# --- Filename Templates -----------------------------------------------------
FILENAME_TEMPLATES = {
    "artwork": "{seo_slug}.jpg",
    "mockup": "{seo_slug}-MU-{num:02d}.jpg",
    "thumbnail": "{seo_slug}-THUMB.jpg",
    "analyse": "{seo_slug}-ANALYSE.jpg",
    "listing_json": "{seo_slug}-listing.json",
    "qc_json": "{seo_slug}.qc.json",
}

# --- Allowed Extensions & Sizes --------------------------------------------
ALLOWED_EXTENSIONS = set(os.getenv("ALLOWED_EXTENSIONS", "jpg,jpeg,png").split(","))
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "32"))
ANALYSE_MAX_DIM = int(os.getenv("ANALYSE_MAX_DIM", "2400"))
ANALYSE_MAX_MB = int(os.getenv("ANALYSE_MAX_MB", "1"))

# --- Image Dimensions -------------------------------------------------------
THUMB_WIDTH = int(os.getenv("THUMB_WIDTH", "400"))
THUMB_HEIGHT = int(os.getenv("THUMB_HEIGHT", "400"))


# --- Mockup Categories ------------------------------------------------------
def get_mockup_categories() -> list[str]:
    override = os.getenv("MOCKUP_CATEGORIES")
    if override:
        return [c.strip() for c in override.split(",") if c.strip()]
    if MOCKUPS_CATEGORISED_DIR.exists():
        return sorted(
            [
                f.name
                for f in MOCKUPS_CATEGORISED_DIR.iterdir()
                if f.is_dir() and f.name.lower() != "uncategorised"
            ]
        )
    return []


MOCKUP_CATEGORIES = get_mockup_categories()

# --- Signature Settings -----------------------------------------------------
SIGNATURE_SIZE_PERCENTAGE = float(os.getenv("SIGNATURE_SIZE_PERCENTAGE", "0.05"))
SIGNATURE_MARGIN_PERCENTAGE = float(os.getenv("SIGNATURE_MARGIN_PERCENTAGE", "0.03"))

# --- SKU Tracking -----------------------------------------------------------
SKU_TRACKER = Path(
    os.getenv("SKU_TRACKER_PATH", BASE_DIR / "settings" / "sku_tracker.json")
)

# File used by the web UI to report progress of analysis jobs
ANALYSIS_STATUS_FILE = Path(
    os.getenv("ANALYSIS_STATUS_FILE", LOGS_DIR / "analysis_status.json")
)

# Feature flags --------------------------------------------------------------
# Toggle visibility of Upgrade/Subscription links in the UI. Set the
# environment variable ``ENABLE_UPGRADE`` to ``true`` to enable.
ENABLE_UPGRADE = os.getenv("ENABLE_UPGRADE", "false").lower() == "true"

# --- API Keys ---------------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- AI Model Configuration -------------------------------------------------
OPENAI_PRIMARY_MODEL = os.getenv("OPENAI_PRIMARY_MODEL", "gpt-4o")
OPENAI_FALLBACK_MODEL = os.getenv("OPENAI_FALLBACK_MODEL", "gpt-4-turbo")
GEMINI_PRIMARY_MODEL = os.getenv("GEMINI_PRIMARY_MODEL", "gemini-1.5-pro")


def get_openai_model() -> str:
    """Return the best available model with fallback."""
    primary = OPENAI_PRIMARY_MODEL
    fallback = OPENAI_FALLBACK_MODEL
    return primary if primary else fallback

# --- Additional Script Paths and Outputs -----------------------------------
PATCHES_DIR = Path(os.getenv("PATCHES_DIR", BASE_DIR / "patches"))
PATCH_INPUT = Path(os.getenv("PATCH_INPUT", BASE_DIR / "copy-git-apply.txt"))
# Output location for signed artworks generated by utilities
SIGNED_OUTPUT_DIR = Path(
    os.getenv("SIGNED_OUTPUT_DIR", BASE_DIR / "outputs" / "signed")
)
# Log file for the mockup categoriser script
MOCKUP_CATEGORISATION_LOG = Path(
    os.getenv("MOCKUP_CATEGORISATION_LOG", BASE_DIR / "mockup_categorisation_log.txt")
)

# Midjourney sorting helper defaults
MIDJOURNEY_CSV_PATH = Path(
    os.getenv("MIDJOURNEY_CSV_PATH", BASE_DIR / "inputs" / "autojourney.csv")
)
MIDJOURNEY_INPUT_DIR = Path(
    os.getenv("MIDJOURNEY_INPUT_DIR", BASE_DIR / "inputs" / "midjourney")
)
MIDJOURNEY_OUTPUT_DIR = Path(
    os.getenv("MIDJOURNEY_OUTPUT_DIR", BASE_DIR / "outputs" / "midjourney_sorted")
)
MIDJOURNEY_METADATA_CSV = Path(
    os.getenv(
        "MIDJOURNEY_METADATA_CSV",
        MIDJOURNEY_OUTPUT_DIR / "art_narrator_image_metadata.csv",
    )
)

# --- Ensure Critical Folders Exist -----------------------------------------
for folder in [
    ARTWORKS_INPUT_DIR,
    MOCKUPS_INPUT_DIR,
    ARTWORKS_PROCESSED_DIR,
    LOGS_DIR,
    DEV_LOGS_DIR,
    PARSE_FAILURE_DIR,
    OPENAI_PROMPT_LOG_DIR,
    OPENAI_RESPONSE_LOG_DIR,
    GIT_LOG_DIR,
    PATCHES_DIR,
    SIGNED_OUTPUT_DIR,
    SELLBRITE_OUTPUT_DIR,
    UPLOADS_TEMP_DIR,
    DATA_DIR,
    AIGW_PROMPTS_DIR,
]:
    try:
        folder.mkdir(parents=True, exist_ok=True)
    except Exception as exc:  # pragma: no cover - simple safety
        raise RuntimeError(f"Could not create required folder {folder}: {exc}")

```

---
## 📄 `ezygallery/app.py`

```py
"""Ezy Gallery Flask Entrypoint — Robbie Mode™ (July 2025)

This file is a lightly modified clone of the Art Narrator ``app.py`` and
serves as the main entrypoint for the Ezy Gallery site. Only branding and
Sellbrite related functionality have been changed.
"""

from __future__ import annotations

import logging
import os
import json
from pathlib import Path
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    current_app,
)
from werkzeug.routing import BuildError
from dotenv import load_dotenv
from flask_migrate import Migrate
import uuid
import datetime
import menu_loader

from models import db

# ==== Modular Imports ====
from config import LOGS_DIR
from routes.artwork_routes import bp as artwork_bp
from routes.admin_debug import bp as admin_bp
from routes.admin_routes import bp as admin_routes_bp
from routes.gdws_admin_routes import bp as gdws_admin_bp
from routes.aigw_routes import bp as aigw_bp
from routes.mockup_routes import bp as mockups_bp
from routes.prompt_options import bp as prompt_options_bp
from routes.prompt_ui import bp as prompt_ui_bp
from routes.prompt_whisperer import bp as whisperer_bp
from routes.metrics_api import bp as metrics_bp
from routes.documentation_routes import bp as documentation_bp
from routes.management_routes import bp as management_bp
from routes.openai_guidance import bp as openai_guidance_bp
from auth import bp as auth_bp
from routes.legal_routes import bp as info_bp
import no_cache_toggle
from routes.session_tracker import is_active as session_is_active
import login_bypass_toggle as login_bypass

# ==== Versioning & Env ====
APP_VERSION = "2.5.1"
load_dotenv()

# ==== Flask App Initialization ====
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "mockup-secret-key")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["TEMPLATES_AUTO_RELOAD"] = True  # Always reload templates on change
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0  # Flask disables static file cache
if os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true":
    app.config["SESSION_COOKIE_SECURE"] = True
app.permanent_session_lifetime = datetime.timedelta(days=14)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "SQLALCHEMY_DATABASE_URI", ""
)
if not app.config["SQLALCHEMY_DATABASE_URI"]:
    import config as cfg

    app.config["SQLALCHEMY_DATABASE_URI"] = cfg.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

# ==== Version Check ====
def check_versions() -> None:
    print("--- Running System Version Check ---")
    version_file = Path(__file__).parent / "version.json"
    try:
        with open(version_file, "r", encoding="utf-8") as f:
            expected = json.load(f)
    except FileNotFoundError:
        print("\u26A0\uFE0F WARNING: version.json not found. Skipping version check.")
        return

    import config
    loaded = {
        "app_version": APP_VERSION,
        "config_version": getattr(config, "CONFIG_VERSION", "Not Set"),
        "env_version": os.getenv("ENV_VERSION", "Not Set"),
        "openai_primary_model": config.OPENAI_PRIMARY_MODEL,
        "openai_fallback_model": config.OPENAI_FALLBACK_MODEL,
        "gemini_primary_model": config.GEMINI_PRIMARY_MODEL,
    }
    for key, expected_val in expected.items():
        loaded_val = loaded.get(key, "Not Set")
        if str(loaded_val) != str(expected_val):
            print(f"\u274C MISMATCH: {key} - Expected '{expected_val}', but found '{loaded_val}'")
        else:
            print(f"\u2705 MATCH: {key} - Version '{loaded_val}'")
    print("--- Version Check Complete ---")
check_versions()

# ==== Logging ====
logging.basicConfig(
    filename=LOGS_DIR / "composites-workflow.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
from utils.db_logger import setup_logging
setup_logging(app)

# ==== Blueprint Registration ====
for bp in [
    artwork_bp, admin_bp, admin_routes_bp,
    gdws_admin_bp, aigw_bp, mockups_bp, info_bp, auth_bp, prompt_options_bp,
    prompt_ui_bp, whisperer_bp, documentation_bp, metrics_bp,
    management_bp, openai_guidance_bp,
]:
    app.register_blueprint(bp)

# ==== Context Processors for Cache-Busting & Admin Status ====
@app.context_processor
def inject_login_bypass():
    return {
        "login_bypass_enabled": login_bypass.is_enabled(),
        "login_bypass_remaining": login_bypass.remaining_str() or None,
    }

@app.context_processor
def inject_no_cache():
    def url_for_static(endpoint: str, **values):
        url = url_for(endpoint, **values)
        # Hard cache bust: always append version or uuid
        if endpoint == "static" and no_cache_toggle.is_enabled() and values.get("filename") != "favicon.ico":
            url += f"?v={uuid.uuid4()}"
        elif endpoint == "static" and "filename" in values and not values.get("filename", "").startswith("favicon"):
            # Always bust cache even if toggle is off: append short version
            url += f"?v={APP_VERSION}"
        return url
    return {
        "url_for_static": url_for_static,
        "forced_no_cache_active": no_cache_toggle.is_enabled(),
        "forced_no_cache_remaining": no_cache_toggle.remaining_str(),
    }

@app.context_processor
def inject_config():
    """Make selected config options available in templates."""
    import config
    return {"config": config}


@app.context_processor
def inject_mega_menu():
    """Provide mega menu data to all templates."""
    return {"mega_menu": menu_loader.MENU_DATA}

# ==== Flask Pre-Request: Login Required, Session Validation, Auto-Reload for Dev ====
@app.before_request
def require_login():
    if request.endpoint is None or request.endpoint.startswith("static"):
        return
    if request.endpoint in {"auth.login", "auth.logout"} or request.endpoint.startswith("prompt_options."):
        return
    if not session.get("user"):
        if login_bypass.is_enabled() and not request.path.startswith("/admin"):
            return
        return redirect(url_for("auth.login", next=request.url))
    if not session_is_active(session.get("user"), session.get("token", "")):
        session.clear()
        flash("Session expired or revoked", "warning")
        return redirect(url_for("auth.login", next=request.url))
    # Force reload of templates if under dev/debug or if .touch file is present (for Gunicorn hot reload workaround)
    if app.config.get("TEMPLATES_AUTO_RELOAD", False):
        try:
            import importlib
            importlib.reload(current_app.jinja_env)
        except Exception:
            pass

# ==== Error Handling ====
@app.errorhandler(BuildError)
def handle_build_error(err):
    app.logger.error("BuildError: %s", err)
    return render_template("missing_endpoint.html", error=err), 500

# ==== Healthcheck Endpoint ====
@app.route("/healthz")
def healthz():
    return "OK"

# ==== Gunicorn Stale Process Auto-Killer (Only Runs if Main) ====
def kill_gunicorn_zombies():
    """Force kill all old gunicorn procs for stale cache/hanging reload prevention."""
    import subprocess
    try:
        out = subprocess.check_output("pgrep -f gunicorn", shell=True)
        for pid in out.decode().strip().splitlines():
            # Don't kill our own process
            if int(pid) != os.getpid():
                os.system(f"kill -9 {pid}")
    except Exception:
        pass

# ==== Flask Factory for WSGI ====
def create_app() -> Flask:
    return app

# ==== Entrypoint: Always Purge Python Bytecode, Gunicorn Kill, Start Clean ====
if __name__ == "__main__":
    print("🧹 Purging all __pycache__ and *.pyc files for fresh start...")
    for root, dirs, files in os.walk("."):
        for d in dirs:
            if d == "__pycache__":
                try:
                    fullpath = os.path.join(root, d)
                    os.system(f"rm -rf {fullpath}")
                except Exception:
                    pass
        for f in files:
            if f.endswith(".pyc") or f.endswith(".pyo"):
                try:
                    os.remove(os.path.join(root, f))
                except Exception:
                    pass
    # Kill stale Gunicorn procs if any
    kill_gunicorn_zombies()
    port = int(os.getenv("PORT", 8080))
    debug = os.getenv("DEBUG", "true").lower() == "true"
    print(f"\U0001f3a8 Starting Ezy Gallery UI at http://0.0.0.0:{port}/ ...")
    app.run(debug=debug, host="0.0.0.0", port=port)

```

---
## 📄 `ezygallery/templates/upload.html`

```html
{# [WF-STEP-1] This page shows the circled step number at the top of the content, using .page-step-icon #}
{% extends "main.html" %}
{% block title %}Upload Artwork{% endblock %}
{% block content %}
<div class="page-step-wrapper" style="text-align: center; margin-bottom: 1.5em;">
<div class="step-label">STAGE</div>
<img class="page-step-icon" src="{{ url_for_static('static', filename='icons/svg/light/number-circle-one-light.svg') }}" alt="STAGE 1" />
</div>
<h2 class="mb-3">Upload New Artwork</h2>
<form id="upload-form" method="post" enctype="multipart/form-data">
  <input id="file-input" type="file" name="images" accept="image/*" multiple hidden aria-hidden="true">
  <div id="dropzone" class="upload-container" aria-label="Artwork upload drop zone" aria-describedby="dropzone-desc" tabindex="0" role="button" title="Upload images">
    <div class="upload-dropzone">
      <img src="{{ url_for_static('static', filename='icons/svg/light/upload-light.svg') }}" class="dropzone-icon" alt="" aria-hidden="true"/>
      <p id="dropzone-desc" class="dropzone-text">Drop ya art here, mate!<br><span class="small">or tap to choose file(s)</span></p>
      <div class="spinner-overlay"><div class="spinner"></div></div>
    </div>
  </div>
  <noscript>
    <p class="upload-noscript">Drag and drop not supported. Please use the file selector.</p>
  </noscript>
  <p class="module-help">
    <a href="{{ url_for('documentation.howto_upload') }}">How-To</a>
    <a href="{{ url_for('documentation.docs_all') }}#uploads-howto">Full Docs</a>
  </p>
  <ul id="upload-list" class="upload-list"></ul>
</form>
<script src="{{ url_for_static('static', filename='js/upload.js') }}"></script>
{% endblock %}

```

---
## 📄 `ezygallery/templates/debug_parse_ai.html`

```html
{% extends 'main.html' %}
{% block title %}Parse AI Output{% endblock %}
{% block content %}
<h1>Debug: Parse AI Output</h1>
<form method="post">
  <textarea name="raw" rows="15" cols="80">{{ raw }}</textarea><br>
  <button type="submit">Parse</button>
</form>
{% if error %}<p style="color:red">{{ error }}</p>{% endif %}
{% if parsed %}
<pre>{{ parsed | tojson(indent=2) }}</pre>
{% endif %}
{% endblock %}

```

---
## 📄 `ezygallery/templates/dws_editor.html`

```html
{% extends "main.html" %}
{% block title %}Generic Description Writing System (GDWS) Editor{% endblock %}

{% block content %}
<!-- SortableJS for Drag-and-Drop functionality -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.15.0/Sortable.min.js"></script>

<!-- Custom styles moved to static/css/custom.css -->


<div class="dws-container">
    <!-- Sidebar for Master Controls -->
    <aside class="dws-sidebar">
        <h1>GDWS Controls</h1>
        
        <div class="dws-rules-box">
            <label for="aspect-ratio-selector">Select Aspect Ratio Template</label>
            <select id="aspect-ratio-selector" name="aspect-ratio-selector">
                <option value="4x5">4x5</option>
                <option value="16x9">16x9</option>
                <option value="1x1">1x1</option>
                <option value="A-Series-Verical">A-Series-Verical</option>
            </select>
        </div>

        <!-- Master Actions -->
        <div>
            <h2>Master Actions</h2>
            <button id="save-all-btn" class="btn-black">
                <img class="icon-inline" src="{{ url_for_static('static', filename='icons/svg/light/floppy-disk-light.svg') }}" alt="" />
                Save All Changes
            </button>
            <button id="add-paragraph-btn" class="btn-black">
                <img class="icon-inline" src="{{ url_for_static('static', filename='icons/svg/light/plus-circle-light.svg') }}" alt="" />
                Add New Paragraph
            </button>
            <button id="regenerate-all-btn" class="btn-black">
                <img class="icon-inline" src="{{ url_for_static('static', filename='icons/svg/light/arrows-clockwise-light.svg') }}" alt="" />
                Regenerate All
            </button>
            <button id="shuffle-btn" class="btn-black">
                <img class="icon-inline" src="{{ url_for_static('static', filename='icons/svg/light/shuffle-light.svg') }}" alt="" />
                Shuffle Paragraphs
            </button>
        </div>

        <!-- AI & Content Rules -->
        <div class="dws-rules-box">
            <h2>AI & Content Rules</h2>
            <div>
                <label for="ai-provider">AI Provider</label>
                <select id="ai-provider" name="ai-provider">
                    <option value="openai">OpenAI</option>
                    <option value="gemini">Gemini</option>
                    <option value="random">Random</option>
                    <option value="combined">Combined</option>
                </select>
            </div>
            <div>
                <label for="min-words">Min Words per Block</label>
                <input type="number" id="min-words" value="20">
            </div>
            <div>
                <label for="max-words">Max Words per Block</label>
                <input type="number" id="max-words" value="150">
            </div>
            <button id="save-rules-btn" class="btn-black">Save Rules</button>
        </div>

        <!-- System Version Check -->
        <div class="dws-rules-box">
            <h2>System Versions</h2>
            <div id="version-checker">
                <p>Loading version status...</p>
            </div>
            <div>
                <label for="new-version-key">Update Version For:</label>
                <select id="new-version-key">
                    <option value="app_version">App Version</option>
                    <option value="config_version">Config.py Version</option>
                    <option value="env_version">.env Version</option>
                    <option value="openai_primary_model">OpenAI Primary Model</option>
                    <option value="openai_fallback_model">OpenAI Fallback Model</option>
                    <option value="gemini_primary_model">Gemini Primary Model</option>
                </select>
                <label for="new-version-value">New Version #:</label>
                <input type="text" id="new-version-value" placeholder="e.g., 1.2.1 or gpt-4o">
                <button id="save-new-version-btn" class="btn-black">Save New Version</button>
            </div>
        </div>
        <p style="text-align:center; font-size:0.8em; color:#999; margin-top:2em;">Ezy Gallery GDWS v1.5</p>
    </aside>

    <!-- Main Content Area for Paragraph Cards -->
    <main class="dws-main-content">
        <div id="header-blocks"></div>
        <div id="draggable-blocks"></div>
        <div id="footer-blocks"></div>
    </main>
</div>

<!-- Delete Confirmation Modal -->
<div id="delete-modal" class="modal-overlay">
    <div class="modal-box">
        <h3>Confirm Deletion</h3>
        <p>Are you sure you want to delete this paragraph block? This cannot be undone.</p>
        <div style="margin-top: 1.5em; text-align: right;">
            <button id="cancel-delete-btn" class="btn">Cancel</button>
            <button id="confirm-delete-btn" class="btn-black">Delete</button>
        </div>
    </div>
</div>

<!-- JavaScript for all interactivity -->
<script>
    document.addEventListener('DOMContentLoaded', () => {
        let currentBlockToDelete = null;
        let currentCardToDelete = null;
        let minWords = 20;
        let maxWords = 150;

        const headerContainer = document.getElementById('header-blocks');
        const draggableContainer = document.getElementById('draggable-blocks');
        const footerContainer = document.getElementById('footer-blocks');
        const deleteModal = document.getElementById('delete-modal');
        const aspectRatioSelector = document.getElementById('aspect-ratio-selector');
        const slugify = (text) => text.toString().toLowerCase().replace(/[^\w\s-]/g, '').trim().replace(/[-\s]+/g, '_');

        const renderBlocks = (blocks) => {
            headerContainer.innerHTML = '';
            draggableContainer.innerHTML = '';
            footerContainer.innerHTML = '';

            blocks.forEach(block => {
                const card = document.createElement('div');
                card.className = 'paragraph-card';
                card.dataset.id = block.id;
                card.dataset.isNew = block.isNew ? 'true' : 'false';
                card.dataset.baseText = block.base_text || '';
                card.dataset.baseInstructions = block.base_instructions || '';

                const content = block.current_text || '';
                const words = content.split(/\s+/).filter(Boolean).length;
                const chars = content.length;
                const wordCountErrorClass = (words < minWords || words > maxWords) ? 'error' : '';

                card.innerHTML = `
                    <div class="paragraph-card-header">
                        ${!block.pinned ? '<div class="drag-handle">☰</div>' : '<div class="pinned-placeholder"></div>'}
                        <input type="text" value="${block.title}">
                    </div>
                    <textarea>${content}</textarea>
                    <input type="text" class="ai-instruction-input" placeholder="AI Instructions" value="${block.base_instructions || ''}">
                    <div class="paragraph-card-footer">
                        <div class="count-container">
                            <span class="word-count-display ${wordCountErrorClass}">${words} words</span>
                            <span class="count-separator">/</span>
                            <span class="char-count-display">${chars} chars</span>
                        </div>
                        <div class="paragraph-card-actions">
                            <button class="regenerate-btn btn-card-action">
                                <img class="icon-inline" src="{{ url_for_static("static", filename="icons/svg/light/arrows-clockwise-light.svg") }}" alt="" />
                                <span class="btn-text">Regenerate</span>
                                <div class="spinner-overlay"><div class="spinner"></div></div>
                            </button>
                            ${block.deletable ? '<button class="delete-btn btn-card-action"><img class="icon-inline" src="{{ url_for_static("static", filename="icons/svg/light/trash-light.svg") }}" alt="" />Delete</button>' : ''}
                            <button class="save-btn btn-card-action">
                                <img class="icon-inline" src="{{ url_for_static("static", filename="icons/svg/light/floppy-disk-light.svg") }}" alt="" />
                                Save
                            </button>
                        </div>
                    </div>
                `;
                
                const container = block.pinned === 'top' ? headerContainer : block.pinned === 'bottom' ? footerContainer : draggableContainer;
                container.appendChild(card);
            });

            attachAllListeners();
        };

        const loadTemplate = async (aspectRatio) => {
            const res = await fetch(`/admin/gdws/template/${aspectRatio}`);
            const data = await res.json();
            minWords = data.settings?.minWords || 20;
            maxWords = data.settings?.maxWords || 150;
            document.getElementById('min-words').value = minWords;
            document.getElementById('max-words').value = maxWords;
            renderBlocks(data.blocks);
        };

        new Sortable(draggableContainer, {
            animation: 150,
            handle: '.drag-handle',
            ghostClass: 'sortable-ghost',
            chosenClass: 'sortable-chosen',
        });
        
        const updateCounts = (textarea) => {
            const card = textarea.closest('.paragraph-card');
            const wordDisplay = card.querySelector('.word-count-display');
            const charDisplay = card.querySelector('.char-count-display');
            
            const content = textarea.value;
            const words = content.split(/\s+/).filter(Boolean).length;
            const chars = content.length;

            wordDisplay.textContent = `${words} words`;
            charDisplay.textContent = `${chars} chars`;
            
            wordDisplay.classList.toggle('error', words < minWords || words > maxWords);
        };
        
        const attachCardListeners = (card) => {
            const id = card.dataset.id;
            const deleteBtn = card.querySelector('.delete-btn');
            const regenerateBtn = card.querySelector('.regenerate-btn');
            const saveBtn = card.querySelector('.save-btn');
            const textarea = card.querySelector('textarea');
            const instructionInput = card.querySelector('.ai-instruction-input');
            instructionInput.value = card.dataset.baseInstructions || '';
            const titleInput = card.querySelector('.paragraph-card-header input[type="text"]');
            let originalTitle = titleInput.value;

            if (deleteBtn) {
                deleteBtn.onclick = () => {
                    currentBlockToDelete = id;
                    currentCardToDelete = card;
                    deleteModal.style.display = 'flex';
                };
            }
            
            if (regenerateBtn) {
                regenerateBtn.onclick = async () => {
                    const btnText = regenerateBtn.querySelector('.btn-text');
                    const spinner = regenerateBtn.querySelector('.spinner-overlay');

                    btnText.style.visibility = 'hidden';
                    spinner.style.display = 'flex';
                    regenerateBtn.disabled = true;

                    const aiProvider = document.getElementById('ai-provider').value;
                    const instructions = instructionInput.value;
                    const res = await fetch('/admin/gdws/regenerate-paragraph', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            base_text: card.dataset.baseText,
                            current_text: textarea.value,
                            instructions,
                            ai_provider: aiProvider
                        })
                    });
                    const data = await res.json();
                    textarea.value = data.new_content;
                    updateCounts(textarea);

                    btnText.style.visibility = 'visible';
                    spinner.style.display = 'none';
                    regenerateBtn.disabled = false;
                };
            }

            if (saveBtn) {
                saveBtn.onclick = () => {
                    const isNew = card.dataset.isNew === 'true';
                    const payload = {
                        id: isNew ? `var_${Date.now()}` : id,
                        title: titleInput.value,
                        content: textarea.value,
                        type: slugify(titleInput.value)
                    };

                    if (!isNew && originalTitle !== titleInput.value) {
                        fetch('/admin/gdws/rename-paragraph-type', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ old_title: originalTitle, new_title: titleInput.value })
                        });
                        originalTitle = titleInput.value;
                    }

                    fetch('/admin/gdws/save-paragraph', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    }).then(res => res.json()).then(data => {
                        if (data.status === 'success') {
                            alert('Paragraph saved!');
                            card.dataset.id = data.new_id;
                            card.dataset.isNew = 'false';
                        } else {
                            alert(`Error: ${data.message}`);
                        }
                    });
                };
            }

            if (textarea) {
                textarea.addEventListener('input', () => updateCounts(textarea));
                updateCounts(textarea);
            }
        };
        
        const attachAllListeners = () => {
            document.querySelectorAll('.paragraph-card').forEach(attachCardListeners);
        };

        aspectRatioSelector.addEventListener('change', (e) => {
            loadTemplate(e.target.value);
        });

        const versionCheckerContainer = document.getElementById('version-checker');
        const fetchVersionStatus = async () => {
            const mockStatus = {
                expected: { 
                    app_version: "2.5.1",
                    config_version: "1.2.0", 
                    env_version: "1.1.0", 
                    openai_primary_model: "gpt-4o",
                    openai_fallback_model: "gpt-4-turbo"
                },
                loaded: { 
                    app_version: "2.5.1",
                    config_version: "1.2.0", 
                    env_version: "1.0.0", // Mismatch example
                    openai_primary_model: "gpt-4.1", // Mismatch example
                    openai_fallback_model: "gpt-4-turbo"
                }
            };
            
            let html = '';
            for (const key in mockStatus.expected) {
                const expected = mockStatus.expected[key];
                const loaded = mockStatus.loaded[key] || 'Not Set';
                const isMatch = expected === loaded;
                const statusClass = isMatch ? 'status-match' : 'status-mismatch';
                const statusIcon = isMatch ? '✅' : '❌';
                
                html += `
                    <div class="version-status">
                        <strong>${key.replace(/_/g, ' ').replace(/(?:^|\s)\S/g, a => a.toUpperCase())}:</strong>
                        <span class="${statusClass}">${statusIcon} ${isMatch ? 'Match' : 'Mismatch'}</span><br>
                        <small>Expected: ${expected} | Loaded: ${loaded}</small>
                    </div>
                `;
            }
            versionCheckerContainer.innerHTML = html;
        };
        fetchVersionStatus();

        document.getElementById('save-new-version-btn').addEventListener('click', () => {
            const key = document.getElementById('new-version-key').value;
            const value = document.getElementById('new-version-value').value;
            if (!value) {
                alert('Please enter a new version number.');
                return;
            }
            console.log(`Saving new version: { "${key}": "${value}" }`);
            alert('New version saved to console!');
        });


        // --- OTHER EVENT LISTENERS ---
        document.getElementById('add-paragraph-btn').addEventListener('click', () => {
            const newId = `block_${Date.now()}`;
            const newBlock = { id: newId, title: "New Paragraph", content: "", pinned: false, deletable: true, isNew: true };
            renderBlocks([...getCurrentBlocks(), newBlock]);
        });

        document.getElementById('shuffle-btn').addEventListener('click', () => {
            const cards = Array.from(draggableContainer.children);
            for (let i = cards.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [cards[i], cards[j]] = [cards[j], cards[i]];
            }
            cards.forEach(card => draggableContainer.appendChild(card));
        });

        document.getElementById('save-rules-btn').addEventListener('click', () => {
            minWords = parseInt(document.getElementById('min-words').value, 10);
            maxWords = parseInt(document.getElementById('max-words').value, 10);
            console.log('Saving rules:', { minWords, maxWords });
            alert('Content rules saved!');
            document.querySelectorAll('textarea').forEach(updateCounts);
        });

        document.getElementById('cancel-delete-btn').addEventListener('click', () => {
            deleteModal.style.display = 'none';
        });

        document.getElementById('confirm-delete-btn').addEventListener('click', () => {
            if (currentCardToDelete) {
                currentCardToDelete.remove();
            }
            deleteModal.style.display = 'none';
            console.log(`Deleted block ${currentBlockToDelete}`);
        });
        
        document.getElementById('save-all-btn').addEventListener('click', () => {
            const allBlocks = [];
            const containers = [headerContainer, draggableContainer, footerContainer];
            containers.forEach(container => {
                container.querySelectorAll('.paragraph-card').forEach(card => {
                    allBlocks.push({
                        id: card.dataset.id,
                        title: card.querySelector('input[type="text"]').value,
                        content: card.querySelector('textarea').value,
                        pinned: card.closest('#header-blocks') ? 'top' : (card.closest('#footer-blocks') ? 'bottom' : false)
                    });
                });
            });

            console.log("Saving all data:", JSON.stringify(allBlocks, null, 2));
            alert("All changes saved to console! Check the developer tools.");
        });

        document.getElementById('regenerate-all-btn').addEventListener('click', () => {
            document.querySelectorAll('.regenerate-btn').forEach(btn => btn.click());
        });
        
        const getCurrentBlocks = () => {
             const allBlocks = [];
            const containers = [headerContainer, draggableContainer, footerContainer];
            containers.forEach(container => {
                container.querySelectorAll('.paragraph-card').forEach(card => {
                    allBlocks.push({
                        id: card.dataset.id,
                        title: card.querySelector('input[type="text"]').value,
                        content: card.querySelector('textarea').value,
                        pinned: card.closest('#header-blocks') ? 'top' : (card.closest('#footer-blocks') ? 'bottom' : false),
                        deletable: !!card.querySelector('.delete-btn')
                    });
                });
            });
            return allBlocks;
        };

        // Initial load
        loadTemplate(aspectRatioSelector.value);
    });
</script>
{% endblock %}

```

---
## 📄 `ezygallery/templates/account.html`

```html
{% extends "main.html" %}
{% block title %}Your Account{% endblock %}
{% block content %}
<section class="info-page">
  <h1>Your Account</h1>
  {% if session.get('user') %}
  <p>Logged in as <strong>{{ session['user'] }}</strong>.</p>
  <p><a href="{{ url_for('auth.logout') }}">Logout</a></p>
  {% else %}
  <p>You are not logged in. <a href="{{ url_for('auth.login') }}">Login here</a>.</p>
  {% endif %}
</section>
{% endblock %}

```

---
## 📄 `ezygallery/templates/terms.html`

```html
{% extends "main.html" %}
{% block title %}Terms & Limitations{% endblock %}
{% block content %}
<section class="legal-page">
  <h1>Terms & Limitations</h1>
  <p>These terms govern your use of Ezy Gallery and any artwork created or sold through this site. By continuing to browse or purchase, you agree to the following.</p>
  <h2>Intellectual Property</h2>
  <p>All artwork and site content remain the property of their respective creators. You may not reuse or resell images without explicit permission.</p>
  <h2>Licensing</h2>
  <p>Digital downloads are for personal use only. Printed products may not be scanned or reproduced. Commercial licensing can be arranged—contact us for details.</p>
  <h2>User Responsibilities</h2>
  <p>Please keep your account secure and only upload images you have the right to use. We reserve the right to remove content that breaches copyright or these terms.</p>
  <h2>Disclaimers</h2>
  <p>While we work hard to provide accurate descriptions and imagery, colours may vary on different screens and final prints. We are not liable for incidental damages or losses.</p>
  <h2>Liability</h2>
  <p>To the extent permitted by law, our total liability is limited to the amount you paid for the relevant product or service.</p>
</section>
{% endblock %}

```

---
## 📄 `ezygallery/templates/debug_status.html`

```html
{% extends 'main.html' %}
{% block title %}System Status{% endblock %}
{% block content %}
<h1>Debug: System Status</h1>
<ul>
  <li>OpenAI Key Configured: {{ info.openai_key }}</li>
  <li>Processed Folder Exists: {{ info.processed_dir }}</li>
  <li>Finalised Folder Exists: {{ info.finalised_dir }}</li>
  <li>Parse Failures: {{ info.parse_failures|length }}</li>
</ul>
{% if info.parse_failures %}
<h2>Failed Parses</h2>
<ul>
  {% for f in info.parse_failures %}
  <li>{{ f }} - <a href="{{ url_for('admin.parse_ai', file=f) }}">retry parse</a></li>
  {% endfor %}
</ul>
{% endif %}
{% endblock %}

```

---
## 📄 `ezygallery/templates/locked.html`

```html
{# Gallery of all finalised artworks with edit and export actions. #}
{% extends "main.html" %}
{% block title %}Locked Artworks{% endblock %}
{% block content %}
<h1>Locked Artworks</h1>
<p class="help-tip">These artworks are locked and cannot be edited until unlocked.</p>
<div class="view-toggle">
  <button id="grid-view-btn" class="btn-small">Grid</button>
  <button id="list-view-btn" class="btn-small">List</button>
</div>
{% if not artworks %}
  <p>No artworks have been finalised yet. Come back after you approve some beautiful pieces!</p>
{% else %}
<div class="finalised-grid">
  {% for art in artworks %}
  <div class="final-card">
    <div class="card-thumb">
      {% if art.main_image %}
      <a href="{{ url_for('artwork.finalised_image', seo_folder=art.seo_folder, filename=art.main_image) }}" class="final-img-link" data-img="{{ url_for('artwork.finalised_image', seo_folder=art.seo_folder, filename=art.main_image) }}">
        <img src="{{ url_for('artwork.finalised_image', seo_folder=art.seo_folder, filename=art.main_image) }}" class="card-img-top" alt="{{ art.title }}">
      </a>
      {% else %}
      <img src="{{ url_for_static('static', filename='img/no-image.svg') }}" class="card-img-top" alt="No image">
      {% endif %}
    </div>
    <div class="card-details">
      <div class="file-name" title="{{ art.filename }}">{{ art.filename }}</div>
      <div class="card-title">{{ art.title }} <span class="locked-badge" title="{{ art.lock_reason }}">Locked</span></div>
      <div class="lock-meta">Locked by {{ art.locked_by }} on {{ art.locked_at }}{% if art.lock_reason %} – {{ art.lock_reason }}{% endif %}</div>
      <div class="desc-snippet" title="{{ art.description }}">
        {{ art.description[:200] }}{% if art.description|length > 200 %}...{% endif %}
      </div>
      <div>SKU: {{ art.sku }}</div>
      <div>Price: {{ art.price }}</div>
      <div>Colours: {{ art.primary_colour }} / {{ art.secondary_colour }}</div>
      <div>SEO: {{ art.seo_filename }}</div>
      <div>Tags: {{ art.tags|join(', ') }}</div>
      <div>Materials: {{ art.materials|join(', ') }}</div>
      {% if art.mockups %}
      <div class="mini-mockup-grid">
        {% for m in art.mockups %}
        <img src="{{ url_for('artwork.finalised_image', seo_folder=art.seo_folder, filename=m.filename) }}" alt="mockup"/>
        {% endfor %}
      </div>
      {% endif %}
      {% if art.images %}
      <details class="img-urls">
        <summary>Image URLs</summary>
        <ul>
          {% for img in art.images %}
          <li>
            <a href="{{ url_for('artwork.finalised_image', seo_folder=art.seo_folder, filename=img.split('/')[-1]) }}" target="_blank">/{{ img }}</a>
          </li>
          {% endfor %}
        </ul>
      </details>
      {% endif %}
    </div>
  <div class="final-actions">
    <a class="btn-black btn-disabled" aria-disabled="true">Edit</a>
    <form method="post" action="{{ url_for('artwork.unlock_listing', aspect=art.aspect, filename=art.filename) }}" class="lock-form" style="display:inline;">
      <input type="hidden" name="reason" value="">
      <button type="submit" class="btn-black">Unlock</button>
    </form>
    <form method="post" action="{{ url_for('artwork.delete_finalised', aspect=art.aspect, filename=art.filename) }}" class="locked-delete-form" style="display:inline;">
      <input type="hidden" name="confirm" value="">
      <button type="submit" class="btn-black btn-danger">Delete</button>
    </form>
  </div>
  </div>
  {% endfor %}
</div>
{% endif %}
<div id="final-modal-bg" class="modal-bg">
  <button id="final-modal-close" class="modal-close" aria-label="Close modal">&times;</button>
  <div class="modal-img"><img id="final-modal-img" src="" alt="Full image"/></div>
</div>
<script>
  document.querySelectorAll('.final-img-link').forEach(link => {
    link.addEventListener('click', function(e){
      e.preventDefault();
      const modal = document.getElementById('final-modal-bg');
      const img = document.getElementById('final-modal-img');
      img.src = this.dataset.img;
      modal.style.display = 'flex';
    });
  });
  document.getElementById('final-modal-close').onclick = function(){
    document.getElementById('final-modal-bg').style.display='none';
    document.getElementById('final-modal-img').src='';
  };
  document.getElementById('final-modal-bg').onclick = function(e){
    if(e.target===this){
      this.style.display='none';
      document.getElementById('final-modal-img').src='';
    }
  };
  document.querySelectorAll('.locked-delete-form').forEach(f=>{
    f.addEventListener('submit',function(ev){
      const val=prompt('This listing is locked and will be permanently deleted. Type DELETE to confirm');
      if(val!=='DELETE'){ev.preventDefault();}
      else{this.querySelector('input[name="confirm"]').value='DELETE';}
    });
  });
  document.querySelectorAll('.lock-form').forEach(f=>{
    f.addEventListener('submit',function(ev){
      const r=prompt('Reason for lock/unlock? (optional)');
      if(r!==null) this.querySelector('input[name="reason"]').value=r;
    });
  });
  const gBtn=document.getElementById('grid-view-btn');
  const lBtn=document.getElementById('list-view-btn');
  const grid=document.querySelector('.finalised-grid');
  function apply(v){ if(v==='list'){grid.classList.add('list-view');} else {grid.classList.remove('list-view');} }
  if(gBtn) gBtn.addEventListener('click',()=>{apply('grid'); localStorage.setItem('lockedView','grid');});
  if(lBtn) lBtn.addEventListener('click',()=>{apply('list'); localStorage.setItem('lockedView','list');});
  apply(localStorage.getItem('lockedView')||'grid');
</script>
{% endblock %}

```

---
## 📄 `ezygallery/templates/about.html`

```html
{% extends "main.html" %}
{% block title %}About Ezy Gallery{% endblock %}
{% block content %}
<section class="info-page">
  <h1>About</h1>
  <p>Ezy Gallery is the passion project of a small Aussie team led by artist Robin Custance. We blend creative spirit with smart automation to help artists showcase and sell their work online.</p>
  <p>From humble beginnings experimenting with digital brushes to building a full e-commerce platform, our goal is simple: empower creatives with ethical, inclusive tools.</p>
</section>
{% endblock %}

```

---
## 📄 `ezygallery/templates/upgrade.html`

```html
{% extends "main.html" %}
{% block title %}Upgrade to Premium{% endblock %}
{% block content %}
<section class="info-page">
  <h1>Upgrade to Premium</h1>
  <p>Unlock advanced features and priority support by upgrading your Ezy Gallery account.</p>
  <p class="mt-2">Contact us if you’d like early access to premium tools.</p>
</section>
{% endblock %}

```

---
## 📄 `ezygallery/templates/prompt_generator.html`

```html
{% extends 'main.html' %}
{% block title %}AI Prompt Generator{% endblock %}
{% block content %}
<h1>AI Prompt Generator</h1>
<form id="prompt-form">
  <label>Genre:
    <select name="genre" id="genre-select"></select>
  </label><br>
  <label>Style:
    <select name="style" id="style-select"></select>
  </label><br>
  <label>Technique:
    <select name="technique" id="technique-select"></select>
  </label><br>
  <label>Medium:
    <select name="medium" id="medium-select"></select>
  </label><br>
  <label>Palette:
    <select name="palette" id="palette-select"></select>
  </label><br>
  <label>Texture:
    <select name="texture" id="texture-select"></select>
  </label><br>
  <button type="submit">Generate Prompt</button>
</form>
<pre id="prompt-output"></pre>
<script>
const fields = ['genre','style','technique','medium','palette','texture'];
fields.forEach(f => {
  fetch(`/api/prompt-options/${f}s`)
    .then(r=>r.json())
    .then(opts => {
      const sel=document.getElementById(`${f}-select`);
      opts.forEach(o=>{ const opt=document.createElement('option'); opt.value=o; opt.textContent=o; sel.appendChild(opt); });
    });
});
document.getElementById('prompt-form').addEventListener('submit',e=>{
  e.preventDefault();
  const data = {};
  fields.forEach(f=>{ data[f]=document.getElementById(`${f}-select`).value; });
  document.getElementById('prompt-output').textContent = JSON.stringify(data, null, 2);
});
</script>
{% endblock %}

```

---
## 📄 `ezygallery/templates/contact.html`

```html
{% extends "main.html" %}
{% block title %}Contact{% endblock %}
{% block content %}
<section class="info-page">
  <h1>Contact</h1>
  <p>We love hearing from fellow artists and art lovers. If you have questions or just want to say g’day, drop us a line at <a href="mailto:info@example.com">info@example.com</a>.</p>
  <p>While this site doesn’t have automated email sending just yet, we check our inbox regularly and will get back to you as soon as we can.</p>
</section>
{% endblock %}

```

---
## 📄 `ezygallery/templates/aigw.html`

```html
{% extends "main.html" %}
{% block title %}AI Image Generator Whisperer{% endblock %}
{% block content %}
<h1>AI Image Generator Whisperer</h1>
<form method="post" id="prompt-form">
  <div class="form-block">
    <label for="prompt">Base Prompt</label>
    <textarea id="prompt" name="prompt" rows="3" required></textarea>
  </div>
  <div class="selector-grid">
    {% for key, vals in options.items() %}
    <div class="selector-col">
      <label for="sel-{{ key }}">{{ key.replace('_',' ').title() }}</label>
      <select id="sel-{{ key }}" name="{{ key }}">
        <option value="">Let the AI decide</option>
        {% for v in vals %}
        <option value="{{ v }}">{{ v }}</option>
        {% endfor %}
      </select>
    </div>
    {% endfor %}
  </div>
  <button type="submit" class="btn-black">Save Prompt</button>
</form>
<div class="summary-box">
  <h2>Current Selections</h2>
  <ul id="summary-list"></ul>
</div>
<script>
  function updateSummary() {
    const summary = document.getElementById('summary-list');
    summary.innerHTML = '';
    const prompt = document.getElementById('prompt').value.trim();
    if(prompt){
      const li = document.createElement('li');
      li.textContent = `Prompt: ${prompt}`;
      summary.appendChild(li);
    }
    document.querySelectorAll('.selector-col select').forEach(sel=>{
      if(sel.value){
        const li = document.createElement('li');
        li.textContent = `${sel.previousElementSibling.textContent}: ${sel.value}`;
        summary.appendChild(li);
      }
    });
  }
  document.getElementById('prompt-form').addEventListener('input', updateSummary);
  updateSummary();
</script>
<!-- Styles moved to static/css/custom.css -->
{% endblock %}

```

---
## 📄 `ezygallery/templates/prompt_whisperer.html`

```html
{% extends "main.html" %}
{% block title %}Prompt Whisperer | Ezy Gallery{% endblock %}
{% block content %}
<h2>AI Image Prompt Whisperer</h2>
<p class="module-help">
  <a href="{{ url_for('documentation.howto_whisperer') }}">How-To</a>
  |
  <a href="{{ url_for('documentation.docs_all') }}#whisperer-howto">Full Docs</a>
</p>
<div class="whisperer-form">
  <label for="prompt">Prompt</label>
  <textarea id="prompt" rows="4">{{ prompt }}</textarea>

  <label for="instructions">Instructions</label>
  <input id="instructions" type="text" placeholder="Optional guidance" />

  <label for="word_count">Word Count</label>
  <select id="word_count">
    {% for n in [10,20,40,60,100] %}
    <option value="{{n}}">{{n}}</option>
    {% endfor %}
  </select>

  <label for="category">Category</label>
  <select id="category">
    {% for cat in categories %}
    <option value="{{cat}}">{{cat}}</option>
    {% endfor %}
  </select>

  <fieldset>
    <legend>Prompt Randomness</legend>
    {% for r in [0,20,40,60,80,100] %}
    <label><input type="radio" name="randomness" value="{{r}}" {% if r==40 %}checked{% endif %}>{{r}}</label>
    {% endfor %}
  </fieldset>

  <fieldset>
    <legend>Sentiment</legend>
    {% for s in sentiments %}
    <label><input type="radio" name="sentiment" value="{{s}}" {% if loop.index==1 %}checked{% endif %}>{{s}}</label>
    {% endfor %}
  </fieldset>

  <div class="actions">
    <button id="generate">Generate Prompt</button>
    <button id="save">Save Prompt</button>
    <button id="clear" type="button">Clear</button>
  </div>
</div>
<p class="example">Example: <span id="example">A mystical landscape with shimmering light.</span></p>
<script src="{{ url_for_static('static', filename='js/prompt_whisperer.js') }}"></script>
{% endblock %}

```

---
## 📄 `ezygallery/templates/gallery.html`

```html
{% extends 'main.html' %}
{% block title %}Gallery{% endblock %}
{% block content %}
  <h1>Gallery Placeholder</h1>
  <p class="module-help">
    <a href="{{ url_for('documentation.howto_gallery') }}">How-To</a>
    |
    <a href="{{ url_for('documentation.docs_all') }}#gallery-howto">Full Docs</a>
  </p>
  <p>The gallery page is under construction.</p>
{% endblock %}

```

---
## 📄 `ezygallery/templates/artworks.html`

```html
{# [WF-STEP-2] This page shows the circled step number at the top of the content, using .page-step-icon #}
{# Use blueprint-prefixed endpoints like 'artwork.home' in url_for #}
{% extends "main.html" %}
{% from 'components/stage_indicator.html' import stage_indicator %}
{% block title %}Artwork Gallery | Ezy Gallery{% endblock %}
{% block content %}
{{ stage_indicator(2, 'Gallery', True) }}

<div class="gallery-section">

  {% if ready_artworks %}
    <h2 class="mb-3">Ready to Analyze</h2>
    <div class="artwork-grid">
      {% for art in ready_artworks %}
      <div class="gallery-card">
        <div class="card-thumb">
          <img class="card-img-top"
               src="{{ url_for('artwork.temp_image', filename=art.thumb) }}"
               alt="{{ art.title }}">
        </div>
        <div class="card-details">
          <div class="file-name" title="{{ art.filename }}">{{ art.filename }}</div>
          <form method="post" action="{{ url_for('artwork.analyze_upload', base=art.base) }}" class="analyze-form">
            <button type="submit" class="btn btn-primary">Analyze</button>
          </form>
        </div>
      </div>
      {% endfor %}
    </div>
  {% endif %}

  {% if processed_artworks %}
    <h2 class="mb-3 mt-5">Processed Artworks</h2>
    <div class="artwork-grid">
      {% for art in processed_artworks %}
      <div class="gallery-card">
        <div class="card-thumb">
          <img class="card-img-top"
               src="{{ url_for('artwork.processed_image', seo_folder=art.seo_folder, filename=art.thumb) }}"
               alt="{{ art.title }}">
        </div>
        <div class="card-details">
          <div class="file-name" title="{{ art.filename }}">{{ art.filename }}</div>
          <a href="{{ url_for('artwork.edit_listing', aspect=art.aspect, filename=art.filename) }}"
             class="btn btn-secondary">Review</a>
        </div>
      </div>
      {% endfor %}
    </div>
  {% endif %}

  {% if finalised_artworks %}
    <h2 class="mb-3 mt-5">Finalised Artworks</h2>
    <div class="artwork-grid">
      {% for art in finalised_artworks %}
      <div class="gallery-card">
        <div class="card-thumb">
          <img class="card-img-top"
               src="{{ url_for('artwork.finalised_image', seo_folder=art.seo_folder, filename=art.thumb) }}"
               alt="{{ art.title }}">
        </div>
        <div class="card-details">
          <div class="file-name" title="{{ art.filename }}">{{ art.filename }}</div>
          <a href="{{ url_for('artwork.edit_listing', aspect=art.aspect, filename=art.filename) }}" class="btn btn-secondary">Edit</a>
        </div>
      </div>
      {% endfor %}
    </div>
  {% endif %}
  {% if not ready_artworks and not processed_artworks and not finalised_artworks %}
    <p class="empty-msg">No artworks found. Please upload artwork to get started!</p>
  {% endif %}

</div>

{% endblock %}

```

---
## 📄 `ezygallery/templates/privacy.html`

```html
{% extends "main.html" %}
{% block title %}Privacy Policy{% endblock %}
{% block content %}
<section class="legal-page">
  <h1>Privacy Policy</h1>
  <p>Welcome to Ezy Gallery! We value your privacy and are committed to protecting your personal information. This policy explains what data we collect and how we use it.</p>
  <h2>Information We Collect</h2>
  <p>We collect basic contact details if you choose to create an account or sign up to our mailing list. We also gather anonymous analytics to understand how visitors use the site. Cookies help remember your preferences and keep you logged in.</p>
  <h2>How We Use Your Data</h2>
  <p>Your information is used solely to run the site and deliver our services. We may email you with updates or important notices. Usage data helps us improve features and keep everything running smoothly.</p>
  <h2>Third-Party Services</h2>
  <p>Ezy Gallery relies on trusted partners such as OpenAI for AI features, print-on-demand services to manufacture products, and payment providers to securely process purchases. These services may process some of your data under their own policies.</p>
  <h2>Your Rights</h2>
  <p>You can request a copy of your information or ask us to delete it at any time. Just reach out via the contact details below and we’ll help you out.</p>
  <h2>Contact</h2>
  <p>For any privacy questions, email <a href="mailto:info@example.com">info@example.com</a>.</p>
</section>
{% endblock %}

```

---
## 📄 `ezygallery/templates/test_description.html`

```html
{% extends "main.html" %}
{% block title %}Test Combined Description{% endblock %}
{% block content %}
<h1>Test Combined Description</h1>
<div class="desc-text" style="white-space: pre-wrap;border:1px solid #ccc;padding:10px;">
  {{ combined_description }}
</div>
{% endblock %}

```

---
## 📄 `ezygallery/templates/index.html`

```html
{# Use blueprint-prefixed endpoints like 'artwork.home' in url_for #}
{% extends "main.html" %}
{% block title %}Ezy Gallery Home{% endblock %}
{% block content %}

<!-- ========== [IN.1] Home Hero Section ========== -->
<div class="home-hero">
  <h1>Welcome to Ezy Gallery The Art Listing Machine</h1>
  <p class="home-intro">
    G’day! Start in the Artwork Gallery, analyze new pieces, review your AI-generated listings and mockups, and prep everything for marketplace export—all streamlined for you.
  </p>
  <p class="module-help">
    <a href="{{ url_for('documentation.howto_home') }}">How-To</a>
    |
    <a href="{{ url_for('documentation.docs_all') }}#home-howto">Full Docs</a>
  </p>
</div>

<!-- ========== [IN.2] Home Quick Actions ========== -->
<div class="workflow-grid">
  <a href="{{ url_for('artwork.upload_artwork') }}" class="step-btn">
    <img class="step-num-icon" src="{{ url_for_static('static', filename='icons/svg/light/number-circle-one-light.svg') }}" alt="Stage 1" />
    Upload to Gallery
  </a>
  <a href="{{ url_for('artwork.artworks') }}" class="step-btn">
    <img class="step-num-icon" src="{{ url_for_static('static', filename='icons/svg/light/number-circle-two-light.svg') }}" alt="Stage 2" />
    Gallery / Analyze
  </a>
  {% if latest_artwork %}
  <a href="{{ url_for('artwork.edit_listing', aspect=latest_artwork.aspect, filename=latest_artwork.filename) }}" class="step-btn">
    <img class="step-num-icon" src="{{ url_for_static('static', filename='icons/svg/light/number-circle-three-light.svg') }}" alt="Stage 3" />
    Edit &amp; Finalise
  </a>
  {% else %}
  <span class="step-btn disabled">
    <img class="step-num-icon" src="{{ url_for_static('static', filename='icons/svg/light/number-circle-three-light.svg') }}" alt="Stage 3" />
    Edit &amp; Finalise
  </span>
  {% endif %}
  <a href="{{ url_for('artwork.finalised_gallery') }}" class="step-btn">
    <img class="step-num-icon" src="{{ url_for_static('static', filename='icons/svg/light/number-circle-four-light.svg') }}" alt="Stage 4" />
    Finalised Gallery
  </a>
  <span class="step-btn disabled">
    <img class="step-num-icon" src="{{ url_for_static('static', filename='icons/svg/light/number-circle-five-light.svg') }}" alt="Stage 5" />
    Publish (coming soon)
  </span>
</div>

<!-- ========== [IN.3] How It Works Section ========== -->
<section class="how-it-works">
  <h2>How It Works</h2>
  <div class="how-it-works-steps">
    <div class="how-step">
      <img class="step-num-icon" src="{{ url_for_static('static', filename='icons/svg/light/number-circle-one-light.svg') }}" alt="Step 1" />
      <strong>Upload:</strong> Chuck your artwork into the gallery (easy drag & drop).
    </div>
    <div class="how-step">
      <img class="step-num-icon" src="{{ url_for_static('static', filename='icons/svg/light/number-circle-two-light.svg') }}" alt="Step 2" />
      <strong>Analyze:</strong> Let the AI do its magic—SEO, titles, pro description, the lot.
    </div>
    <div class="how-step">
      <img class="step-num-icon" src="{{ url_for_static('static', filename='icons/svg/light/number-circle-three-light.svg') }}" alt="Step 3" />
      <strong>Edit & Finalise:</strong> Quick review and tweak, fix anything you like.
    </div>
    <div class="how-step">
      <img class="step-num-icon" src="{{ url_for_static('static', filename='icons/svg/light/number-circle-four-light.svg') }}" alt="Step 4" />
      <strong>Mockups:</strong> Instantly see your art in bedrooms, offices, nurseries—looks a million bucks.
    </div>
    <div class="how-step">
      <img class="step-num-icon" src="{{ url_for_static('static', filename='icons/svg/light/number-circle-five-light.svg') }}" alt="Step 5" />
      <strong>Final Gallery:</strong> See all your finished work, ready for showtime.
    </div>
  </div>
</section>
{% endblock %}

```

---
## 📄 `ezygallery/templates/composites_preview.html`

```html
{# Use blueprint-prefixed endpoints like 'artwork.home' in url_for #}
{% extends "main.html" %}
{% block title %}Composite Preview | Ezy Gallery{% endblock %}
{% block content %}
<h1 style="text-align:center;">Composite Preview: {{ seo_folder }}</h1>
{% if listing %}
  <div style="text-align:center;margin-bottom:1.5em;">
    <img src="{{ url_for('artwork.processed_image', seo_folder=seo_folder, filename=seo_folder+'.jpg') }}" alt="artwork" style="max-width:260px;border-radius:8px;box-shadow:0 2px 6px #0002;">
  </div>
{% endif %}
{% if images %}
<div class="grid">
  {% for img in images %}
  <div class="item">
    {% if img.exists %}
    <img src="{{ url_for('artwork.processed_image', seo_folder=seo_folder, filename=img.filename) }}" alt="{{ img.filename }}">
    {% else %}
    <div class="missing-img">Image Not Found</div>
    {% endif %}
    <div style="font-size:0.9em;color:#555;word-break:break-all;">{{ img.filename }}</div>
    {% if img.category %}<div style="color:#888;font-size:0.9em;">{{ img.category }}</div>{% endif %}
    <form method="post" action="{{ url_for('artwork.regenerate_composite', seo_folder=seo_folder, slot_index=img.index) }}">
      <button type="submit" class="btn btn-reject">Regenerate</button>
    </form>
  </div>
  {% endfor %}
</div>
<form method="post" action="{{ url_for('artwork.approve_composites', seo_folder=seo_folder) }}" style="text-align:center;margin-top:2em;">
  <button type="submit" class="composite-btn">Finalize &amp; Approve</button>
</form>
{% else %}
<p style="text-align:center;margin:2em 0;">No composites found.</p>
{% endif %}
<div style="text-align:center;margin-top:2em;">
  <a href="{{ url_for('artwork.select') }}" class="composite-btn">Back to Selector</a>
</div>
{% endblock %}

```

---
## 📄 `ezygallery/templates/upload_results.html`

```html
{% extends "main.html" %}
{% block title %}Upload Results{% endblock %}
{% block content %}
<h2 class="mb-3">Upload Summary</h2>
<ul>
  {% for r in results %}
    <li>{% if r.success %}✅ {{ r.original }}{% else %}❌ {{ r.original }}: {{ r.error }}{% endif %}</li>
  {% endfor %}
</ul>
<a href="{{ url_for('artwork.artworks') }}" class="btn btn-primary">Return to Gallery</a>
{% endblock %}

```

---
## 📄 `ezygallery/templates/mockup_selector.html`

```html
{# Use blueprint-prefixed endpoints like 'artwork.home' in url_for #}
{% extends "main.html" %}
{% block title %}Select Mockups | Ezy Gallery{% endblock %}
{% block content %}
<h1>🖼️ Select Your Mockup Lineup</h1>
<div class="grid">
  {% for slot, options in zipped %}
  <div class="item">
    {% if slot.image %}
      <img src="{{ url_for('artwork.mockup_img', category=slot.category, filename=slot.image) }}" alt="{{ slot.category }}" />
    {% else %}
      <p>No images for {{ slot.category }}</p>
    {% endif %}
    <strong>{{ slot.category }}</strong>
    <form method="post" action="{{ url_for('artwork.regenerate') }}">
      <input type="hidden" name="slot" value="{{ loop.index0 }}" />
      <button type="submit">🔄 Regenerate</button>
    </form>
    <form method="post" action="{{ url_for('artwork.swap') }}">
      <input type="hidden" name="slot" value="{{ loop.index0 }}" />
      <select name="new_category">
        <!-- DEBUG: Options for slot {{ loop.index0 }}: {{ options|join(", ") }} -->
        {% for c in options %}
        <option value="{{ c }}" {% if c == slot.category %}selected{% endif %}>{{ c }}</option>
        {% endfor %}
      </select>
      <button type="submit">🔁 Swap</button>
    </form>
  </div>
  {% endfor %}
</div>
<form method="post" action="{{ url_for('artwork.proceed') }}">
  <button class="composite-btn" type="submit">✅ Generate Composites</button>
</form>
<div style="text-align:center;margin-top:1em;">
  {% if session.latest_seo_folder %}
    <a href="{{ url_for('artwork.composites_specific', seo_folder=session.latest_seo_folder) }}" class="composite-btn" style="background:#666;">👁️ Preview Composites</a>
  {% else %}
    <a href="{{ url_for('artwork.composites_preview') }}" class="composite-btn" style="background:#666;">👁️ Preview Composites</a>
  {% endif %}
</div>
{% endblock %}

```

---
## 📄 `ezygallery/templates/edit_listing.html`

```html
{% extends "main.html" %}
{% block title %}Edit Artwork Listing{% endblock %}
{% block content %}
{% set final_preview_url = url_for('artwork.finalised_image', seo_folder=seo_folder, filename=artwork.seo_filename) %}
<div class="bg-gray-50 dark:bg-gray-900 min-h-screen py-12">
  <div class="container mx-auto px-4 sm:px-6 lg:px-8 max-w-3xl">

    <!-- Header -->
    <div class="text-center mb-8">
      <h1 class="text-4xl sm:text-5xl font-extrabold text-gray-900 dark:text-white">Edit Listing</h1>
      <div class="mt-2 flex items-center justify-center gap-4 text-lg">
        <span class="font-semibold text-gray-600 dark:text-gray-400">
          Status:
          <span class="font-bold {% if finalised %}text-green-500{% else %}text-yellow-500{% endif %}">
            {% if finalised %}Finalised{% else %}In Progress{% endif %}
          </span>
        </span>
        {% if locked %}
        <span class="flex items-center gap-2 text-red-500 font-bold">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 1a4.5 4.5 0 00-4.5 4.5V9H5a2 2 0 00-2 2v6a2 2 0 002 2h10a2 2 0 002-2v-6a2 2 0 00-2-2h-.5V5.5A4.5 4.5 0 0010 1zm3 8V5.5a3 3 0 10-6 0V9h6z" clip-rule="evenodd" />
          </svg>
          Locked
        </span>
        {% endif %}
      </div>
    </div>

    <!-- Artwork Preview and Mockups -->
    <div class="mb-8">
      <div class="primary-thumb-container text-center mb-4">
        <label class="block font-semibold mb-1">Primary Thumbnail</label>
        <img id="primary-thumb" src="{{ thumbnail_url }}" alt="{{ artwork.title }} primary thumbnail" tabindex="0" class="primary-thumb rounded shadow-md cursor-pointer">
      </div>
      <div id="thumbnail-grid" class="mockup-grid">
        <img src="{{ thumbnail_url }}" class="mockup-thumb" alt="Thumbnail 1" tabindex="0">
        {% for url in mockup_urls %}
          <img src="{{ url }}" class="mockup-thumb" alt="Mockup {{ loop.index }}" tabindex="0">
        {% endfor %}
      </div>
    </div>

    <!-- Edit Form -->
    <div class="bg-white dark:bg-gray-800 p-8 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 mb-8">
      <form id="edit-form" method="POST" autocomplete="off" class="space-y-6">
        {% set fields = ['title', 'description', 'tags', 'materials', 'primary_colour', 'secondary_colour', 'seo_filename', 'price', 'sku'] %}
        {% for field in fields %}
        <div>
          <label for="{{ field }}" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">{{ field.replace('_', ' ')|title }}</label>
          {% if field in ['primary_colour', 'secondary_colour'] %}
          <select id="{{ field }}" name="{{ field }}" class="block w-full rounded-md bg-gray-100 dark:bg-gray-700 border-gray-300 dark:border-gray-600 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" {% if not editable %}disabled{% endif %}>
            {% for col in colour_options %}<option value="{{ col }}" {% if artwork[field]==col %}selected{% endif %}>{{ col }}</option>{% endfor %}
          </select>
          {% elif field == 'description' %}
          <textarea id="{{ field }}" name="{{ field }}" rows="12" class="block w-full rounded-md bg-gray-100 dark:bg-gray-700 border-gray-300 dark:border-gray-600 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" {% if not editable %}disabled{% endif %}>{{ artwork[field]|e }}</textarea>
          {% elif field == 'sku' %}
          <input type="text" id="{{ field }}" value="{{ artwork[field]|e }}" class="block w-full rounded-md bg-gray-200 dark:bg-gray-700 border-transparent text-gray-500 focus:ring-0" readonly disabled>
          {% else %}
          <input type="text" id="{{ field }}" name="{{ field }}" value="{{ artwork[field]|e }}" class="block w-full rounded-md bg-gray-100 dark:bg-gray-700 border-gray-300 dark:border-gray-600 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" {% if not editable %}disabled{% endif %}>
          {% endif %}
        </div>
        {% endfor %}
      </form>
    </div>

    <!-- Action Buttons -->
    <div class="space-y-3">
      <button form="edit-form" type="submit" name="action" value="save" class="w-full bg-gray-800 dark:bg-gray-200 hover:bg-gray-900 dark:hover:bg-white text-white dark:text-black font-bold py-3 px-4 rounded-lg transition-colors shadow-md disabled:opacity-50">Save Changes</button>
      <button form="edit-form" type="submit" name="action" value="delete" class="w-full bg-gray-800 dark:bg-gray-200 hover:bg-red-600 dark:hover:bg-red-500 text-white dark:text-black hover:text-white dark:hover:text-white font-bold py-3 px-4 rounded-lg transition-colors shadow-md delete-btn disabled:opacity-50">Delete</button>
      {% if not finalised %}
      <form method="post" action="{{ url_for('artwork.finalise_artwork', aspect=aspect, filename=filename) }}" class="w-full"><button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg transition-colors shadow-md">Finalise</button></form>
      {% endif %}
      <form method="POST" action="{{ url_for('artwork.analyze_artwork', aspect=aspect, filename=filename) }}" class="w-full"><button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-4 rounded-lg transition-colors shadow-md disabled:opacity-50" {% if locked %}disabled{% endif %}>Re-analyse Artwork</button></form>
    </div>

  </div>
</div>

<!-- Modal Carousel -->
<div id="carousel-modal" class="carousel-modal" aria-hidden="true">
  <div class="carousel-content">
    <button class="carousel-close" aria-label="Close">&times;</button>
    <button class="carousel-nav left" aria-label="Previous">&#10094;</button>
    <img id="carousel-img" class="carousel-img" src="" alt="Mockup preview">
    <button class="carousel-nav right" aria-label="Next">&#10095;</button>
    <div id="carousel-counter" class="carousel-counter"></div>
  </div>
</div>
<script>
const mockupUrls = [{{ thumbnail_url|tojson }}, ...{{ mockup_urls|tojson }}];
let currentIndex = 0;
const modal = document.getElementById('carousel-modal');
const modalImg = document.getElementById('carousel-img');
const counter = document.getElementById('carousel-counter');

function showImage() {
  modalImg.src = mockupUrls[currentIndex];
  if(counter) counter.textContent = `${currentIndex + 1} / ${mockupUrls.length}`;
}

function openCarousel(startIndex = 0) {
  currentIndex = startIndex;
  showImage();
  modal.classList.add('active');
  modal.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
}

function closeCarousel() {
  modal.classList.remove('active');
  modal.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
}

function nextImage() { currentIndex = (currentIndex + 1) % mockupUrls.length; showImage(); }
function prevImage() { currentIndex = (currentIndex - 1 + mockupUrls.length) % mockupUrls.length; showImage(); }

document.querySelectorAll('#primary-thumb, #thumbnail-grid img').forEach((img, idx) => {
  img.addEventListener('click', () => openCarousel(idx));
  img.addEventListener('keydown', e => { if(e.key==='Enter' || e.key===' ') { e.preventDefault(); openCarousel(idx); }});
});

document.querySelector('.carousel-close').addEventListener('click', closeCarousel);
document.querySelector('.carousel-nav.right').addEventListener('click', nextImage);
document.querySelector('.carousel-nav.left').addEventListener('click', prevImage);
modal.addEventListener('click', e => { if(e.target === modal) closeCarousel(); });

document.addEventListener('keydown', e => {
  if(!modal.classList.contains('active')) return;
  if(e.key === 'Escape') closeCarousel();
  else if(e.key === 'ArrowRight') nextImage();
  else if(e.key === 'ArrowLeft') prevImage();
});

const delBtn = document.querySelector('.delete-btn');
if(delBtn){
  delBtn.addEventListener('click', e => { if(!confirm('Delete this artwork and all files?')) e.preventDefault(); });
}
</script>

<style>
.primary-thumb-container img.primary-thumb { max-width: 260px; width: 100%; height: auto; }
.mockup-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px,1fr)); gap: 0.5rem; }
.mockup-thumb { width: 100%; height: 120px; object-fit: cover; cursor: pointer; border: 2px solid #ddd; }
.carousel-modal { display:none; position:fixed; inset:0; background:rgba(0,0,0,0.9); align-items:center; justify-content:center; z-index:1000; }
.carousel-modal.active { display:flex; }
.carousel-content { position:relative; width:85vw; height:85vh; display:flex; align-items:center; justify-content:center; }
.carousel-content img { max-width:100%; max-height:100%; }
.carousel-nav { position:absolute; top:50%; transform:translateY(-50%); background:none; border:none; color:#fff; font-size:2rem; cursor:pointer; }
.carousel-nav.left { left:10px; }
.carousel-nav.right { right:10px; }
.carousel-close { position:absolute; top:10px; right:10px; background:none; border:none; color:#fff; font-size:2rem; cursor:pointer; }
#carousel-counter { position:absolute; bottom:10px; right:50%; transform:translateX(50%); color:#fff; font-size:1rem; }
</style>
{% endblock %}

```

---
## 📄 `ezygallery/templates/review.html`

```html
{# Use blueprint-prefixed endpoints like 'artwork.home' in url_for #}
{% extends "main.html" %}
{% block title %}Review | Ezy Gallery{% endblock %}
{% block content %}
<h1>Review &amp; Approve Listing</h1>
<section class="review-artwork">
  <h2>{{ artwork.title }}</h2>
  <div class="artwork-images">
    <img src="{{ url_for_static('static', filename='outputs/processed/' ~ artwork.seo_name ~ '/' ~ artwork.main_image) }}"
         alt="Main artwork" class="main-art-img">
    <img src="{{ url_for_static('static', filename='outputs/processed/' ~ artwork.seo_name ~ '/' ~ artwork.thumb) }}"
         alt="Thumbnail" class="thumb-img">
  </div>
  <h3>Description</h3>
  <div class="art-description">
    <pre style="white-space: pre-wrap; font-family:inherit;">{{ artwork.description }}</pre>
  </div>
  <h3>Mockups</h3>
  <div class="grid">
    {% for slot in slots %}
    <div class="item">
      <img src="{{ url_for('artwork.mockup_img', category=slot.category, filename=slot.image) }}" alt="{{ slot.category }}">
      <strong>{{ slot.category }}</strong>
    </div>
    {% endfor %}
  </div>
</section>
<form method="get" action="{{ url_for('artwork.select') }}">
  <input type="hidden" name="reset" value="1">
  <button class="composite-btn" type="submit">Start Over</button>
</form>
<div style="text-align:center;margin-top:1.5em;">
  <a href="{{ url_for('artwork.composites_specific', seo_folder=artwork.seo_name) }}" class="composite-btn" style="background:#666;">Preview Composites</a>
</div>
{% endblock %}

```

---
## 📄 `ezygallery/templates/finalised.html`

```html
{# [WF-STEP-4] This page shows the circled step number at the top of the content, using .page-step-icon #}
{# Gallery of all finalised artworks with edit and export actions. #}
{% extends "main.html" %}
{% from 'components/stage_indicator.html' import stage_indicator %}
{% block title %}Finalised Artworks{% endblock %}
{% block content %}
{{ stage_indicator(4, 'Finalise', True) }}
<h1>Finalised Artworks</h1>
<p class="help-tip">Finalised artworks are ready for publishing. You can still edit or delete them here.</p>
<div class="view-toggle">
  <button id="grid-view-btn" class="btn-small">Grid</button>
  <button id="list-view-btn" class="btn-small">List</button>
</div>
{% if not artworks %}
  <p>No artworks have been finalised yet. Come back after you approve some beautiful pieces!</p>
{% else %}
<div class="finalised-grid">
  {% for art in artworks %}
  <div class="final-card">
    <div class="card-thumb">
      {% if art.main_image %}
      <a href="{{ url_for('artwork.finalised_image', seo_folder=art.seo_folder, filename=art.main_image) }}" class="final-img-link" data-img="{{ url_for('artwork.finalised_image', seo_folder=art.seo_folder, filename=art.main_image) }}">
        <img src="{{ url_for('artwork.finalised_image', seo_folder=art.seo_folder, filename=art.main_image) }}" class="card-img-top" alt="{{ art.title }}">
      </a>
      {% else %}
      <img src="{{ url_for_static('static', filename='img/no-image.svg') }}" class="card-img-top" alt="No image">
      {% endif %}
    </div>
    <div class="card-details">
      <div class="file-name" title="{{ art.filename }}">{{ art.filename }}</div>
      <div class="card-title">{{ art.title }}{% if art.locked %} <span class="locked-badge" title="{{ art.lock_reason }}">Locked</span>{% endif %}</div>
      {% if art.locked %}<div class="lock-meta">Locked by {{ art.locked_by }} on {{ art.locked_at }}{% if art.lock_reason %} – {{ art.lock_reason }}{% endif %}</div>{% endif %}
      <div class="desc-snippet" title="{{ art.description }}">
        {{ art.description[:200] }}{% if art.description|length > 200 %}...{% endif %}
      </div>
      <div>SKU: {{ art.sku }}</div>
      <div>Price: {{ art.price }}</div>
      <div>Colours: {{ art.primary_colour }} / {{ art.secondary_colour }}</div>
      <div>SEO: {{ art.seo_filename }}</div>
      <div>Tags: {{ art.tags|join(', ') }}</div>
      <div>Materials: {{ art.materials|join(', ') }}</div>
      {% if art.mockups %}
      <div class="mini-mockup-grid">
        {% for m in art.mockups %}
        <img src="{{ url_for('artwork.finalised_image', seo_folder=art.seo_folder, filename=m.filename) }}" alt="mockup"/>
        {% endfor %}
      </div>
      {% endif %}
      {% if art.images %}
      <details class="img-urls">
        <summary>Image URLs</summary>
        <ul>
          {% for img in art.images %}
          <li>
            <a href="{{ url_for('artwork.finalised_image', seo_folder=art.seo_folder, filename=img.split('/')[-1]) }}" target="_blank">/{{ img }}</a>
          </li>
          {% endfor %}
        </ul>
      </details>
      {% endif %}
    </div>
  <div class="final-actions">
    {% if art.locked %}
      <a class="btn-black btn-disabled" aria-disabled="true">Edit</a>
      <form method="post" action="{{ url_for('artwork.unlock_listing', aspect=art.aspect, filename=art.filename) }}" class="lock-form" style="display:inline;">
        <input type="hidden" name="reason" value="">
        <button type="submit" class="btn-black">Unlock</button>
      </form>
      <form method="post" action="{{ url_for('artwork.delete_finalised', aspect=art.aspect, filename=art.filename) }}" class="locked-delete-form" style="display:inline;">
        <input type="hidden" name="confirm" value="">
        <button type="submit" class="btn-black btn-danger">Delete</button>
      </form>
    {% else %}
      <a href="{{ url_for('artwork.edit_listing', aspect=art.aspect, filename=art.filename) }}" class="btn-black">Edit</a>
      <form method="post" action="{{ url_for('artwork.lock_listing', aspect=art.aspect, filename=art.filename) }}" class="lock-form" style="display:inline;">
        <input type="hidden" name="reason" value="">
        <button type="submit" class="btn-black">Lock it in</button>
      </form>
      <form method="post" action="{{ url_for('artwork.delete_finalised', aspect=art.aspect, filename=art.filename) }}" onsubmit="return confirm('Delete this artwork?');" style="display:inline;">
        <button type="submit" class="btn-black btn-danger">Delete</button>
      </form>
      <form method="post" action="{{ url_for('exports.run_single_export', seo_folder=art.seo_name) }}" style="display:inline;">
        <button type="submit" class="btn-black">Export One</button>
      </form>
    {% endif %}
  </div>
  </div>
  {% endfor %}
</div>
{% endif %}
<div id="final-modal-bg" class="modal-bg">
  <button id="final-modal-close" class="modal-close" aria-label="Close modal">&times;</button>
  <div class="modal-img"><img id="final-modal-img" src="" alt="Full image"/></div>
</div>
<script>
  document.querySelectorAll('.final-img-link').forEach(link => {
    link.addEventListener('click', function(e){
      e.preventDefault();
      const modal = document.getElementById('final-modal-bg');
      const img = document.getElementById('final-modal-img');
      img.src = this.dataset.img;
      modal.style.display = 'flex';
    });
  });
  document.getElementById('final-modal-close').onclick = function(){
    document.getElementById('final-modal-bg').style.display='none';
    document.getElementById('final-modal-img').src='';
  };
  document.getElementById('final-modal-bg').onclick = function(e){
    if(e.target===this){
      this.style.display='none';
      document.getElementById('final-modal-img').src='';
    }
  };
  document.querySelectorAll('.locked-delete-form').forEach(f=>{
    f.addEventListener('submit',function(ev){
      const val=prompt('This listing is locked and will be permanently deleted. Type DELETE to confirm');
      if(val!=='DELETE'){ev.preventDefault();}
      else{this.querySelector('input[name="confirm"]').value='DELETE';}
    });
  });
  document.querySelectorAll('.lock-form').forEach(f=>{
    f.addEventListener('submit',function(ev){
      const r=prompt('Reason for lock/unlock? (optional)');
      if(r!==null) this.querySelector('input[name="reason"]').value=r;
    });
  });
  const gBtn=document.getElementById('grid-view-btn');
  const lBtn=document.getElementById('list-view-btn');
  const grid=document.querySelector('.finalised-grid');
  function apply(v){
    if(v==='list'){grid.classList.add('list-view');} else {grid.classList.remove('list-view');}
  }
  if(gBtn) gBtn.addEventListener('click',()=>{apply('grid'); localStorage.setItem('view','grid');});
  if(lBtn) lBtn.addEventListener('click',()=>{apply('list'); localStorage.setItem('view','list');});
  apply(localStorage.getItem('view')||'grid');
</script>
{% endblock %}

```

---
## 📄 `ezygallery/templates/main.html`

```html
<!DOCTYPE html>
<!-- The 'dark' class will be toggled on this html tag -->
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Ezy Gallery{% endblock %}</title>
    <!-- Favicons & Web Manifest -->
    <link rel="apple-touch-icon" sizes="180x180" href="{{ url_for('static', filename='favicons/apple-touch-icon.png') }}">
    <link rel="icon" type="image/png" sizes="32x32" href="{{ url_for('static', filename='favicons/favicon-32x32.png') }}">
    <link rel="icon" type="image/png" sizes="16x16" href="{{ url_for('static', filename='favicons/favicon-16x16.png') }}">
    <link rel="manifest" href="{{ url_for('static', filename='favicons/site.webmanifest') }}">
    <link rel="shortcut icon" href="{{ url_for('static', filename='favicons/favicon.ico') }}">
    <meta name="msapplication-TileColor" content="#ffffff">
    <meta name="theme-color" content="#ffffff">
    <!-- Android-specific -->
    <link rel="icon" type="image/png" sizes="192x192" href="{{ url_for('static', filename='favicons/android-chrome-192x192.png') }}">
    <link rel="icon" type="image/png" sizes="512x512" href="{{ url_for('static', filename='favicons/android-chrome-512x512.png') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/custom.css')}}">
</head>
<body>
    <div class="page-wrapper">
        {% include 'components/header.html' %}

        <!-- Main Content of the page -->
        <main class="main-content">
            {% block content %}{% endblock %}
        </main>

        <!-- Footer Section -->
        <footer class="site-footer">
            <div class="footer-content">
                <div class="footer-columns">
                    <div class="footer-col">
                        <h4>Ezy Gallery</h4>
                        <p>Aboriginal Australian art powered by next-gen automation &amp; heart.</p>
                    </div>
                    <div class="footer-col">
                        <h4>Links</h4>
                        <ul>
                            <li><a href="{{ url_for('artwork.home') }}">Home</a></li>
                            <li><a href="{{ url_for('artwork.upload_artwork') }}">Upload</a></li>
                            <li><a href="{{ url_for('documentation.docs_all') }}">Docs</a></li>
                            <li><a href="{{ url_for('info.contact') }}">Contact</a></li>
                            <li><a href="{{ url_for('info.privacy') }}">Privacy</a></li>
                            <li><a href="{{ url_for('info.about') }}">About</a></li>
                        </ul>
                    </div>
                    {% if session.get('user') == 'robbie' %}
                    <div class="footer-col">
                        <h4>Admin</h4>
                        <ul>
                            <li><a href="{{ url_for('admin_routes.admin_all') }}#cache-control">Cache Control</a></li>
                            <li><a href="{{ url_for('admin_routes.admin_all') }}#git-log">Git Log</a></li>
                            <li><a href="{{ url_for('admin_routes.login_disabled') }}">Auth Disabled</a></li>
                            <li><a href="{{ url_for('admin_routes.admin_all') }}#login-bypass">Login Bypass</a></li>
                        </ul>
                    </div>
                    {% endif %}
                </div>
                <div class="copyright-bar">
                    <p>© 2025 Robin Custance. All rights reserved.</p>
                </div>
            </div>
        </footer>
        {% include 'components/overlay_menu.html' %}
    </div>

    <!-- Link to the external JavaScript file -->
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>

</body>
</html>

```

---
## 📄 `ezygallery/templates/gdws_base_editor.html`

```html
{% extends "main.html" %}
{% block title %}GDWS Base Editor{% endblock %}
{% block content %}
<h1>GDWS Base Paragraph Editor</h1>
<p>This page allows editing the base text and instructions for each paragraph variation.</p>
{% endblock %}

```

---
## 📄 `ezygallery/templates/accessibility.html`

```html
{% extends "main.html" %}
{% block title %}Accessibility{% endblock %}
{% block content %}
<section class="legal-page">
  <h1>Accessibility</h1>
  <p><em>Last updated: July 25, 2019</em></p>
  <p>We are committed to making this site accessible to everyone. If you encounter any difficulty accessing content, please let us know.</p>
  <p>You can reach us at <a href="mailto:accessibility@leafgroup.com">accessibility@leafgroup.com</a>.</p>
  <h2>Accessibility Features</h2>
  <ul>
    <li>Text alternatives for non-text content</li>
    <li>Captions for videos with audio</li>
    <li>Keyboard accessibility</li>
    <li>Clear headings and labels</li>
  </ul>
  <p>This website aims to meet WCAG 2.0 Level AA guidelines.</p>
  <p>We welcome your feedback and strive to respond within 5 business days.</p>
</section>
{% endblock %}

```

---
## 📄 `ezygallery/templates/missing_endpoint.html`

```html
{# Use blueprint-prefixed endpoints like 'artwork.home' in url_for #}
{% extends "main.html" %}
{% block title %}Missing Endpoint{% endblock %}
{% block content %}
<h1>Endpoint Error</h1>
<p>{{ error }}</p>
{% endblock %}

```

---
## 📄 `ezygallery/templates/templates_components/email_templates.html`

```html
{% extends "main.html" %}

{% block title %}Email Templates | Ezy Gallery{% endblock %}

{% block content %}
<h1>Email Templates</h1>
<p>This page is currently under construction. Check back soon!</p>
{% endblock %}

```

---
## 📄 `ezygallery/templates/templates_components/listing_templates.html`

```html
{% extends "main.html" %}

{% block title %}Listing Templates | Ezy Gallery{% endblock %}

{% block content %}
<h1>Listing Templates</h1>
<p>This page is currently under construction. Check back soon!</p>
{% endblock %}

```

---
## 📄 `ezygallery/templates/management_suite/openai_guidance.html`

```html
{% extends "main.html" %}
{% block title %}OpenAI Guidance | Ezy Gallery{% endblock %}
{% block content %}
<h1>OpenAI Guidance Management</h1>
<form method="post">
  <textarea name="guidance" rows="20" style="width:100%">{{ text }}</textarea>
  <button type="submit" class="btn btn-primary">Save</button>
</form>
<h2>History</h2>
<ul>
  {% for v in versions %}
  <li><a href="{{ url_for('openai_guidance.revert', name=v) }}">{{ v }}</a></li>
  {% else %}
  <li>No previous versions</li>
  {% endfor %}
</ul>
<h2>Test Prompt</h2>
<form id="test-form">
  <textarea name="prompt" rows="4" style="width:100%" placeholder="Test prompt"></textarea>
  <button type="submit" class="btn">Send</button>
</form>
<pre id="test-result"></pre>
<script>
  document.getElementById('test-form').addEventListener('submit', async e => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const res = await fetch('{{ url_for('openai_guidance.test_prompt') }}', {method:'POST', body:fd});
    const data = await res.json();
    document.getElementById('test-result').textContent = data.result;
  });
</script>
{% endblock %}

```

---
## 📄 `ezygallery/templates/management_suite/index.html`

```html
{% extends "main.html" %}
{% block title %}Management Suite | Ezy Gallery{% endblock %}
{% block content %}
<h1>Management Suite</h1>
<p class="module-help">Central hub for all admin modules.</p>
<ul class="management-links">
  <li><a href="{{ url_for('gdws_admin.editor') }}">GDWS</a></li>
  <li><a href="{{ url_for('mockups.index') }}">Mockup Management</a></li>
  <li><a href="{{ url_for('openai_guidance.manage') }}">OpenAI Guidance</a></li>
  <li>Export Management (coming soon)</li>
  <li>Integration Settings (coming soon)</li>
</ul>
{% endblock %}

```

---
## 📄 `ezygallery/templates/auth/login.html`

```html
{% extends "main.html" %}
{% block title %}Login{% endblock %}
{% block content %}
<div class="login-container">
  <h2>Admin Login</h2>
  {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      <div class="flash">
        {% for category, msg in messages %}
          <div class="flash-{{ category|default('info') }}">{{ msg }}</div>
        {% endfor %}
      </div>
    {% endif %}
  {% endwith %}
  <form method="post" class="login-form" autocomplete="on">
    <input type="hidden" name="next" value="{{ next or '' }}">
    <label for="username">Username</label>
    <input id="username" name="username" type="text" required autocomplete="username" autofocus>
    <label for="password">Password</label>
    <div class="pw-wrap">
      <input id="password" name="password" type="password" required autocomplete="current-password">
      <button type="button" id="toggle-password"
        aria-label="Show password" tabindex="0" class="pw-toggle-btn">
        <svg id="eye-icon" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
          <ellipse cx="12" cy="12" rx="9" ry="6"></ellipse>
          <circle cx="12" cy="12" r="2.5"></circle>
        </svg>
      </button>
    </div>
    <button type="submit">Login</button>
  </form>
</div>
<!-- Styles moved to static/css/custom.css -->
<script>
  (() => {
    const pwInput = document.getElementById('password');
    const pwToggle = document.getElementById('toggle-password');
    const eyeIcon = document.getElementById('eye-icon');
    let isShown = false;

    // Open eye icon displayed when password is hidden
    const openEye = `<ellipse cx="12" cy="12" rx="9" ry="6"></ellipse>
      <circle cx="12" cy="12" r="2.5"></circle>`;

    // Crossed eye icon displayed when password is visible
    const closedEye = `<ellipse cx="12" cy="12" rx="9" ry="6"></ellipse>
      <circle cx="12" cy="12" r="2.5"></circle>
      <line x1="4" y1="20" x2="20" y2="4" stroke="currentColor" stroke-width="2"></line>`;

    function togglePassword() {
      const start = pwInput.selectionStart;
      const end = pwInput.selectionEnd;
      isShown = !isShown;
      pwInput.type = isShown ? 'text' : 'password';
      pwToggle.setAttribute('aria-label', isShown ? 'Hide password' : 'Show password');
      eyeIcon.innerHTML = isShown ? closedEye : openEye;
      pwInput.focus();
      if (start !== null && end !== null) {
        pwInput.setSelectionRange(start, end);
      }
    }

    pwToggle.addEventListener('click', togglePassword);
    pwToggle.addEventListener('keydown', e => {
      if (e.key === ' ' || e.key === 'Enter') {
        e.preventDefault();
        togglePassword();
      }
    });
  })();
</script>
{% endblock %}

```

---
## 📄 `ezygallery/templates/docs/docs_all.html`

```html
{% extends "main.html" %}
{% block title %}Documentation Index | Ezy Gallery{% endblock %}
{% block content %}
<h1>Documentation Index</h1>
<div class="docs-layout">
  <aside class="doc-sidebar">
    <ul>
      <li><a href="#home-howto">Home</a></li>
      <li><a href="#uploads-howto">Uploads</a></li>
      <li><a href="#analyze-howto">Analyze</a></li>
      <li><a href="#gallery-howto">Gallery</a></li>
      <li><a href="#exports-howto">Exports</a></li>
      <li><a href="#whisperer-howto">Prompt Whisperer</a></li>
    </ul>
  </aside>
  <div class="docs-main">

<!-- ====== [HOME] from howto_home.html ====== -->
<section id="home-howto" class="info-page">
  <h2>How to Home</h2>
  <p>This guide explains the basics of using the home module.</p>
</section>
<hr>

<!-- ====== [UPLOADS] from howto_upload.html ====== -->
<section id="uploads-howto" class="info-page">
  <h2>How to Upload</h2>
  <p>This guide explains the basics of using the upload module.</p>
</section>
<hr>

<!-- ====== [ANALYZE] from howto_analyze.html ====== -->
<section id="analyze-howto" class="info-page">
  <h2>How to Analyze</h2>
  <p>This guide explains the basics of using the analyze module.</p>
</section>
<hr>

<!-- ====== [GALLERY] from howto_gallery.html ====== -->
<section id="gallery-howto" class="info-page">
  <h2>How to Gallery</h2>
  <p>This guide explains the basics of using the gallery module.</p>
</section>
<hr>

<!-- ====== [EXPORTS] from howto_exports.html ====== -->
<section id="exports-howto" class="info-page">
  <h2>Exports Unavailable</h2>
  <p>The Sellbrite export module from Art Narrator has been removed for Ezy Gallery.</p>
</section>
<hr>

<!-- ====== [WHISPERER] from howto_whisperer.html ====== -->
<section id="whisperer-howto" class="info-page">
  <h2>How to Whisperer</h2>
  <p>This guide explains the basics of using the whisperer module.</p>
</section>
  </div>
</div>
{% endblock %}

```

---
## 📄 `ezygallery/templates/documentation/howto_analyze.html`

```html
{% extends "main.html" %}
{% block title %}How to Analyze | Ezy Gallery{% endblock %}
{% block content %}
<section class="info-page">
  <h1>How to Analyze</h1>
  <p>This guide explains the basics of using the analyze module.</p>
</section>
{% endblock %}

```

---
## 📄 `ezygallery/templates/documentation/qa_audit_index.html`

```html
{% extends "main.html" %}

{% block title %}Qa Audit Index | Ezy Gallery{% endblock %}

{% block content %}
<h1>Qa Audit Index</h1>
<p>This page is currently under construction. Check back soon!</p>
{% endblock %}

```

---
## 📄 `ezygallery/templates/documentation/sitemap.html`

```html
{% extends "main.html" %}

{% block title %}Sitemap | Ezy Gallery{% endblock %}

{% block content %}
<h1>Sitemap</h1>
<p>This page is currently under construction. Check back soon!</p>
{% endblock %}

```

---
## 📄 `ezygallery/templates/documentation/howto_upload.html`

```html
{% extends "main.html" %}
{% block title %}How to Upload | Ezy Gallery{% endblock %}
{% block content %}
<section class="info-page">
  <h1>How to Upload</h1>
  <p>This guide explains the basics of using the upload module.</p>
</section>
{% endblock %}

```

---
## 📄 `ezygallery/templates/documentation/howto_home.html`

```html
{% extends "main.html" %}
{% block title %}How to Home | Ezy Gallery{% endblock %}
{% block content %}
<section class="info-page">
  <h1>How to Home</h1>
  <p>This guide explains the basics of using the home module.</p>
</section>
{% endblock %}

```

---
## 📄 `ezygallery/templates/documentation/how_to_guides.html`

```html
{% extends "main.html" %}

{% block title %}How To Guides | Ezy Gallery{% endblock %}

{% block content %}
<section class="info-page">
  <h1>How-To Guides</h1>
  <ul class="doc-list">
    <li><a href="{{ url_for('documentation.docs_all') }}">Full Documentation Index</a></li>
    <li><a href="{{ url_for('documentation.howto_home') }}">Artwork Home</a></li>
    <li><a href="{{ url_for('documentation.howto_upload') }}">Upload</a></li>
    <li><a href="{{ url_for('documentation.howto_analyze') }}">Analyze</a></li>
    <li><a href="{{ url_for('documentation.howto_gallery') }}">Gallery</a></li>
    <li><a href="{{ url_for('documentation.howto_exports') }}">Exports (N/A)</a></li>
    <li><a href="{{ url_for('documentation.howto_whisperer') }}">Prompt Whisperer</a></li>
    <li><a href="{{ url_for('documentation.faq') }}">FAQ</a></li>
  </ul>
</section>
{% endblock %}

```

---
## 📄 `ezygallery/templates/documentation/project_readme.html`

```html
{% extends "main.html" %}

{% block title %}Project Readme | Ezy Gallery{% endblock %}

{% block content %}
<h1>Project Readme</h1>
<p>This page is currently under construction. Check back soon!</p>
{% endblock %}

```

---
## 📄 `ezygallery/templates/documentation/delete_candidates.html`

```html
{% extends "main.html" %}

{% block title %}Delete Candidates | Ezy Gallery{% endblock %}

{% block content %}
<h1>Delete Candidates</h1>
<p>This page is currently under construction. Check back soon!</p>
{% endblock %}

```

---
## 📄 `ezygallery/templates/documentation/changelog.html`

```html
{% extends "main.html" %}

{% block title %}Changelog | Ezy Gallery{% endblock %}

{% block content %}
<h1>Changelog</h1>
<p>This page is currently under construction. Check back soon!</p>
{% endblock %}

```

---
## 📄 `ezygallery/templates/documentation/task_list.html`

```html
{% extends "main.html" %}

{% block title %}Task List | Ezy Gallery{% endblock %}

{% block content %}
<h1>Task List</h1>
<p>This page is currently under construction. Check back soon!</p>
{% endblock %}

```

---
## 📄 `ezygallery/templates/documentation/faq.html`

```html
{% extends "main.html" %}

{% block title %}Faq | Ezy Gallery{% endblock %}

{% block content %}
<h1>Faq</h1>
<p>This page is currently under construction. Check back soon!</p>
{% endblock %}

```

---
## 📄 `ezygallery/templates/documentation/howto_exports.html`

```html
{% extends "main.html" %}
{% block title %}How to Exports | Ezy Gallery{% endblock %}
{% block content %}
<section class="info-page">
  <h1>Exports Unavailable</h1>
  <p>The original Art Narrator project includes a Sellbrite export feature. Ezy Gallery does not currently support exporting listings.</p>
</section>
{% endblock %}

```

---
## 📄 `ezygallery/templates/documentation/howto_whisperer.html`

```html
{% extends "main.html" %}
{% block title %}How to Whisperer | Ezy Gallery{% endblock %}
{% block content %}
<section class="info-page">
  <h1>How to Whisperer</h1>
  <p>This guide explains the basics of using the whisperer module.</p>
</section>
{% endblock %}

```

---
## 📄 `ezygallery/templates/documentation/api_reference.html`

```html
{% extends "main.html" %}

{% block title %}Api Reference | Ezy Gallery{% endblock %}

{% block content %}
<h1>Api Reference</h1>
<p>This page is currently under construction. Check back soon!</p>
{% endblock %}

```

---
## 📄 `ezygallery/templates/documentation/howto_gallery.html`

```html
{% extends "main.html" %}
{% block title %}How to Gallery | Ezy Gallery{% endblock %}
{% block content %}
<section class="info-page">
  <h1>How to Gallery</h1>
  <p>This guide explains the basics of using the gallery module.</p>
</section>
{% endblock %}

```

---
## 📄 `ezygallery/templates/exports/nembol.html`

```html
{% extends "main.html" %}

{% block title %}Nembol | Ezy Gallery{% endblock %}

{% block content %}
<h1>Nembol</h1>
<p class="module-help">
  <a href="{{ url_for('documentation.howto_exports') }}">How-To</a>
  |
  <a href="{{ url_for('documentation.docs_all') }}#exports-howto">Full Docs</a>
</p>
<p>This page is currently under construction. Check back soon!</p>
{% endblock %}

```

---
## 📄 `ezygallery/templates/components/header.html`

```html
{# =============================================================
   File: header.html
   Purpose: Site header with theme toggle and menu button
   -------------------------------------------------------------
   TABLE OF CONTENTS
   [header-html-1] Bypass banner
   [header-html-2] Primary header layout
   [header-html-3] Right-side account & theme controls
   ============================================================= #}

{% if login_bypass_enabled %}
<div class="login-bypass-banner">🟡 Login system is temporarily bypassed by admin</div>
{% endif %}
<header class="site-header">
  <div class="header-content">
    {# [header-html-2] Left logo area #}
    <div class="header-left">
      <img src="{{ url_for('static', filename='icons/svg/light/palette-light.svg') }}" alt="Palette Icon" class="header-icon">
      <a href="{{ url_for('artwork.home') }}" class="logo">Ezy Gallery</a>
    </div>
    <div class="header-center">
      <nav class="main-nav" aria-label="Primary">
        <ul class="main-nav-links">
          <li><a href="{{ url_for('artwork.upload_artwork') }}">Upload</a></li>
          <li><a href="{{ url_for('artwork.artworks') }}">Gallery</a></li>
          <li><a href="{{ url_for('artwork.finalised_gallery') }}">Finalised</a></li>
          <li><a href="{{ url_for('management.dashboard') }}">Management</a></li>
          <li><a href="{{ url_for('documentation.docs_all') }}">Docs</a></li>
        </ul>
      </nav>
      <button id="menuToggle" class="menu-toggle" aria-controls="overlayMenu" aria-expanded="false">
        <span>Menu</span>
        <img src="{{ url_for('static', filename='icons/svg/light/arrow-circle-down-light.svg') }}" alt="Open menu" class="header-icon arrow-icon">
      </button>
    </div>
    {# [header-html-3] Right account/login and theme toggle #}
    <div class="header-right">
      {% if session.get('user') %}
      <a href="{{ url_for('auth.account') }}" id="userAuthLink" class="header-icon-link" aria-label="Account">
        <img id="userIcon" src="{{ url_for('static', filename='icons/svg/light/user-circle-light.svg') }}" alt="User Icon" class="header-icon">
        <span class="sr-only">Account</span>
      </a>
      <span class="login-greeting">Hi {{ session['user'].title() }}</span>
      {% else %}
      <a href="{{ url_for('auth.login') }}" id="userAuthLink" class="header-icon-link">Login</a>
      {% endif %}
      <button id="themeToggle" class="theme-toggle-btn" aria-label="Toggle theme">
        <img id="themeIcon" src="{{ url_for('static', filename='icons/svg/light/moon-light.svg') }}" alt="Theme Toggle Icon" class="header-icon">
      </button>
    </div>
  </div>
</header>

```

---
## 📄 `ezygallery/templates/components/stage_indicator.html`

```html
{# =============================================================
   File: stage_indicator.html
   Purpose: macro to render a numbered workflow stage circle
   -------------------------------------------------------------
   TABLE OF CONTENTS
   [stage-indicator-html-1] Stage indicator macro
   ============================================================= #}

{% macro stage_indicator(number, label, active=False) %}
<div class="page-step-wrapper{% if active %} active{% endif %}">
  <div class="stage-circle">{{ number }}</div>
  <div class="stage-label">{{ label }}</div>
</div>
{% endmacro %}


```

---
## 📄 `ezygallery/templates/components/mega_menu.html`

```html
{% if session.get('user') == 'robbie' %}
<li><a href="{{ url_for('admin_routes.admin_all') }}#login-bypass">Login Bypass</a></li>
{% endif %}

```

---
## 📄 `ezygallery/templates/components/overlay_menu.html`

```html
{# =============================================================
   File: overlay_menu.html
   Purpose: Fullscreen overlay navigation menu
   -------------------------------------------------------------
   TABLE OF CONTENTS
   [ovmenu-html-1] Overlay container & close button
   [ovmenu-html-2] Menu link groups
   [ovmenu-html-3] Admin management links
   ============================================================= #}

<nav id="overlayMenu" aria-hidden="true">
  {# [ovmenu-html-1] Overlay container & close button #}
  <button id="overlayClose" class="overlay-close" aria-label="Close Menu">&times;</button>
  <div class="overlay-content">
    <div class="overlay-columns">
      {# [ovmenu-html-2] Menu link groups from menu.json #}
      {% for section, items in mega_menu.items() %}
      <div class="overlay-col">
        <h3 class="menu-header">{{ section }}</h3>
        <ul class="overlay-links">
        {% for item in items %}
          {% if item.label == 'Upgrade' and not session.get('user') %}
          {% else %}
          <li><a href="{{ item.url }}">{{ item.label }}</a></li>
          {% endif %}
        {% endfor %}
        </ul>
      </div>
      {% endfor %}

      {# [ovmenu-html-3] Extra admin tools visible only for Robbie #}
      {% if session.get('user') == 'robbie' %}
      <div class="overlay-col">
        <h3 class="menu-header">Management Suite</h3>
        <ul class="overlay-links">
          <li><a href="{{ url_for('management.dashboard') }}">Suite Home</a></li>
          <li><a href="{{ url_for('gdws_admin.editor') }}">GDWS</a></li>
          <li><a href="{{ url_for('mockups.index') }}">Mockup Management</a></li>
          <li><a href="{{ url_for('openai_guidance.manage') }}">OpenAI Guidance</a></li>
          <li><a href="{{ url_for('admin_routes.admin_all') }}#dashboard">Dashboard</a></li>
          <li><a href="{{ url_for('admin_routes.admin_all') }}#user-management">User Management</a></li>
          <li><a href="{{ url_for('admin_routes.admin_all') }}#settings">Settings</a></li>
          <li><a href="{{ url_for('admin_routes.admin_all') }}#prompt-options">Prompt Options</a></li>
          <li><a href="{{ url_for('admin_routes.admin_all') }}#security">Security</a></li>
          <li><a href="{{ url_for('admin_routes.admin_all') }}#sessions">Sessions</a></li>
          <li><a href="{{ url_for('admin_routes.admin_all') }}#cache-control">Cache Control</a></li>
          <li><a href="{{ url_for('admin_routes.admin_all') }}#git-log">Git Log</a></li>
          <li><a href="{{ url_for('admin_routes.login_disabled') }}">Auth Disabled</a></li>
          <li><a href="{{ url_for('admin_routes.admin_all') }}#login-bypass">Login Bypass</a></li>
        </ul>
      </div>
      {% endif %}
    </div>
  </div>
</nav>

```

---
## 📄 `ezygallery/templates/admin/admin_all.html`

```html
{% extends "main.html" %}
{% block title %}Admin Console | Ezy Gallery{% endblock %}
{% block content %}
<h1>Admin Console</h1>
<nav class="admin-toc">
  <ul>
    <li><a href="#dashboard">Dashboard</a></li>
    <li><a href="#security">Security</a></li>
    <li><a href="#login-bypass">Login Bypass</a></li>
    <li><a href="#cache-control">Cache Control</a></li>
    <li><a href="#prompt-options">Prompt Options</a></li>
    <li><a href="#git-log">Git Log</a></li>
    <li><a href="{{ url_for('admin_routes.view_logs') }}">Log Viewer</a></li>
    <li><a href="#sessions">Sessions</a></li>
    <li><a href="#settings">Settings</a></li>
    <li><a href="#user-management">User Management</a></li>
  </ul>
</nav>
<hr>

<!-- ====== [dashboard.html] ====== -->
<section id="dashboard">
  <h2>Admin Dashboard</h2>
  <p>Welcome, {{ session['user'] }}. This area will provide admin statistics and quick links.</p>
</section>
<hr>

<!-- ====== [security.html] ====== -->
<section id="security">
  <h2>Security Controls</h2>
  <form method="post" action="{{ url_for('admin_routes.security') }}">
    <label for="duration">Bypass Duration</label>
    <select name="duration" id="duration">
      <option value="300">5 minutes</option>
      <option value="600">10 minutes</option>
      <option value="3600">1 hour</option>
      <option value="86400">1 day</option>
    </select>
    <button type="submit" name="action" value="enable" class="btn btn-warning">Enable</button>
    <button type="submit" name="action" value="disable" class="btn btn-danger">Disable</button>
  </form>
  <p>Status: {% if remaining %}<strong>ACTIVE</strong> ({{ remaining }}){% else %}Not active{% endif %}</p>
</section>
<hr>

<!-- ====== [login_bypass.html] ====== -->
<section id="login-bypass">
  <h2>Login Bypass</h2>
  <form method="post" action="{{ url_for('admin_routes.login_bypass_panel') }}">
    {% if active %}
    <p>Status: <strong>ACTIVE</strong> ({{ remaining }})</p>
    <button type="submit" name="action" value="disable" class="btn btn-danger">Disable</button>
    {% else %}
    <p>Status: Inactive</p>
    <button type="submit" name="action" value="enable" class="btn btn-warning">Enable for 2 Hours</button>
    {% endif %}
  </form>
</section>
<hr>

<!-- ====== [cache_control.html] ====== -->
<section id="cache-control">
  <h2>Cache Control</h2>
  <form method="post" action="{{ url_for('admin_routes.cache_control') }}">
    <button type="submit" name="action" value="enable" class="btn btn-warning">Enable</button>
    <button type="submit" name="action" value="disable" class="btn btn-danger">Disable</button>
  </form>
  <p>Status: {% if cache_status %}<strong>ACTIVE</strong> ({{ cache_remaining }}){% else %}Not active{% endif %}</p>
</section>
<hr>

<!-- ====== [prompt_options.html] ====== -->
<section id="prompt-options">
  <h2>Prompt Options</h2>
  <select id="category-select"></select>
  <textarea id="options-text" rows="10" cols="50"></textarea><br>
  <button id="save-btn">Save</button>
  <div id="status"></div>
  <script>
  const categories = {{ categories|tojson }};
  const select = document.getElementById('category-select');
  const textArea = document.getElementById('options-text');
  const statusEl = document.getElementById('status');
  categories.forEach(c => {
    const opt = document.createElement('option');
    opt.value = c;
    opt.textContent = c;
    select.appendChild(opt);
  });
  function loadOptions(cat){
    fetch(`/api/prompt-options/${cat}`)
      .then(r => r.json())
      .then(d => { textArea.value = JSON.stringify(d, null, 2); });
  }
  select.addEventListener('change', () => loadOptions(select.value));
  document.getElementById('save-btn').addEventListener('click', () => {
    const data = textArea.value;
    fetch(`/admin/prompt-options/${select.value}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: data
    }).then(r => r.json()).then(d => { statusEl.textContent = d.message; });
  });
  if (categories.length) loadOptions(categories[0]);
  </script>
</section>
<hr>

<!-- ====== [git_log.html] ====== -->
<section id="git-log">
  <h2>Debug: Git Log</h2>
  <pre>
  {% for line in log_lines %}
  {{ line }}
  {% endfor %}
  </pre>
</section>
<hr>

<!-- ====== [sessions.html] ====== -->
<section id="sessions">
  <h2>Active Sessions</h2>
  <table class="session-table">
    <thead>
      <tr><th>User</th><th>Session ID</th><th>Timestamp</th><th>Action</th></tr>
    </thead>
    <tbody>
    {% for user, sessions in sessions.items() %}
      {% for s in sessions %}
      <tr>
        <td>{{ user }}</td>
        <td>{{ s.session_id[:6] }}</td>
        <td>{{ s.timestamp }}</td>
        <td>
          <form method="post" action="{{ url_for('admin_routes.active_sessions') }}" style="display:inline">
            <input type="hidden" name="username" value="{{ user }}">
            <input type="hidden" name="session_id" value="{{ s.session_id }}">
            <button type="submit" class="btn btn-danger">Revoke</button>
          </form>
        </td>
      </tr>
      {% endfor %}
    {% endfor %}
    </tbody>
  </table>
</section>
<hr>

<!-- ====== [settings.html] ====== -->
<section id="settings">
  <h2>Admin Settings</h2>
  <p>This page will allow configuration of system options.</p>
</section>
<hr>

<!-- ====== [user_management.html] ====== -->
<section id="user-management">
  <h2>User Management</h2>
  <p>This page is currently under construction. Check back soon!</p>
</section>
{% endblock %}

```

---
## 📄 `ezygallery/templates/admin/git_log.html`

```html
{% extends 'main.html' %}
{% block title %}Git Commit Log{% endblock %}
{% block content %}
<h1>Debug: Git Log</h1>
<pre>
{% for line in log_lines %}
{{ line }}
{% endfor %}
</pre>
{% endblock %}

```

---
## 📄 `ezygallery/templates/admin/login-disabled.html`

```html
{% extends 'main.html' %}
{% block title %}Login Disabled{% endblock %}
{% block content %}
<h1>Login Disabled</h1>
<p>Login functionality is currently disabled. Please contact the administrator for access.</p>
{% endblock %}

```

---
## 📄 `ezygallery/templates/admin/settings.html`

```html
{% extends "main.html" %}
{% block title %}Settings | Ezy Gallery{% endblock %}
{% block content %}
<h1>Admin Settings</h1>
<p>This page will allow configuration of system options.</p>
{% endblock %}

```

---
## 📄 `ezygallery/templates/admin/login_bypass.html`

```html
{% extends 'main.html' %}
{% block title %}Login Bypass{% endblock %}
{% block content %}
<h1>Login Bypass</h1>
<form method="post">
  {% if active %}
  <p>Status: <strong>ACTIVE</strong> ({{ remaining }})</p>
  <button type="submit" name="action" value="disable" class="btn btn-danger">Disable</button>
  {% else %}
  <p>Status: Inactive</p>
  <button type="submit" name="action" value="enable" class="btn btn-warning">Enable for 2 Hours</button>
  {% endif %}
</form>
{% endblock %}

```

---
## 📄 `ezygallery/templates/admin/prompt_options.html`

```html
{% extends 'main.html' %}
{% block title %}Prompt Options Admin{% endblock %}
{% block content %}
<h1>Prompt Options</h1>
<select id="category-select"></select>
<textarea id="options-text" rows="10" cols="50"></textarea><br>
<button id="save-btn">Save</button>
<div id="status"></div>
<script>
const categories = {{ categories|tojson }};
const select = document.getElementById('category-select');
const textArea = document.getElementById('options-text');
const statusEl = document.getElementById('status');
categories.forEach(c => {
  const opt = document.createElement('option');
  opt.value = c;
  opt.textContent = c;
  select.appendChild(opt);
});
function loadOptions(cat){
  fetch(`/api/prompt-options/${cat}`)
    .then(r => r.json())
    .then(d => { textArea.value = JSON.stringify(d, null, 2); });
}
select.addEventListener('change', () => loadOptions(select.value));
document.getElementById('save-btn').addEventListener('click', () => {
  const data = textArea.value;
  fetch(`/admin/prompt-options/${select.value}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: data
  }).then(r => r.json()).then(d => { statusEl.textContent = d.message; });
});
if (categories.length) loadOptions(categories[0]);
</script>
{% endblock %}

```

---
## 📄 `ezygallery/templates/admin/logs.html`

```html
{% extends 'main.html' %}
{% block title %}Log Viewer{% endblock %}
{% block content %}
<h1>Application Logs</h1>
<form method="get" class="log-filter-form">
  <label>Level:
    <select name="level">
      <option value="">All</option>
      {% for lv in ['INFO','WARNING','ERROR','CRITICAL'] %}
        <option value="{{ lv }}" {% if request.args.get('level')==lv %}selected{% endif %}>{{ lv }}</option>
      {% endfor %}
    </select>
  </label>
  <label>User: <input type="text" name="user" value="{{ request.args.get('user','') }}"></label>
  <button type="submit" class="btn btn-sm">Filter</button>
</form>
<table class="log-table">
  <tr><th>Time</th><th>Level</th><th>Event</th><th>Message</th><th>User</th></tr>
  {% for entry in entries %}
    <tr>
      <td>{{ entry.timestamp }}</td>
      <td>{{ entry.level }}</td>
      <td>{{ entry.event_type }}</td>
      <td>{{ entry.message }}</td>
      <td>{{ entry.user_id or '' }}</td>
    </tr>
  {% endfor %}
</table>
{% if not entries %}<p>No log entries found.</p>{% endif %}
{% endblock %}

```

---
## 📄 `ezygallery/templates/admin/dashboard.html`

```html
{% extends "main.html" %}
{% block title %}Admin Dashboard | Ezy Gallery{% endblock %}
{% block content %}
<h1>Admin Dashboard</h1>
<p>Welcome, {{ session['user'] }}. This area will provide admin statistics and quick links.</p>
{% endblock %}

```

---
## 📄 `ezygallery/templates/admin/security.html`

```html
{% extends 'main.html' %}
{% block title %}Security Controls{% endblock %}
{% block content %}
<h1>Security Controls</h1>
<form method="post">
  <label for="duration">Bypass Duration</label>
  <select name="duration" id="duration">
    <option value="300">5 minutes</option>
    <option value="600">10 minutes</option>
    <option value="3600">1 hour</option>
    <option value="86400">1 day</option>
  </select>
  <button type="submit" name="action" value="enable" class="btn btn-warning">Enable</button>
  <button type="submit" name="action" value="disable" class="btn btn-danger">Disable</button>
</form>
<p>Status: {% if remaining %}<strong>ACTIVE</strong> ({{ remaining }}){% else %}Not active{% endif %}</p>
{% endblock %}

```

---
## 📄 `ezygallery/templates/admin/sessions.html`

```html
{% extends 'main.html' %}
{% block title %}Active Sessions{% endblock %}
{% block content %}
<h1>Active Sessions</h1>
<table class="session-table">
  <thead>
    <tr><th>User</th><th>Session ID</th><th>Timestamp</th><th>Action</th></tr>
  </thead>
  <tbody>
  {% for user, sessions in sessions.items() %}
    {% for s in sessions %}
    <tr>
      <td>{{ user }}</td>
      <td>{{ s.session_id[:6] }}</td>
      <td>{{ s.timestamp }}</td>
      <td>
        <form method="post" style="display:inline">
          <input type="hidden" name="username" value="{{ user }}">
          <input type="hidden" name="session_id" value="{{ s.session_id }}">
          <button type="submit" class="btn btn-danger">Revoke</button>
        </form>
      </td>
    </tr>
    {% endfor %}
  {% endfor %}
  </tbody>
</table>
{% endblock %}

```

---
## 📄 `ezygallery/templates/admin/user_management.html`

```html
{% extends "main.html" %}

{% block title %}User Management | Ezy Gallery{% endblock %}

{% block content %}
<h1>User Management</h1>
<p>This page is currently under construction. Check back soon!</p>
{% endblock %}

```

---
## 📄 `ezygallery/templates/admin/cache_control.html`

```html
{% extends 'main.html' %}
{% block title %}Cache Control{% endblock %}
{% block content %}
<h1>Cache Control</h1>
<form method="post">
  <button type="submit" name="action" value="enable" class="btn btn-warning">Enable</button>
  <button type="submit" name="action" value="disable" class="btn btn-danger">Disable</button>
</form>
<p>Status: {% if status %}<strong>ACTIVE</strong> ({{ remaining }}){% else %}Not active{% endif %}</p>
{% endblock %}

```

---
## 📄 `ezygallery/templates/mockups/upload.html`

```html
{% extends "main.html" %}
{% block title %}Upload Mockups{% endblock %}
{% block content %}
<h2>Upload Mockups</h2>
<form method="post" enctype="multipart/form-data">
  <label for="aspect">Aspect Ratio:</label>
  <select name="aspect" id="aspect">
    {% for a in aspects %}
      <option value="{{ a }}">{{ a }}</option>
    {% endfor %}
  </select>
  <input type="file" name="images" multiple required accept="image/png">
  <button type="submit" class="btn btn-primary">Upload</button>
</form>
{% endblock %}

```

---
## 📄 `ezygallery/templates/mockups/gallery.html`

```html
{% extends "main.html" %}
{% block title %}{{ aspect }} Gallery{% endblock %}
{% block content %}
<h2>{{ aspect }} Categories</h2>
<ul class="category-list">
  {% for c in categories %}
    <li><a href="{{ url_for('mockups.category_gallery', aspect=aspect, category=c.name) }}">{{ c.name }} ({{ c.count }})</a></li>
  {% endfor %}
</ul>
{% endblock %}

```

---
## 📄 `ezygallery/templates/mockups/detail.html`

```html
{% extends "main.html" %}
{% block title %}Edit {{ meta.filename }}{% endblock %}
{% block content %}
<h2>Edit {{ meta.filename }}</h2>
<form method="post">
  <label>Category</label>
  <select name="category">
    {% for c in categories %}
      <option value="{{ c }}" {% if c==meta.category %}selected{% endif %}>{{ c }}</option>
    {% endfor %}
  </select>
  <label>Description</label>
  <textarea name="description">{{ meta.description }}</textarea>
  <button type="submit" name="action" value="save" class="btn btn-primary">Save</button>
  <button type="submit" name="action" value="delete" class="btn btn-danger" onclick="return confirm('Delete mockup?')">Delete</button>
</form>
<p><a href="{{ url_for('mockups.image', aspect=meta.aspect, category=meta.category, filename=meta.filename) }}">Download Image</a></p>
<p><a href="{{ url_for('mockups.gallery', aspect=meta.aspect) }}">Back</a></p>
{% endblock %}

```

---
## 📄 `ezygallery/templates/mockups/category_gallery.html`

```html
{% extends "main.html" %}
{% block title %}{{ category }} - {{ aspect }}{% endblock %}
{% block content %}
<h2>{{ category }} - {{ aspect }}</h2>
<div class="mockup-grid">
  {% for img in images %}
    <div class="mockup-card">
      <img src="{{ url_for('mockups.image', aspect=aspect, category=category, filename=img) }}" alt="{{ category }} mockup" class="mockup-thumb">
    </div>
  {% endfor %}
</div>
{% if not images %}<p>No mockups found.</p>{% endif %}
{% endblock %}

```

---
## 📄 `ezygallery/templates/mockups/index.html`

```html
{% extends "main.html" %}
{% block title %}Mockup Categoriser | Ezy Gallery{% endblock %}
{% block content %}
<h2>Select Aspect Ratio</h2>
<ul class="aspect-list">
  {% for a in aspects %}
    <li><a href="{{ url_for('mockups.gallery', aspect=a) }}">{{ a }}</a></li>
  {% endfor %}
</ul>
<a href="{{ url_for('mockups.upload') }}" class="btn btn-primary">Upload Mockups</a>
{% endblock %}

```

---
## 📄 `ezygallery/templates/mockups/categories.html`

```html
{% extends "main.html" %}

{% block title %}Mockups Categories | Ezy Gallery{% endblock %}

{% block content %}
<h1>Mockups Categories</h1>
<p>This page is currently under construction. Check back soon!</p>
{% endblock %}

```

---
## 📄 `ezygallery/templates/mockups/review.html`

```html
{% extends "main.html" %}

{% block title %}Mockups Review | Ezy Gallery{% endblock %}

{% block content %}
<h1>Mockups Review</h1>
<p>This page is currently under construction. Check back soon!</p>
{% endblock %}

```

---
## 📄 `ezygallery/models/upload_event.py`

```py
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



```

---
## 📄 `ezygallery/models/__init__.py`

```py
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


```

---
## 📄 `ezygallery/models/log_entry.py`

```py
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


```

---
## 📄 `ezygallery/utils/sku_assigner.py`

```py
# === [ ART Narrator: SKU Assigner ] ====================================
# File: utils/sku_assigner.py  (or wherever fits your project layout)

import json
from pathlib import Path
import threading

SKU_PREFIX = "RJC-"
SKU_DIGITS = 4  # e.g., 0122 for 122

_LOCK = threading.Lock()  # for thread/process safety

def get_next_sku(tracker_path: Path) -> str:
    """Safely increment and return the next sequential SKU."""
    print("[SKU DEBUG] Using tracker file:", tracker_path)
    with _LOCK:
        # 1. Load or create tracker file
        if tracker_path.exists():
            with open(tracker_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                last_sku = int(data.get("last_sku", 0))
        else:
            last_sku = 0

        # 2. Increment
        next_sku_num = last_sku + 1
        next_sku_str = f"{SKU_PREFIX}{next_sku_num:0{SKU_DIGITS}d}"

        # 3. Write back to tracker
        data = {"last_sku": next_sku_num}
        with open(tracker_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return next_sku_str

def peek_next_sku(tracker_path: Path) -> str:
    """Return what the next SKU would be without incrementing."""
    print("[SKU DEBUG] Peeking tracker file:", tracker_path)
    if tracker_path.exists():
        with open(tracker_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            last_sku = int(data.get("last_sku", 0))
    else:
        last_sku = 0

    next_sku_num = last_sku + 1
    next_sku_str = f"{SKU_PREFIX}{next_sku_num:0{SKU_DIGITS}d}"
    return next_sku_str


```

---
## 📄 `ezygallery/utils/openai_utils.py`

```py
"""Utility helpers for selecting the best available OpenAI model."""

from __future__ import annotations

import os
from openai import OpenAI
from config import (
    OPENAI_PRIMARY_MODEL,
    OPENAI_FALLBACK_MODEL,
    get_openai_model as config_get_openai_model,
)

# Use existing API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

_openai_client: OpenAI | None = None


def _get_client() -> OpenAI:
    """Return a cached OpenAI client."""
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAI(api_key=OPENAI_API_KEY)
    return _openai_client


def check_model_availability(model_name: str) -> bool:
    """Return True if the model can be retrieved via the API."""
    if not OPENAI_API_KEY:
        return False
    client = _get_client()
    try:
        client.models.retrieve(model_name)
        return True
    except Exception:
        return False


def get_openai_model() -> str:
    """Return the first available model from the configured fallback chain."""
    primary = OPENAI_PRIMARY_MODEL
    fallback = OPENAI_FALLBACK_MODEL

    chain = [primary]
    if fallback and fallback != primary:
        chain.append(fallback)
    if "gpt-4-turbo" not in chain:
        chain.append("gpt-4-turbo")

    for model in chain:
        if check_model_availability(model):
            return model
    # Final fallback if all checks fail
    return config_get_openai_model()

```

---
## 📄 `ezygallery/utils/ai_services.py`

```py
"""Thin wrappers around external AI service APIs."""

import os
from openai import OpenAI
from .openai_utils import get_openai_model
# import google.generativeai as genai  # Uncomment when you add the Gemini library

# --- LOAD API KEYS ---
# Make sure these are in your .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- INITIALIZE CLIENTS ---
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
# genai.configure(api_key=GEMINI_API_KEY)  # Uncomment for Gemini


def call_openai_api(prompt: str) -> str:
    """Sends a prompt to the OpenAI API and returns the rewritten text."""
    if not OPENAI_API_KEY:
        return "OpenAI API key not configured. Please set it in your .env file."
    global openai_client
    if openai_client is None:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
    try:
        model_to_use = get_openai_model()
        response = openai_client.chat.completions.create(
            model=model_to_use,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert copywriter. Rewrite the user's text based on their instruction. "
                        "Be creative and professional. Only return the rewritten text, with no extra commentary."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return f"Error from OpenAI: {e}"


def call_gemini_api(prompt: str) -> str:
    """Sends a prompt to the Gemini API and returns the rewritten text."""
    if not GEMINI_API_KEY:
        return "Gemini API key not configured. Please set it in your .env file."
    # TODO: Implement the actual Gemini API call here
    # model = genai.GenerativeModel('gemini-1.5-pro')
    # response = model.generate_content(prompt)
    # return response.text
    return f"(Gemini response for: '{prompt}')"  # Mock response


def call_ai_to_rewrite(prompt: str, provider: str) -> str:
    """Master function to call the appropriate AI provider."""
    if provider == "openai":
        return call_openai_api(prompt)
    elif provider == "gemini":
        return call_gemini_api(prompt)
    # Add logic for 'random' or 'combined' if desired
    else:
        return call_openai_api(prompt)  # Default to OpenAI

```

---
## 📄 `ezygallery/utils/db_logger.py`

```py
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


```

---
## 📄 `ezygallery/routes/prompt_ui.py`

```py
"""UI route for manual prompt generation."""

from flask import Blueprint, render_template
from routes import utils

bp = Blueprint('prompt_ui', __name__)

@bp.route('/prompt-generator')
def prompt_generator():
    """Render the simple prompt generator UI."""
    return render_template('prompt_generator.html', menu=utils.get_menu())

```

---
## 📄 `ezygallery/routes/management_routes.py`

```py
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

```

---
## 📄 `ezygallery/routes/gdws_admin_routes.py`

```py
"""Admin interface for the Guided Description Writing System (GDWS)."""

from flask import Blueprint, render_template, request, jsonify
import json
import os
import random
import re
from pathlib import Path
import shutil
from datetime import datetime

from config import BASE_DIR
from routes.utils import get_menu
from utils.ai_services import call_ai_to_rewrite  # We will create this module next

GDWS_CONTENT_PATH = BASE_DIR / "gdws_content"

bp = Blueprint("gdws_admin", __name__, url_prefix="/admin/gdws")

def slugify(text):
    """A simple function to create a filesystem-safe name."""
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '_', text)


def get_paragraph_folders(aspect: str) -> list[str]:
    """Return paragraph type folders for an aspect ratio."""
    aspect_path = GDWS_CONTENT_PATH / aspect
    if not aspect_path.exists():
        return []
    return [p.name for p in aspect_path.iterdir() if p.is_dir()]


@bp.route("/")
def editor():
    """Renders the main GDWS editor page."""
    return render_template("dws_editor.html", menu=get_menu())


@bp.route("/base-editor")
def base_editor():
    """Simple page to edit base paragraph text."""
    return render_template("gdws_base_editor.html", menu=get_menu())


@bp.route("/template/<aspect_ratio>")
def get_template_data(aspect_ratio):
    """
    Fetches a set of paragraphs for a given aspect ratio template.
    This simulates the final assembly process for preview in the editor.
    """
    # Note: In this new model, aspect ratio might just define which paragraph
    # types to load, or it might load a base template that you can edit.
    # For now, we'll load one random variation from each folder.

    all_blocks = []
    paragraph_folders = get_paragraph_folders(aspect_ratio)

    aspect_path = GDWS_CONTENT_PATH / aspect_ratio
    for folder_name in paragraph_folders:
        folder_path = aspect_path / folder_name
        variations = list(folder_path.glob("*.json"))
        if variations:
            random_variation_path = random.choice(variations)
            with open(random_variation_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data.setdefault('deletable', True)
            data.setdefault('pinned', False)
            all_blocks.append(data)

    # You can add logic here for pinned blocks etc.
    # This is a simplified example.
    return jsonify({"templateId": aspect_ratio, "blocks": all_blocks})


@bp.route("/regenerate-paragraph", methods=['POST'])
def regenerate_paragraph():
    """Handles AI regeneration for a single paragraph."""
    data = request.json
    prompt = (
        f"Instruction: \"{data.get('instructions', '')}\"\n"
        f"Base Text to refer to: \"{data.get('base_text', '')}\"\n"
        f"Current Text to rewrite: \"{data.get('current_text', '')}\""
    )

    new_text = call_ai_to_rewrite(
        prompt,
        provider=data.get('ai_provider', 'openai')
    )

    return jsonify({"new_content": new_text})


@bp.route("/save-paragraph", methods=['POST'])
def save_paragraph():
    """Saves a single paragraph variation to a JSON file."""
    data = request.json
    title = data.get('title')
    content = data.get('content')

    # The folder name is derived from the title
    folder_name = slugify(title)
    folder_path = GDWS_CONTENT_PATH / folder_name
    folder_path.mkdir(exist_ok=True)

    # Create a unique filename for this variation
    variation_id = data.get('id', f"var_{int(datetime.now().timestamp())}")
    file_path = folder_path / f"{variation_id}.json"

    save_data = {
        "id": variation_id,
        "title": title,
        "content": content,
        "version": "1.0",
        "last_updated": datetime.now().isoformat()
    }

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(save_data, f, indent=4)

    return jsonify({"status": "success", "message": f"Saved {file_path}", "new_id": variation_id})


@bp.route("/rename-paragraph-type", methods=['POST'])
def rename_paragraph_type():
    """Renames a paragraph folder when a title is changed."""
    data = request.json
    old_title = data.get('old_title')
    new_title = data.get('new_title')

    old_folder_name = slugify(old_title)
    new_folder_name = slugify(new_title)

    old_path = GDWS_CONTENT_PATH / old_folder_name
    new_path = GDWS_CONTENT_PATH / new_folder_name

    if not old_path.exists():
        return jsonify({"status": "error", "message": "Original folder not found."}), 404

    if new_path.exists():
        return jsonify({"status": "error", "message": "A paragraph type with that name already exists."}), 400

    shutil.move(str(old_path), str(new_path))

    return jsonify({"status": "success", "message": f"Renamed folder to {new_folder_name}"})


@bp.route("/save-base-paragraph", methods=['POST'])
def save_base_paragraph():
    """Save edits to the base text and instructions."""
    data = request.json
    file_path = Path(data.get('file'))
    if not file_path.is_file():
        return jsonify({"status": "error", "message": "File not found"}), 404
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            existing = json.load(f)
    except Exception:
        existing = {}
    existing.update({
        "base_text": data.get('base_text', existing.get('base_text', '')),
        "base_instructions": data.get('base_instructions', existing.get('base_instructions', '')),
    })
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(existing, f, indent=2)
    return jsonify({"status": "success"})


@bp.route('/email-templates')
def email_templates():
    """Placeholder page for email templates."""
    return render_template('templates_components/email_templates.html', menu=get_menu())


@bp.route('/listing-templates')
def listing_templates():
    """Placeholder page for listing templates."""
    return render_template('templates_components/listing_templates.html', menu=get_menu())

```

---
## 📄 `ezygallery/routes/prompt_whisperer.py`

```py
"""Blueprint for AI Image Prompt Whisperer."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from flask import Blueprint, render_template, request, jsonify, session
from openai import OpenAI

bp = Blueprint("whisperer", __name__, url_prefix="/prompt-whisperer")

DATA_DIR = Path("descriptions")
PROMPT_SAVE_DIR = Path("prompts")
CATEGORY_FILE = Path("static/data/art_categories.json")

client = OpenAI()

SENTIMENTS = [
    "Joyful",
    "Melancholic",
    "Mystical",
    "Peaceful",
    "Dynamic",
    "Playful",
    "Majestic",
    "Uplifting",
    "Ethereal",
    "Dramatic",
]


def load_categories() -> list[str]:
    """Load list of art categories from disk."""
    try:
        with open(CATEGORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


@bp.route("/")
def index() -> str:
    """Render the main Prompt Whisperer page."""
    last_prompt = session.get("last_prompt", "")
    cats = load_categories()
    return render_template(
        "prompt_whisperer.html",
        prompt=last_prompt,
        categories=cats,
        sentiments=SENTIMENTS,
    )


@bp.post("/generate")
def generate() -> "json":
    """Generate a new prompt using OpenAI."""
    data = request.get_json() or {}
    instructions = data.get("instructions", "")
    word_count = int(data.get("word_count", 40))
    category = data.get("category", "")
    randomness = int(data.get("randomness", 40))
    sentiment = data.get("sentiment", "Mystical")

    try:
        with open(DATA_DIR / "artworks.json", "r", encoding="utf-8") as f:
            trending = json.load(f)
    except Exception:
        trending = []
    trending_desc = "; ".join(a.get("description", "") for a in trending[:3])

    sys_msg = (
        "You are an AI prompt whisperer helping artists craft unique image prompts."
    )
    user_msg = (
        f"Create a {word_count}-word prompt in a {sentiment.lower()} tone. "
        f"Category suggestion: {category}. "
        f"Trending inspirations: {trending_desc}. "
        f"{instructions}"
    )
    temp = max(0.0, min(1.0, randomness / 100))
    try:
        resp = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": user_msg}],
            max_tokens=word_count * 2,
            temperature=temp,
        )
        prompt = resp.choices[0].message.content.strip()
    except Exception as exc:  # pragma: no cover - network failure
        prompt = f"Error generating prompt: {exc}"

    session["last_prompt"] = prompt
    return jsonify({"prompt": prompt, "category": category})


@bp.post("/save")
def save_prompt() -> "json":
    """Persist a generated prompt for later reference."""
    data = request.get_json() or {}
    prompt = data.get("prompt", "")
    category = data.get("category", "Uncategorised")
    info = {
        "prompt": prompt,
        "instructions": data.get("instructions", ""),
        "word_count": int(data.get("word_count", 0)),
        "randomness": int(data.get("randomness", 0)),
        "sentiment": data.get("sentiment", ""),
        "timestamp": datetime.utcnow().isoformat(),
    }
    dest = PROMPT_SAVE_DIR / category
    dest.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    with open(dest / f"{ts}.json", "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2)
    return jsonify({"saved": True})

```

---
## 📄 `ezygallery/routes/metrics_api.py`

```py
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


```

---
## 📄 `ezygallery/routes/aigw_routes.py`

```py
"""Routes for the AI Image Generator Whisperer (AIGW) tool."""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for, flash

import config
from routes import utils

# --- SECTION: Blueprint setup ---

bp = Blueprint("aigw", __name__, url_prefix="/aigw")

OPTIONS_FILE = config.AIGW_OPTIONS_FILE
PROMPTS_DIR = config.AIGW_PROMPTS_DIR
PROMPTS_DIR.mkdir(parents=True, exist_ok=True)

# --- SECTION: Helper functions ---

def _load_options() -> dict:
    """Return selector options from JSON or defaults."""
    if OPTIONS_FILE.exists():
        try:
            with open(OPTIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "genre": [
            "Abstract",
            "Landscape",
            "Portrait",
            "Still Life",
            "Wildlife",
            "Cityscape",
            "Fantasy",
            "Surrealism",
            "Conceptual",
            "Minimalism",
        ],
        "style": [
            "Impressionism",
            "Expressionism",
            "Pop Art",
            "Realism",
            "Cubism",
            "Fauvism",
            "Art Nouveau",
            "Modernism",
            "Traditional Aboriginal Dot Art",
            "Street Art",
        ],
        "technique": [
            "Brushwork",
            "Stippling",
            "Impasto",
            "Sgraffito",
            "Crosshatching",
            "Glazing",
            "Splattering",
            "Digital Blending",
            "Spray Painting",
            "Collage",
        ],
        "medium": [
            "Oil Paint",
            "Acrylic",
            "Watercolour",
            "Ink",
            "Digital (Tablet/Procreate)",
            "Pastel",
            "Charcoal",
            "Mixed Media",
            "Gouache",
            "Spray Paint",
        ],
        "colour_palette": [
            "Earth Tones",
            "Pastels",
            "Monochrome",
            "Vibrant Rainbow",
            "Cool Blues/Greens",
            "Warm Reds/Yellows",
            "Muted Neutrals",
            "Black & White",
            "High Contrast",
            "Outback Ochres",
        ],
        "texture": [
            "Smooth",
            "Rough",
            "Matte",
            "Glossy",
            "Thick Impasto",
            "Fine Detail",
            "Weathered",
            "Layered",
            "Textured Paper/Canvas",
            "Iridescent",
        ],
        "lighting": [
            "Golden Hour",
            "Backlit",
            "Soft Ambient",
            "Dramatic Shadows",
            "Spotlit",
            "Neon Glow",
            "Overcast",
            "Studio",
            "Candlelit",
            "Moody Rim",
        ],
        "mood": [
            "Nostalgic",
            "Adventurous",
            "Mysterious",
            "Whimsical",
            "Serene",
            "Energetic",
            "Melancholic",
            "Triumphant",
            "Romantic",
            "Contemplative",
        ],
        "perspective": [
            "Bird's Eye",
            "Worm's Eye",
            "Eye-Level",
            "Dutch Angle",
            "Isometric",
            "Macro",
            "Wide Shot",
            "Close Up",
            "Tilt Shift",
            "Panoramic",
        ],
        "era": [
            "Contemporary",
            "Retro 80s",
            "Classical",
            "Future",
            "Renaissance",
            "Victorian",
            "Postmodern",
            "Ancient",
            "Roaring 20s",
            "Space Age",
        ],
        "format": [
            "4x5",
            "1x1",
            "16x9",
            "3x4",
            "4x3",
            "5x7",
            "7x5",
            "A-Series-Vertical",
            "A-Series-Horizontal",
            "Panoramic",
        ],
        "focal_point": [
            "Foreground",
            "Background",
            "Centered",
            "Off-center",
            "Left Third",
            "Right Third",
            "Symmetrical",
            "Rule of Thirds",
            "Golden Ratio",
            "Diagonal",
        ],
    }


def _save_prompt(data: dict) -> None:
    """Save prompt data to a JSON file."""
    file_path = PROMPTS_DIR / f"{data['id']}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# --- SECTION: Main editor route ---

@bp.route("/", methods=["GET", "POST"], endpoint="editor")
def editor():
    """Render the prompt builder and handle saves."""
    options = _load_options()
    if request.method == "POST":
        data = {k: request.form.get(k, "") for k in options.keys()}
        data["prompt"] = request.form.get("prompt", "")
        data["id"] = uuid.uuid4().hex
        _save_prompt(data)
        flash("Prompt saved", "success")
        return redirect(url_for("aigw.editor"))
    return render_template(
        "aigw.html", menu=utils.get_menu(), options=options
    )


```

---
## 📄 `ezygallery/routes/utils.py`

```py
"""Shared helper functions for route modules."""

import os
import json
import random
import re
import logging
import csv
import fcntl
from pathlib import Path
from typing import List, Tuple, Dict, Optional, Iterable
import datetime

from utils.sku_assigner import get_next_sku, peek_next_sku

from dotenv import load_dotenv
from flask import session
from PIL import Image
import cv2
import numpy as np

from config import (
    BASE_DIR,
    ARTWORKS_INPUT_DIR as ARTWORKS_DIR,
    ARTWORKS_PROCESSED_DIR as ARTWORK_PROCESSED_DIR,
    SELECTIONS_DIR,
    COMPOSITES_DIR,
    ARTWORKS_FINALISED_DIR as FINALISED_DIR,
    LOGS_DIR,
    MOCKUPS_CATEGORISED_DIR as MOCKUPS_DIR,
    ANALYSE_MAX_DIM,
    GENERIC_TEXTS_DIR,
    COORDS_DIR as COORDS_ROOT,
    ANALYZE_SCRIPT_PATH,
    GENERATE_SCRIPT_PATH,
    FILENAME_TEMPLATES,
    UPLOADS_TEMP_DIR,
)

# ==============================
# Paths & Configuration
# ==============================
load_dotenv()

# Etsy accepted colour values
ALLOWED_COLOURS = [
    "Beige",
    "Black",
    "Blue",
    "Bronze",
    "Brown",
    "Clear",
    "Copper",
    "Gold",
    "Grey",
    "Green",
    "Orange",
    "Pink",
    "Purple",
    "Rainbow",
    "Red",
    "Rose gold",
    "Silver",
    "White",
    "Yellow",
]

ALLOWED_COLOURS_LOWER = {c.lower(): c for c in ALLOWED_COLOURS}

Image.MAX_IMAGE_PIXELS = None
for directory in [
    ARTWORKS_DIR,
    MOCKUPS_DIR,
    ARTWORK_PROCESSED_DIR,
    SELECTIONS_DIR,
    COMPOSITES_DIR,
    FINALISED_DIR,
    LOGS_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)

# ==============================
# Utility Helpers
# ==============================

def get_categories() -> List[str]:
    """Return sorted list of mockup categories."""
    return sorted([
        f.name
        for f in MOCKUPS_DIR.iterdir()
        if f.is_dir() and f.name.lower() != "uncategorised"
    ])


def random_image(category: str) -> Optional[str]:
    """Return a random image filename for the given category."""
    cat_dir = MOCKUPS_DIR / category
    images = [f.name for f in cat_dir.glob("*.png")]
    return random.choice(images) if images else None


def init_slots() -> None:
    """Initialise mockup slot selections in the session."""
    cats = get_categories()
    session["slots"] = [{"category": c, "image": random_image(c)} for c in cats]


def compute_options(slots) -> List[List[str]]:
    """Return category options for each slot."""
    cats = get_categories()
    return [cats for _ in slots]


def get_aspect_ratios() -> List[str]:
    """Return detected aspect ratios under the mockups folder."""
    aspects: set[str] = set()
    for p in MOCKUPS_DIR.parent.iterdir():
        if not p.is_dir():
            continue
        name = p.name
        if name.endswith("-categorised"):
            aspects.add(name.replace("-categorised", ""))
        elif re.match(r"^\d+x\d+$", name):
            aspects.add(name)
    return sorted(aspects)


def get_categories_for_aspect(aspect: str) -> List[str]:
    """Return category list for a specific aspect ratio."""
    base = MOCKUPS_DIR.parent / f"{aspect}-categorised"
    if not base.exists():
        return []
    return sorted(
        [d.name for d in base.iterdir() if d.is_dir() and d.name.lower() != "uncategorised"]
    )


def log_mockup_action(action: str, user: str, info: str) -> None:
    """Append a log entry for mockup actions."""
    log_file = LOGS_DIR / "mockup_actions.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.utcnow().isoformat()
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{timestamp}\t{user}\t{action}\t{info}\n")


def relative_to_base(path: Path | str) -> str:
    """Return a path string relative to the project root."""
    return str(Path(path).resolve().relative_to(BASE_DIR))


def resize_image_for_long_edge(image: Image.Image, target_long_edge: int = 2000) -> Image.Image:
    """Resize image maintaining aspect ratio."""
    width, height = image.size
    if width > height:
        new_width = target_long_edge
        new_height = int(height * (target_long_edge / width))
    else:
        new_height = target_long_edge
        new_width = int(width * (target_long_edge / height))
    return image.resize((new_width, new_height), Image.LANCZOS)


def apply_perspective_transform(art_img: Image.Image, mockup_img: Image.Image, dst_coords: list) -> Image.Image:
    """Overlay artwork onto mockup using perspective transform."""
    w, h = art_img.size
    src_points = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    dst_points = np.float32(dst_coords)
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    art_np = np.array(art_img)
    warped = cv2.warpPerspective(art_np, matrix, (mockup_img.width, mockup_img.height))
    mask = np.any(warped > 0, axis=-1).astype(np.uint8) * 255
    mask = Image.fromarray(mask).convert("L")
    composite = Image.composite(Image.fromarray(warped), mockup_img, mask)
    return composite


def latest_composite_folder() -> Optional[str]:
    """Return the most recent composite output folder name."""
    latest_time = 0
    latest_folder = None
    for folder in ARTWORK_PROCESSED_DIR.iterdir():
        if not folder.is_dir():
            continue
        images = list(folder.glob("*-mockup-*.jpg"))
        if not images:
            continue
        recent = max(images, key=lambda p: p.stat().st_mtime)
        if recent.stat().st_mtime > latest_time:
            latest_time = recent.stat().st_mtime
            latest_folder = folder.name
    return latest_folder


def latest_analyzed_artwork() -> Optional[Dict[str, str]]:
    """Return info about the most recently analysed artwork."""
    latest_time = 0
    latest_info = None
    for folder in ARTWORK_PROCESSED_DIR.iterdir():
        if not folder.is_dir():
            continue
        listing = folder / f"{folder.name}-listing.json"
        if not listing.exists():
            continue
        t = listing.stat().st_mtime
        if t > latest_time:
            latest_time = t
            try:
                with open(listing, "r", encoding="utf-8") as f:
                    data = json.load(f)
                latest_info = {
                    "aspect": data.get("aspect_ratio"),
                    "filename": data.get("filename"),
                }
            except Exception:
                continue
    return latest_info


def clean_display_text(text: str) -> str:
    """Collapse excess whitespace/newlines in description text."""
    if not text:
        return ""
    cleaned = text.strip()
    cleaned = re.sub(r"\n{2,}", "\n\n", cleaned)
    return cleaned


def build_full_listing_text(ai_desc: str, generic_text: str) -> str:
    """Combine AI description and generic text into one string."""
    parts = [clean_display_text(ai_desc), clean_display_text(generic_text)]
    combined = "\n\n".join([p for p in parts if p])
    return clean_display_text(combined)


def slugify(text: str) -> str:
    """Return a slug suitable for filenames."""
    text = re.sub(r"[^\w\- ]+", "", text)
    text = text.strip().replace(" ", "-")
    return re.sub("-+", "-", text).lower()


def prettify_slug(slug: str) -> str:
    """Return a human friendly title from a slug or filename."""
    name = os.path.splitext(slug)[0]
    name = name.replace("-", " ").replace("_", " ")
    name = re.sub(r"\s+", " ", name)
    return name.title()


def list_processed_artworks() -> Tuple[List[Dict], set]:
    """Collect processed artworks and set of original filenames."""
    items: List[Dict] = []
    processed_names: set = set()
    for folder in ARTWORK_PROCESSED_DIR.iterdir():
        if not folder.is_dir():
            continue
        listing_path = folder / f"{folder.name}-listing.json"
        if not listing_path.exists():
            continue
        try:
            with open(listing_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue
        original_name = data.get("filename")
        if original_name:
            processed_names.add(original_name)
        items.append(
            {
                "seo_folder": folder.name,
                "filename": original_name or f"{folder.name}.jpg",
                "aspect": data.get("aspect_ratio", ""),
                "title": data.get("title") or prettify_slug(folder.name),
                "thumb": f"{folder.name}-THUMB.jpg",
            }
        )
    items.sort(key=lambda x: x["title"].lower())
    return items, processed_names


def list_ready_to_analyze(_: set) -> List[Dict]:
    """Return artworks uploaded but not yet analyzed."""
    ready: List[Dict] = []
    for qc_path in UPLOADS_TEMP_DIR.glob("*.qc.json"):
        base = qc_path.name[:-8]  # remove .qc.json
        try:
            with open(qc_path, "r", encoding="utf-8") as f:
                qc = json.load(f)
        except Exception:
            continue
        ext = qc.get("extension", "jpg")
        aspect = qc.get("aspect_ratio", "")
        title = prettify_slug(Path(qc.get("original_filename", base)).stem)
        ready.append(
            {
                "aspect": aspect,
                "filename": f"{base}.{ext}",
                "title": title,
                "thumb": f"{base}-thumb.jpg",
                "base": base,
            }
        )
    ready.sort(key=lambda x: x["title"].lower())
    return ready


def list_finalised_artworks() -> List[Dict]:
    """Return artworks that have been finalised."""
    items: List[Dict] = []
    if FINALISED_DIR.exists():
        for folder in FINALISED_DIR.iterdir():
            if not folder.is_dir():
                continue
            listing_file = folder / f"{folder.name}-listing.json"
            if not listing_file.exists():
                continue
            try:
                with open(listing_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                continue
            items.append(
                {
                    "seo_folder": folder.name,
                    "filename": data.get("filename", f"{folder.name}.jpg"),
                    "aspect": data.get("aspect_ratio", ""),
                    "title": data.get("title") or prettify_slug(folder.name),
                    "thumb": f"{folder.name}-THUMB.jpg",
                }
            )
    items.sort(key=lambda x: x["title"].lower())
    return items


def list_finalised_artworks_extended() -> List[Dict]:
    """Return detailed info for finalised artworks including locked state."""
    items: List[Dict] = []
    if FINALISED_DIR.exists():
        for folder in FINALISED_DIR.iterdir():
            if not folder.is_dir():
                continue
            listing_file = folder / f"{folder.name}-listing.json"
            if not listing_file.exists():
                continue
            try:
                with open(listing_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                continue
            items.append(
                {
                    "seo_folder": folder.name,
                    "title": data.get("title") or prettify_slug(folder.name),
                    "description": data.get("description", ""),
                    "sku": data.get("sku", ""),
                    "primary_colour": data.get("primary_colour", ""),
                    "secondary_colour": data.get("secondary_colour", ""),
                    "price": data.get("price", ""),
                    "seo_filename": data.get("seo_filename", f"{folder.name}.jpg"),
                    "tags": data.get("tags", []),
                    "materials": data.get("materials", []),
                    "aspect": data.get("aspect_ratio", ""),
                    "filename": data.get("filename", f"{folder.name}.jpg"),
                    "locked": data.get("locked", False),
                    "images": [
                        str(p)
                        for p in data.get("images", [])
                        if (BASE_DIR / p).exists()
                    ],
                }
            )
    items.sort(key=lambda x: x["title"].lower())
    return items


def find_seo_folder_from_filename(aspect: str, filename: str) -> str:
    """Return the best matching SEO folder for ``filename``.

    This searches both processed and finalised outputs and compares the given
    base name against multiple permutations found in each listing file. If
    multiple folders match, the most recently modified one is returned.
    """

    basename = Path(filename).stem.lower()
    slug_base = slugify(basename)
    candidates: list[tuple[float, str]] = []

    for base in (ARTWORK_PROCESSED_DIR, FINALISED_DIR):
        for folder in base.iterdir():
            if not folder.is_dir():
                continue
            listing_file = folder / FILENAME_TEMPLATES["listing_json"].format(seo_slug=folder.name)
            if not listing_file.exists():
                continue
            try:
                with open(listing_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                continue

            stems = {
                Path(data.get("filename", "")).stem.lower(),
                Path(data.get("seo_filename", "")).stem.lower(),
                folder.name.lower(),
                slugify(Path(data.get("filename", "")).stem),
                slugify(Path(data.get("seo_filename", "")).stem),
                slugify(folder.name),
            }

            if basename in stems or slug_base in stems:
                candidates.append((listing_file.stat().st_mtime, folder.name))

    if not candidates:
        raise FileNotFoundError(f"SEO folder not found for {filename}")

    return max(candidates, key=lambda x: x[0])[1]


def regenerate_one_mockup(seo_folder: str, slot_idx: int) -> bool:
    """Regenerate a single mockup in-place."""
    folder = ARTWORK_PROCESSED_DIR / seo_folder
    listing_file = folder / f"{seo_folder}-listing.json"
    if not listing_file.exists():
        folder = FINALISED_DIR / seo_folder
        listing_file = folder / f"{seo_folder}-listing.json"
        if not listing_file.exists():
            return False
    with open(listing_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    mockups = data.get("mockups", [])
    if slot_idx < 0 or slot_idx >= len(mockups):
        return False
    entry = mockups[slot_idx]
    if isinstance(entry, dict):
        category = entry.get("category")
    else:
        category = Path(entry).parent.name
    mockup_files = list((MOCKUPS_DIR / category).glob("*.png"))
    if not mockup_files:
        return False
    new_mockup = random.choice(mockup_files)
    aspect = data.get("aspect_ratio")
    coords_path = COORDS_ROOT / aspect / f"{new_mockup.stem}.json"
    art_path = folder / f"{seo_folder}.jpg"
    output_path = folder / f"{seo_folder}-{new_mockup.stem}.jpg"
    try:
        with open(coords_path, "r", encoding="utf-8") as cf:
            c = json.load(cf)["corners"]
        dst = [[c[0]["x"], c[0]["y"]], [c[1]["x"], c[1]["y"]], [c[3]["x"], c[3]["y"]], [c[2]["x"], c[2]["y"]]]
        art_img = Image.open(art_path).convert("RGBA")
        art_img = resize_image_for_long_edge(art_img)
        mock_img = Image.open(new_mockup).convert("RGBA")
        composite = apply_perspective_transform(art_img, mock_img, dst)
        composite.convert("RGB").save(output_path, "JPEG", quality=85)
        data.setdefault("mockups", [])[slot_idx] = {
            "category": category,
            "source": f"{category}/{new_mockup.name}",
            "composite": output_path.name,
        }
        with open(listing_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logging.error("Regenerate error: %s", e)
        return False


def swap_one_mockup(seo_folder: str, slot_idx: int, new_category: str) -> bool:
    """Swap a mockup to a new category and regenerate."""
    folder = ARTWORK_PROCESSED_DIR / seo_folder
    listing_file = folder / f"{seo_folder}-listing.json"
    if not listing_file.exists():
        folder = FINALISED_DIR / seo_folder
        listing_file = folder / f"{seo_folder}-listing.json"
        if not listing_file.exists():
            return False
    with open(listing_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    mockups = data.get("mockups", [])
    if slot_idx < 0 or slot_idx >= len(mockups):
        return False
    mockup_files = list((MOCKUPS_DIR / new_category).glob("*.png"))
    if not mockup_files:
        return False
    new_mockup = random.choice(mockup_files)
    aspect = data.get("aspect_ratio")
    coords_path = COORDS_ROOT / aspect / f"{new_mockup.stem}.json"
    art_path = folder / f"{seo_folder}.jpg"
    output_path = folder / f"{seo_folder}-{new_mockup.stem}.jpg"
    try:
        with open(coords_path, "r", encoding="utf-8") as cf:
            c = json.load(cf)["corners"]
        dst = [[c[0]["x"], c[0]["y"]], [c[1]["x"], c[1]["y"]], [c[3]["x"], c[3]["y"]], [c[2]["x"], c[2]["y"]]]
        art_img = Image.open(art_path).convert("RGBA")
        art_img = resize_image_for_long_edge(art_img)
        mock_img = Image.open(new_mockup).convert("RGBA")
        composite = apply_perspective_transform(art_img, mock_img, dst)
        composite.convert("RGB").save(output_path, "JPEG", quality=85)
        data.setdefault("mockups", [])[slot_idx] = {
            "category": new_category,
            "source": f"{new_category}/{new_mockup.name}",
            "composite": output_path.name,
        }
        with open(listing_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logging.error("Swap error: %s", e)
        return False


def get_menu() -> List[Dict[str, str | None]]:
    """Return navigation items for templates."""
    from flask import url_for

    menu = [
        {"name": "Home", "url": url_for("artwork.home")},
        {"name": "Artwork Gallery", "url": url_for("artwork.artworks")},
        {"name": "Finalised", "url": url_for("artwork.finalised_gallery")},
    ]
    if session.get("user") == os.getenv("ADMIN_USER", "robbie"):
        menu.append({"name": "Management Suite", "url": url_for("management.dashboard")})
    latest = latest_analyzed_artwork()
    if latest:
        menu.append({
            "name": "Review Latest Listing",
            "url": url_for("artwork.edit_listing", aspect=latest["aspect"], filename=latest["filename"]),
        })
    else:
        menu.append({"name": "Review Latest Listing", "url": None})
    return menu


def get_allowed_colours() -> List[str]:
    """Return the list of allowed Etsy colour values."""
    return ALLOWED_COLOURS.copy()


def infer_sku_from_filename(filename: str) -> Optional[str]:
    """Infer SKU from an SEO filename using 'RJC-XXXX' at the end."""
    m = re.search(r"RJC-([A-Za-z0-9-]+)(?:\.jpg)?$", filename or "")
    return f"RJC-{m.group(1)}" if m else None


def sync_filename_with_sku(seo_filename: str, sku: str) -> str:
    """Return SEO filename updated so the SKU matches the given value."""
    if not seo_filename:
        return seo_filename
    if not sku:
        return seo_filename
    return re.sub(r"RJC-[A-Za-z0-9-]+(?=\.jpg$)", sku, seo_filename)


def is_finalised_image(path: str | Path) -> bool:
    """Return True if the given path is within the finalised-artwork folder."""
    try:
        Path(path).resolve().relative_to(FINALISED_DIR)
        return True
    except Exception:
        return False


def parse_csv_list(text: str) -> List[str]:
    """Parse a comma-separated string into a list of trimmed values."""
    import csv

    if not text:
        return []
    reader = csv.reader([text], skipinitialspace=True)
    row = next(reader, [])
    return [item.strip() for item in row if item.strip()]


def join_csv_list(items: List[str]) -> str:
    """Join a list of strings into a comma-separated string for display."""
    return ", ".join(item.strip() for item in items if item.strip())


def listing_lock_info(listing: Path) -> tuple[bool, str | None, str | None, str | None]:
    """Return lock state and metadata for a listing JSON."""
    locked = False
    locked_by = None
    locked_at = None
    reason = None
    if listing.exists():
        try:
            with open(listing, "r", encoding="utf-8") as f:
                data = json.load(f)
            locked = bool(data.get("locked"))
            locked_by = data.get("locked_by")
            locked_at = data.get("locked_at")
            reason = data.get("lock_reason")
        except Exception:
            pass
    if (listing.parent / ".lock").exists():
        locked = True
    return locked, locked_by, locked_at, reason


def update_listing_lock(listing: Path, lock: bool, user: str, reason: str | None = None) -> None:
    """Set or clear lock details on ``listing`` and manage ``.lock`` file."""
    data = {}
    if listing.exists():
        try:
            with open(listing, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            pass
    data["locked"] = lock
    if lock:
        data["locked_by"] = user
        data["locked_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        if reason:
            data["lock_reason"] = reason
    else:
        data.pop("locked_by", None)
        data.pop("locked_at", None)
        data.pop("lock_reason", None)
    with open(listing, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    lock_file = listing.parent / ".lock"
    if lock:
        lock_file.touch(exist_ok=True)
    elif lock_file.exists():
        lock_file.unlink()


def read_generic_text(aspect: str) -> str:
    """Return the generic text block for the given aspect ratio."""
    path = GENERIC_TEXTS_DIR / f"{aspect}.txt"
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        logging.warning("Generic text for %s not found", aspect)
        return ""


def clean_terms(items: List[str]) -> Tuple[List[str], List[str]]:
    """Clean list entries by stripping invalid characters and hyphens."""
    cleaned: List[str] = []
    changed = False
    for item in items:
        new = re.sub(r"[^A-Za-z0-9 ,]", "", item)
        new = new.replace("-", "")
        new = re.sub(r"\s+", " ", new).strip()
        cleaned.append(new)
        if new != item.strip():
            changed = True
    return cleaned, cleaned if changed else []


def resolve_listing_paths(aspect: str, filename: str) -> Tuple[str, Path, Path, bool]:
    """Return the folder and listing path for an artwork.

    Searches both processed and finalised directories using
    :func:`find_seo_folder_from_filename` and returns a tuple of
    ``(seo_folder, folder_path, listing_path, finalised)``.
    Raises ``FileNotFoundError`` if nothing matches.
    """

    seo_folder = find_seo_folder_from_filename(aspect, filename)
    processed_dir = ARTWORK_PROCESSED_DIR / seo_folder
    final_dir = FINALISED_DIR / seo_folder

    listing = processed_dir / f"{seo_folder}-listing.json"
    if listing.exists():
        return seo_folder, processed_dir, listing, False

    listing = final_dir / f"{seo_folder}-listing.json"
    if listing.exists():
        return seo_folder, final_dir, listing, True

    raise FileNotFoundError(f"Listing file for {filename} not found")


def find_aspect_filename_from_seo_folder(seo_folder: str) -> Optional[Tuple[str, str]]:
    """Return the aspect ratio and main filename for a given SEO folder.

    The lookup checks both processed and finalised folders. Information is
    primarily loaded from the listing JSON, but if fields are missing the
    filename is inferred from disk contents. Filenames are normalised to use a
    ``.jpg`` extension and to match the actual casing on disk when possible.
    """

    for base in (ARTWORK_PROCESSED_DIR, FINALISED_DIR):
        folder = base / seo_folder
        listing = folder / f"{seo_folder}-listing.json"
        aspect = ""
        filename = ""

        if listing.exists():
            try:
                with open(listing, "r", encoding="utf-8") as lf:
                    data = json.load(lf)
                aspect = data.get("aspect_ratio") or data.get("aspect") or ""
                filename = (
                    data.get("seo_filename")
                    or data.get("filename")
                    or data.get("seo_name")
                    or ""
                )
                if not filename:
                    for key in ("main_jpg_path", "orig_jpg_path", "thumb_jpg_path"):
                        val = data.get(key)
                        if val:
                            filename = Path(val).name
                            break
            except Exception as e:  # noqa: BLE001
                logging.error("Failed reading listing for %s: %s", seo_folder, e)

        if folder.exists() and not filename:
            # Look for an image whose stem matches the folder name
            for p in folder.iterdir():
                if p.suffix.lower() in {".jpg", ".jpeg", ".png"} and p.stem.lower() == seo_folder.lower():
                    filename = p.name
                    break

        if filename:
            if not filename.lower().endswith(".jpg"):
                filename = f"{Path(filename).stem}.jpg"
            # Normalise casing to match actual disk file
            disk_file = folder / filename
            if not disk_file.exists():
                stem = Path(filename).stem.lower()
                for p in folder.iterdir():
                    if p.suffix.lower() in {".jpg", ".jpeg", ".png"} and p.stem.lower() == stem:
                        filename = p.name
                        break
            return aspect, filename

    return None


def assign_or_get_sku(
    listing_json_path: Path, tracker_path: Path, *, force: bool = False
) -> str:
    """Return existing SKU or assign the next sequential one.

    Parameters
    ----------
    listing_json_path:
        Path to the ``*-listing.json`` file.
    tracker_path:
        Path to ``sku_tracker.json`` storing ``last_sku``.
    force:
        If ``True`` always allocate a new SKU even if one exists.
    """
    listing_json_path = Path(listing_json_path)
    tracker_path = Path(tracker_path)

    logger = logging.getLogger(__name__)

    if not listing_json_path.exists():
        raise FileNotFoundError(listing_json_path)

    try:
        with open(listing_json_path, "r", encoding="utf-8") as lf:
            data = json.load(lf)
    except Exception as exc:  # pragma: no cover - unexpected IO
        logger.error("Failed reading %s: %s", listing_json_path, exc)
        raise

    existing = str(data.get("sku") or "").strip()
    seo_field = str(data.get("seo_filename") or "").strip()
    if existing and not force:
        new_seo = sync_filename_with_sku(seo_field, existing)
        if new_seo != seo_field:
            data["seo_filename"] = new_seo
            try:
                with open(listing_json_path, "w", encoding="utf-8") as lf:
                    json.dump(data, lf, indent=2, ensure_ascii=False)
            except Exception as exc:  # pragma: no cover - unexpected IO
                logger.error("Failed writing SEO filename to %s: %s", listing_json_path, exc)
                raise
        return existing

    # Allocate the next SKU using the central assigner
    sku = get_next_sku(tracker_path)
    data["sku"] = sku
    if seo_field:
        data["seo_filename"] = sync_filename_with_sku(seo_field, sku)
    try:
        with open(listing_json_path, "w", encoding="utf-8") as lf:
            json.dump(data, lf, indent=2, ensure_ascii=False)
    except Exception as exc:  # pragma: no cover - unexpected IO
        logger.error("Failed writing SKU %s to %s: %s", sku, listing_json_path, exc)
        raise

    logger.info("Assigned SKU %s to %s", sku, listing_json_path.name)
    return sku


def assign_sequential_sku(listing_json_path: Path, tracker_path: Path) -> str:
    """Backward compatible wrapper for ``assign_or_get_sku``."""
    return assign_or_get_sku(listing_json_path, tracker_path)


def validate_all_skus(listings: Iterable[Dict], tracker_path: Path) -> list[str]:
    """Return a list of SKU validation errors for the given listings."""
    tracker_last = 0
    try:
        with open(tracker_path, "r", encoding="utf-8") as tf:
            tracker_last = int(json.load(tf).get("last_sku", 0))
    except Exception:
        pass

    errors: list[str] = []
    seen: dict[int, int] = {}
    nums: list[int] = []

    for idx, data in enumerate(listings):
        sku = str(data.get("sku") or "")
        m = re.fullmatch(r"RJC-(\d{4})", sku)
        if not m:
            errors.append(f"Listing {idx}: invalid or missing SKU")
            continue
        num = int(m.group(1))
        if num in seen:
            errors.append(f"Duplicate SKU {sku} in listings {seen[num]} and {idx}")
        seen[num] = idx
        nums.append(num)

    if nums:
        nums.sort()
        for a, b in zip(nums, nums[1:]):
            if b != a + 1:
                errors.append(f"Gap or out-of-sequence SKU between {a:04d} and {b:04d}")
                break
        if nums[-1] > tracker_last:
            errors.append("Tracker last_sku behind recorded SKUs")

    return errors


```

---
## 📄 `ezygallery/routes/legal_routes.py`

```py
"""General informational pages: Privacy Policy, Terms, About, Contact."""

from __future__ import annotations

from flask import Blueprint, render_template

bp = Blueprint("info", __name__)


@bp.route("/privacy")
def privacy() -> str:
    """Display the Privacy Policy page."""
    return render_template("privacy.html")


@bp.route("/terms")
def terms() -> str:
    """Display the Terms & Limitations page."""
    return render_template("terms.html")


@bp.route("/about")
def about() -> str:
    """Display the About page."""
    return render_template("about.html")


@bp.route("/accessibility")
def accessibility() -> str:
    """Display the Accessibility page."""
    return render_template("accessibility.html")


@bp.route("/upgrade")
def upgrade() -> str:
    """Display the Upgrade to Premium page."""
    return render_template("upgrade.html")


@bp.route("/contact")
def contact() -> str:
    """Display the Contact page."""
    return render_template("contact.html")

```

---
## 📄 `ezygallery/routes/session_tracker.py`

```py
"""Utilities for tracking and limiting active user sessions."""

from __future__ import annotations

import json
import threading
import datetime
from pathlib import Path
import contextlib
import fcntl

from config import LOGS_DIR

REGISTRY_FILE = LOGS_DIR / "session_registry.json"
_LOCK = threading.Lock()


def _load_registry() -> dict:
    """Load the session registry JSON file."""
    if not REGISTRY_FILE.exists():
        return {}
    try:
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            with contextlib.suppress(OSError):
                fcntl.flock(f, fcntl.LOCK_SH)
            data = json.load(f)
    except Exception:
        REGISTRY_FILE.unlink(missing_ok=True)
        return {}
    return data


def _save_registry(data: dict) -> None:
    """Safely write the session registry back to disk."""
    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = REGISTRY_FILE.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    tmp.replace(REGISTRY_FILE)


def register_session(username: str, session_id: str) -> bool:
    """Register a session ID for the given user. Return False if limit reached."""
    with _LOCK:
        data = _load_registry()
        sessions = data.get(username, [])
        if len(sessions) >= 5:
            return False
        sessions.append({
            "session_id": session_id,
            "timestamp": datetime.datetime.utcnow().isoformat()
        })
        data[username] = sessions
        _save_registry(data)
    return True


def remove_session(username: str, session_id: str) -> None:
    """Remove a session entry for ``username``."""
    with _LOCK:
        data = _load_registry()
        if username in data:
            data[username] = [s for s in data[username] if s.get("session_id") != session_id]
            if not data[username]:
                data.pop(username, None)
            _save_registry(data)


def all_sessions() -> dict:
    """Return the entire session registry."""
    with _LOCK:
        return _load_registry()


def is_active(username: str, session_id: str) -> bool:
    """Check if the given session ID is active for ``username``."""
    data = all_sessions()
    return any(s.get("session_id") == session_id for s in data.get(username, []))

```

---
## 📄 `ezygallery/routes/prompt_options.py`

```py

"""API endpoints for retrieving AI prompt option values."""

from __future__ import annotations

import json
from pathlib import Path
from flask import Blueprint, jsonify, abort

OPTIONS_DIR = Path('config/ai_prompt_options')

bp = Blueprint('prompt_options', __name__, url_prefix='/api')

@bp.route('/prompt-options/<category>')
def get_prompt_options(category: str):
    """Return JSON list of prompt options for the given category."""
    file = OPTIONS_DIR / f'{category}.json'
    if file.is_file():
        with open(file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except Exception:
                data = []
        return jsonify(data)
    return jsonify([])


```

---
## 📄 `ezygallery/routes/artwork_routes.py`

```py
"""Artwork-related Flask routes.

This module powers the full listing workflow from initial review to
finalisation. It handles validation, moving files, regenerating image link
lists and serving gallery pages for processed and finalised artworks.
"""

from __future__ import annotations

import json
import subprocess
import uuid
import random
from pathlib import Path
import shutil
import os
import datetime
import logging
from config import (
    ARTWORKS_PROCESSED_DIR,
    ARTWORKS_FINALISED_DIR,
    BASE_DIR,
    ANALYSIS_STATUS_FILE,
)
import config

from PIL import Image
import io
import scripts.analyze_artwork as aa
from models import db, UploadEvent

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    send_from_directory,
    Response,
)
import re

from . import utils
from .utils import (
    ALLOWED_COLOURS_LOWER,
    relative_to_base,
    FINALISED_DIR,
    parse_csv_list,
    join_csv_list,
    read_generic_text,
    clean_terms,
    infer_sku_from_filename,
    sync_filename_with_sku,
    is_finalised_image,
    get_allowed_colours,
)

bp = Blueprint("artwork", __name__)


# --- SECTION: Helper Functions ---


def _write_analysis_status(step: str, percent: int, file: str | None = None) -> None:
    """Write simple progress info for frontend polling."""
    try:
        ANALYSIS_STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
        ANALYSIS_STATUS_FILE.write_text(
            json.dumps({"step": step, "percent": percent, "file": file})
        )
    except Exception:
        pass


@bp.route("/status/analyze")
def analysis_status():
    """Return JSON progress info for the current analysis job."""
    if ANALYSIS_STATUS_FILE.exists():
        data = json.loads(ANALYSIS_STATUS_FILE.read_text())
    else:
        data = {"step": "idle", "percent": 0}
    return Response(json.dumps(data), mimetype="application/json")


def validate_listing_fields(data: dict, generic_text: str) -> list[str]:
    """Return a list of validation error messages for the listing."""
    errors: list[str] = []

    title = data.get("title", "").strip()
    if not title:
        errors.append("Title cannot be blank")
    if len(title) > 140:
        errors.append("Title exceeds 140 characters")

    tags = data.get("tags", [])
    if len(tags) > 13:
        errors.append("Too many tags (max 13)")
    seen = set()
    for t in tags:
        if not t or len(t) > 20:
            errors.append(f"Invalid tag: '{t}'")
        if "-" in t or "," in t:
            errors.append(f"Tag may not contain hyphens or commas: '{t}'")
        if not re.fullmatch(r"[A-Za-z0-9 ]+", t):
            errors.append(f"Tag has invalid characters: '{t}'")
        low = t.lower()
        if low in seen:
            errors.append(f"Duplicate tag: '{t}'")
        seen.add(low)

    materials = data.get("materials", [])
    if len(materials) > 13:
        errors.append("Too many materials (max 13)")
    seen_mats = set()
    for m in materials:
        if len(m) > 45:
            errors.append(f"Material too long: '{m}'")
        if not re.fullmatch(r"[A-Za-z0-9 ,]+", m):
            errors.append(f"Material has invalid characters: '{m}'")
        ml = m.lower()
        if ml in seen_mats:
            errors.append(f"Duplicate material: '{m}'")
        seen_mats.add(ml)

    seo_filename = data.get("seo_filename", "")
    if len(seo_filename) > 70:
        errors.append("SEO filename exceeds 70 characters")
    if " " in seo_filename or not re.fullmatch(r"[A-Za-z0-9.-]+", seo_filename):
        errors.append("SEO filename has invalid characters or spaces")
    if not re.search(
        r"Artwork-by-Robin-Custance-RJC-[A-Za-z0-9-]+\.jpg$", seo_filename
    ):
        errors.append(
            "SEO filename must end with 'Artwork-by-Robin-Custance-RJC-XXXX.jpg'"
        )

    sku = data.get("sku", "")
    if not sku:
        errors.append("SKU is required")
    if len(sku) > 32 or not re.fullmatch(r"[A-Za-z0-9-]+", sku):
        errors.append("SKU must be <=32 chars and alphanumeric/hyphen")
    if sku and not sku.startswith("RJC-"):
        errors.append("SKU must start with 'RJC-'")
    if sku and infer_sku_from_filename(seo_filename or "") != sku:
        errors.append("SKU must match value in SEO filename")

    try:
        price = float(data.get("price"))
        if abs(price - 17.88) > 1e-2:
            errors.append("Price must be 17.88")
    except Exception:
        errors.append("Price must be a number (17.88)")

    for colour_key in ("primary_colour", "secondary_colour"):
        col = data.get(colour_key, "").strip()
        if not col:
            errors.append(f"{colour_key.replace('_', ' ').title()} is required")
            continue
        if col.lower() not in ALLOWED_COLOURS_LOWER:
            errors.append(f"{colour_key.replace('_', ' ').title()} invalid")

    images = [i.strip() for i in data.get("images", []) if str(i).strip()]
    if not images:
        errors.append("At least one image required")
    for img in images:
        if " " in img or not re.search(r"\.(jpg|jpeg|png)$", img, re.I):
            errors.append(f"Invalid image filename: '{img}'")
        if not is_finalised_image(img):
            errors.append(f"Image not in finalised-artwork folder: '{img}'")

    desc = data.get("description", "").strip()
    if len(desc.split()) < 400:
        errors.append("Description must be at least 400 words")
    GENERIC_MARKER = "About the Artist – Robin Custance"
    if generic_text:
        # Normalise whitespace for both description and generic block
        desc_norm = " ".join(desc.split()).lower()
        generic_norm = " ".join(generic_text.split()).lower()
        # Only require that the generic marker exists somewhere in the description (case-insensitive)
        if GENERIC_MARKER.lower() not in desc_norm:
            errors.append(
                f"Description must include the correct generic context block: {GENERIC_MARKER}"
            )
        if "<" in desc or ">" in desc:
            errors.append("Description may not contain HTML")

        return errors


# --- SECTION: Basic Views ---
@bp.app_context_processor
def inject_latest_artwork():
    """Inject info about the most recently analysed artwork into templates."""
    latest = utils.latest_analyzed_artwork()
    return dict(latest_artwork=latest)


@bp.route("/")
def home():
    """Homepage showing the most recently analysed artwork."""
    latest = utils.latest_analyzed_artwork()
    return render_template("index.html", menu=utils.get_menu(), latest_artwork=latest)


@bp.route("/upload", methods=["GET", "POST"])
def upload_artwork():
    """Upload new artwork files and run pre-QC then AI analysis."""
    if request.method == "POST":
        files = request.files.getlist("images")
        results = []
        for f in files:
            res = _process_upload_file(f)
            results.append(res)

        if (
            request.accept_mimetypes.accept_json
            and not request.accept_mimetypes.accept_html
        ):
            return json.dumps(results), 200, {"Content-Type": "application/json"}

        successes = [r for r in results if r["success"]]
        if successes:
            flash(f"Uploaded {len(successes)} file(s) successfully", "success")
        failures = [r for r in results if not r["success"]]
        for f in failures:
            flash(f"{f['original']}: {f['error']}", "danger")

        if request.accept_mimetypes.accept_html:
            return redirect(url_for("artwork.artworks"))
        return json.dumps(results), 200, {"Content-Type": "application/json"}
    return render_template("upload.html", menu=utils.get_menu())


@bp.route("/artworks")
def artworks():
    """List artworks in various processing states."""
    processed, processed_names = utils.list_processed_artworks()
    ready = utils.list_ready_to_analyze(processed_names)
    finalised = utils.list_finalised_artworks()
    return render_template(
        "artworks.html",
        ready_artworks=ready,
        processed_artworks=processed,
        finalised_artworks=finalised,
        menu=utils.get_menu(),
    )


# --- SECTION: Mockup Selection ---
@bp.route("/select", methods=["GET", "POST"])
def select():
    """Display and manage mockup slot selections."""
    if "slots" not in session or request.args.get("reset") == "1":
        utils.init_slots()
    slots = session["slots"]
    options = utils.compute_options(slots)
    zipped = list(zip(slots, options))
    return render_template("mockup_selector.html", zipped=zipped, menu=utils.get_menu())


@bp.route("/regenerate", methods=["POST"])
def regenerate():
    """Regenerate a random mockup image for a slot."""
    slot_idx = int(request.form["slot"])
    slots = session.get("slots", [])
    if 0 <= slot_idx < len(slots):
        cat = slots[slot_idx]["category"]
        slots[slot_idx]["image"] = utils.random_image(cat)
        session["slots"] = slots
    return redirect(url_for("artwork.select"))


@bp.route("/swap", methods=["POST"])
def swap():
    """Swap a slot to a new category and random image."""
    slot_idx = int(request.form["slot"])
    new_cat = request.form["new_category"]
    slots = session.get("slots", [])
    if 0 <= slot_idx < len(slots):
        slots[slot_idx]["category"] = new_cat
        slots[slot_idx]["image"] = utils.random_image(new_cat)
        session["slots"] = slots
    return redirect(url_for("artwork.select"))


@bp.route("/proceed", methods=["POST"])
def proceed():
    """Persist selected mockups and invoke composite generation."""
    slots = session.get("slots", [])
    if not slots:
        flash("No mockups selected!", "danger")
        return redirect(url_for("artwork.select"))
    utils.SELECTIONS_DIR.mkdir(parents=True, exist_ok=True)
    selection_id = str(uuid.uuid4())
    selection_file = utils.SELECTIONS_DIR / f"{selection_id}.json"
    with open(selection_file, "w") as f:
        json.dump(slots, f, indent=2)
    log_file = utils.LOGS_DIR / f"composites_{selection_id}.log"
    try:
        result = subprocess.run(
            ["python3", str(utils.GENERATE_SCRIPT_PATH), str(selection_file)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=utils.BASE_DIR,
        )
        with open(log_file, "w") as log:
            log.write("=== STDOUT ===\n")
            log.write(result.stdout)
            log.write("\n\n=== STDERR ===\n")
            log.write(result.stderr)
        if result.returncode == 0:
            flash("Composites generated successfully!", "success")
        else:
            flash("Composite generation failed. See logs for details.", "danger")
    except Exception as e:
        with open(log_file, "a") as log:
            log.write(f"\n\n=== Exception ===\n{str(e)}")
        flash("Error running the composite generator.", "danger")

    latest = utils.latest_composite_folder()
    if latest:
        session["latest_seo_folder"] = latest
        return redirect(url_for("artwork.composites_specific", seo_folder=latest))
    return redirect(url_for("artwork.composites_preview"))


# --- SECTION: Artwork Analysis ---


@bp.route("/analyze/<aspect>/<filename>", methods=["POST"], endpoint="analyze_artwork")
def analyze_artwork_route(aspect, filename):
    """Run the AI analysis pipeline for a stored artwork."""
    artwork_path = utils.ARTWORKS_DIR / aspect / filename
    _write_analysis_status("starting", 0, filename)
    if not artwork_path.exists():
        try:
            fallback_folder = utils.find_seo_folder_from_filename(aspect, filename)
            for base in (utils.ARTWORK_PROCESSED_DIR, utils.FINALISED_DIR):
                candidate = base / fallback_folder / f"{fallback_folder}.jpg"
                if candidate.exists():
                    artwork_path = candidate
                    break
        except FileNotFoundError:
            pass
    log_id = str(uuid.uuid4())
    log_file = utils.LOGS_DIR / f"analyze_{log_id}.log"
    try:
        cmd = ["python3", str(utils.ANALYZE_SCRIPT_PATH), str(artwork_path)]
        _write_analysis_status("openai_call", 20, filename)
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300,
        )
        with open(log_file, "w") as log:
            log.write("=== STDOUT ===\n")
            log.write(result.stdout)
            log.write("\n\n=== STDERR ===\n")
            log.write(result.stderr)
        if result.returncode != 0:
            flash(
                f"❌ Analysis failed for {filename}: {result.stderr}",
                "danger",
            )
            _write_analysis_status("failed", 100, filename)
    except Exception as e:
        with open(log_file, "a") as log:
            log.write(f"\n\n=== Exception ===\n{str(e)}")
        flash(f"❌ Error running analysis: {str(e)}", "danger")
        _write_analysis_status("failed", 100, filename)

    try:
        seo_folder = utils.find_seo_folder_from_filename(aspect, filename)
    except FileNotFoundError:
        flash(
            f"Analysis complete, but no SEO folder/listing found for {filename} ({aspect}).",
            "warning",
        )
        return redirect(url_for("artwork.artworks"))

    listing_path = (
        utils.ARTWORK_PROCESSED_DIR
        / seo_folder
        / config.FILENAME_TEMPLATES["listing_json"].format(seo_slug=seo_folder)
    )
    locked, _, _, _ = utils.listing_lock_info(listing_path)
    if locked:
        flash("Artwork is locked", "danger")
        logging.getLogger(__name__).warning(
            "Blocked by lock %s", seo_folder, extra={"event_type": "lock"}
        )
        return redirect(
            url_for("artwork.edit_listing", aspect=aspect, filename=filename)
        )
    new_filename = f"{seo_folder}.jpg"
    try:
        with open(listing_path, "r", encoding="utf-8") as lf:
            listing_data = json.load(lf)
            new_filename = listing_data.get("seo_filename", new_filename)
    except Exception:
        pass

    try:
        cmd = ["python3", str(utils.GENERATE_SCRIPT_PATH), seo_folder]
        _write_analysis_status("generating", 60, filename)
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=utils.BASE_DIR,
            timeout=600,
        )
        composite_log_file = utils.LOGS_DIR / f"composite_gen_{log_id}.log"
        with open(composite_log_file, "w") as log:
            log.write("=== STDOUT ===\n")
            log.write(result.stdout)
            log.write("\n\n=== STDERR ===\n")
            log.write(result.stderr)
        if result.returncode != 0:
            flash("Artwork analyzed, but mockup generation failed. See logs.", "danger")
    except Exception as e:
        flash(f"Composites generation error: {e}", "danger")

    _write_analysis_status("done", 100, filename)
    return redirect(
        url_for("artwork.edit_listing", aspect=aspect, filename=new_filename)
    )


@bp.post("/analyze-upload/<base>")
def analyze_upload(base):
    """Analyze an uploaded image from the temporary folder."""
    logger = logging.getLogger(__name__)
    qc_path = config.UPLOADS_TEMP_DIR / f"{base}.qc.json"
    if not qc_path.exists():
        flash("Artwork not found", "danger")
        return redirect(url_for("artwork.artworks"))
    try:
        with open(qc_path, "r", encoding="utf-8") as f:
            qc = json.load(f)
    except Exception:
        flash("Invalid QC data", "danger")
        return redirect(url_for("artwork.artworks"))

    ext = qc.get("extension", "jpg")
    orig_path = config.UPLOADS_TEMP_DIR / f"{base}.{ext}"
    processed_root = ARTWORKS_PROCESSED_DIR
    log_id = uuid.uuid4().hex
    log_file = utils.LOGS_DIR / f"analyze_{log_id}.log"
    _write_analysis_status("starting", 0, orig_path.name)
    logger.info("Analysis start %s", base, extra={"event_type": "analysis"})
    event = (
        UploadEvent.query.filter_by(upload_id=base)
        .order_by(UploadEvent.id.desc())
        .first()
    )
    if event:
        event.analysis_start_time = datetime.datetime.utcnow()
        event.status = "started"
        db.session.commit()

    try:
        cmd = ["python3", str(utils.ANALYZE_SCRIPT_PATH), str(orig_path)]
        _write_analysis_status("openai_call", 20, orig_path.name)
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=300
        )
        with open(log_file, "w") as log:
            log.write("=== STDOUT ===\n")
            log.write(result.stdout)
            log.write("\n\n=== STDERR ===\n")
            log.write(result.stderr)
        if result.returncode != 0:
            flash(f"❌ Analysis failed: {result.stderr}", "danger")
            logger.error(
                "Analysis subprocess failed: %s",
                result.stderr,
                extra={"event_type": "analysis"},
            )
            _write_analysis_status("failed", 100, orig_path.name)
            if event:
                event.status = "error"
                event.error_msg = result.stderr[:1024]
                db.session.commit()
            return redirect(url_for("artwork.artworks"))
    except Exception as e:  # noqa: BLE001
        with open(log_file, "a") as log:
            log.write(f"\n\n=== Exception ===\n{str(e)}")
        flash(f"❌ Error running analysis: {e}", "danger")
        logger.error("Analysis exception: %s", e, extra={"event_type": "analysis"})
        _write_analysis_status("failed", 100, orig_path.name)
        if event:
            event.status = "error"
            event.error_msg = str(e)[:1024]
            db.session.commit()
        return redirect(url_for("artwork.artworks"))

    try:
        seo_folder = utils.find_seo_folder_from_filename(
            qc.get("aspect_ratio", ""), orig_path.name
        )
    except FileNotFoundError:
        flash(
            f"Analysis complete, but no SEO folder/listing found for {orig_path.name} ({qc.get('aspect_ratio','')}).",
            "warning",
        )
        return redirect(url_for("artwork.artworks"))

    listing_data = None
    listing_path = (
        utils.ARTWORK_PROCESSED_DIR
        / seo_folder
        / config.FILENAME_TEMPLATES["listing_json"].format(seo_slug=seo_folder)
    )
    if listing_path.exists():
        try:
            with open(listing_path, "r", encoding="utf-8") as lf:
                listing_data = json.load(lf)
        except Exception:
            listing_data = None

    for suffix in [f".{ext}", "-thumb.jpg", "-analyse.jpg", ".qc.json"]:
        temp_file = config.UPLOADS_TEMP_DIR / f"{base}{suffix}"
        if not temp_file.exists():
            continue
        template_key = (
            "analyse"
            if suffix == "-analyse.jpg"
            else (
                "thumbnail"
                if suffix == "-thumb.jpg"
                else "qc_json" if suffix.endswith(".qc.json") else "artwork"
            )
        )
        dest = (
            processed_root
            / seo_folder
            / config.FILENAME_TEMPLATES[template_key].format(seo_slug=seo_folder)
        )
        if suffix == "-analyse.jpg" and dest.exists():
            ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            dest = dest.with_name(f"{dest.stem}-{ts}{dest.suffix}")
        try:
            shutil.move(str(temp_file), dest)
        except Exception as exc:
            logger.error(
                "Failed moving %s to %s: %s",
                temp_file,
                dest,
                exc,
                extra={"event_type": "analysis"},
            )
            flash(f"File move failed for {temp_file.name}: {exc}", "danger")
            _write_analysis_status("failed", 100, orig_path.name)
            if event:
                event.status = "error"
                event.error_msg = str(exc)[:1024]
                db.session.commit()
            return redirect(url_for("artwork.artworks"))

    try:
        cmd = ["python3", str(utils.GENERATE_SCRIPT_PATH), seo_folder]
        _write_analysis_status("generating", 60, orig_path.name)
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=utils.BASE_DIR,
            timeout=600,
        )
        composite_log = utils.LOGS_DIR / f"composite_gen_{log_id}.log"
        with open(composite_log, "w") as log:
            log.write("=== STDOUT ===\n")
            log.write(result.stdout)
            log.write("\n\n=== STDERR ===\n")
            log.write(result.stderr)
        if result.returncode != 0:
            flash("Artwork analyzed, but mockup generation failed.", "danger")
            logger.error(
                "Mockup generation failed for %s",
                seo_folder,
                extra={"event_type": "analysis"},
            )
    except Exception as e:  # noqa: BLE001
        flash(f"Composites generation error: {e}", "danger")
        logger.error(
            "Composites generation exception: %s", e, extra={"event_type": "analysis"}
        )

    aspect = (
        listing_data.get("aspect_ratio", qc.get("aspect_ratio", ""))
        if listing_data
        else qc.get("aspect_ratio", "")
    )
    new_filename = f"{seo_folder}.jpg"
    if listing_data:
        new_filename = listing_data.get("seo_filename", new_filename)
    _write_analysis_status("done", 100, orig_path.name)
    if event:
        event.analysis_end_time = datetime.datetime.utcnow()
        event.status = "analysed"
        db.session.commit()
    logger.info("Analysis finished %s", base, extra={"event_type": "analysis"})
    return redirect(
        url_for("artwork.edit_listing", aspect=aspect, filename=new_filename)
    )


@bp.route("/review/<aspect>/<filename>")
def review_artwork(aspect, filename):
    """Legacy URL – redirect to the new edit/review page."""
    return redirect(url_for("artwork.finalised_gallery"))


@bp.route("/review/<aspect>/<filename>/regenerate/<int:slot_idx>", methods=["POST"])
def review_regenerate_mockup(aspect, filename, slot_idx):
    """Regenerate a specific mockup while reviewing legacy listings."""
    seo_folder = utils.find_seo_folder_from_filename(aspect, filename)
    utils.regenerate_one_mockup(seo_folder, slot_idx)
    return redirect(url_for("artwork.finalised_gallery"))


@bp.route("/review/<seo_folder>/swap/<int:slot_idx>", methods=["POST"])
def review_swap_mockup(seo_folder, slot_idx):
    """Swap a mockup to a new category during legacy review."""
    new_cat = request.form["new_category"]
    if not utils.swap_one_mockup(seo_folder, slot_idx, new_cat):
        flash("Failed to swap mockup", "danger")

    info = utils.find_aspect_filename_from_seo_folder(seo_folder)
    if info:
        aspect, filename = info
        return redirect(
            url_for("artwork.edit_listing", aspect=aspect, filename=filename)
        )

    flash(
        "Could not locate the correct artwork for editing after swap. Please check the gallery.",
        "warning",
    )
    return redirect(url_for("artwork.finalised_gallery"))


@bp.route("/edit-listing")
def edit_listing_blank():
    """Fallback page shown when no listing is specified."""
    flash("No listing selected", "warning")
    return render_template(
        "edit_listing.html",
        artwork={},
        aspect="",
        filename="",
        seo_folder="",
        mockups=[],
        mockup_urls=[],
        thumb_url="",
        menu=utils.get_menu(),
        errors=None,
        colour_options=get_allowed_colours(),
        categories=utils.get_categories(),
        finalised=False,
        locked=False,
        editable=False,
        openai_analysis=None,
        generic_text="",
    )


@bp.route("/edit-listing/<aspect>/<filename>", methods=["GET", "POST"])
def edit_listing(aspect, filename):
    """Display and update a processed or finalised artwork listing."""
    logger = logging.getLogger(__name__)

    try:
        seo_folder, folder, listing_path, finalised = utils.resolve_listing_paths(
            aspect, filename
        )
    except FileNotFoundError:
        flash(f"Artwork not found: {filename}", "danger")
        logger.error("Listing not found: %s", filename, extra={"event_type": "listing"})
        return redirect(url_for("artwork.artworks"))

    try:
        with open(listing_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:  # noqa: BLE001
        flash(f"Error loading listing: {e}", "danger")
        logger.error(
            "Error loading %s: %s", listing_path, e, extra={"event_type": "listing"}
        )
        return redirect(url_for("artwork.artworks"))

    generic_text = read_generic_text(aspect)
    if generic_text:
        data["generic_text"] = generic_text

    openai_info = data.get("openai_analysis")
    if openai_info is not None and not isinstance(openai_info, (list, dict)):
        try:
            openai_info = json.loads(openai_info)
        except Exception:
            openai_info = None

    # Locate generated mockup preview images under static/generated
    gen_dir_rel = Path("generated") / aspect / Path(filename).stem
    gen_dir = config.BASE_DIR / "static" / gen_dir_rel
    generated_mockups: list[str] = []
    if not gen_dir.exists():
        gen_dir_rel = Path("generated") / aspect / seo_folder
        gen_dir = config.BASE_DIR / "static" / gen_dir_rel
    if gen_dir.exists():
        for idx in range(9):
            comp = gen_dir / f"composite-{idx}.jpg"
            if comp.exists():
                generated_mockups.append(
                    url_for("static", filename=(gen_dir_rel / comp.name).as_posix())
                )

    if request.method == "POST":
        locked, _, _, _ = utils.listing_lock_info(listing_path)
        if locked:
            flash("Artwork is locked", "danger")
            logging.getLogger(__name__).warning(
                "Blocked by lock %s", seo_folder, extra={"event_type": "lock"}
            )
            return redirect(
                url_for("artwork.edit_listing", aspect=aspect, filename=filename)
            )

        action = request.form.get("action", "save")

        seo_field = request.form.get(
            "seo_filename", data.get("seo_filename", f"{seo_folder}.jpg")
        ).strip()
        # SKU comes exclusively from the listing JSON; users cannot edit it
        sku_val = str(data.get("sku", "")).strip()
        inferred = infer_sku_from_filename(seo_field) or ""
        if sku_val and inferred and sku_val != inferred:
            sku_val = inferred
            flash("SKU updated to match SEO filename", "info")
        elif not sku_val:
            sku_val = inferred
        seo_val = sync_filename_with_sku(seo_field, sku_val)

        form_data = {
            "title": request.form.get("title", data.get("title", "")).strip(),
            "description": request.form.get(
                "description", data.get("description", "")
            ).strip(),
            "tags": parse_csv_list(request.form.get("tags", "")),
            "materials": parse_csv_list(request.form.get("materials", "")),
            "primary_colour": request.form.get(
                "primary_colour", data.get("primary_colour", "")
            ).strip(),
            "secondary_colour": request.form.get(
                "secondary_colour", data.get("secondary_colour", "")
            ).strip(),
            "seo_filename": seo_val,
            "price": request.form.get("price", data.get("price", "17.88")).strip(),
            "sku": sku_val,
            "images": [
                i.strip()
                for i in request.form.get("images", "").splitlines()
                if i.strip()
            ],
        }

        form_data["tags"], cleaned_tags = clean_terms(form_data["tags"])
        form_data["materials"], cleaned_mats = clean_terms(form_data["materials"])
        if cleaned_tags:
            flash(f"Cleaned tags: {join_csv_list(form_data['tags'])}", "success")
        if cleaned_mats:
            flash(
                f"Cleaned materials: {join_csv_list(form_data['materials'])}", "success"
            )

        if action == "delete":
            shutil.rmtree(utils.ARTWORK_PROCESSED_DIR / seo_folder, ignore_errors=True)
            shutil.rmtree(utils.FINALISED_DIR / seo_folder, ignore_errors=True)
            try:
                os.remove(utils.ARTWORKS_DIR / aspect / filename)
            except Exception:
                pass
            logging.getLogger(__name__).warning(
                "Artwork deleted %s", seo_folder, extra={"event_type": "listing"}
            )
            flash("Artwork deleted", "success")
            return redirect(url_for("artwork.artworks"))

        folder.mkdir(parents=True, exist_ok=True)
        img_files = [
            p for p in folder.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png"}
        ]
        form_data["images"] = [relative_to_base(p) for p in sorted(img_files)]

        errors = validate_listing_fields(form_data, generic_text)
        if errors:
            form_data["images"] = "\n".join(form_data.get("images", []))
            form_data["tags"] = join_csv_list(form_data.get("tags", []))
            form_data["materials"] = join_csv_list(form_data.get("materials", []))

            mockups = []
            for idx, mp in enumerate(data.get("mockups", [])):
                if isinstance(mp, dict):
                    out = folder / mp.get("composite", "")
                    cat = mp.get("category", "")
                else:
                    p = Path(mp)
                    out = folder / f"{seo_folder}-{p.stem}.jpg"
                    cat = p.parent.name
                mockups.append(
                    {"path": out, "category": cat, "exists": out.exists(), "index": idx}
                )

            mockup_urls: list[str] = []
            thumbnail_url = ""
            seo_name = Path(form_data.get("seo_filename") or f"{seo_folder}.jpg").stem
            mockup_folder = FINALISED_DIR / seo_folder
            if mockup_folder.exists():
                for f in sorted(mockup_folder.iterdir()):
                    fname = f.name
                    if "MU-" in fname and fname.lower().endswith(".jpg"):
                        mockup_urls.append(
                            url_for("artwork.finalised_image", seo_folder=seo_folder, filename=fname)
                        )
                    if fname.lower() == f"{seo_name.lower()}-thumb.jpg":
                        thumbnail_url = url_for(
                            "artwork.finalised_image", seo_folder=seo_folder, filename=fname
                        )

            return render_template(
                "edit_listing.html",
                artwork=form_data,
                errors=errors,
                aspect=aspect,
                filename=filename,
                seo_folder=seo_folder,
                mockups=mockups,
                mockup_urls=mockup_urls,
                thumbnail_url=thumbnail_url,
                thumb_url=thumbnail_url,
                generated_mockups=generated_mockups,
                menu=utils.get_menu(),
                colour_options=get_allowed_colours(),
                categories=utils.get_categories(),
                finalised=finalised,
                locked=data.get("locked", False),
                editable=not data.get("locked", False),
                openai_analysis=openai_info,
                generic_text=generic_text,
            )

        data.update(form_data)
        data["generic_text"] = generic_text

        full_desc = re.sub(r"\s+$", "", form_data["description"])
        gen = generic_text.strip()
        if gen and not full_desc.endswith(gen):
            full_desc = re.sub(r"\n{3,}", "\n\n", full_desc.rstrip()) + "\n\n" + gen
        data["description"] = full_desc.strip()

        with open(listing_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logging.getLogger(__name__).info(
            "Listing updated %s", seo_folder, extra={"event_type": "listing"}
        )

        flash("Listing updated", "success")
        return redirect(
            url_for("artwork.edit_listing", aspect=aspect, filename=filename)
        )

    raw_ai = data.get("ai_listing")
    ai = {}
    fallback_ai: dict = {}

    def parse_fallback(text: str) -> dict:
        match = re.search(r"```json\s*({.*?})\s*```", text, re.DOTALL)
        if not match:
            match = re.search(r"({.*})", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                return {}
        return {}

    if isinstance(raw_ai, dict):
        ai = raw_ai
        if isinstance(raw_ai.get("fallback_text"), str):
            fallback_ai.update(parse_fallback(raw_ai.get("fallback_text")))
    elif isinstance(raw_ai, str):
        try:
            ai = json.loads(raw_ai)
        except Exception:
            fallback_ai.update(parse_fallback(raw_ai))

    if isinstance(data.get("fallback_text"), str):
        fallback_ai.update(parse_fallback(data["fallback_text"]))

    price = data.get("price") or ai.get("price") or fallback_ai.get("price") or "17.88"
    sku = (
        data.get("sku")
        or ai.get("sku")
        or fallback_ai.get("sku")
        or infer_sku_from_filename(data.get("seo_filename", ""))
        or ""
    )
    primary = (
        data.get("primary_colour")
        or ai.get("primary_colour")
        or fallback_ai.get("primary_colour", "")
    )
    secondary = (
        data.get("secondary_colour")
        or ai.get("secondary_colour")
        or fallback_ai.get("secondary_colour", "")
    )

    images = data.get("images")
    if not images:
        processed_dir = utils.ARTWORK_PROCESSED_DIR / seo_folder
        final_dir = utils.FINALISED_DIR / seo_folder
        img_paths: list[Path] = []
        for base_dir in (processed_dir, final_dir):
            if base_dir.exists():
                img_paths.extend(
                    p
                    for p in base_dir.iterdir()
                    if p.suffix.lower() in {".jpg", ".jpeg", ".png"}
                )
        images = [relative_to_base(p) for p in sorted({p for p in img_paths})]
    else:
        images = [relative_to_base(Path(p)) for p in images]

    artwork = {
        "title": data.get("title") or ai.get("title") or fallback_ai.get("title", ""),
        "description": data.get("description")
        or ai.get("description")
        or fallback_ai.get("description", ""),
        "tags": join_csv_list(
            data.get("tags") or ai.get("tags") or fallback_ai.get("tags", [])
        ),
        "materials": join_csv_list(
            data.get("materials")
            or ai.get("materials")
            or fallback_ai.get("materials", [])
        ),
        "primary_colour": primary,
        "secondary_colour": secondary,
        "seo_filename": data.get("seo_filename")
        or ai.get("seo_filename")
        or fallback_ai.get("seo_filename")
        or f"{seo_folder}.jpg",
        "price": price,
        "sku": sku,
        "images": "\n".join(images),
    }

    if not artwork.get("title"):
        artwork["title"] = seo_folder.replace("-", " ").title()
    if not artwork.get("description"):
        artwork["description"] = (
            "(No description found. Try re-analyzing or check AI output.)"
        )

    artwork["full_listing_text"] = utils.build_full_listing_text(
        artwork.get("description", ""), data.get("generic_text", "")
    )

    mockups = []
    for idx, mp in enumerate(data.get("mockups", [])):
        if isinstance(mp, dict):
            out = folder / mp.get("composite", "")
            cat = mp.get("category", "")
        else:
            p = Path(mp)
            out = folder / f"{seo_folder}-{p.stem}.jpg"
            cat = p.parent.name
        mockups.append({"path": out, "category": cat, "exists": out.exists(), "index": idx})
    mockup_urls: list[str] = []
    thumbnail_url = ""
    seo_name = Path(artwork.get("seo_filename", f"{seo_folder}.jpg")).stem
    mockup_folder = FINALISED_DIR / seo_folder
    if mockup_folder.exists():
        for f in sorted(mockup_folder.iterdir()):
            fname = f.name
            if "MU-" in fname and fname.lower().endswith(".jpg"):
                mockup_urls.append(
                    url_for("artwork.finalised_image", seo_folder=seo_folder, filename=fname)
                )
            if fname.lower() == f"{seo_name.lower()}-thumb.jpg":
                thumbnail_url = url_for(
                    "artwork.finalised_image", seo_folder=seo_folder, filename=fname
                )

    if not thumbnail_url:
        thumbnail_url = url_for(
            "artwork.processed_image",
            seo_folder=seo_folder,
            filename=f"{seo_folder}-THUMB.jpg",
        )
    thumb_url = thumbnail_url
    return render_template(
        "edit_listing.html",
        artwork=artwork,
        aspect=aspect,
        filename=filename,
        seo_folder=seo_folder,
        mockups=mockups,
        mockup_urls=mockup_urls,
        thumbnail_url=thumbnail_url,
        thumb_url=thumb_url,
        generated_mockups=generated_mockups,
        menu=utils.get_menu(),
        errors=None,
        colour_options=get_allowed_colours(),
        categories=utils.get_categories(),
        finalised=finalised,
        locked=data.get("locked", False),
        editable=not data.get("locked", False),
        openai_analysis=openai_info,
        generic_text=data.get("generic_text", ""),
    )


_PROCESSED_REL = ARTWORKS_PROCESSED_DIR.relative_to(BASE_DIR).as_posix()
_FINALISED_REL = ARTWORKS_FINALISED_DIR.relative_to(BASE_DIR).as_posix()


@bp.route(f"/static/{_PROCESSED_REL}/<seo_folder>/<filename>")
def processed_image(seo_folder, filename):
    """Serve artwork images from processed or finalised folders."""
    final_folder = utils.FINALISED_DIR / seo_folder
    if (final_folder / filename).exists():
        folder = final_folder
    else:
        folder = utils.ARTWORK_PROCESSED_DIR / seo_folder
    return send_from_directory(folder, filename)


@bp.route(f"/static/{_FINALISED_REL}/<seo_folder>/<filename>")
def finalised_image(seo_folder, filename):
    """Serve images strictly from the finalised-artwork folder."""
    folder = utils.FINALISED_DIR / seo_folder
    return send_from_directory(folder, filename)


@bp.route("/artwork-img/<aspect>/<filename>")
def artwork_image(aspect, filename):
    """Serve the original uploaded artwork if it exists."""
    folder = utils.ARTWORKS_DIR / aspect
    candidate = folder / filename
    if candidate.exists():
        return send_from_directory(str(folder.resolve()), filename)
    alt_folder = utils.ARTWORKS_DIR / f"{aspect}-artworks" / Path(filename).stem
    candidate = alt_folder / filename
    if candidate.exists():
        return send_from_directory(str(alt_folder.resolve()), filename)
    return "", 404


@bp.route("/temp-img/<filename>")
def temp_image(filename):
    """Serve images from the temporary upload directory."""
    return send_from_directory(config.UPLOADS_TEMP_DIR, filename)


@bp.route("/mockup-img/<category>/<filename>")
def mockup_img(category, filename):
    """Return a stored mockup image by category."""
    return send_from_directory(utils.MOCKUPS_DIR / category, filename)


@bp.route("/composite-img/<folder>/<filename>")
def composite_img(folder, filename):
    """Serve generated composite images."""
    return send_from_directory(utils.COMPOSITES_DIR / folder, filename)


@bp.route("/composites")
def composites_preview():
    """Redirect to the latest composite preview if available."""
    latest = utils.latest_composite_folder()
    if latest:
        return redirect(url_for("artwork.composites_specific", seo_folder=latest))
    flash("No composites found", "warning")
    return redirect(url_for("artwork.artworks"))


@bp.route("/composites/<seo_folder>")
def composites_specific(seo_folder):
    """Show composite images for a specific SEO folder."""
    folder = utils.ARTWORK_PROCESSED_DIR / seo_folder
    json_path = folder / f"{seo_folder}-listing.json"
    images = []
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as jf:
            listing = json.load(jf)
        for idx, mp in enumerate(listing.get("mockups", [])):
            if isinstance(mp, dict):
                out = folder / mp.get("composite", "")
                cat = mp.get("category", "")
            else:
                p = Path(mp)
                out = folder / f"{seo_folder}-{p.stem}.jpg"
                cat = p.parent.name
            images.append(
                {
                    "filename": out.name,
                    "category": cat,
                    "index": idx,
                    "exists": out.exists(),
                }
            )
    else:
        for idx, img in enumerate(sorted(folder.glob(f"{seo_folder}-mockup-*.jpg"))):
            images.append(
                {"filename": img.name, "category": None, "index": idx, "exists": True}
            )
    return render_template(
        "composites_preview.html",
        images=images,
        folder=seo_folder,
        menu=utils.get_menu(),
    )


@bp.route("/composites/<seo_folder>/regenerate/<int:slot_index>", methods=["POST"])
def regenerate_composite(seo_folder, slot_index):
    """Regenerate a single composite image in-place."""
    utils.regenerate_one_mockup(seo_folder, slot_index)
    return redirect(url_for("artwork.composites_specific", seo_folder=seo_folder))


@bp.route("/approve_composites/<seo_folder>", methods=["POST"])
def approve_composites(seo_folder):
    """Mark composites as approved (placeholder)."""
    flash("Composites approved", "success")
    return redirect(url_for("artwork.composites_specific", seo_folder=seo_folder))


@bp.route("/finalise/<aspect>/<filename>", methods=["GET", "POST"])
def finalise_artwork(aspect, filename):
    """Move processed artwork to finalised location and update listing data."""
    logger = logging.getLogger(__name__)
    try:
        seo_folder = utils.find_seo_folder_from_filename(aspect, filename)
    except FileNotFoundError:
        flash(f"Artwork not found: {filename}", "danger")
        logger.error(
            "Finalise failed, not found: %s", filename, extra={"event_type": "finalise"}
        )
        return redirect(url_for("artwork.artworks"))

    processed_dir = utils.ARTWORK_PROCESSED_DIR / seo_folder
    final_dir = utils.FINALISED_DIR / seo_folder
    log_path = utils.LOGS_DIR / "finalise.log"

    # ------------------------------------------------------------------
    # Move processed artwork into the finalised location and update paths
    # ------------------------------------------------------------------
    try:
        if final_dir.exists():
            raise FileExistsError(f"{final_dir} already exists")

        shutil.move(str(processed_dir), str(final_dir))

        # Marker file indicating finalisation time
        (final_dir / "finalised.txt").write_text(
            datetime.datetime.now().isoformat(), encoding="utf-8"
        )

        # Remove original artwork from input directory if it still exists
        orig_input = utils.ARTWORKS_DIR / aspect / filename
        try:
            os.remove(orig_input)
        except FileNotFoundError:
            pass

        # Update any stored paths within the listing JSON
        listing_file = final_dir / f"{seo_folder}-listing.json"
        if listing_file.exists():
            # Always allocate a fresh SKU on finalisation
            utils.assign_or_get_sku(listing_file, config.SKU_TRACKER, force=True)
            with open(listing_file, "r", encoding="utf-8") as lf:
                listing_data = json.load(lf)
            listing_data.setdefault("locked", False)

            def _swap_path(p: str) -> str:
                return p.replace(
                    str(utils.ARTWORK_PROCESSED_DIR), str(utils.FINALISED_DIR)
                )

            for key in (
                "main_jpg_path",
                "orig_jpg_path",
                "thumb_jpg_path",
                "processed_folder",
            ):
                if isinstance(listing_data.get(key), str):
                    listing_data[key] = _swap_path(listing_data[key])

            if isinstance(listing_data.get("images"), list):
                listing_data["images"] = [
                    _swap_path(img) if isinstance(img, str) else img
                    for img in listing_data["images"]
                ]

            imgs = [
                p
                for p in final_dir.iterdir()
                if p.suffix.lower() in {".jpg", ".jpeg", ".png"}
            ]
            listing_data["images"] = [utils.relative_to_base(p) for p in sorted(imgs)]

            with open(listing_file, "w", encoding="utf-8") as lf:
                json.dump(listing_data, lf, indent=2, ensure_ascii=False)

        with open(log_path, "a", encoding="utf-8") as log:
            user = session.get("user", "anonymous")
            log.write(
                f"{datetime.datetime.now().isoformat()} - {seo_folder} by {user}\n"
            )

        logger.info(
            "Finalised artwork %s", seo_folder, extra={"event_type": "finalise"}
        )
        flash("Artwork finalised", "success")
    except Exception as e:  # noqa: BLE001
        flash(f"Failed to finalise artwork: {e}", "danger")
        logger.error(
            "Finalise error %s: %s", seo_folder, e, extra={"event_type": "finalise"}
        )

    return redirect(url_for("artwork.finalised_gallery"))


@bp.route("/finalised")
def finalised_gallery():
    """Display all finalised artworks in a gallery view."""
    artworks = []
    if utils.FINALISED_DIR.exists():
        for folder in utils.FINALISED_DIR.iterdir():
            if not folder.is_dir():
                continue
            listing_file = folder / f"{folder.name}-listing.json"
            if not listing_file.exists():
                continue
            try:
                with open(listing_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                continue
            entry = {
                "seo_folder": folder.name,
                "title": data.get("title") or utils.prettify_slug(folder.name),
                "description": data.get("description", ""),
                "sku": data.get("sku", ""),
                "primary_colour": data.get("primary_colour", ""),
                "secondary_colour": data.get("secondary_colour", ""),
                "price": data.get("price", ""),
                "seo_filename": data.get("seo_filename", f"{folder.name}.jpg"),
                "tags": data.get("tags", []),
                "materials": data.get("materials", []),
                "aspect": data.get("aspect_ratio", ""),
                "filename": data.get("filename", f"{folder.name}.jpg"),
                "locked": data.get("locked", False),
                "mockups": [],
            }

            for mp in data.get("mockups", []):
                if isinstance(mp, dict):
                    out = folder / mp.get("composite", "")
                else:
                    p = Path(mp)
                    out = folder / f"{folder.name}-{p.stem}.jpg"
                if out.exists():
                    entry["mockups"].append({"filename": out.name})

            # Filter images that actually exist on disk
            images = []
            for img in data.get("images", []):
                img_path = utils.BASE_DIR / img
                if img_path.exists():
                    images.append(img)
            entry["images"] = images

            ts = folder / "finalised.txt"
            entry["date"] = (
                ts.stat().st_mtime if ts.exists() else listing_file.stat().st_mtime
            )

            main_img = folder / f"{folder.name}.jpg"
            entry["main_image"] = main_img.name if main_img.exists() else None

            artworks.append(entry)
    artworks.sort(key=lambda x: x.get("date", 0), reverse=True)
    return render_template("finalised.html", artworks=artworks, menu=utils.get_menu())


@bp.route("/locked")
def locked_gallery():
    """Show gallery of locked artworks only."""
    locked_items = [
        a for a in utils.list_finalised_artworks_extended() if a.get("locked")
    ]
    return render_template("locked.html", artworks=locked_items, menu=utils.get_menu())


@bp.post("/update-links/<aspect>/<filename>")
def update_links(aspect, filename):
    """Regenerate image URL list from disk for either processed or finalised artwork.

    If the request was sent via AJAX (accepting JSON or using the ``XMLHttpRequest``
    header) the refreshed list of image URLs is returned as JSON rather than
    performing a redirect. This allows the edit page to update the textarea in
    place without losing form state.
    """

    wants_json = (
        "application/json" in request.headers.get("Accept", "")
        or request.headers.get("X-Requested-With") == "XMLHttpRequest"
    )

    try:
        seo_folder, folder, listing_file, _ = utils.resolve_listing_paths(
            aspect, filename
        )
    except FileNotFoundError:
        msg = "Artwork not found"
        if wants_json:
            return {"success": False, "message": msg, "images": []}, 404
        flash(msg, "danger")
        return redirect(url_for("artwork.artworks"))

    locked, _, _, _ = utils.listing_lock_info(listing_file)
    if locked:
        msg = "Artwork is locked"
        if wants_json:
            return {"success": False, "message": msg, "images": []}, 403
        logging.getLogger(__name__).warning(
            "Blocked by lock %s", seo_folder, extra={"event_type": "lock"}
        )
        flash(msg, "danger")
        return redirect(
            url_for("artwork.edit_listing", aspect=aspect, filename=filename)
        )

    try:
        with open(listing_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        imgs = [
            p for p in folder.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png"}
        ]
        data["images"] = [utils.relative_to_base(p) for p in sorted(imgs)]
        with open(listing_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        msg = "Image links updated"
        if wants_json:
            return {"success": True, "message": msg, "images": data["images"]}
        flash(msg, "success")
    except Exception as e:  # noqa: BLE001
        msg = f"Failed to update links: {e}"
        if wants_json:
            return {"success": False, "message": msg, "images": []}, 500
        flash(msg, "danger")
    return redirect(url_for("artwork.edit_listing", aspect=aspect, filename=filename))


@bp.post("/finalise/delete/<aspect>/<filename>")
def delete_finalised(aspect, filename):
    """Delete a finalised artwork folder."""
    try:
        seo_folder = utils.find_seo_folder_from_filename(aspect, filename)
    except FileNotFoundError:
        flash("Artwork not found", "danger")
        return redirect(url_for("artwork.finalised_gallery"))
    folder = utils.FINALISED_DIR / seo_folder
    listing_file = folder / f"{seo_folder}-listing.json"
    locked, _, _, _ = utils.listing_lock_info(listing_file)
    if locked:
        flash("Artwork is locked; unlock before deleting", "danger")
        logging.getLogger(__name__).warning(
            "Blocked by lock %s", seo_folder, extra={"event_type": "lock"}
        )
        return redirect(
            url_for("artwork.edit_listing", aspect=aspect, filename=filename)
        )
    try:
        shutil.rmtree(folder)
        flash("Finalised artwork deleted", "success")
    except Exception as e:  # noqa: BLE001
        flash(f"Delete failed: {e}", "danger")
    return redirect(url_for("artwork.finalised_gallery"))


@bp.post("/lock/<aspect>/<filename>")
def lock_listing(aspect, filename):
    """Mark a finalised artwork as locked."""
    try:
        seo, folder, listing, finalised = utils.resolve_listing_paths(aspect, filename)
    except FileNotFoundError:
        flash("Artwork not found", "danger")
        return redirect(url_for("artwork.artworks"))
    if not finalised:
        flash("Artwork must be finalised before locking", "danger")
        return redirect(
            url_for("artwork.edit_listing", aspect=aspect, filename=filename)
        )
    reason = request.form.get("reason", "").strip()
    try:
        with open(listing, "r", encoding="utf-8") as f:
            data = json.load(f)
        utils.update_listing_lock(listing, True, session.get("user", "unknown"), reason)
        logging.getLogger(__name__).info(
            "Listing locked %s", seo, extra={"event_type": "lock"}
        )
        flash("Artwork locked", "success")
    except Exception as exc:  # noqa: BLE001
        flash(f"Failed to lock: {exc}", "danger")
    return redirect(url_for("artwork.edit_listing", aspect=aspect, filename=filename))


@bp.post("/unlock/<aspect>/<filename>")
def unlock_listing(aspect, filename):
    """Unlock a previously locked artwork."""
    try:
        seo, folder, listing, _ = utils.resolve_listing_paths(aspect, filename)
    except FileNotFoundError:
        flash("Artwork not found", "danger")
        return redirect(url_for("artwork.artworks"))
    reason = request.form.get("reason", "").strip()
    try:
        with open(listing, "r", encoding="utf-8") as f:
            data = json.load(f)
        utils.update_listing_lock(
            listing, False, session.get("user", "unknown"), reason
        )
        logging.getLogger(__name__).info(
            "Listing unlocked %s", seo, extra={"event_type": "lock"}
        )
        flash("Artwork unlocked", "success")
    except Exception as exc:  # noqa: BLE001
        flash(f"Failed to unlock: {exc}", "danger")
    return redirect(url_for("artwork.edit_listing", aspect=aspect, filename=filename))


@bp.post("/reset-sku/<aspect>/<filename>")
def reset_sku(aspect, filename):
    """Force reassign a new SKU for the given artwork."""
    try:
        seo, folder, listing, _ = utils.resolve_listing_paths(aspect, filename)
    except FileNotFoundError:
        flash("Artwork not found", "danger")
        return redirect(url_for("artwork.artworks"))
    try:
        utils.assign_or_get_sku(listing, config.SKU_TRACKER, force=True)
        flash("SKU reset", "success")
    except Exception as exc:  # noqa: BLE001
        flash(f"Failed to reset SKU: {exc}", "danger")
    return redirect(url_for("artwork.edit_listing", aspect=aspect, filename=filename))




@bp.route("/logs/openai")
@bp.route("/logs/openai/<date>")
def view_openai_logs(date: str | None = None):
    """Return the tail of the most recent OpenAI analysis log."""
    logs = sorted(
        config.LOGS_DIR.glob("analyze-openai-calls-*.log"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not logs:
        return Response("No logs found", mimetype="text/plain")

    target = None
    if date:
        cand = config.LOGS_DIR / f"analyze-openai-calls-{date}.log"
        if cand.exists():
            target = cand
    if not target:
        target = logs[0]

    text = target.read_text(encoding="utf-8")
    lines = text.strip().splitlines()[-50:]
    return Response("\n".join(lines), mimetype="text/plain")


@bp.route("/next-sku")
def preview_next_sku():
    """Return the next SKU without reserving it."""
    next_sku = peek_next_sku(config.SKU_TRACKER)
    return Response(next_sku, mimetype="text/plain")


def _process_upload_file(file_storage):
    """Handle single uploaded file through QC, AI and relocation."""
    logger = logging.getLogger(__name__)
    result = {"original": file_storage.filename, "success": False, "error": ""}
    filename = file_storage.filename
    if not filename:
        result["error"] = "No filename"
        logger.error("Upload missing filename")
        return result
    ext = Path(filename).suffix.lower().lstrip(".")
    if ext not in config.ALLOWED_EXTENSIONS:
        result["error"] = "Invalid file type"
        logger.warning("Rejected file type: %s", ext, extra={"event_type": "upload"})
        return result
    data = file_storage.read()
    if len(data) > config.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        result["error"] = "File too large"
        logger.warning(
            "Upload too large: %s bytes", len(data), extra={"event_type": "upload"}
        )
        return result
    try:
        with Image.open(io.BytesIO(data)) as im:
            im.verify()
    except Exception:
        result["error"] = "Corrupted image"
        logger.error(
            "Corrupted image uploaded: %s", filename, extra={"event_type": "upload"}
        )
        return result

    safe = aa.slugify(Path(filename).stem)
    unique = uuid.uuid4().hex[:8]
    base = f"{safe}-{unique}"

    start_ts = datetime.datetime.utcnow()
    event = UploadEvent(
        user_id=session.get("user"),
        upload_id=base,
        filename=filename,
        upload_start_time=start_ts,
        upload_end_time=start_ts,
        status="started",
        session_id=session.get("token"),
        ip_address=request.remote_addr,
        user_agent=request.headers.get("User-Agent"),
    )
    db.session.add(event)
    db.session.flush()
    config.UPLOADS_TEMP_DIR.mkdir(parents=True, exist_ok=True)
    orig_path = config.UPLOADS_TEMP_DIR / f"{base}.{ext}"
    with open(orig_path, "wb") as f:
        f.write(data)

    with Image.open(orig_path) as img:
        width, height = img.size
        thumb_path = config.UPLOADS_TEMP_DIR / f"{base}-thumb.jpg"
        thumb = img.copy()
        thumb.thumbnail((config.THUMB_WIDTH, config.THUMB_HEIGHT))
        thumb.save(thumb_path, "JPEG", quality=80)

    analyse_path = config.UPLOADS_TEMP_DIR / f"{base}-analyse.jpg"
    with Image.open(orig_path) as img:
        w, h = img.size
        scale = config.ANALYSE_MAX_DIM / max(w, h)
        if scale < 1.0:
            img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        img = img.convert("RGB")

        q = 85
        while True:
            img.save(analyse_path, "JPEG", quality=q, optimize=True)
            if (
                analyse_path.stat().st_size <= config.ANALYSE_MAX_MB * 1024 * 1024
                or q <= 60
            ):
                break
            q -= 5

    aspect = aa.get_aspect_ratio(orig_path)

    qc_data = {
        "original_filename": filename,
        "extension": ext,
        "image_shape": [width, height],
        "filesize_bytes": len(data),
        "aspect_ratio": aspect,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    qc_path = config.UPLOADS_TEMP_DIR / f"{base}.qc.json"
    qc_path.write_text(json.dumps(qc_data, indent=2))

    event.upload_end_time = datetime.datetime.utcnow()
    event.status = "uploaded"
    db.session.commit()

    logger.info(
        "Uploaded %s", filename, extra={"event_type": "upload", "details": base}
    )

    result.update(
        {"success": True, "base": base, "aspect": aspect, "event_id": event.id}
    )
    return result

```

---
## 📄 `ezygallery/routes/mockup_routes.py`

```py
"""Mockup upload and categorisation UI."""
from __future__ import annotations

import base64
import json
import os
import shutil
import subprocess
import uuid
import datetime
from pathlib import Path

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    abort,
    session,
    send_from_directory,
    flash,
)
from openai import OpenAI
from utils.openai_utils import get_openai_model

import config
from . import utils

bp = Blueprint("mockups", __name__, url_prefix="/mockups")

client = OpenAI(api_key=config.OPENAI_API_KEY)


def _encode_image(path: Path) -> str:
    """Return base64 string for an image file."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _analyse_mockup(image_path: Path, categories: list[str]) -> tuple[str, str]:
    """Return (category, description) from OpenAI."""
    system_prompt = (
        "You help organise mockup preview images for digital artwork. "
        "Classify the image into one of these categories:\n"
        f"{', '.join(categories)}\n"
        "Return only the category name."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{_encode_image(image_path)}"},
                }
            ],
        },
    ]
    try:
        resp = client.chat.completions.create(model=get_openai_model(), messages=messages, max_tokens=20, temperature=0)
        cat = resp.choices[0].message.content.strip()
        if cat not in categories:
            cat = "Uncategorised"
    except Exception:
        cat = "Uncategorised"

    desc_prompt = (
        "Describe the mockup style, mood and room context in one short professional sentence."
    )
    try:
        dresp = client.chat.completions.create(
            model=get_openai_model(),
            messages=[{"role": "system", "content": desc_prompt}, {"role": "user", "content": {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{_encode_image(image_path)}"}}}],
            max_tokens=60,
            temperature=0.3,
        )
        desc = dresp.choices[0].message.content.strip()
    except Exception:
        desc = ""
    return cat, desc


def _run_coords(image_path: Path, output_path: Path) -> None:
    """Generate perspective coordinates for a mockup image."""
    script = config.SCRIPTS_DIR / "generate_mockup_coords.py"
    subprocess.run(["python", str(script), str(image_path), str(output_path)], check=True)


@bp.route("/")
def index():
    """List available aspect ratios for mockup images."""
    aspects = utils.get_aspect_ratios()
    return render_template("mockups/index.html", aspects=aspects, menu=utils.get_menu())


@bp.route("/upload", methods=["GET", "POST"])
def upload():
    """Upload new mockup images and categorise via AI."""
    if session.get("role") != "admin":
        abort(403)
    aspects = utils.get_aspect_ratios()
    if request.method == "POST":
        aspect = request.form.get("aspect")
        files = request.files.getlist("images")
        dest_uncat = config.MOCKUPS_INPUT_DIR / aspect / "uncategorised"
        dest_uncat.mkdir(parents=True, exist_ok=True)
        cat_base = config.MOCKUPS_INPUT_DIR / f"{aspect}-categorised"
        results = []
        for f in files:
            filename = f.filename or f"upload-{uuid.uuid4().hex}.png"
            temp_path = dest_uncat / filename
            f.save(temp_path)
            categories = utils.get_categories_for_aspect(aspect)
            if not categories:
                categories = ["Uncategorised"]
            ai_cat, desc = _analyse_mockup(temp_path, categories)
            dest_dir = cat_base / ai_cat
            dest_dir.mkdir(parents=True, exist_ok=True)
            final_path = dest_dir / filename
            shutil.move(temp_path, final_path)
            coords_file = dest_dir / f"{final_path.stem}.coords.json"
            _run_coords(final_path, coords_file)
            meta = {
                "filename": final_path.name,
                "aspect": aspect,
                "category": ai_cat,
                "ai_category": ai_cat,
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "original": filename,
                "description": desc,
                "coords": coords_file.name,
            }
            with open(dest_dir / f"{final_path.stem}.json", "w", encoding="utf-8") as mf:
                json.dump(meta, mf, indent=2)
            utils.log_mockup_action("upload", session.get("user", "?"), f"{aspect}/{ai_cat}/{filename}")
            results.append(meta)
        flash(f"Uploaded {len(results)} mockup(s)", "success")
        return redirect(url_for("mockups.gallery", aspect=aspect))
    return render_template("mockups/upload.html", aspects=aspects, menu=utils.get_menu())


@bp.route("/gallery/<aspect>")
def gallery(aspect):
    """Show categories for a given aspect ratio."""
    cats = utils.get_categories_for_aspect(aspect)
    items = []
    base = config.MOCKUPS_INPUT_DIR / f"{aspect}-categorised"
    for c in cats:
        count = len(list((base / c).glob("*.png")))
        items.append({"name": c, "count": count})
    return render_template("mockups/gallery.html", aspect=aspect, categories=items, menu=utils.get_menu())


@bp.route("/gallery/<aspect>/<category>")
def category_gallery(aspect, category):
    """Display all mockups inside a category."""
    folder = config.MOCKUPS_INPUT_DIR / f"{aspect}-categorised" / category
    images = sorted(p.name for p in folder.glob("*.png"))
    return render_template("mockups/category_gallery.html", aspect=aspect, category=category, images=images, menu=utils.get_menu())


@bp.route("/img/<aspect>/<category>/<filename>")
def image(aspect, category, filename):
    """Serve a raw mockup image file."""
    folder = config.MOCKUPS_INPUT_DIR / f"{aspect}-categorised" / category
    return send_from_directory(folder, filename)


@bp.route("/detail/<aspect>/<category>/<filename>", methods=["GET", "POST"])
def detail(aspect: str, category: str, filename: str):
    """View and edit metadata for a specific mockup."""
    folder = config.MOCKUPS_INPUT_DIR / f"{aspect}-categorised" / category
    meta_path = folder / f"{Path(filename).stem}.json"
    if not meta_path.exists():
        abort(404)
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    if request.method == "POST":
        action = request.form.get("action")
        if action == "delete":
            os.remove(folder / filename)
            os.remove(meta_path)
            coords = folder / meta.get("coords", "")
            if coords.exists():
                coords.unlink()
            utils.log_mockup_action("delete", session.get("user", "?"), f"{aspect}/{category}/{filename}")
            flash("Deleted", "success")
            return redirect(url_for("mockups.category_gallery", aspect=aspect, category=category))
        meta["category"] = request.form.get("category", meta.get("category"))
        meta["description"] = request.form.get("description", meta.get("description"))
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)
        utils.log_mockup_action("edit", session.get("user", "?"), f"{aspect}/{category}/{filename}")
        flash("Saved", "success")
    categories = utils.get_categories_for_aspect(aspect)
    return render_template("mockups/detail.html", meta=meta, categories=categories, menu=utils.get_menu())



@bp.route('/review')
def review():
    """Placeholder page for reviewing mockups."""
    return render_template('mockups/review.html', menu=utils.get_menu())


@bp.route('/categories')
def categories():
    """Placeholder page for mockup categories."""
    return render_template('mockups/categories.html', menu=utils.get_menu())

```

---
## 📄 `ezygallery/routes/admin_debug.py`

```py

"""Debug and administration endpoints used during development.

These routes expose helper pages for inspecting AI parse output, viewing
application status and peeking at SKU sequencing. They are not secured
and should only be enabled in development environments.
"""

from __future__ import annotations

import datetime
import json

from flask import Blueprint, request, render_template, Response

import config
from routes import utils
from utils.sku_assigner import peek_next_sku
from scripts.analyze_artwork import parse_text_fallback

bp = Blueprint("admin", __name__, url_prefix="/admin")
# TODO: Protect admin debug routes with authentication/authorization


@bp.route("/debug/parse-ai", methods=["GET", "POST"])
def parse_ai():
    """Manually parse AI output or saved failures for debugging.

    This route allows pasting raw JSON or selecting a previously failed parse
    file. It attempts to load JSON and falls back to the older text parser on
    failure.
    """
    raw = ""
    parsed = None
    error = ""
    file_name = request.args.get("file")
    if file_name:
        path = config.PARSE_FAILURE_DIR / file_name
        if path.exists():
            raw = path.read_text(encoding="utf-8")
    if request.method == "POST":
        raw = request.form.get("raw", "")
        try:
            parsed = json.loads(raw)
        except Exception as exc:  # noqa: BLE001
            try:
                parsed = parse_text_fallback(raw)
                error = f"Input was not valid JSON: {exc}"
            except Exception as inner:  # noqa: BLE001
                error = f"Parse failed: {inner}"
                config.PARSE_FAILURE_DIR.mkdir(parents=True, exist_ok=True)
                ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                fail_file = config.PARSE_FAILURE_DIR / f"parse_fail_{ts}.txt"
                fail_file.write_text(raw, encoding="utf-8")
    return render_template(
        "debug_parse_ai.html",
        raw=raw,
        parsed=parsed,
        error=error,
        menu=utils.get_menu(),
    )


@bp.route("/debug/next-sku")
def preview_next_sku_admin():
    """Return the next SKU value without reserving it."""
    return Response(peek_next_sku(config.SKU_TRACKER), mimetype="text/plain")


@bp.route("/debug/status")
def debug_status():
    """Display simple environment diagnostic information."""
    info = {
        "openai_key": bool(config.OPENAI_API_KEY),
        "processed_dir": config.ARTWORKS_PROCESSED_DIR.exists(),
        "finalised_dir": config.ARTWORKS_FINALISED_DIR.exists(),
        "parse_failures": sorted(
            p.name for p in config.PARSE_FAILURE_DIR.glob("*.txt")
        ),
    }
    return render_template("debug_status.html", info=info, menu=utils.get_menu())

```

---
## 📄 `ezygallery/routes/openai_guidance.py`

```py
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

```

---
## 📄 `ezygallery/routes/__init__.py`

```py

"""Flask route blueprints for the Capital Art application.

This package groups all blueprint modules that define the HTTP endpoints
used by the project. Importing this package ensures each blueprint can be
registered with the main Flask app.
"""

```

---
## 📄 `ezygallery/routes/documentation_routes.py`

```py

"""Static documentation pages served through Flask routes."""

from __future__ import annotations

from flask import Blueprint, render_template
from routes import utils

bp = Blueprint('documentation', __name__, url_prefix='/docs')

@bp.route('/project-readme')
def project_readme():
    """Render the main project README."""
    return render_template('documentation/project_readme.html', menu=utils.get_menu())

@bp.route('/changelog')
def changelog():
    """Show the project changelog."""
    return render_template('documentation/changelog.html', menu=utils.get_menu())

@bp.route('/qa-audit-index')
def qa_audit_index():
    """Overview page for QA audit reports."""
    return render_template('documentation/qa_audit_index.html', menu=utils.get_menu())

@bp.route('/task-list')
def task_list():
    """Display the internal task list."""
    return render_template('documentation/task_list.html', menu=utils.get_menu())

@bp.route('/delete-candidates')
def delete_candidates():
    """List documentation pages marked for potential deletion."""
    return render_template('documentation/delete_candidates.html', menu=utils.get_menu())

@bp.route('/sitemap')
def sitemap():
    """Site map for navigating documentation pages."""
    return render_template('documentation/sitemap.html', menu=utils.get_menu())

@bp.route('/api-reference')
def api_reference():
    """API reference index page."""
    return render_template('documentation/api_reference.html', menu=utils.get_menu())

@bp.route('/how-to-guides')
def how_to_guides():
    """Entry point for how-to guides."""
    return render_template('documentation/how_to_guides.html', menu=utils.get_menu())

@bp.route('/all')
def docs_all():
    """Unified documentation index with all how-to pages."""
    return render_template('docs/docs_all.html', menu=utils.get_menu())

@bp.route('/faq')
def faq():
    """Frequently asked questions."""
    return render_template('documentation/faq.html', menu=utils.get_menu())

@bp.route('/howto-home')
def howto_home():
    """How-to guide: Home page."""
    return render_template('documentation/howto_home.html', menu=utils.get_menu())

@bp.route('/howto-upload')
def howto_upload():
    """Guide for uploading artwork."""
    return render_template('documentation/howto_upload.html', menu=utils.get_menu())

@bp.route('/howto-analyze')
def howto_analyze():
    """Guide for running AI analysis."""
    return render_template('documentation/howto_analyze.html', menu=utils.get_menu())

@bp.route('/howto-gallery')
def howto_gallery():
    """Guide to the gallery views."""
    return render_template('documentation/howto_gallery.html', menu=utils.get_menu())

@bp.route('/howto-exports')
def howto_exports():
    """Guide for exporting listings."""
    return render_template('documentation/howto_exports.html', menu=utils.get_menu())

@bp.route('/howto-whisperer')
def howto_whisperer():
    """Guide for the Prompt Whisperer tool."""
    return render_template('documentation/howto_whisperer.html', menu=utils.get_menu())

```

---
## 📄 `ezygallery/routes/admin_routes.py`

```py
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

```

---
## 📄 `ezygallery/static/css/legacy_style_unused.css`

```css
/* Legacy stylesheet retained for reference. All rules now split into base.css, layout.css, theme.css and components.css */
/* ==============================
   ART Narrator Mockup Selector & Approval UI
   Full Style Sheet — Robbie Mode™
   ============================== */

/* --------- [ 0. Global Styles & Variables ] --------- */
:root {
  --main-bg: #f9f9f9;
  --main-txt: #222;
  --accent: #000000;
  --accent-dark: #414141;
  --border: #ddd;
  --card-bg: #fff;
  --shadow: 0 2px 6px rgba(0,0,0,0.06);
  --radius: 0px;
  --thumb-radius: 0px;
  --menu-height: 64px;
  --gallery-gap: 2em;
}

body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
  background: var(--main-bg);
  color: var(--main-txt);
  margin: 0;
  padding: 0;
  min-height: 100vh;
}

/* --------- [ 1. Header/Menu/Nav ] --------- */
header, nav, .main-nav {
  background: var(--accent);
  color: #fff;
  height: var(--menu-height);
  display: flex;
  align-items: center;
  padding: 0 2em;
  font-size: 1.08em;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  gap: 1.7em;
}
nav a, .main-nav a {
  color: #fff;
  text-decoration: none;
  margin-right: 2em;
  font-weight: 500;
  letter-spacing: 0.01em;
  transition: color 0.2s;
}
nav a:hover,
nav a.active,
.main-nav a:hover { color: #ffe873; }

.logo {
  font-size: 1.22em;
  font-weight: bold;
  margin-right: 2.5em;
  letter-spacing: 0.04em;
}

/* --------- [ 2. Main Layout ] --------- */
main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2.5em 1em 2em 1em;
}
@media (max-width: 700px) {
  main { padding: 1.1em 0.4em; }
}

/* === [RA.1] Review Artwork Grid Layout === */
.review-artwork-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 38px;
  justify-content: center;
  align-items: flex-start;
  max-width: 1400px;
  margin: 2.5em auto;
}
.mockup-col {
  flex: 1 1 0;
  min-width: 340px;
  max-width: 540px;
  display: block;
}
.main-thumb {
  text-align: center;
  margin-bottom: 1.5em;
}
.main-thumbnail-img {
  max-width: 300px;
  border-radius: 0px;
  box-shadow: 0 2px 12px #0002;
  cursor: pointer;
}
.thumb-note {
  font-size: 0.96em;
  color: #888;
  margin-top: 0.4em;
}

h3, .mockup-previews-title {
  margin: 0 0 18px 0;
  font-weight: 700;
  font-size: 1.23em;
}
.mockup-preview-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}
.mockup-card {
  background: #fff;
  border-radius: 0px;
  box-shadow: 0 2px 10px #0001;
  padding: 11px 7px;
  text-align: center;
}
.mockup-thumb-img {
  width: 100%;
  border-radius: 0px;
  margin-bottom: 6px;
  box-shadow: 0 1px 6px rgba(0,0,0,0.09);
  background: #eee;
  cursor: pointer;
  transition: box-shadow 0.15s;
}
.mockup-thumb-img:focus { outline: 2.5px solid var(--accent); }
.mockup-number { font-size: 0.96em; margin-bottom: 6px; }
form { margin: 0.3em 0; display: inline; }
select {
  margin: 2px 0 0 0px;
  border-radius: 0px;
  padding: 2px 8px;
  font-size: 0.97em;
}
.btn, .btn-sm {
  padding: 4px 12px;
  border-radius: 0px;
  font-size: 1em;
  background: #f7f7f7;
  border: 1px solid #bbb;
  cursor: pointer;
  transition: background 0.18s, border 0.18s;
}
.btn-primary {
  background: var(--accent);
  color: #fff;
  border: none;
}

.btn-primary:hover,
.btn:hover { background: #d1f8da; }
.btn-primary:hover { background: var(--accent-dark); color: #ffe873; }
.btn-danger:hover { background: var(--accent-dark); color: #ff6868; }

/* === [CA.ARTY-BUTTONS] ART Narrator Black Button Style === */
.btn-black {
  background: #000 !important;
  color: #fff !important;
  border: none !important;
  border-radius: 0 !important;
  font-weight: bold;
  font-size: 1.06em;
  letter-spacing: 0.01em;
  padding: 0.8em 1.6em;
  display: inline-block;
  cursor: pointer;
  transition: background 0.16s, color 0.16s;
  margin: 0.2em 0;
  box-shadow: 0 1px 6px rgba(0,0,0,0.07);
  text-align: center;
  text-decoration: none;
}
.btn-black:hover, .btn-black:focus {
  background: #222 !important;
  color: #ffe873 !important;
  text-decoration: none;
}

.btn-black.btn-disabled, .btn-black[disabled] {
  pointer-events: none;
  opacity: 0.45;
  filter: grayscale(0.3);
}

.desc-col {
  flex: 1 1 0;
  min-width: 340px;
  max-width: 600px;
  display: block;
}
h1 { font-size: 2em; line-height: 1.3; text-align: center; margin-bottom: 0.9em; }
.desc-panel {
  margin-bottom: 1.7em;
  background: #fafbfc;
  border-radius: 0px;
  box-shadow: 0 1px 4px #0001;
  padding: 16px;
  overflow-x: auto;
}
.desc-panel h2 { margin-bottom: 10px; font-size: 1.13em; }
.desc-text {
  white-space: pre-wrap;
  background: #fafbfc;
  border-radius: 0px;
  box-shadow: 0 1px 4px #0001;
  padding: 16px;
  min-height: 110px;
  max-height: 350px;
  overflow-y: auto;
  font-size: 1.05em;
}
.desc-panel pre {
  white-space: pre-wrap;
  background: #fafbfc;
  border-radius: 0px;
  box-shadow: 0 1px 4px #0001;
  padding: 16px;
  min-height: 110px;
  max-height: 350px;
  overflow-y: auto;
  font-size: 1.05em;
}
.artist-bio {
  background: #fafbfc;
  border-radius: 0px;
  box-shadow: 0 1px 4px #0001;
  padding: 16px;
  white-space: pre-line;
  font-size: 1.05em;
  margin-bottom: 2em;
}
.colour-info-grid {
  display: flex;
  gap: 22px;
  justify-content: center;
  margin-bottom: 2.2em;
}
.colour-info-grid .label {
  font-weight: 600;
  font-size: 1.02em;
  margin-bottom: 5px;
}
.colour-box {
  background: #fcfcfc;
  border-radius: 0px;
  border: 1px solid #e2e4e8;
  min-height: 38px;
  padding: 7px 12px;
  font-size: 0.97em;
  white-space: pre-line;
  overflow-x: auto;
}
.reanalyse-label {
  margin-bottom: 10px;
  font-size: 1.07em;
  font-weight: 500;
}
textarea {
  width: 100%;
  max-width: 400px;
  padding: 10px;
  border-radius: 0px;
  border: 1px solid #ccd2da;
  resize: vertical;
  font-size: 1em;
  margin-bottom: 9px;
}
.back-link {
  text-align: center;
  margin-top: 1.4em;
}
.back-link a {
  font-size: 1em;
  color: #6c38b1;
  padding: 7px 18px;
  text-decoration: underline;
}
.card-img-top {
  max-width: 100%;
  max-height: 300px;
  object-fit: cover;
  object-position: center;
}

/* --------- [ 6. Modal/Fullscreen Image View — Borderless Edition ] --------- */
.modal-bg {
  display: none;
  position: fixed; z-index: 99;
  left: 0; top: 0; width: 100vw; height: 100vh;
  background: rgba(34,34,34,0.68);
  align-items: center; justify-content: center;
}
.modal-bg.active { display: flex !important; }

.modal-img {
  background: transparent !important;
  border-radius: 0 !important;
  padding: 0 !important;
  max-width: 94vw;
  max-height: 93vh;
  box-shadow: 0 5px 26px rgba(0,0,0,0.22);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-img img {
  max-width: 88vw;
  max-height: 80vh;
  border-radius: 0 !important;
  border: none !important;
  background: none !important;
  display: block;
  box-shadow: none !important;
}

.modal-close {
  position: absolute;
  top: 2.3vh;
  right: 2.6vw;
  font-size: 2em;
  color: #fff;
  background: none;
  border: none;
  cursor: pointer;
  z-index: 101;
  text-shadow: 0 2px 6px #000;
}
.modal-close:focus { outline: 2px solid #ffe873; }

/* --------- [ 7. Footer ] --------- */
footer, .gallery-footer {
  text-align: center;
  margin-top: 4em;
  padding: 1.2em 0;
  font-size: 1em;
  color: #777;
  background: #f2f2f2;
  border-top: 1px solid #ececec;
  letter-spacing: 0.01em;
}
footer a { color: var(--accent); text-decoration: underline; }
footer a:hover { color: var(--accent-dark); }

/* --------- [ 8. Light/Dark Mode Ready ] --------- */
body.dark, .dark main {
  background: #191e23 !important;
  color: #f1f1f1 !important;
}
body.dark header, body.dark nav {
  background: #14171a;
  color: #eee;
}
body.dark .item, body.dark .gallery-item,
body.dark .desc-panel, body.dark .modal-img {
  background: #252b30;
  color: #eaeaea;
  border-color: #444;
}
body.dark .desc-panel { box-shadow: 0 3px 10px rgba(0,0,0,0.33); }
body.dark .gallery-footer, body.dark footer {
  background: #1a1a1a;
  color: #bbb;
  border-top: 1px solid #252b30;
}

:focus-visible {
  outline: 2.2px solid #ffa52a;
  outline-offset: 1.5px;
}
@media print {
  header, nav, .composite-btn, .btn, button, select, .gallery-footer, footer { display: none !important; }
  .desc-panel { border: none !important; box-shadow: none !important; }
  body { background: #fff !important; color: #222 !important; }
  main { padding: 0 !important; }
}

/* --------- [ 10. Misc — Spacing, Inputs, Forms ] --------- */
label { display: inline-block; margin-bottom: 0.2em; font-weight: 500; }
input, textarea {
  border: 1px solid #bbb;
  border-radius: 0px;
  padding: 0.3em 0.55em;
  font-size: 1em;
  background: #fff;
  color: #232324;
}
input:focus, textarea:focus { border-color: var(--accent); }
::-webkit-scrollbar { width: 9px; background: #eee; border-radius: 5px; }
::-webkit-scrollbar-thumb { background: #ccc; border-radius: 0px; }
::-webkit-scrollbar-thumb:hover { background: #aaa; }

/* Responsive tweaks */
@media (max-width: 1200px) {
  .review-artwork-grid { max-width: 98vw; }
}
@media (max-width: 900px) {
  .review-artwork-grid { flex-direction: column; gap: 2em; }
  .mockup-col, .desc-col { max-width: 100%; min-width: 0; }
  .mockup-preview-grid { grid-template-columns: repeat(2,1fr); }
}
@media (max-width: 600px) {
  .mockup-preview-grid { grid-template-columns: 1fr; gap: 0.9em; }
  .review-artwork-grid { margin: 1.2em 0.2em; }
  .main-thumb { margin-bottom: 1em; }
  .desc-panel { padding: 1em 0.6em; }
}


/* ===============================
   [ ART Narrator Artwork Gallery Grid ]
   =============================== */
.gallery-section {
  margin: 2.5em auto 3.5em auto;
  max-width: 1250px;
  padding: 0 1em;
}
.artwork-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2.4em;
  margin-bottom: 2em;
}
.gallery-card {
  background: var(--card-bg);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: box-shadow 0.18s, transform 0.12s;
  min-height: 365px;
  padding: 10px;
  overflow: hidden;
}
.gallery-card:hover {
  box-shadow: 0 4px 16px #0002;
  transform: translateY(-4px) scale(1.013);
}
.card-thumb {
  width: 100%;
  background: #f4f4f4;
  text-align: center;
  padding: 22px 0 7px 0;
}
.card-img-top {
  max-width: 94%;
  max-height: 210px;
  border-radius: var(--thumb-radius);
  object-fit: cover;
  box-shadow: 0 1px 7px #0001;
  background: #fafafa;
}
.card-details {
  flex: 1 1 auto;
  width: 100%;
  text-align: center;
  padding: 12px 13px 20px 13px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.card-title {
  font-size: 0.9em;
  font-weight: 400;
  margin-bottom: 7px;
  line-height: 1.2;
  color: var(--main-txt);
  min-height: 3em;
}
.btn, .btn-primary, .btn-secondary {
  margin-top: 7px;
  width: 90%;
  min-width: 90px;
  align-self: center;
}

.flash {
  background: #ffe6e6;
  border: 1px solid #f5b5b5;
  color: #740000;
  border-radius: 6px;
  padding: 10px 14px;
  margin-bottom: 1.2em;
}
.flash ul { margin: 0; padding-left: 1.2em; }
@media (max-width: 800px) {
  .artwork-grid { gap: 1.3em; }
  .card-thumb { padding: 12px 0 4px 0; }
  .card-title { font-size: 1em; }
}

/* === Finalised Gallery === */
.finalised-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.6em;
  margin-top: 1.5em;
  justify-content: center;
}
.finalised-grid.list-view {
  display: block;
}
.finalised-grid.list-view .final-card {
  flex-direction: row;
  max-width: none;
  margin-bottom: 1em;
}
.finalised-grid.list-view .card-thumb {
  width: 150px;
  margin-right: 1em;
}
.final-card {
  background: var(--card-bg);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 10px;
  display: flex;
  flex-direction: column;
  max-width: 350px;
  margin: 0 auto;
}
.final-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-top: auto;
}
.final-actions .btn {
  flex: 1 1 auto;
  min-width: 100px;
  width: auto;
  margin-top: 0;
}
.edit-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-top: 1em;
}
.edit-actions .btn {
  flex: 1 1 auto;
  min-width: 100px;
  width: auto;
  margin-top: 0;
}
.finalised-badge {
  font-size: 0.9em;
  color: #d40000;
  align-self: center;
  padding: 4px 8px;
}
.view-toggle {
  margin-top: 0.5em;
}
.view-toggle button {
  margin-right: 0.5em;
}
.locked-badge {
  font-size: 0.9em;
  color: #0066aa;
  padding: 2px 6px;
  border: 1px solid #0066aa;
  margin-left: 6px;
}
.mini-mockup-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 4px;
  margin-top: 6px;
}
.mini-mockup-grid img {
  width: 100%;
  max-height: 120px;
  object-fit: contain;
  border-radius: 4px;
  box-shadow: 0 1px 4px #0001;
}
.desc-snippet {
  font-size: 0.92em;
  margin: 4px 0 8px 0;
  line-height: 1.3;
}
@media (max-width: 800px) {
  .finalised-grid {
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  }
}

/* ===============================
   [ Edit Artwork Listing Page ]
   =============================== */
/* --- Edit Action Buttons Area --- */
.edit-listing-col {
  max-width: 540px;
  width: 100%;
}

.long-field {
  width: 100%;
  max-width: 540px;
  box-sizing: border-box;
  font-size: 1.05em;
  padding: 0.6em;
  margin-bottom: 1em;
  border-radius: 0 !important;   /* FORCE SQUARE */
}

.price-sku-row,
.row-inline {
  display: flex;
  gap: 1em;
}
.price-sku-row > div,
.row-inline > div {
  flex: 1;
}

.edit-actions-col {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 0.7em;
  margin: 2em 0 0 0;
  width: 100%;
  max-width: 540px;
}

.wide-btn {
  width: 100%;
  font-size: 1.12em;
  font-weight: bold;
  padding: 1em 0;
  border-radius: 0 !important;   /* FORCE SQUARE */
}

/* ====== SQUARE CORNERS: NO ROUNDING ANYWHERE ====== */
input,
textarea,
select,
button,
.mockup-thumb-img,
.main-thumbnail-img,
.mockup-card,
.swap-form,
.edit-listing-col,
.flash-error,
form,
.mockup-preview-grid,
.main-thumb {
  border-radius: 0 !important;
}

/* ====== SQUARE IMAGE THUMBNAILS ====== */
.mockup-thumb-img, .main-thumbnail-img {
  border-radius: 0 !important;
  border: 1px solid #eee;
  box-shadow: none;
  width: 100%;
  height: auto;
  display: block;
}

/* Other style fixes */
.flash-error {
  background: #fbeaea;
  color: #a60000;
  border-left: 5px solid #e10000;
  margin-bottom: 1.5em;
  padding: 1em;
  border-radius: 0 !important;
}
.status-line {
  font-weight: bold;
  font-size: 1.2em;
  margin-bottom: 1.1em;
}
.status-finalised { color: #c00; }
.status-pending { color: #ef7300; }

.missing-img {
  width: 100%;
  padding: 20px 0;
  background: #eee;
  color: #777;
  font-size: 0.9em;
  border-radius: 0 !important;
}
.empty-msg {
  text-align: center;
  margin: 2em 0;
  font-size: 1.2em;
  color: #555;
  border-radius: 0 !important;
}

/* Responsive - match what you want */
@media (max-width: 800px) {
  .edit-listing-col, .review-artwork-grid { padding: 1em; }
  .row-inline, .price-sku-row { flex-direction: column; gap: 0.5em; }
}

/* ===============================
   [ Upload Dropzone ]
   =============================== */
.upload-dropzone {
  border: 2px dashed #bbb;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  color: #666;
  transition: background 0.2s, border-color 0.2s;
}
.upload-dropzone.dragover {
  border-color: #333;
  background: #f9f9f9;
}

.upload-list {
  margin-top: 1em;
  list-style: none;
  padding: 0;
  font-size: 0.9rem;
}
.upload-list li {
  margin: 0.2em 0;
}
.upload-list li.success { color: green; }
.upload-list li.error { color: red; }

.upload-progress {
  position: relative;
  background: #eee;
  height: 8px;
  margin: 2px 0;
  width: 100%;
  overflow: hidden;
}
.upload-progress-bar {
  background: var(--accent);
  height: 100%;
  width: 0;
  transition: width 0.2s;
}
.upload-percent {
  margin-left: 4px;
  font-size: 0.8em;
}

/* --------- [ Workflow Step Grid ] --------- */
.workflow-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1em;
  margin: 2em 0;
}
.step-btn {
  display: block;
  padding: 0.8em;
  background: var(--accent);
  color: #fff;
  text-align: center;
  text-decoration: none;
  border-radius: var(--radius);
}
.step-btn.disabled {
  background: #ccc;
  pointer-events: none;
  color: #666;
}

/* --------- [ Analysis Progress Modal ] --------- */
.analysis-modal {
  display: none;
  position: fixed;
  z-index: 100;
  left: 0;
  top: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.65);
  align-items: center;
  justify-content: center;
}
.analysis-modal.active { display: flex; }

.analysis-box {
  background: #fff;
  padding: 1em 1.2em;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}
.analysis-log {
  font-family: monospace;
  background: #fafbfc;
  border: 1px solid #ddd;
  padding: 0.6em;
  max-height: 60vh;
  overflow-y: auto;
  white-space: pre-wrap;
  font-size: 0.92em;
}
.analysis-log .log-error { color: #b00; }
.analysis-log .latest { background: #eef; }

.analysis-progress {
  background: #eee;
  height: 10px;
  margin: 0.5em 0;
  width: 100%;
}
.analysis-progress-bar {
  background: var(--accent);
  height: 100%;
  width: 0;
  transition: width 0.3s ease;
}
.analysis-status {
  font-size: 0.9em;
  margin-bottom: 0.6em;
}
.analysis-friendly {
  text-align: center;
  font-size: 0.9em;
  margin-top: 0.6em;
  font-style: italic;
}

/* ===============================
   [ OpenAI Details Table ]
   =============================== */
.openai-details table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 2em;
  font-size: 0.8em;    /* smaller for both columns */
  table-layout: fixed;
}

.openai-details th,
.openai-details td {
  padding-bottom: 0.35em;
  vertical-align: top;
  word-break: break-word;
}

/* Make the first column (labels) nice and wide, second takes rest */
.openai-details th {
  width: 105px;    /* adjust as needed for your headings */
  min-width: 95px;
  font-weight: 600;
  text-align: left;
  font-size: 0.8em;
  white-space: nowrap;   /* keep all on one line */
  padding-bottom: 10px;
  padding-right: 1em;
}

.openai-details td {
  font-size: 0.8em;
}

@media (max-width: 650px) {
  .openai-details th {
    width: 110px;
    min-width: 90px;
    font-size: 0.8em;
  }
  .openai-details td {
    font-size: 0.8em;
  }
}

.openai-details table tr:nth-child(even) {
  background: #dddddd;
}

.openai-details th,
.openai-details td {
  padding: 0.33em 0.6em 0.33em 0.3em;
}

/* ===============================
   [ Sellbrite Exports ]
   =============================== */
.export-actions { margin-bottom: 1em; }
.exports-table { width: 100%; border-collapse: collapse; }
.exports-table th, .exports-table td { padding: 0.4em 0.6em; border-bottom: 1px solid #ddd; }
.exports-table tr:nth-child(even) { background: #f5f5f5; }
.export-log { background: #f5f5f5; padding: 1em; white-space: pre-wrap; }
```

---
## 📄 `ezygallery/static/css/custom.css`

```css
/* Custom styles extracted from existing stylesheets for easier management */

/* From style.css starting line 60 */
/* --- [3] Header Styles --- */
.site-header {
    padding: 1.5rem 2rem;
    border-bottom: 1px solid var(--border-color-light);
    position: relative;
    z-index: 1000;
}

html.overlay-open .site-header {
    display: none;
}
html.overlay-open #menuToggle {
    display: none; /* Hide menu button when overlay is active */
}

html.dark .site-header {
    border-bottom-color: var(--border-color-dark);
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 1rem;
    width: 100%;
}

.header-left, .header-right {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex: 1;
}

.header-center {
    flex: 0 1 auto;
    text-align: center;
}

/* Primary horizontal navigation */
.main-nav {
    display: inline-block;
    margin-right: 1rem;
}
.main-nav-links {
    display: flex;
    gap: 1.2rem;
    list-style: none;
    padding: 0;
    margin: 0;
}
.main-nav a {
    text-decoration: none;
    font-size: 0.95rem;
    color: var(--text-color-light);
}
html.dark .main-nav a {
    color: var(--text-color-dark);
}
.main-nav a:hover {
    text-decoration: underline;
}

.header-right {
    justify-content: flex-end;
}

.logo, .cart, .menu-toggle {
    color: var(--text-color-light);
    text-decoration: none;
    font-weight: 500;
    white-space: nowrap;
}

html.dark .logo, html.dark .cart, html.dark .menu-toggle {
    color: var(--text-color-dark);
}

.menu-toggle {
    background: none;
    border: 1px solid var(--text-color-light);
    padding: 0.5rem 1rem;
    cursor: pointer;
    border-radius: 0;
    font-family: monospace;
    font-size: 1rem;
    transition: background-color 0.2s, color 0.2s;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}

html.dark .menu-toggle {
    border-color: var(--text-color-dark);
}

.menu-toggle:hover {
    background-color: var(--text-color-light);
    color: var(--bg-color-light);
}

html.dark .menu-toggle:hover {
    background-color: var(--text-color-dark);
    color: var(--bg-color-dark);
}

/* --- [4] Icon Styles --- */
.header-icon {
    width: 24px;
    height: 24px;
    vertical-align: middle;
}

.arrow-icon {
    width: 20px;
    height: 20px;
}

html.dark .header-icon {
    filter: invert(1);
}

.menu-toggle:hover .header-icon {
    filter: invert(1);
}
html.dark .menu-toggle:hover .header-icon {
    filter: none;
}


.header-icon-link, .theme-toggle-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: none;
    border: none;
    padding: 0.25rem;
    cursor: pointer;
    border-radius: 0;
    transition: background-color 0.2s;
}

.header-icon-link:hover, .theme-toggle-btn:hover {
    background-color: rgba(0,0,0,0.05);
}

html.dark .header-icon-link:hover, html.dark .theme-toggle-btn:hover {
    background-color: rgba(255,255,255,0.1);
}


/* --- [5] Main Overlay Menu Styles --- */
#overlayMenu {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 2000;
    visibility: hidden;
    opacity: 0;
    transition: opacity 0.4s cubic-bezier(0.25, 1, 0.5, 1), visibility 0.4s cubic-bezier(0.25, 1, 0.5, 1);
    background-color: var(--overlay-bg-light);
    -webkit-backdrop-filter: blur(15px);
    backdrop-filter: blur(15px);
    display: flex;
    align-items: center; /* Center content vertically */
    justify-content: center; /* Center content horizontally */
    overflow-y: auto;
}

html.dark #overlayMenu {
    background-color: var(--overlay-bg-dark);
}

#overlayMenu .overlay-close {
    position: absolute;
    top: 1.5rem;
    right: 2rem;
    background: none;
    border: none;
    font-size: 2.5rem;           /* Large enough for comfortable taps */
    line-height: 1;
    padding: 0.25em;              /* Increase tap target */
    color: var(--text-color-light);
    cursor: pointer;
}

html.dark #overlayMenu .overlay-close {
    color: var(--text-color-dark);
}

#overlayMenu .overlay-close:focus {
    outline: 2px solid var(--accent-color-light);
}

html.dark #overlayMenu .overlay-close:focus {
    outline-color: var(--accent-color-dark);
}

#overlayMenu.is-active {
    visibility: visible;
    opacity: 1;
}

.overlay-header {
    position: absolute; /* Changed from fixed */
    top: 0;
    left: 0;
    width: 100%;
    padding: 1.5rem 2rem;
    box-sizing: border-box;
    z-index: 1001; /* Ensure header is on top of content */
}

.overlay-content {
    text-align: center;
    width: 90%;
    max-width: 900px;
    padding: 6rem 0; /* Adjust padding to not be obscured by header */
}

.overlay-columns {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 2rem;
}

.overlay-col ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

/* Overlay link list */
.overlay-links {
    list-style: none;
    padding: 0;
    margin: 0;
}

.overlay-links li {
    font-size: clamp(1.25rem, 5vw, 2rem);
    font-weight: 500;
    line-height: 1.4;
    margin: 0.5em 0;
    transform: translateY(20px);
    opacity: 0;
    transition: opacity 0.5s ease, transform 0.5s ease;
}

#overlayMenu.is-active .overlay-links li {
    transform: translateY(0);
    opacity: 1;
}

/* Staggered animation */
#overlayMenu.is-active .overlay-links li:nth-child(1) { transition-delay: 0.25s; }
#overlayMenu.is-active .overlay-links li:nth-child(2) { transition-delay: 0.30s; }
#overlayMenu.is-active .overlay-links li:nth-child(3) { transition-delay: 0.35s; }
#overlayMenu.is-active .overlay-links li:nth-child(4) { transition-delay: 0.40s; }
#overlayMenu.is-active .overlay-links li:nth-child(5) { transition-delay: 0.45s; }
#overlayMenu.is-active .overlay-links li:nth-child(6) { transition-delay: 0.50s; }
#overlayMenu.is-active .overlay-links li:nth-child(7) { transition-delay: 0.55s; }

.overlay-content a {
    color: var(--text-color-light);
    text-decoration: none;
    transition: color 0.3s ease;
}

.menu-header {
    font-size: 0.9em;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-top: 1.2em;
    color: var(--accent-color-light);
}

html.dark .overlay-content a {
    color: var(--text-color-dark);
}

html.dark .menu-header {
    color: var(--accent-color-dark);
}

.overlay-content a:hover {
    color: var(--accent-color-light);
}

html.dark .overlay-content a:hover {
    color: var(--accent-color-dark);
}

/* --- [7] Main Content & Footer Styles --- */
.main-content {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
    flex-grow: 1;
}

.site-footer {
    background-color: var(--bg-color-light);
    border-top: 1px solid var(--border-color-light);
    padding: 3rem 2rem;
    color: var(--text-color-light);
}

html.dark .site-footer {
    background-color: var(--bg-color-dark);
    border-top-color: var(--border-color-dark);
    color: var(--text-color-dark);
}

.footer-content {
    max-width: 1600px;
    margin: 0 auto;
}

.footer-columns {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.footer-col h4 {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 1rem;
}

.footer-col p {
    font-size: 0.9rem;
    line-height: 1.6;
    opacity: 0.8;
}

.footer-col ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.footer-col ul li {
    margin-bottom: 0.5rem;
}

.footer-col a {
    color: var(--text-color-light);
    text-decoration: none;
    opacity: 0.8;
    transition: opacity 0.2s;
}

html.dark .footer-col a {
    color: var(--text-color-dark);
}

.footer-col a:hover {
    opacity: 1;
    text-decoration: underline;
}

.newsletter-form {
    display: flex;
}

.newsletter-form input {
    flex-grow: 1;
    border: 1px solid var(--border-color-light);
    border-right: none;
    padding: 0.75rem;
    background: transparent;
    color: var(--text-color-light);
    font-family: monospace;
}
html.dark .newsletter-form input {
    border-color: var(--border-color-dark);
    color: var(--text-color-dark);
}

.newsletter-form button {
    background: transparent;
    border: 1px solid var(--border-color-light);
    padding: 0.5rem;
    cursor: pointer;
}
html.dark .newsletter-form button {
    border-color: var(--border-color-dark);
}

/* Documentation layout */
.docs-layout {
    display: flex;
    gap: 2rem;
    align-items: flex-start;
}
.doc-sidebar {
    flex: 0 0 200px;
    position: sticky;
    top: 5rem;
    align-self: flex-start;
}
.doc-sidebar ul {
    list-style: none;
    padding: 0;
    margin: 0;
}
.doc-sidebar li {
    margin-bottom: 0.5rem;
}
.doc-sidebar a {
    text-decoration: none;
    font-weight: 500;
    color: var(--text-color-light);
}
html.dark .doc-sidebar a { color: var(--text-color-dark); }
.doc-sidebar a:hover { text-decoration: underline; }

.docs-main {
    flex: 1;
}

.copyright-bar {
    border-top: 1px solid var(--border-color-light);
    padding-top: 1.5rem;
    margin-top: 2rem;
    text-align: center;
    font-size: 0.8rem;
    opacity: 0.7;
}
html.dark .copyright-bar {
    border-top-color: var(--border-color-dark);
}

/* --- [8] Responsive Styles for Mobile --- */
@media (max-width: 768px) {
    .overlay-links li {
        font-size: clamp(1.1rem, 5.5vw, 1.6rem);
    }
    .main-nav { display: none; }
    .docs-layout { flex-direction: column; }
    .doc-sidebar { position: static; width: 100%; }
}

@media (max-width: 600px) {
    .header-left, .header-right {
        gap: 0.5rem; /* Reduce spacing between header elements */
    }
    .menu-toggle {
        padding: 0.35rem 0.7rem;
        font-size: 0.8rem; /* Slightly smaller button text */
    }
    .header-icon {
        width: 19px;
        height: 19px;
    }
    .arrow-icon {
        width: 16px;
        height: 16px;
    }
    .logo {
        font-size: 0.8rem; /* Scale logo text down */
    }
    .overlay-links li {
        font-size: 1.4rem; /* Smaller overlay menu text */
        line-height: 1.3;
    }
    .overlay-columns { grid-template-columns: 1fr; }
}

/* From components.css line 960 */

.login-bypass-banner {
  background: #333;
  color: #fff;
  text-align: center;
  padding: 0.6em;
  font-weight: 600;
}

/* -------------------------------------------------------
   Styles extracted from templates (inline <style> blocks)
   ------------------------------------------------------- */

/* From dws_editor.html */
.dws-container {
    display: flex;
    gap: 2em;
    align-items: flex-start;
    max-width: 1400px;
    margin: 0 auto;
}
.dws-sidebar {
    width: 300px;
    flex-shrink: 0;
    background-color: var(--card-bg);
    padding: 1.5em;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    border: 1px solid var(--border);
}
.dws-main-content { flex-grow: 1; }
.dws-sidebar h1, .dws-sidebar h2 { text-align: left; margin-bottom: 0.5em; }
.dws-sidebar h1 { font-size: 1.5em; margin-bottom: 1em; }
.dws-sidebar h2 { font-size: 1.2em; margin-top: 1.5em; border-bottom: 1px solid var(--border); padding-bottom: 0.3em; }
.dws-sidebar .btn-black { width: 100%; margin-bottom: 0.75em; }
.dws-rules-box {
    background-color: #f7f7f7;
    padding: 1em;
    margin-top: 1em;
    border-radius: var(--radius);
}
.dws-rules-box label { font-weight: 500; font-size: 0.9em; }
.dws-rules-box input,
.dws-rules-box select { width: 100%; box-sizing: border-box; margin-top: 0.2em; margin-bottom: 0.8em; }
.paragraph-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    padding: 1.5em;
    margin-bottom: 1em;
    box-shadow: var(--shadow);
    transition: box-shadow 0.2s ease-in-out;
    border-radius: var(--radius);
}
.paragraph-card:hover { box-shadow: 0 6px 12px rgba(0,0,0,0.1); }
.paragraph-card-header {
    display: flex;
    align-items: center;
    margin-bottom: 1em;
    gap: 0.8em;
}
.drag-handle { cursor: grab; font-size: 1.5em; color: #999; }
.pinned-placeholder { width: 1.5em; }
.paragraph-card-header input[type="text"] {
    font-size: 1.2em;
    font-weight: bold;
    border: none;
    background: transparent;
    padding: 0.2em;
    width: 100%;
}
.paragraph-card-header input[type="text"]:focus { background: #f0f0f0; }
.paragraph-card textarea {
    width: 100%;
    box-sizing: border-box;
    height: 150px;
    resize: vertical;
    padding: 0.8em;
    font-size: 1em;
    line-height: 1.6;
}
.ai-instruction-input {
    width: 100%;
    box-sizing: border-box;
    margin-top: 0.8em;
    padding: 0.5em;
    font-size: 0.9em;
    border: 1px solid #ddd;
}
.paragraph-card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1em;
    font-size: 0.9em;
}
.word-count-display.error { color: #c00; font-weight: bold; }
.count-separator { margin: 0 0.5em; }
.paragraph-card-actions .btn-card-action {
    margin-left: 0.5em;
    font-size: 0.9em;
    padding: 0.4em 0.8em;
    background: #f0f0f0;
    border: none;
    color: #333;
    cursor: pointer;
    transition: background-color 0.2s;
    font-weight: 500;
    border-radius: var(--radius);
    position: relative;
}
.paragraph-card-actions .btn-card-action:hover { background: #dcdcdc; }
.paragraph-card-actions .delete-btn:hover { background: #a60000; color: #fff; }
.sortable-ghost { opacity: 0.4; background: #eef; border: 1px dashed var(--accent); }
.sortable-chosen { cursor: grabbing; }
.modal-overlay {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.6);
    align-items: center;
    justify-content: center;
    z-index: 1000;
}
.modal-box {
    background: white;
    padding: 2em;
    max-width: 500px;
    width: 90%;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    border-radius: var(--radius);
}
.modal-box .btn { background: #f0f0f0; border: 1px solid #ccc; color: #333; }
#confirm-delete-btn:hover { background-color: #a60000 !important; }
.spinner-overlay {
    display: none;
    position: absolute;
    inset: 0;
    background: rgba(255, 255, 255, 0.8);
    align-items: center;
    justify-content: center;
}
.spinner-overlay.active {
    display: flex;
}
.spinner {
    border: 3px solid #f3f3f3;
    border-top: 3px solid #3498db;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    animation: spin 1s linear infinite;
}
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
.version-status { font-size: 0.85em; margin-bottom: 0.5em; }
.version-status .status-match { color: #28a745; font-weight: bold; }
.version-status .status-mismatch { color: #dc3545; font-weight: bold; }

/* From aigw.html */
.selector-grid { display:flex; flex-wrap:wrap; gap:1em; margin-bottom:1em; }
.selector-col { flex:1 1 200px; min-width:200px; display:flex; flex-direction:column; }
.summary-box {
    background: var(--card-bg);
    padding: 1em;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    max-width: 600px;
    margin-top: 2em;
}

/* Number icon treatment */
.step-num-icon {
  width: 70px;
  height: 70px;
  margin-right: 8px;
  vertical-align: middle;
}
.step-btn .step-num-icon {
  filter: brightness(0) invert(1);
}
.how-step .step-num-icon {
  filter: none;
}
.theme-dark .how-step .step-num-icon {
  filter: brightness(0) invert(1);
}
.theme-dark .step-num-icon {
  filter: brightness(0) invert(1);
}
.page-step-icon {
  display: block;
  margin: 0 auto 1em auto;
  max-width: 50px;
  width: 100%;
  height: auto;
}
.theme-dark .page-step-icon {
  filter: brightness(0) invert(1);
}
/* From auth/login.html */
.pw-wrap {
    position: relative;
    display: flex;
    align-items: center;
}
#password { width: 100%; padding-right: 2.6em; }
.pw-toggle-btn {
    position: absolute;
    right: 0.5em;
    top: 50%;
    transform: translateY(-50%);
    background: transparent;
    border: none;
    padding: 0;
    margin: 0;
    cursor: pointer;
    display: flex;
    align-items: center;
    height: 2.2em;
    width: 2.2em;
    color: var(--input-text);
    outline: none;
}
.pw-toggle-btn:focus { outline: 2px solid #ffe873; }
/* --------- [ Workflow Step Grid ] --------- */
.workflow-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1em;
  margin: 2em 0;
}
.step-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5em;
  padding: 0.6em 1em;
  background: transparent;
  color: var(--button-bg);
  border: 2px solid var(--button-bg);
  text-decoration: none;
  border-radius: var(--radius);
  transition: background 0.16s, color 0.16s;
}
.step-btn:hover {
  background: var(--button-bg);
  color: var(--button-text);
}
.step-btn.disabled {
  background: #555;
  border: 2px solid #555;
  pointer-events: none;
  color: #aaa;
}
/* From review.html inline styles */
.main-art-img { max-width: 360px; }
.thumb-img { max-width: 120px; }
.art-description { max-width: 431px; }

/* ===============================
   Upload Dropzone Enhancements
   =============================== */
.upload-container {
  position: relative;
  max-width: 600px;
  margin: 0 auto;
  width: 100%;
}
.upload-dropzone {
  border: 2px dashed var(--border);
  padding: 2em;
  text-align: center;
  cursor: pointer;
  color: var(--text-color-light);
  background: var(--bg-color-light);
  transition: background var(--transition-fast), border-color var(--transition-fast);
  min-height: 160px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  touch-action: manipulation;
}
html.dark .upload-dropzone {
  color: var(--text-color-dark);
  background: var(--bg-color-dark);
  border-color: var(--border-color-dark);
}
.upload-dropzone.dragover {
  border-color: var(--accent);
  background: var(--overlay-bg-light);
}
html.dark .upload-dropzone.dragover {
  background: var(--overlay-bg-dark);
}
.upload-container:focus .upload-dropzone {
  outline: 2px solid var(--accent);
  outline-offset: 4px;
}
.upload-dropzone.disabled {
  opacity: 0.6;
  pointer-events: none;
}
.dropzone-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 0.5em;
  pointer-events: none;
}
.dropzone-text {
  margin: 0;
  font-size: 1rem;
}
html.dark .spinner-overlay {
  background: rgba(0, 0, 0, 0.6);
}

/* === [GLOBAL INPUT STYLES] =============================================== */
.input,
.textarea,
.select {
  width: 100%;
  max-width: 100%;
  padding: 0.6em;
  font-size: 1em;
  border: 1px solid var(--border);
  background: var(--input-bg);
  color: var(--input-text);
  border-radius: 0;
}
.input:focus,
.textarea:focus,
.select:focus,
.btn:focus,
button:focus {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
.textarea { resize: vertical; }

/* ===============================================================
   [EL-CAROUSEL] Edit Listing Page Layout & Modal Carousel
   =============================================================== */
.edit-listing-container { max-width: 1200px; margin: 0 auto; }
.artwork-info-section { display: flex; flex-wrap: wrap; gap: 2em; }
.artwork-main-img { flex: 1 1 260px; min-width: 240px; text-align: center; }
.edit-form-section { flex: 2 1 360px; min-width: 260px; }
@media (max-width: 900px) {
  .artwork-info-section { flex-direction: column; }
}

.mockup-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
  margin-top: 1rem;
  margin-bottom: 2em;
}
@media (min-width: 600px) {
  .mockup-grid { grid-template-columns: repeat(3, 1fr); }
}
@media (min-width: 900px) {
  .mockup-grid { grid-template-columns: repeat(5, 1fr); }
}
.mockup-thumb {
  width: 100%;
  height: auto;
  cursor: zoom-in;
  object-fit: cover;
  border: 2px solid var(--border-color-light);
  display: block;
  margin: 0 auto;
  transition: box-shadow 0.18s, border-color 0.18s;
}
.mockup-thumb:hover { box-shadow: 0 0 10px #ccc; }
.mockup-thumb.current { border-color: var(--accent-color-light, #ed7214); }

/* ---------------------------------------------------------------
   [EL-MOCKUP-GRID] Hero image and 2x5 thumbnail grid
   --------------------------------------------------------------- */
.hero-image {
  text-align: center;
  margin-bottom: 1em;
}
.hero-image img {
  width: 100%;
  max-width: 520px;
  height: auto;
  display: block;
  margin: 0 auto 0.5em;
  cursor: zoom-in;
}

.carousel-modal {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.9);
  align-items: center;
  justify-content: center;
  z-index: 5000;
}
.carousel-modal.active { display: flex; }
.carousel-content {
  position: relative;
  max-width: 95vw;
  max-height: 95vh;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}
.carousel-img {
  max-width: 95vw;
  max-height: 60vh;
  margin-bottom: 0.8em;
  border-radius: 0;
  background: #222;
}
.carousel-nav {
  position: absolute;
  top: 50%;
  background: rgba(0,0,0,0.5);
  color: #fff;
  border: none;
  font-size: 2.4rem;
  cursor: pointer;
  padding: 0.3em 0.6em;
  border-radius: 0;
  z-index: 1;
  transform: translateY(-50%);
  transition: background 0.17s;
}
.carousel-nav.left { left: -70px; }
.carousel-nav.right { right: -70px; }
.carousel-close {
  position: absolute;
  top: 20px; right: 30px;
  background: none;
  color: #fff;
  border: none;
  font-size: 2.2rem;
  cursor: pointer;
}
.carousel-counter {
  color: #fff;
  margin-top: 0.6em;
  font-size: 1.2rem;
}
@media (max-width: 700px) {
  .carousel-nav.left { left: 10px; }
  .carousel-nav.right { right: 10px; }
  .carousel-img { max-height: 40vh; }
  .carousel-content { max-width: 99vw; }
}



```

---
## 📄 `ezygallery/static/css/theme.css`

```css
/* =====================================
   ART Narrator Theme Variables & Fonts
   Uses local variable fonts only
   ===================================== */

:root {
  --button-bg: #000;
  --button-text: #fff;
  --button-hover-bg: #222;
  --input-bg: #fafafa;
  --input-text: #222;
  --footer-bg: #ededed;
  --footer-txt: #444;
  --footer-link: #111;
  --footer-link-hover: #000;
  --link-hover: #f47b2fdc;
  --link-active: #f47b2fdc;
  --nav-bg: #f8f8f8;
}

.theme-light {
  --card-bg: var(--light-card-bg);
}

.theme-dark {
  --main-bg: var(--dark-bg);
  --main-txt: var(--dark-txt);
  --card-bg: var(--dark-card-bg);
  --accent: #fff;
  --accent-dark: #333;
  --border: #444;
  --button-bg: #111;
  --button-text: #fff;
  --button-hover-bg: #222;
  --input-bg: #222;
  --input-text: #fff;
  --footer-bg: var(--dark-bg);
  --footer-txt: var(--dark-txt);
  --footer-link: #fff;
  --footer-link-hover: #ffd700;
  --nav-bg: #111;
}

/* 🎨 Hover Backgrounds for Gallery Cards */
.theme-dark .gallery-card:hover {
  background-color: var(--dark-card-hover-bg);
}
.theme-light .gallery-card:hover {
  background-color: var(--light-card-hover-bg);
}

body {
  font-family: monospace;
  background: var(--main-bg);
  color: var(--main-txt);
  font-smooth: always;
  font-weight: 400;
  -webkit-font-smoothing: antialiased;
  margin: 0;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}

h1, h2, h3 {
  font-family: monospace;
  font-weight: 400;
  letter-spacing: 0.02em;
}
.brand-logo, .footer-brand {
  font-family: monospace;
  font-weight: 400;
  letter-spacing: 0.02em;
}

a {
  color: var(--footer-link);
  text-decoration: none;
  transition: color 0.2s, font-weight 0.2s;
}
a:hover, a:focus {
  color: var(--link-hover);
  font-weight: 600;
}

.skip-link {
  position: absolute;
  left: -999px;
  top: -999px;
  background: var(--nav-bg);
  color: var(--footer-link);
  padding: 0.5em 1em;
  z-index: 1000;
}
.skip-link:focus {
  left: 0.5em;
  top: 0.5em;
}

/* Navigation */
.site-nav {
  display: flex;
  align-items: center;
  background: var(--nav-bg);
  color: var(--footer-link);
  border-bottom: 1px solid var(--border);
  min-height: var(--menu-height);
  padding: 0 2em;
  font-family: monospace;
}
.brand-logo {
  font-size: 2em;
  font-weight: 400;
  color: var(--footer-link);
  text-decoration: none;
  letter-spacing: 0em;
  display: flex;
  align-items: center;
  margin-right: 2em;
  white-space: nowrap;
}
.brand-logo .brand-icon {
  width: 1.5em;
  height: 1.5em;
  margin-right: 0.4em;
}
.brand-logo:hover {
  color: var(--link-hover);
}
.brand-logo.active {
  color: var(--link-active);
}
.theme-dark .brand-icon {
  filter: brightness(0) invert(1);
}
.site-nav a {
  color: var(--footer-link);
  font-family: monospace;
  margin-right: 1.5em;
  white-space: nowrap;
  font-weight: 400;
  transition: color 0.2s;
}
.site-nav a:hover,
.site-nav a:focus {
  color: var(--link-hover);
}
.site-nav a.active {
  color: var(--link-active);
}

.theme-toggle {
  margin-left: auto;
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 0;
}
.theme-toggle img {
  width: 28px;
  height: 28px;
}
.theme-dark .theme-toggle img {
  filter: brightness(0) invert(1);
}
.theme-light .theme-toggle img {
  filter: none;
}

.nav-toggle {
  background: none;
  border: none;
  cursor: pointer;
  display: none;
  align-items: center;
  margin-left: auto;
  padding: 0;
}
.nav-toggle img {
  width: 28px;
  height: 28px;
}
.nav-toggle #icon-close {
  display: none;
}
.theme-dark .nav-toggle img {
  filter: brightness(0) invert(1);
}
.nav-toggle.open #icon-menu { display: none; }
.nav-toggle.open #icon-close { display: inline; }

.nav-links {
  display: flex;
  align-items: center;
  flex: 1;
}
.nav-links a { white-space: nowrap; }

/* Dropdown menus */
.dropdown { position: relative; }
.dropdown-toggle {
  background: none;
  border: none;
  cursor: pointer;
  font-weight: 400;
  margin-left:-10px;
  color: var(--footer-link);
}
.dropdown-toggle:hover,
.dropdown-toggle:focus { color: var(--link-hover); }
.dropdown-menu {
  display: none;
  position: absolute;
  top: calc(100% + 0.3em);
  left: 0;
  background: var(--nav-bg);
  border: 1px solid var(--border);
  list-style: none;
  padding: 0.5em 0;
  min-width: 160px;
  z-index: 1000;
}
.dropdown-menu li a {
  display: block;
  padding: 0.3em 1em;
  color: var(--footer-link);
  white-space: nowrap;
}
.dropdown-menu li a:hover,
.dropdown-menu li a:focus { color: var(--link-hover); }
.dropdown.open > .dropdown-menu { display: block; }

.profile-area {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 1em;
  position: relative;
}
.login-greeting {
  font-size: 0.9em;
  color: var(--footer-link);
}
.profile-area .dropdown-menu { right: 0; left: auto; }

@media (max-width: 700px) {
  .nav-links {
    display: none;
    position: absolute;
    top: var(--menu-height);
    left: 0;
    width: 100%;
    background: var(--main-bg);
    flex-direction: column;
    align-items: center;
    padding: 1em 0;
    border-bottom: 1px solid var(--border);
    z-index: 1000;
  }
  .nav-links.active {
    display: flex;
  }
  .nav-toggle { display: flex; }
  .profile-area { flex-direction: column; gap: 0.6em; margin-left: 0; }
  .dropdown-menu {
    position: static;
    width: 100%;
    border: none;
  }
  .site-nav { position: relative; }
}

@media (min-width: 700px) {
  .nav-links { display: flex; }
  .nav-toggle { display: none; }
  .profile-area { margin-left: auto; flex-direction: row; }
}

/* Footer layout */
.site-footer {
  width: 100%;
  background: var(--footer-bg);
  color: var(--footer-txt);
  font-size: 1rem;
  border-top: 1px solid var(--border);
  margin-top: 2em;
  padding-top: 2em;
  padding-bottom: 1em;
}
.footer-columns {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: flex-start;
  gap: 2em;
  width: 100%;
  max-width: var(--max-width);
  margin: 0 auto;
}
.footer-col {
  flex: 1 1 0;
  min-width: 160px;
  margin-bottom: 1.5em;
}
.footer-brand {
  font-size: 1.2em;
  font-weight: 400;
  margin-bottom: 0.5em;
  display: block;
}
.footer-col a {
  color: var(--footer-link);
  text-decoration: none;
  display: block;
  margin: 0.4em 0;
  font-family: monospace;
  font-weight: 500;
  font-size: 1em;
  transition: color 0.2s;
}
.footer-col a:hover,
.footer-col a:focus {
  color: var(--link-hover);
}
.footer-col a.active {
  color: var(--link-active);
}
.copyright-bar {
  width: 100%;
  text-align: center;
  font-size: 0.9em;
  color: var(--footer-txt);
  margin-top: 1em;
  border-top: 1px solid var(--border);
  padding-top: 0.6em;
}
@media (max-width: 900px) {
  .footer-columns {
    flex-direction: column;
    gap: 0.5em;
  }
  .footer-col {
    min-width: 0;
    margin-bottom: 0.5em;
  }
}

/* Number icon treatment */
.step-num-icon {
  width: 50px;
  height: 50px;
  margin-right: 8px;
  vertical-align: middle;
}
.step-btn .step-num-icon {
  filter: brightness(0) invert(1);
}
.how-step .step-num-icon {
  filter: none;
}
.theme-dark .how-step .step-num-icon {
  filter: brightness(0) invert(1);
}
.theme-dark .step-num-icon {
  filter: brightness(0) invert(1);
}
.page-step-icon {
  display: block;
  margin: 0 auto 1em auto;
  max-width: 50px;
  width: 100%;
  height: auto;
}
.theme-dark .page-step-icon {
  filter: brightness(0) invert(1);
}

/* ============================
   [ CSV PANEL BEAUTIFICATION ]
   ============================ */

.csv-preview {
  display: flex;
  flex-direction: column;
  gap: 2.5em;
  margin-top: 2em;
  padding: 0 1em;
}

.csv-artwork-panel {
  display: flex;
  flex-direction: column;
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 2em;
  box-shadow: var(--shadow-deep);
}

.csv-thumb img {
  max-width: 180px;
  max-height: 180px;
  border-radius: 8px;
  box-shadow: var(--shadow);
  margin-bottom: 1em;
}

.csv-fields {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1.5em;
}

.csv-field {
  display: flex;
  flex-direction: column;
}

.csv-label {
  font-weight: 700;
  color: var(--accent-dark);
  font-size: 0.85em;
  margin-bottom: 0.3em;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  opacity: 0.85;
}

.csv-value {
  font-size: 0.92em;
  color: var(--main-txt);
  line-height: 1.5;
  white-space: pre-wrap;
  background: rgba(255, 255, 255, 0.04);
  padding: 0.5em 0.7em;
  border-radius: 6px;
  border: 1px solid var(--border-light);
  overflow-wrap: break-word;
}

.csv-value:empty::after {
  content: "—";
  opacity: 0.5;
}

.csv-field-description {
  max-height: 220px;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.05);
  font-family: var(--font-mono);
}

.csv-field-description::-webkit-scrollbar {
  width: 8px;
}
.csv-field-description::-webkit-scrollbar-thumb {
  background-color: var(--accent);
  border-radius: 4px;
}

.csv-status {
  margin-top: 1em;
  font-size: 0.85em;
  color: var(--accent-muted);
  text-align: right;
}


/* Admin dropdown styling */
.admin-dropdown > .dropdown-toggle {
  background: var(--accent-dark);
  color: #fff;
  padding: 0.2em 0.6em;
  border-radius: 4px;
}

.admin-dropdown > .dropdown-menu {
  background: var(--accent-dark);
  border-color: var(--accent-dark);
}

.admin-dropdown > .dropdown-menu a {
  color: #fff;
}

.admin-dropdown > .dropdown-menu a:hover,
.admin-dropdown > .dropdown-menu a:focus {
  color: #ffe873;
}

@media (max-width: 600px) {
  .page-step-icon {
    max-width: 40px;
  }
  .step-num-icon {
    width: 40px;
    height: 40px;
  }
}

.stage-label {
  text-align: center;
  font-family: serif;
  font-weight: 700;
  letter-spacing: 0.1em;
  margin-bottom: 0.2em;
  color: var(--footer-link);
}
.theme-dark .stage-label {
  color: var(--footer-link);  /* or override to white if needed */
}

/* Wrapper for page stage indicator */
.page-step-wrapper {
  margin-bottom: 1.5em;
  text-align: center;
}

/* CSS number circle for workflow stages */
.stage-circle {
  width: 55px;
  height: 55px;
  border: 2px solid var(--accent);
  border-radius: 50%;
  background: var(--button-bg);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.4em;
  margin: 0 auto 0.3em;
}
.page-step-wrapper.active .stage-circle {
  box-shadow: 0 0 6px var(--accent);
  transform: scale(1.05);
}

@media (max-width: 600px) {
  .stage-circle {
    width: 40px;
    height: 40px;
    font-size: 1.1em;
  }
}

.inline-icon {
  display: inline-block;
  vertical-align: middle;
  width: 3em;
  height: 3em;
  margin-right: 0.4em;
}

#coffee-icon {
  content: url('/static/icons/svg/light/coffee-light.svg');
}
.theme-dark #coffee-icon {
  content: url('/static/icons/svg/dark/coffee-dark.svg');
}

/* Profile icon switch based on system theme */
#profile-icon {
  content: url('/static/icons/svg/light/user-circle-light.svg');
}
@media (prefers-color-scheme: dark) {
  #profile-icon {
    content: url('/static/icons/svg/dark/user-circle-dark.svg');
  }
}

```

---
## 📄 `ezygallery/static/css/components.css`

```css
/* ==============================
   ART Narrator Components
   Scope: buttons, cards, forms, galleries, modals
   ============================== */
/* === [RA.1] Review Artwork Grid Layout === */
.review-artwork-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 38px;
  justify-content: center;
  align-items: flex-start;
  max-width: 1400px;
  margin: 2.5em auto;
}
.mockup-col {
  flex: 1 1 0;
  min-width: 340px;
  max-width: 540px;
  display: block;
}
.main-thumb {
  text-align: center;
  margin-bottom: 1.5em;
}
.main-thumbnail-img {
  max-width: 300px;
  border-radius: 0px;
  box-shadow: none;
  cursor: pointer;
}
.thumb-note {
  font-size: 0.96em;
  color: #888;
  margin-top: 0.4em;
}

h3, .mockup-previews-title {
  margin: 0 0 18px 0;
  font-weight: 700;
  font-size: 1.23em;
}
.mockup-preview-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}
.mockup-card {
  background: var(--card-bg);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  padding: 11px 7px;
  text-align: center;
}
.mockup-thumb-img {
  width: 100%;
  border-radius: var(--thumb-radius);
  margin-bottom: 6px;
  box-shadow: none;
  background: var(--card-bg);
  cursor: pointer;
  transition: box-shadow 0.15s;
}
.mockup-thumbnail { /* new alias for responsive mockup thumbs */
  width: 100%;
  height: auto;
  display: block;
}
.mockup-thumb-img:focus { outline: 2.5px solid var(--accent); }
.mockup-number { font-size: 0.96em; margin-bottom: 6px; }
form { margin: 0.3em 0; display: inline; }
select {
  margin: 2px 0 0 0px;
  border-radius: var(--radius);
  padding: 2px 8px;
  font-size: 0.97em;
  background: var(--input-bg);
  color: var(--input-text);
  border: 1px solid var(--border);
}

.btn,
.btn-sm,
.btn-black,
.btn-primary,
.btn-secondary,
.btn-warning,
.btn-danger,
.btn-small,
.composite-btn,
.btn-reject,
button {
  background: var(--button-bg);
  color: var(--button-text);
  border: 1px solid var(--button-bg);
  border-radius: var(--radius);
  padding: 0.5em 1em;
  font-size: 1em;
  font-weight: 500;
  font-family: monospace;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  transition: background 0.16s, color 0.16s;
  margin: 0.2em 0;
}

.btn:hover,
.btn-sm:hover,
.btn-black:hover,
.btn-primary:hover,
.btn-secondary:hover,
.btn-warning:hover,
.btn-danger:hover,
.btn-small:hover,
.composite-btn:hover,
.btn-reject:hover,
button:hover {
  background: var(--button-hover-bg);
  color: var(--button-text);
}

.btn-danger {
  background: #b50000;
  border-color: #b50000;
}

.btn-warning {
  background: #ea8b00;
  border-color: #ea8b00;
}

.btn-disabled,
.btn[disabled],
.btn-black.btn-disabled,
.btn-black[disabled] {
  pointer-events: none;
  opacity: 0.45;
  filter: grayscale(0.3);
}


.desc-col {
  flex: 1 1 0;
  min-width: 340px;
  max-width: 600px;
  display: block;
}
h1 { font-size: 2em; line-height: 1.3; text-align: center; margin-bottom: 0.9em; }
.desc-panel {
  margin-bottom: 1.7em;
  background: var(--card-bg);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  padding: 16px;
  overflow-x: auto;
}
.desc-panel h2 { margin-bottom: 10px; font-size: 1.13em; }
.desc-text {
  white-space: pre-wrap;
  background: var(--card-bg);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  padding: 16px;
  min-height: 110px;
  max-height: 350px;
  overflow-y: auto;
  font-size: 1.05em;
}
.desc-panel pre {
  white-space: pre-wrap;
  background: var(--card-bg);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  padding: 16px;
  min-height: 110px;
  max-height: 350px;
  overflow-y: auto;
  font-size: 1.05em;
}
.artist-bio {
  background: var(--card-bg);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  padding: 16px;
  white-space: pre-line;
  font-size: 1.05em;
  margin-bottom: 2em;
}
.colour-info-grid {
  display: flex;
  gap: 22px;
  justify-content: center;
  margin-bottom: 2.2em;
}
.colour-info-grid .label {
  font-weight: 600;
  font-size: 1.02em;
  margin-bottom: 5px;
}
.colour-box {
  background: var(--card-bg);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  min-height: 38px;
  padding: 7px 12px;
  font-size: 0.97em;
  white-space: pre-line;
  overflow-x: auto;
}
.reanalyse-label {
  margin-bottom: 10px;
  font-size: 1.07em;
  font-weight: 500;
}
textarea {
  width: 100%;
  max-width: 400px;
  padding: 10px;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  background: var(--input-bg);
  color: var(--input-text);
  resize: vertical;
  font-size: 1em;
  margin-bottom: 9px;
}
.back-link {
  text-align: center;
  margin-top: 1.4em;
}
.back-link a {
  font-size: 1em;
  color: var(--button-bg);
  padding: 7px 18px;
  text-decoration: underline;
}
.card-img-top {
  max-width: 100%;
  max-height: 300px;
  object-fit: cover;
  object-position: center;
}

/* --------- [ 6. Modal/Fullscreen Image View — Borderless Edition ] --------- */
.modal-bg {
  display: none;
  position: fixed; z-index: 99;
  left: 0; top: 0; width: 100vw; height: 100vh;
  background: rgba(34,34,34,0.68);
  align-items: center; justify-content: center;
}
.modal-bg.active { display: flex !important; }

.modal-img {
  background: transparent !important;
  border-radius: 0 !important;
  padding: 0 !important;
  max-width: 94vw;
  max-height: 93vh;
  box-shadow: 0 5px 26px rgba(0,0,0,0.22);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-img img {
  max-width: 88vw;
  max-height: 80vh;
  border-radius: 0 !important;
  border: none !important;
  background: none !important;
  display: block;
  box-shadow: none !important;
}

.modal-close {
  position: absolute;
  top: 1px;
  right: 1px;
  font-size: 1.7em;
  color: #fff;
  background: none;
  border: none;
  cursor: pointer;
  z-index: 101;
  text-shadow: 0 2px 6px #000;
}
.modal-close:focus { outline: 2px solid #ffe873; }

/* === [RA.2] Carousel Modal Lightbox === */
.carousel-modal {
  display: none;
  position: fixed;
  inset: 0;
  z-index: 101;
  background: rgba(0,0,0,0.8);
  align-items: center;
  justify-content: center;
}
.carousel-modal.active { display: flex; }
.carousel-frame {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5em;
  max-width: 90vw;
  max-height: 90vh;
}
.carousel-image {
  max-width: 90vw;
  max-height: 90vh;
  border: none;
}
.carousel-control, .carousel-close {
  background: none;
  border: none;
  cursor: pointer;
  width: 40px;
  height: 40px;
  padding: 0;
}
.carousel-control img, .carousel-close img { width: 100%; height: 100%; }
html.dark .carousel-control img,
html.dark .carousel-close img { filter: invert(1); }
.carousel-close { position: absolute; top: 8px; right: 8px; }
.carousel-control:focus-visible,
.carousel-close:focus-visible { outline: 2px solid #ffe873; }
@media (max-width: 600px) {
  .carousel-control, .carousel-close { width: 32px; height: 32px; }
}

/* --------- [ 7. Footer ] --------- */
footer, .gallery-footer {
  text-align: center;
  margin-top: 4em;
  padding: 1.2em 0;
  font-size: 1em;
  color: #777;
  background: #f2f2f2;
  border-top: 1px solid #ececec;
  letter-spacing: 0.01em;
}
footer a { color: var(--accent); text-decoration: none; }
footer a:hover { color: var(--accent-dark); }

/* --------- [ 8. Light/Dark Mode Ready ] --------- */
body.dark, .dark main {
  background: #191e23 !important;
  color: #f1f1f1 !important;
}
body.dark header, body.dark nav {
  background: #14171a;
  color: #eee;
}
body.dark .item, body.dark .gallery-item,
body.dark .desc-panel, body.dark .modal-img {
  background: #252b30;
  color: #eaeaea;
  border-color: #444;
}
body.dark .desc-panel { box-shadow: none; }
body.dark .gallery-footer, body.dark footer {
  background: #1a1a1a;
  color: #bbb;
  border-top: 1px solid #252b30;
}

:focus-visible {
  outline: 2.2px solid #ffa52a;
  outline-offset: 1.5px;
}
@media print {
  header, nav, .composite-btn, .btn, button, select, .gallery-footer, footer { display: none !important; }
  .desc-panel { border: none !important; box-shadow: none !important; }
  body { background: #fff !important; color: #222 !important; }
  main { padding: 0 !important; }
}

/* --------- [ 10. Misc — Spacing, Inputs, Forms ] --------- */
label { display: inline-block; margin-bottom: 0.2em; font-weight: 500; }
input, textarea {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 0.3em 0.55em;
  font-size: 1em;
  background: var(--input-bg);
  color: var(--input-text);
}
input:focus, textarea:focus { border-color: var(--accent-dark); }
::-webkit-scrollbar { width: 9px; background: #eee; border-radius: 0px; }
::-webkit-scrollbar-thumb { background: #ccc; border-radius: 0px; }
::-webkit-scrollbar-thumb:hover { background: #aaa; }

/* Responsive tweaks */
@media (max-width: 1200px) {
  .review-artwork-grid { max-width: 98vw; }
}
@media (max-width: 900px) {
  .review-artwork-grid { flex-direction: column; gap: 2em; }
  .mockup-col, .desc-col { max-width: 100%; min-width: 0; }
  .mockup-preview-grid { grid-template-columns: repeat(2,1fr); }
}
@media (max-width: 600px) {
  .mockup-preview-grid { grid-template-columns: 1fr; gap: 0.9em; }
  .review-artwork-grid { margin: 1.2em 0.2em; }
  .main-thumb { margin-bottom: 1em; }
  .desc-panel { padding: 1em 0.6em; }
}


/* ===============================
   [ ART Narrator Artwork Gallery Grid ]
   =============================== */
.gallery-section {
  margin: 2.5em auto 3.5em auto;
  max-width: var(--max-width);
  padding: 0 var(--container-padding);
}
.artwork-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--gallery-gap);
  margin-bottom: 2em;
}
.gallery-card {
  border-radius: var(--radius);
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: background-color var(--transition-fast), box-shadow var(--transition-fast);
  min-height: 365px;
  padding: 10px;
  overflow: hidden;
  background-color: transparent; /* <-- Default: no background */
}
/* 🌙 DARK MODE hover background */
@media (prefers-color-scheme: dark) {
  .gallery-card:hover {
    background-color: var(--dark-card-hover-bg);
  }
}
/* ☀️ LIGHT MODE hover background */
@media (prefers-color-scheme: light) {
  .gallery-card:hover {
    background-color: var(--light-card-hover-bg);
  }
}
.card-thumb {
  width: 100%;
  text-align: center;
  padding: 22px 0 7px 0;
  border-bottom: none;
}
.card-img-top {
  max-width: 94%;
  max-height: 210px;
  border-radius: var(--thumb-radius);
  object-fit: cover;
  box-shadow: none;
  background: var(--card-bg);
}
.card-details {
  flex: 1 1 auto;
  width: 90%;
  text-align: center;
  padding: 12px 13px 20px 13px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.card-title {
  font-size: 0.9em;
  font-weight: 400;
  margin-bottom: 7px;
  line-height: 1.2;
  color: var(--main-txt);
  min-height: 3em;
}
.file-name {
  font-family: var(--font-code);
  font-size: 0.85em;
  line-height: 1.3;
  word-break: break-all;
  height: 5.5em;
  overflow: hidden;
}
.btn, .btn-primary, .btn-secondary {
  margin-top: 7px;
  width: 80%;
  min-width: 90px;
  align-self: center;
}

.flash {
  margin-bottom: 1.2em;
}
.flash-success {
  background: #e6ffe6;
  border: 1px solid #b5f5b5;
  color: #005500;
  padding: 1em;
}
.flash-warning {
  background: #fff8e6;
  border: 1px solid #f0d48a;
  color: #985f00;
  padding: 1em;
}
.flash-error {
  background: #fbeaea;
  color: #a60000;
  border-left: 5px solid #e10000;
  padding: 1em;
  border-radius: 0 !important;
}
.flash ul { margin: 0; padding-left: 1.2em; }
@media (max-width: 800px) {
  .artwork-grid { gap: 1.3em; }
  .card-thumb { padding: 12px 0 4px 0; }
  .card-title { font-size: 1em; }
}

/* === Finalised Gallery === */
.finalised-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: var(--gallery-gap);
  margin-top: 1.5em;
  justify-content: center;
}
.finalised-grid.list-view {
  display: block;
}
.finalised-grid.list-view .final-card {
  flex-direction: row;
  max-width: none;
  margin-bottom: 1em;
}
.finalised-grid.list-view .card-thumb {
  width: 150px;
  margin-right: 1em;
}
.final-card {
  background: var(--card-bg);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  padding: 10px;
  display: flex;
  flex-direction: column;
  max-width: 350px;
  margin: 0 auto;
}
.final-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-top: auto;
}
.final-actions .btn {
  flex: 1 1 auto;
  min-width: 100px;
  width: auto;
  margin-top: 0;
}
.edit-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-top: 1em;
}
.edit-actions .btn {
  flex: 1 1 auto;
  min-width: 100px;
  width: auto;
  margin-top: 0;
}
.finalised-badge {
  font-size: 0.9em;
  color: #d40000;
  align-self: center;
  padding: 4px 8px;
}
.view-toggle {
  margin-top: 0.5em;
}
.view-toggle button {
  margin-right: 0.5em;
}
.locked-badge {
  font-size: 0.9em;
  color: var(--button-bg);
  padding: 2px 6px;
  border: 1px solid var(--button-bg);
  margin-left: 6px;
}
.lock-meta {
  font-size: 0.8em;
  margin-bottom: 4px;
  color: #666;
}
.mini-mockup-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 4px;
  margin-top: 6px;
}
.mini-mockup-grid img {
  width: 100%;
  max-height: 120px;
  object-fit: contain;
  border-radius: 0px;
  box-shadow: none;
}
.desc-snippet {
  font-size: 0.92em;
  margin: 4px 0 8px 0;
  line-height: 1.3;
}
@media (max-width: 800px) {
  .finalised-grid {
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  }
}

/* ===============================
   [ Edit Artwork Listing Page ]
   =============================== */
/* --- Edit Action Buttons Area --- */
.edit-listing-col {
  max-width: 540px;
  width: 100%;
}

.long-field {
  width: 100%;
  max-width: 540px;
  box-sizing: border-box;
  font-size: 1.05em;
  padding: 0.6em;
  margin-bottom: 1em;
  border-radius: 0 !important;   /* FORCE SQUARE */
}

.price-sku-row,
.row-inline {
  display: flex;
  gap: 1em;
}
.price-sku-row > div,
.row-inline > div {
  flex: 1;
}

.edit-actions-col {
  display: flex;
  flex-wrap: wrap;
  gap: 0.7em;
  margin: 2em 0 0 0;
  width: 100%;
  max-width: 540px;
}
.edit-actions-col > .action-form,
.edit-actions-col > button {
  flex: 1 1 48%;
}
@media (max-width: 600px) {
  .edit-actions-col {
    flex-direction: column;
  }
  .edit-actions-col > .action-form,
  .edit-actions-col > button {
    flex-basis: 100%;
  }
}

.wide-btn {
  width: 100%;
  font-size: 1.12em;
  font-weight: bold;
  padding: 1em 0;
  border-radius: 0 !important;   /* FORCE SQUARE */
}

/* ====== SQUARE CORNERS: NO ROUNDING ANYWHERE ====== */
input,
textarea,
select,
button,
.mockup-thumb-img,
.main-thumbnail-img,
.mockup-card,
.swap-form,
.edit-listing-col,
.flash-error,
form,
.mockup-preview-grid,
.main-thumb {
  border-radius: 0 !important;
}

/* ====== SQUARE IMAGE THUMBNAILS ====== */
.mockup-thumb-img, .main-thumbnail-img {
  border-radius: var(--thumb-radius) !important;
  border: 1px solid var(--border);
  box-shadow: none;
  width: 100%;
  height: auto;
  display: block;
}

/* Other style fixes */
 .status-line {
  font-weight: bold;
  font-size: 1.2em;
  margin-bottom: 1.1em;
}
.status-finalised { color: #c00; }
.status-pending { color: #ef7300; }

.missing-img {
  width: 100%;
  padding: 20px 0;
  background: #eee;
  color: #777;
  font-size: 0.9em;
  border-radius: 0 !important;
}
.empty-msg {
  text-align: center;
  margin: 2em 0;
  font-size: 1.2em;
  color: #555;
  border-radius: 0 !important;
}

/* Responsive - match what you want */
@media (max-width: 800px) {
  .edit-listing-col, .review-artwork-grid { padding: 1em; }
  .row-inline, .price-sku-row { flex-direction: column; gap: 0.5em; }
}

/* ===============================
   [ Upload Dropzone ]
   =============================== */
.upload-dropzone {
  border: 2px dashed var(--border);
  padding: 40px;
  text-align: center;
  cursor: pointer;
  color: #666;
  transition: background 0.2s, border-color 0.2s;
}
.upload-dropzone.dragover {
  border-color: var(--accent-dark);
  background: #f9f9f9;
}

.upload-list {
  margin-top: 1em;
  list-style: none;
  padding: 0;
  font-size: 0.9rem;
}
.upload-list li {
  margin: 0.2em 0;
}
.upload-list li.success { color: green; }
.upload-list li.error { color: red; }

.upload-progress {
  position: relative;
  background: #eee;
  height: 8px;
  margin: 2px 0;
  width: 100%;
  overflow: hidden;
}
.upload-progress-bar {
  background: var(--accent);
  height: 100%;
  width: 0;
  transition: width 0.2s;
}
.upload-percent {
  margin-left: 4px;
  font-size: 0.8em;
}

/* --------- [ Workflow Step Grid ] --------- */
.workflow-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1em;
  margin: 2em 0;
}
.step-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5em;
  padding: 0.6em 1em;
  background: transparent;
  color: var(--button-bg);
  border: 2px solid var(--button-bg);
  text-decoration: none;
  border-radius: var(--radius);
  transition: background 0.16s, color 0.16s;
}
.step-btn:hover {
  background: var(--button-bg);
  color: var(--button-text);
}
.step-btn.disabled {
  background: #555;
  border: 2px solid #555;
  pointer-events: none;
  color: #aaa;
}

/* Icon for numbered steps */
.step-num-icon {
  width: 1.4em;
  height: 1.4em;
  margin-right: 0.4em;
  color: #fff;
  vertical-align: middle;
}

/* Generic inline icon for buttons and actions */
.icon-inline {
  width: 18px;
  height: 18px;
  margin-right: 6px;
  vertical-align: middle;
}

.step-btn.disabled .step-num-icon { opacity: 0.5; }

/* --------- [ Analysis Progress Modal ] --------- */
.analysis-modal {
  display: none;
  position: fixed;
  z-index: 100;
  left: 0;
  top: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.65);
  align-items: center;
  justify-content: center;
}
.analysis-modal.active { display: flex; }

.analysis-box {
  background: var(--main-bg);
  border: 1px solid var(--border);
  padding: 1em 1.2em;
  max-width: 700px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}
.analysis-log {
  font-family: monospace;
  background: #fafbfc;
  border: 1px solid #ddd;
  padding: 0.6em;
  max-height: 60vh;
  overflow-y: auto;
  white-space: pre-wrap;
  font-size: 0.92em;
}
.analysis-log .log-error { color: #b00; }
.analysis-log .latest { background: #eef; }

.analysis-progress {
  background: #eee;
  height: 10px;
  margin: 0.5em 0;
  width: 100%;
}
.analysis-progress-bar {
  background: var(--accent);
  height: 100%;
  width: 0;
  transition: width 0.3s ease;
}
.analysis-status {
  font-size: 0.9em;
  margin-bottom: 0.6em;
}
.analysis-friendly {
  text-align: center;
  font-size: 0.9em;
  margin-top: 0.6em;
  font-style: italic;
}

/* ===============================
   [ OpenAI Details Table ]
   =============================== */
.openai-details table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 2em;
  font-size: 0.8em;    /* smaller for both columns */
  table-layout: fixed;
}

.openai-details th,
.openai-details td {
  padding-bottom: 0.35em;
  vertical-align: top;
  word-break: break-word;
}

/* Make the first column (labels) nice and wide, second takes rest */
.openai-details th {
  width: 105px;    /* adjust as needed for your headings */
  min-width: 95px;
  font-weight: 600;
  text-align: left;
  font-size: 0.8em;
  white-space: nowrap;   /* keep all on one line */
  padding-bottom: 10px;
  padding-right: 1em;
}

.openai-details td {
  font-size: 0.8em;
}

@media (max-width: 650px) {
  .openai-details th {
    width: 110px;
    min-width: 90px;
    font-size: 0.8em;
  }
  .openai-details td {
    font-size: 0.8em;
  }
}

.openai-details table tr:nth-child(even) {
  background: #dddddd;
}

.openai-details th,
.openai-details td {
  padding: 0.33em 0.6em 0.33em 0.3em;
}

/* ===============================
   [ Sellbrite Exports ]
   =============================== */
.export-actions { margin-bottom: 1em; }
.exports-table {
  width: 100%;
  border-collapse: collapse;
}
.exports-table th,
.exports-table td {
  padding: 0.4em 0.6em;
  border-bottom: 1px solid var(--border);
}
.exports-table tr:nth-child(even) {
  background: #f5f5f5;
}
.theme-dark .exports-table tr:nth-child(even) {
  background: #333;
}
.exports-table th {
  position: sticky;
  top: 0;
  background: var(--main-bg);
  z-index: 2;
}

/* ===============================
   [ Login Form ]
   =============================== */
.login-container {
  max-width: 360px;
  margin: 4em auto;
  padding: 2em;
  border: 1px solid var(--border);
  background: var(--card-bg);
  text-align: center;
}
.login-container input {
  width: 100%;
  margin: 0.5em 0 1em 0;
  padding: 0.5em;
  border: 1px solid var(--border);
  background: var(--input-bg);
  color: var(--input-text);
  border-radius: var(--radius);
}
.login-container button {
  width: 100%;
}


```

---
## 📄 `ezygallery/static/css/layout.css`

```css
/* ==============================
   ART Narrator Layout Styles
   Scope: header, nav, main containers, footer and responsive spacing
   ============================== */

header, .site-nav {
  background: var(--nav-bg);
  color: var(--footer-link);
  height: var(--menu-height);
  display: flex;
  align-items: center;
  padding: 0 2em;
  font-size: 1.2em;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  gap: 1.7em;
  position: sticky;
  top: 0;
  z-index: 999;
}
nav a, .site-nav a {
  color: var(--footer-link);
  text-decoration: none;
  margin-right: 2em;
  font-weight: 400;
  letter-spacing: 0.01em;
  transition: color 0.2s;
}
nav a:hover,
nav a.active,
.site-nav a:hover { color: #ffe873; }
.brand-logo {
  font-family: sans-serif;
  font-weight: 400;
  font-size: 2em;
  letter-spacing: 0.05em;
  margin-right: 2em;
  display: flex;
  align-items: center;
}
.brand-logo .brand-icon {
  width: 24px;
  height: 24px;
  margin-right: 6px;
  color: inherit;
}
.theme-toggle {
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 0;
}
.theme-toggle img {
  width: 28px;
  height: 28px;
}
.theme-dark .theme-toggle { color: #ffe873; }
#icon-moon { display: none; }
.theme-dark #icon-sun { display: none; }
.theme-dark #icon-moon { display: inline; }

.profile-area {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 1em;
  font-size: 0.95em;
}
.profile-area a {
  color: #fff;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}
.profile-area a:hover {
  color: var(--link-hover);
}
.profile-area a.active {
  color: var(--link-active);
}

main {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 2.5em var(--container-padding) 2em var(--container-padding);
}
@media (max-width: 700px) {
  main { padding: 1.1em 0.4em; }
}

footer, .gallery-footer {
  text-align: left;
  margin-top: 4em;
  padding: 2em 1em;
  font-size: 0.95em;
  color: #555;
  background: #f2f2f2;
  border-top: 1px solid #ececec;
  letter-spacing: 0.01em;
  display: block;
}
footer a {
  color: var(--footer-link);
  text-decoration: none;
  display: block;
  margin: 2px 0;
  font-weight: 500;
}
footer a:hover { color: var(--footer-link-hover); }
.footer-col {
  display: flex;
  flex-direction: column;
  text-decoration: none;
  gap: 4px;
}
.footer-brand {
  font-family: sans-serif;
  font-weight: 700;
}
@media (max-width: 700px) {
  footer, .gallery-footer {
    grid-template-columns: 1fr;
    text-align: center;
  }
}

/* Simple layout for policy and info pages */
.legal-page, .info-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 1em;
  line-height: 1.6;
}

/* Mega Menu Layout */
.mega-button {
  background: none;
  border: none;
  cursor: pointer;
  font: inherit;
  color: inherit;
}
.mega-menu {
  position: absolute;
  left: 0;
  right: 0;
  top: var(--menu-height);
  background: var(--nav-bg);
  border-bottom: 1px solid var(--border);
  display: none;
  padding: 2em 1em;
  z-index: 1000;
}
.mega-menu.open {
  display: block;
}
.mega-inner {
  max-width: var(--max-width);
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: var(--gallery-gap);
}
.mega-col h3 {
  margin-top: 0;
  font-size: 1.1em;
  font-weight: 600;
}
.mega-col ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
.mega-col li a {
  display: block;
  padding: 0.3em 0;
  color: var(--footer-link);
  text-decoration: none;
  font-weight: 500;
}
.mega-col li a:hover {
  color: var(--link-hover);
}
@media (max-width: 700px) {
  .mega-menu {
    position: fixed;
    top: var(--menu-height);
    bottom: 0;
    overflow-y: auto;
  }
  .mega-inner {
    grid-template-columns: 1fr;
  }
  .mega-col {
    border-bottom: 1px solid var(--border);
  }
  .mega-col h3 {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5em 0;
    cursor: pointer;
  }
  .mega-col ul {
    display: none;
    padding-bottom: 0.5em;
  }
  .mega-col.open ul {
    display: block;
  }
}


```

---
## 📄 `ezygallery/static/css/base.css`

```css
/* ==============================
   ART Narrator Base Styles
   Scope: core resets, typography, body styles
   ============================== */

body {
  font-family: serif;
  background: var(--main-bg);
  color: var(--main-txt);
  margin: 0;
  padding: 0;
}

.brand, .footer-brand, .brand-logo {
  font-family: serif;
  font-weight: 400;
  letter-spacing: 0.03em;
}
h1, h2, h3 {
  font-family: serif;
  font-weight: 700;
  letter-spacing: 0.03em;
}

h1 { font-size: 2em; line-height: 1.3; text-align: center; margin-bottom: 0.9em; }

label { display: inline-block; margin-bottom: 0.2em; font-weight: 500; }
input, textarea {
  border: 1px solid var(--border);
  border-radius: 0;
  padding: 0.3em 0.55em;
  font-size: 1em;
  background: var(--input-bg);
  color: var(--input-text);
}
input:focus, textarea:focus { border-color: var(--accent-dark); }

::-webkit-scrollbar { width: 9px; background: #eee; border-radius: 0px; }
::-webkit-scrollbar-thumb { background: #ccc; border-radius: 0; }
::-webkit-scrollbar-thumb:hover { background: #aaa; }


a {
  color: var(--footer-link);
  text-decoration: none;
  transition: color 0.2s, font-weight 0.2s;
}
a:hover,
a:focus {
  color: var(--footer-link-hover);
  font-weight: 400;
}


```

---
## 📄 `ezygallery/static/css/theme-vars.css`

```css
:root {
  /* 🎨 Colour Palette */
  --main-bg: #f9f9f9;
  --main-txt: #222;
  --accent: #000000;
  --accent-dark: #414141;
  --border: #ddd;
  --card-bg:none;
  --highlight: #ffeaa7;
  --error: #e74c3c;
  --success: #2ecc71;
  --info: #3498db;

  /* 🌈 Theme Modes */
  --dark-bg: #1e1e1e;
  --dark-txt: #f1f1f1;
  --dark-card-hover-bg: #464646;
  --light-card-hover-bg: #dedede;

  /* ✍️ Fonts */
  --font-body: sans-serif;
  --font-heading: serif;
  --font-code: monospace;

  /* 📐 Layout */
  --max-width: 1280px;
  --container-padding: 2rem;
  --menu-height: 64px;
  --gallery-gap: .5em;

  /* 🧱 Borders & Shadows */
  --radius: 0px;
  --thumb-radius: 0px;
  --shadow: 0 2px 6px rgba(0,0,0,0.06);
  --shadow-deep: 0 4px 10px rgba(0,0,0,0.1);

  /* 🕹 Transitions & Motion */
  --transition-fast: 0.15s ease-in-out;
  --transition-medium: 0.3s ease-in-out;

  /* 🎯 Z-index Layers */
  --z-header: 1000;
  --z-overlay: 9999;
  --z-modal: 1100;
  --z-dropdown: 1050;

  --border-light: #444;
  --accent-muted: #888;
  --font-mono: "SFMono-Regular", Consolas, "Courier New", monospace;
}

```

---
## 📄 `ezygallery/static/css/style.css`

```css
/* ==========================================================================
   File: style.css
   Purpose: Consolidated styles for ART Narrator.
   ========================================================================== */

/* --- [1] CSS Variables for Theming --- */
:root {
    /* Variables used across style.css and custom.css (audit 2025-07-14) */
    --bg-color-light: #f9f9f6;
    --text-color-light: #0d0d0d;
    --border-color-light: #e0e0e0;
    --accent-color-light: #ed7214;
    --overlay-bg-light: rgba(249, 249, 246, 0.85);

    --bg-color-dark: #121212;
    --text-color-dark: #f0f0f0;
    --border-color-dark: #333;
    --accent-color-dark: #ed7214;
    --overlay-bg-dark: rgba(20, 20, 20, 0.85);

    /* GDWS Editor */
    --card-bg: #fff; /* Added from custom.css audit, 2025-07-14 */
    --radius: 0px; /* Added from custom.css audit, 2025-07-14 */
    --shadow: 0 2px 6px rgba(0, 0, 0, 0.06); /* Added from custom.css audit, 2025-07-14 */
    --border: #ddd; /* Added from custom.css audit, 2025-07-14 */
    --accent: var(--accent-color-light); /* Added from custom.css audit, 2025-07-14 */

    /* Auth/Input Controls */
    --input-text: #222; /* Added from custom.css audit, 2025-07-14 */

    /* Workflow Buttons - light mode defaults */
    --button-bg-light: #111;  /* July 2025 UI refresh */
    --button-text-light: #fff;
    --button-hover-bg-light: #fff;
    --button-hover-text-light: #111;

    --button-bg-dark: #fff;
    --button-text-dark: #111;
    --button-hover-bg-dark: #000;
    --button-hover-text-dark: #fff;

    /* defaults applied to light mode */
    --button-bg: var(--button-bg-light);
    --button-text: var(--button-text-light);
    --button-hover-bg: var(--button-hover-bg-light);
    --button-hover-text: var(--button-hover-text-light);

    --input-bg: #fff;
    --input-border: #ccc;
}

/* Visually hidden text for accessibility */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

/* --- [2] Basic Body & Font Styles --- */
html, body {
    height: 100%;
}

body {
    margin: 0;
    font-family: monospace;
    background-color: var(--bg-color-light);
    color: var(--text-color-light);
    transition: background-color 0.3s ease, color 0.3s ease;
    display: flex;
    flex-direction: column;
}

html.dark body {
    background-color: var(--bg-color-dark);
    color: var(--text-color-dark);
    --button-bg: var(--button-bg-dark);
    --button-text: var(--button-text-dark);
    --button-hover-bg: var(--button-hover-bg-dark);
    --button-hover-text: var(--button-hover-text-dark);
    --input-bg: #222;
    --input-border: #555;
}

.page-wrapper {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}

/* --- [3] Global Button & Input Styles (2025 UI Refresh) --- */
button,
.btn,
input,
textarea,
select,
.form-control {
    border-radius: 0;
    border: none;
    padding: 0.7em 1.3em;
    font-weight: bold;
    font-family: inherit;
}

button,
.btn { background: var(--button-bg); color: var(--button-text); }

button:hover,
.btn:hover { background: var(--button-hover-bg); color: var(--button-hover-text); }

input,
textarea,
select { background: var(--input-bg); border: 1px solid var(--input-border); width: 100%; box-sizing: border-box; color: var(--input-text); }


```

---
## 📄 `ezygallery/static/css/menu.css`

```css
.mega-button {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  font: inherit;
}

#mega-arrow {
  margin-left: 4px;
  font-size: 0.9em;
}

.mega-menu {
  position: fixed;
  left: 0;
  right: 0;
  top: var(--menu-height);
  bottom: 0;
  background: var(--nav-bg);
  backdrop-filter: blur(6px);
  padding: 2em 1em;
  display: none;
  overflow-y: auto;
  z-index: 1100;
}

.mega-menu.open { display: block; }

.mega-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.3);
  backdrop-filter: blur(4px);
  z-index: 1090;
}

.mega-overlay.active { display: block; }

.mega-inner {
  max-width: var(--max-width);
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: var(--gallery-gap);
}

.mega-col h3 {
  margin-top: 0;
  font-size: 1em;
  cursor: pointer;
}

.mega-col ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.mega-col li a {
  display: block;
  padding: 0.25em 0;
  color: var(--footer-link);
  text-decoration: none;
  font-size: 0.9em;
}

.mega-col li a:hover {
  color: var(--link-hover);
}

@media (max-width: 700px) {
  .mega-inner { grid-template-columns: 1fr; }
  .mega-col { border-bottom: 1px solid var(--border); }
}

```

---
## 📄 `ezygallery/static/js/edit_listing.js`

```js
/* ==========================================================================
   File: modal-carousel.js
   Purpose: Modal carousel for artwork mockups on the edit listing page
   Sections:
   [MC.1] Carousel Setup and Accessibility
   [MC.2] Form Action Helpers
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('carousel-modal');
    if (!modal) return;

    const imgEl = modal.querySelector('#carousel-img');
    const prevBtn = modal.querySelector('.carousel-nav.left');
    const nextBtn = modal.querySelector('.carousel-nav.right');
    const closeBtn = modal.querySelector('.carousel-close');
    const counterEl = modal.querySelector('#carousel-counter');

    const focusSelector = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
    let focusableEls = [];
    let currentIndex = 0;
    let touchStartX = 0;
    let lastFocus = null;

    const thumbEls = Array.from(document.querySelectorAll('.mockup-grid .mockup-thumb'));
    const mainImg = document.querySelector('.hero-image img');
    const images = mainImg ? [mainImg.src, ...thumbEls.map(el => el.src)] : thumbEls.map(el => el.src);

    function update() {
        imgEl.src = images[currentIndex];
        imgEl.alt = `Mockup Preview ${currentIndex + 1}`;
        if (counterEl) counterEl.textContent = `${currentIndex + 1} / ${images.length}`;
        thumbEls.forEach(t => t.classList.remove('current'));
        if (thumbEls[currentIndex]) {
            thumbEls[currentIndex].classList.add('current');
        }
    }

    function open(index = 0, triggerEl = null) {
        lastFocus = triggerEl || document.activeElement;
        currentIndex = index;
        update();
        modal.classList.add('active');
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        focusableEls = modal.querySelectorAll(focusSelector);
        closeBtn.focus();
    }

    function close() {
        modal.classList.remove('active');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
        if (lastFocus) {
            lastFocus.focus();
        }
    }

    function next() { if (currentIndex < images.length - 1) { currentIndex++; update(); } }
    function prev() { if (currentIndex > 0) { currentIndex--; update(); } }

    prevBtn.addEventListener('click', prev);
    nextBtn.addEventListener('click', next);
    closeBtn.addEventListener('click', close);

    modal.addEventListener('click', e => { if (e.target === modal) close(); });
    modal.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; });
    modal.addEventListener('touchend', e => {
        const diff = e.changedTouches[0].clientX - touchStartX;
        if (diff > 50) prev();
        if (diff < -50) next();
    });

    document.addEventListener('keydown', e => {
        if (!modal.classList.contains('active')) return;
        if (e.key === 'Escape') { close(); }
        else if (e.key === 'ArrowRight') { next(); }
        else if (e.key === 'ArrowLeft') { prev(); }
        else if (e.key === 'Tab') {
            const first = focusableEls[0];
            const last = focusableEls[focusableEls.length - 1];
            if (e.shiftKey && document.activeElement === first) {
                e.preventDefault(); last.focus();
            } else if (!e.shiftKey && document.activeElement === last) {
                e.preventDefault(); first.focus();
            }
        }
    });

    if (mainImg) {
        mainImg.addEventListener('click', () => open(0, mainImg));
        mainImg.addEventListener('keydown', e => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                open(0, mainImg);
            }
        });
    }
    thumbEls.forEach((thumb, idx) => {
        const index = idx + 1;
        thumb.addEventListener('click', () => open(index, thumb));
        thumb.addEventListener('keydown', e => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                open(index, thumb);
            }
        });
    });

    // === [MC.2] Form Action Helpers ===
    function toggleActionBtns() {
        const txt = document.querySelector('textarea[name="images"]');
        const disabled = !(txt && txt.value.trim());
        document.querySelectorAll('.require-images').forEach(btn => { btn.disabled = disabled; });
    }
    const imagesTextarea = document.querySelector('textarea[name="images"]');
    if (imagesTextarea) imagesTextarea.addEventListener('input', toggleActionBtns);
    toggleActionBtns();

    document.querySelectorAll('.lock-form').forEach(f => {
        f.addEventListener('submit', () => {
            const r = prompt('Reason for lock/unlock? (optional)');
            if (r !== null) f.querySelector('input[name="reason"]').value = r;
        });
    });

    const deleteBtn = document.querySelector('.delete-btn');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', e => {
            if (!confirm('Delete this artwork and all files?')) {
                e.preventDefault();
            }
        });
    }
});

```

---
## 📄 `ezygallery/static/js/edit_listing_modal.js`

```js
/* ==========================================================================
   File: edit_listing_modal.js
   Purpose: Modal carousel and form helpers for the edit listing page.
   Sections:
   [ELM.1] Carousel Setup and Accessibility
   [ELM.2] Form Action Helpers
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('carousel-modal');
    if (!modal) return;

    const heroImg = document.getElementById('hero-image');
    const thumbEls = Array.from(document.querySelectorAll('#thumbnail-grid .mockup-thumb'));
    const imgEl = modal.querySelector('#carousel-img');
    const prevBtn = modal.querySelector('.carousel-nav.left');
    const nextBtn = modal.querySelector('.carousel-nav.right');
    const closeBtn = modal.querySelector('.carousel-close');
    const counterEl = modal.querySelector('#carousel-counter');

    const focusSelector = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
    let focusableEls = [];
    let currentIndex = 0;
    let lastFocus = null;
    let touchStartX = 0;

    const images = [heroImg.dataset.fullSrc || heroImg.src, ...thumbEls.map(t => t.dataset.fullSrc || t.src)];

    function update() {
        imgEl.src = images[currentIndex];
        imgEl.alt = `Preview ${currentIndex + 1}`;
        if (counterEl) counterEl.textContent = `${currentIndex + 1} / ${images.length}`;
        thumbEls.forEach(t => t.classList.remove('current'));
        if (thumbEls[currentIndex]) thumbEls[currentIndex].classList.add('current');
    }

    function open(index = 0, trigger = null) {
        lastFocus = trigger || document.activeElement;
        currentIndex = index;
        update();
        modal.classList.add('active');
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        focusableEls = modal.querySelectorAll(focusSelector);
        closeBtn.focus();
    }

    function close() {
        modal.classList.remove('active');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
        if (lastFocus) lastFocus.focus();
    }

    function next() { if (currentIndex < images.length - 1) { currentIndex++; update(); } }
    function prev() { if (currentIndex > 0) { currentIndex--; update(); } }

    prevBtn.addEventListener('click', prev);
    nextBtn.addEventListener('click', next);
    closeBtn.addEventListener('click', close);
    modal.addEventListener('click', e => { if (e.target === modal) close(); });
    modal.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; });
    modal.addEventListener('touchend', e => {
        const diff = e.changedTouches[0].clientX - touchStartX;
        if (diff > 50) prev();
        if (diff < -50) next();
    });

    document.addEventListener('keydown', e => {
        if (!modal.classList.contains('active')) return;
        if (e.key === 'Escape') close();
        else if (e.key === 'ArrowRight') next();
        else if (e.key === 'ArrowLeft') prev();
        else if (e.key === 'Tab') {
            const first = focusableEls[0];
            const last = focusableEls[focusableEls.length - 1];
            if (e.shiftKey && document.activeElement === first) {
                e.preventDefault(); last.focus();
            } else if (!e.shiftKey && document.activeElement === last) {
                e.preventDefault(); first.focus();
            }
        }
    });

    heroImg.addEventListener('click', () => open(0, heroImg));
    heroImg.addEventListener('keydown', e => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            open(0, heroImg);
        }
    });

    thumbEls.forEach((thumb, idx) => {
        const index = idx + 1;
        thumb.addEventListener('click', () => open(index, thumb));
        thumb.addEventListener('keydown', e => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                open(index, thumb);
            }
        });
    });

    // === [ELM.2] Form Action Helpers ===
    function toggleActionBtns() {
        const txt = document.querySelector('textarea[name="images"]');
        const disabled = !(txt && txt.value.trim());
        document.querySelectorAll('.require-images').forEach(btn => { btn.disabled = disabled; });
    }
    const imagesTextarea = document.querySelector('textarea[name="images"]');
    if (imagesTextarea) imagesTextarea.addEventListener('input', toggleActionBtns);
    toggleActionBtns();

    document.querySelectorAll('.lock-form').forEach(f => {
        f.addEventListener('submit', () => {
            const r = prompt('Reason for lock/unlock? (optional)');
            if (r !== null) f.querySelector('input[name="reason"]').value = r;
        });
    });

    const deleteBtn = document.querySelector('.delete-btn');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', e => {
            if (!confirm('Delete this artwork and all files?')) {
                e.preventDefault();
            }
        });
    }
});

```

---
## 📄 `ezygallery/static/js/upload.js`

```js
/* ==========================================================================
   File: upload.js
   Purpose: Handles drag-and-drop artwork uploads with progress feedback.
   ========================================================================== */

/**
 * Initialise upload handling once the DOM is ready.
 */
document.addEventListener('DOMContentLoaded', () => {
    const zone = document.getElementById('dropzone');
    const fileInput = document.getElementById('file-input');
    const list = document.getElementById('upload-list');
    const overlay = zone.querySelector('.spinner-overlay');

    /**
     * Create a list item with progress bar for a file.
     * @param {File} file
     * @returns {{file: File, li: HTMLElement, bar: HTMLElement, txt: HTMLElement}}
     */
    function createRow(file) {
        const li = document.createElement('li');
        li.textContent = file.name + ' ';
        const barWrap = document.createElement('div');
        barWrap.className = 'upload-progress';
        const bar = document.createElement('div');
        bar.className = 'upload-progress-bar';
        barWrap.appendChild(bar);
        const txt = document.createElement('span');
        txt.className = 'upload-percent';
        li.appendChild(barWrap);
        li.appendChild(txt);
        list.appendChild(li);
        return {file, li, bar, txt};
    }

    /**
     * Send a single file to the server.
     * @param {File} file
     * @param {Object} row Row elements returned from createRow
     * @returns {Promise<boolean>} success indicator
     */
    function uploadFile(file, row) {
        return new Promise(resolve => {
            const xhr = new XMLHttpRequest();
            const formData = new FormData();
            formData.append('images', file);
            xhr.open('POST', '/upload');
            xhr.setRequestHeader('Accept', 'application/json');
            xhr.upload.onprogress = e => {
                if (e.lengthComputable) {
                    const p = Math.round(e.loaded / e.total * 100);
                    row.bar.style.width = p + '%';
                    row.txt.textContent = p + '%';
                }
            };
            xhr.onload = () => {
                let ok = false;
                if (xhr.status === 200) {
                    try {
                        const res = JSON.parse(xhr.responseText)[0];
                        ok = !!res.success;
                        row.txt.textContent = ok ? 'Uploaded!' : (res.error || 'Failed');
                    } catch (err) {
                        row.txt.textContent = 'Error';
                    }
                } else {
                    row.txt.textContent = 'Error ' + xhr.status;
                }
                row.li.classList.add(ok ? 'success' : 'error');
                resolve(ok);
            };
            xhr.onerror = () => {
                row.li.classList.add('error');
                row.txt.textContent = 'Failed';
                resolve(false);
            };
            xhr.send(formData);
        });
    }

    /**
     * Preview and upload a set of files.
     * @param {FileList|File[]} files
     */
    async function handleFiles(files) {
        if (!files || !files.length) return;
        list.innerHTML = '';
        const rows = Array.from(files).map(createRow);
        overlay.classList.add('active');
        zone.classList.add('disabled');
        for (const row of rows) {
            await uploadFile(row.file, row);
        }
        overlay.classList.remove('active');
        zone.classList.remove('disabled');
        if (list.querySelector('li.success')) {
            const msg = document.createElement('li');
            msg.className = 'upload-success';
            msg.textContent = 'Success!';
            list.appendChild(msg);
            setTimeout(() => { window.location.href = '/artworks'; }, 800);
        }
    }

    if (!zone) return;

    ['dragenter','dragover'].forEach(evt => {
        zone.addEventListener(evt, e => {
            e.preventDefault();
            zone.classList.add('dragover');
        });
    });
    ['dragleave','drop'].forEach(evt => {
        zone.addEventListener(evt, () => zone.classList.remove('dragover'));
    });
    zone.addEventListener('drop', e => {
        e.preventDefault();
        handleFiles(e.dataTransfer.files);
    });
    zone.addEventListener('click', () => fileInput.click());
    zone.addEventListener('keypress', e => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            fileInput.click();
        }
    });
    fileInput.addEventListener('change', () => handleFiles(fileInput.files));
});

```

---
## 📄 `ezygallery/static/js/prompt_whisperer.js`

```js
document.addEventListener('DOMContentLoaded', () => {
  const promptField = document.getElementById('prompt');
  const instructions = document.getElementById('instructions');
  const wordCount = document.getElementById('word_count');
  const category = document.getElementById('category');
  const randomness = document.querySelectorAll('input[name="randomness"]');
  const sentiment = document.querySelectorAll('input[name="sentiment"]');

  function loadSettings() {
    promptField.value = localStorage.getItem('whisperer_prompt') || promptField.value;
    instructions.value = localStorage.getItem('whisperer_instructions') || '';
    wordCount.value = localStorage.getItem('whisperer_word_count') || wordCount.value;
    category.value = localStorage.getItem('whisperer_category') || category.value;
    const rand = localStorage.getItem('whisperer_randomness');
    if (rand) {
      document.querySelector(`input[name="randomness"][value="${rand}"]`).checked = true;
    }
    const sent = localStorage.getItem('whisperer_sentiment');
    if (sent) {
      document.querySelector(`input[name="sentiment"][value="${sent}"]`).checked = true;
    }
  }

  function saveSettings() {
    localStorage.setItem('whisperer_prompt', promptField.value);
    localStorage.setItem('whisperer_instructions', instructions.value);
    localStorage.setItem('whisperer_word_count', wordCount.value);
    localStorage.setItem('whisperer_category', category.value);
    const randSel = document.querySelector('input[name="randomness"]:checked');
    if (randSel) localStorage.setItem('whisperer_randomness', randSel.value);
    const sentSel = document.querySelector('input[name="sentiment"]:checked');
    if (sentSel) localStorage.setItem('whisperer_sentiment', sentSel.value);
  }

  loadSettings();

  document.getElementById('generate').addEventListener('click', () => {
    saveSettings();
    const payload = {
      instructions: instructions.value,
      word_count: wordCount.value,
      category: category.value,
      randomness: document.querySelector('input[name="randomness"]:checked').value,
      sentiment: document.querySelector('input[name="sentiment"]:checked').value
    };
    fetch('/prompt-whisperer/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).then(r => r.json()).then(d => {
      promptField.value = d.prompt;
      category.value = d.category;
      saveSettings();
    });
  });

  document.getElementById('save').addEventListener('click', () => {
    saveSettings();
    const payload = {
      prompt: promptField.value,
      instructions: instructions.value,
      word_count: wordCount.value,
      category: category.value,
      randomness: document.querySelector('input[name="randomness"]:checked').value,
      sentiment: document.querySelector('input[name="sentiment"]:checked').value
    };
    fetch('/prompt-whisperer/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).then(r => r.json()).then(d => {
      if (d.saved) alert('Prompt saved');
    });
  });

  document.getElementById('clear').addEventListener('click', () => {
    promptField.value = '';
    instructions.value = '';
  });
});

```

---
## 📄 `ezygallery/static/js/script.js`

```js
/* ==========================================================================
   File: script.js
   Purpose: Handles interactive logic for the menu and theme toggling.
   ========================================================================== */

document.addEventListener("DOMContentLoaded", function () {
    const bodyTag = document.body;
    const htmlTag = document.documentElement;

    // === [ THEME TOGGLE LOGIC ] ===
    const themeToggle = document.getElementById("themeToggle");
    const themeIcon = document.getElementById("themeIcon");

    const userIcon = document.getElementById("userIcon");
    const userAuthLink = document.getElementById("userAuthLink");

    const icons = {
        sun: 'static/icons/svg/light/sun-light.svg',
        moon: 'static/icons/svg/light/moon-light.svg',
        user: 'static/icons/svg/light/user-circle-light.svg',
        userChecked: 'static/icons/svg/light/user-circle-check-light.svg'
    };

    const setTheme = (isDark) => {
        htmlTag.classList.toggle('dark', isDark);
        if (themeIcon) themeIcon.src = isDark ? icons.sun : icons.moon;
        localStorage.setItem('darkMode', isDark);
    };

    const savedThemeIsDark = localStorage.getItem('darkMode') === 'true';
    setTheme(savedThemeIsDark);

    const toggleTheme = () => {
        const isCurrentlyDark = htmlTag.classList.contains('dark');
        setTheme(!isCurrentlyDark);
    };

    if (themeToggle) themeToggle.addEventListener('click', toggleTheme);
    
    let isLoggedIn = false;
    const toggleLogin = (e) => {
        e.preventDefault();
        isLoggedIn = !isLoggedIn;
        if (userIcon) userIcon.src = isLoggedIn ? icons.userChecked : icons.user;
    };

    if (userAuthLink) userAuthLink.addEventListener('click', toggleLogin);


    // === [ OVERLAY MENU LOGIC ] ===
    const menuToggle = document.getElementById("menuToggle");
    const overlayMenu = document.getElementById("overlayMenu");
    const overlayClose = document.getElementById("overlayClose");

    let focusableElements = [];
    const focusableSelector = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';

    const openMenu = () => {
        if (!overlayMenu) return;
        overlayMenu.classList.add("is-active");
        overlayMenu.setAttribute('aria-hidden', 'false');
        if (menuToggle) menuToggle.setAttribute('aria-expanded', 'true');
        htmlTag.classList.add('overlay-open');
        bodyTag.style.overflow = 'hidden';
        focusableElements = overlayMenu.querySelectorAll(focusableSelector);
        if (overlayClose) overlayClose.focus();
    };

    const closeMenu = () => {
        if (!overlayMenu) return;
        overlayMenu.classList.remove("is-active");
        overlayMenu.setAttribute('aria-hidden', 'true');
        if (menuToggle) menuToggle.setAttribute('aria-expanded', 'false');
        htmlTag.classList.remove('overlay-open');
        bodyTag.style.overflow = '';
        if (menuToggle) menuToggle.focus();
    };

    if (menuToggle) menuToggle.addEventListener("click", openMenu);
    if (overlayClose) overlayClose.addEventListener("click", closeMenu);

    if (overlayMenu) {
        overlayMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', closeMenu);
        });
        overlayMenu.addEventListener('click', (event) => {
            const content = overlayMenu.querySelector('.overlay-content');
            if (!content.contains(event.target)) {
                closeMenu();
            }
        });
    }

    const handleTabTrap = (event) => {
        if (!overlayMenu.classList.contains('is-active')) return;
        const first = focusableElements[0];
        const last = focusableElements[focusableElements.length - 1];
        if (event.key === 'Tab') {
            if (event.shiftKey) {
                if (document.activeElement === first) {
                    event.preventDefault();
                    last.focus();
                }
            } else {
                if (document.activeElement === last) {
                    event.preventDefault();
                    first.focus();
                }
            }
        }
    };

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && overlayMenu.classList.contains('is-active')) {
            closeMenu();
        }
        handleTabTrap(event);
    });
});

```

---
## 📄 `static/css/menu-style.css`

```css
/* ==========================================================================
   File: style.css
   Purpose: Consolidated styles for ART Narrator.
   ========================================================================== */

/* --- [1] CSS Variables for Theming --- */
:root {
    --bg-color-light: #f9f9f6;
    --text-color-light: #0d0d0d;
    --border-color-light: #e0e0e0;
    --accent-color-light: #ed7214;
    --overlay-bg-light: rgba(249, 249, 246, 0.85);

    --bg-color-dark: #121212;
    --text-color-dark: #f0f0f0;
    --border-color-dark: #333;
    --accent-color-dark: #ed7214;
    --overlay-bg-dark: rgba(20, 20, 20, 0.85);
}

/* --- [2] Basic Body & Font Styles --- */
html, body {
    height: 100%;
}

body {
    margin: 0;
    font-family: monospace;
    background-color: var(--bg-color-light);
    color: var(--text-color-light);
    transition: background-color 0.3s ease, color 0.3s ease;
    display: flex;
    flex-direction: column;
}

html.dark body {
    background-color: var(--bg-color-dark);
    color: var(--text-color-dark);
}

.page-wrapper {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}

/* --- [3] Header Styles --- */
.site-header {
    padding: 1.5rem 2rem;
    border-bottom: 1px solid var(--border-color-light);
    position: relative;
    z-index: 1000;
}

html.dark .site-header {
    border-bottom-color: var(--border-color-dark);
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1600px;
    margin: 0 auto;
}

.header-left, .header-right {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex: 1;
}

.header-center {
    flex: 0 1 auto;
    text-align: center;
}

.header-right {
    justify-content: flex-end;
}

.logo, .cart, .menu-toggle {
    color: var(--text-color-light);
    text-decoration: none;
    font-weight: 500;
}

html.dark .logo, html.dark .cart, html.dark .menu-toggle {
    color: var(--text-color-dark);
}

.menu-toggle {
    background: none;
    border: 1px solid var(--text-color-light);
    padding: 0.5rem 1rem;
    cursor: pointer;
    border-radius: 20px;
    font-family: monospace;
    font-size: 1rem;
    transition: background-color 0.2s, color 0.2s;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}

html.dark .menu-toggle {
    border-color: var(--text-color-dark);
}

.menu-toggle:hover {
    background-color: var(--text-color-light);
    color: var(--bg-color-light);
}

html.dark .menu-toggle:hover {
    background-color: var(--text-color-dark);
    color: var(--bg-color-dark);
}

/* --- [4] Icon Styles --- */
.header-icon {
    width: 24px;
    height: 24px;
    vertical-align: middle;
}

.arrow-icon {
    width: 20px;
    height: 20px;
}

html.dark .header-icon {
    filter: invert(1);
}

.menu-toggle:hover .header-icon {
    filter: invert(1);
}
html.dark .menu-toggle:hover .header-icon {
    filter: none;
}


.header-icon-link, .theme-toggle-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: none;
    border: none;
    padding: 0.25rem;
    cursor: pointer;
    border-radius: 50%;
    transition: background-color 0.2s;
}

.header-icon-link:hover, .theme-toggle-btn:hover {
    background-color: rgba(0,0,0,0.05);
}

html.dark .header-icon-link:hover, html.dark .theme-toggle-btn:hover {
    background-color: rgba(255,255,255,0.1);
}


/* --- [5] Main Overlay Menu Styles --- */
#overlayMenu {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 999;
    visibility: hidden;
    opacity: 0;
    transition: opacity 0.4s cubic-bezier(0.25, 1, 0.5, 1), visibility 0.4s cubic-bezier(0.25, 1, 0.5, 1);
    background-color: var(--overlay-bg-light);
    -webkit-backdrop-filter: blur(15px);
    backdrop-filter: blur(15px);
    display: flex;
    align-items: center; /* Center content vertically */
    justify-content: center; /* Center content horizontally */
    overflow-y: auto;
}

html.dark #overlayMenu {
    background-color: var(--overlay-bg-dark);
}

#overlayMenu.is-active {
    visibility: visible;
    opacity: 1;
}

.overlay-header {
    position: absolute; /* Changed from fixed */
    top: 0;
    left: 0;
    width: 100%;
    padding: 1.5rem 2rem;
    box-sizing: border-box;
    z-index: 1001; /* Ensure header is on top of content */
}

.overlay-content {
    text-align: left;
    width: 90%;
    max-width: 1200px;
    padding: 6rem 0; /* Adjust padding to not be obscured by header */
}

/* --- [6] Two-Column Menu Layout --- */
.menu-columns {
    display: flex;
    justify-content: space-around;
    width: 100%;
    gap: 2rem;
}

.menu-column {
    list-style: none;
    padding: 0;
    margin: 0;
    flex: 1;
}

.overlay-content ul li {
    font-size: 3em;
    font-weight: 500;
    line-height: 1.4;
    margin: 0.5em 0;
    transform: translateY(20px);
    opacity: 0;
    transition: opacity 0.5s ease, transform 0.5s ease;
}

#overlayMenu.is-active .overlay-content ul li {
    transform: translateY(0);
    opacity: 1;
}

/* Staggered animation */
#overlayMenu.is-active .menu-column:nth-child(1) li:nth-child(1) { transition-delay: 0.25s; }
#overlayMenu.is-active .menu-column:nth-child(1) li:nth-child(2) { transition-delay: 0.30s; }
#overlayMenu.is-active .menu-column:nth-child(1) li:nth-child(3) { transition-delay: 0.35s; }
#overlayMenu.is-active .menu-column:nth-child(1) li:nth-child(4) { transition-delay: 0.40s; }
#overlayMenu.is-active .menu-column:nth-child(1) li:nth-child(5) { transition-delay: 0.45s; }
#overlayMenu.is-active .menu-column:nth-child(1) li:nth-child(6) { transition-delay: 0.50s; }
#overlayMenu.is-active .menu-column:nth-child(1) li:nth-child(7) { transition-delay: 0.55s; }

#overlayMenu.is-active .menu-column:nth-child(2) li:nth-child(1) { transition-delay: 0.27s; }
#overlayMenu.is-active .menu-column:nth-child(2) li:nth-child(2) { transition-delay: 0.32s; }
#overlayMenu.is-active .menu-column:nth-child(2) li:nth-child(3) { transition-delay: 0.37s; }
#overlayMenu.is-active .menu-column:nth-child(2) li:nth-child(4) { transition-delay: 0.42s; }
#overlayMenu.is-active .menu-column:nth-child(2) li:nth-child(5) { transition-delay: 0.47s; }
#overlayMenu.is-active .menu-column:nth-child(2) li:nth-child(6) { transition-delay: 0.52s; }
#overlayMenu.is-active .menu-column:nth-child(2) li:nth-child(7) { transition-delay: 0.57s; }

.overlay-content a {
    color: var(--text-color-light);
    text-decoration: none;
    transition: color 0.3s ease;
}

html.dark .overlay-content a {
    color: var(--text-color-dark);
}

.overlay-content a:hover {
    color: var(--accent-color-light);
}

html.dark .overlay-content a:hover {
    color: var(--accent-color-dark);
}

/* --- [7] Main Content & Footer Styles --- */
.main-content {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
    flex-grow: 1;
}

.site-footer {
    background-color: var(--bg-color-light);
    border-top: 1px solid var(--border-color-light);
    padding: 3rem 2rem;
    color: var(--text-color-light);
}

html.dark .site-footer {
    background-color: var(--bg-color-dark);
    border-top-color: var(--border-color-dark);
    color: var(--text-color-dark);
}

.footer-content {
    max-width: 1600px;
    margin: 0 auto;
}

.footer-columns {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.footer-col h4 {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 1rem;
}

.footer-col p {
    font-size: 0.9rem;
    line-height: 1.6;
    opacity: 0.8;
}

.footer-col ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.footer-col ul li {
    margin-bottom: 0.5rem;
}

.footer-col a {
    color: var(--text-color-light);
    text-decoration: none;
    opacity: 0.8;
    transition: opacity 0.2s;
}

html.dark .footer-col a {
    color: var(--text-color-dark);
}

.footer-col a:hover {
    opacity: 1;
    text-decoration: underline;
}

.newsletter-form {
    display: flex;
}

.newsletter-form input {
    flex-grow: 1;
    border: 1px solid var(--border-color-light);
    border-right: none;
    padding: 0.75rem;
    background: transparent;
    color: var(--text-color-light);
    font-family: monospace;
}
html.dark .newsletter-form input {
    border-color: var(--border-color-dark);
    color: var(--text-color-dark);
}

.newsletter-form button {
    background: transparent;
    border: 1px solid var(--border-color-light);
    padding: 0.5rem;
    cursor: pointer;
}
html.dark .newsletter-form button {
    border-color: var(--border-color-dark);
}

.copyright-bar {
    border-top: 1px solid var(--border-color-light);
    padding-top: 1.5rem;
    margin-top: 2rem;
    text-align: center;
    font-size: 0.8rem;
    opacity: 0.7;
}
html.dark .copyright-bar {
    border-top-color: var(--border-color-dark);
}

/* --- [8] Responsive Styles for Mobile --- */
@media (max-width: 768px) {
    .menu-columns {
        flex-direction: column;
        align-items: center;
        text-align: center;
        gap: 0;
    }
    .overlay-content ul li {
        font-size: clamp(1.5rem, 6vw, 2.5rem);
    }
}
```

---
## 📄 `static/css/theme.css`

```css
:root {
    --bg-color: #ffffff;
    --text-color: #000000;
}

.theme-dark {
    --bg-color: #121212;
    --text-color: #e0e0e0;
}

body {
    background-color: var(--bg-color);
    color: var(--text-color);
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
}

```

---
## 📄 `static/css/global.css`

```css
:root {
  --font-header: serif;
  --font-body: sans-serif;
}

body {
  font-family: var(--font-body);
  margin: 0;
  padding: 0;
}

h1, h2, h3 {
  font-family: var(--font-header);
}

header {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: white;
  border-bottom: 1px solid #eee;
}

header .row-1,
header .row-2 {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
}

header .row-2 {
  justify-content: center;
  gap: 2rem;
}

/* Menu overlay styles */
.menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: white;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  padding: 4rem;
  gap: 2rem;
  transform: translateY(-100%);
  transition: transform 0.3s ease;
  font-size: 3rem;
}

body.menu--open .menu-overlay {
  transform: translateY(0);
}

.menu-overlay a {
  text-decoration: none;
  color: black;
}

```

---
## 📄 `static/css/style.css`

```css
body {
    font-family: Arial, Helvetica, sans-serif;
}
h1, h2, h3 {
    font-family: Georgia, "Times New Roman", serif;
}
h1 { letter-spacing: -0.7px; }
h2 { letter-spacing: -0.6px; }
h3 { letter-spacing: -0.5px; }

```

---
## 📄 `static/js/main.js`

```js
document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.getElementById("menu-toggle");
  const menuLinks = document.querySelectorAll(".menu-overlay a");

  menuToggle?.addEventListener("click", () => {
    document.body.classList.toggle("menu--open");
  });

  menuLinks.forEach(link => {
    link.addEventListener("click", () => {
      document.body.classList.remove("menu--open");
    });
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      document.body.classList.remove("menu--open");
    }
  });
});

```

---
## 📄 `static/js/base.js`

```js
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('theme-toggle');
  if (!toggle) return;
  const saved = localStorage.getItem('theme') || 'light';
  applyTheme(saved);

  toggle.addEventListener('click', () => {
    const isDark = document.documentElement.classList.contains('theme-dark');
    applyTheme(isDark ? 'light' : 'dark');
  });
});

function applyTheme(theme) {
  if (theme === 'dark') {
    document.documentElement.classList.add('theme-dark');
  } else {
    document.documentElement.classList.remove('theme-dark');
  }
  localStorage.setItem('theme', theme);
}

```

---
## 📄 `static/js/menu-script.js`

```js
/* ==========================================================================
   File: script.js
   Purpose: Handles interactive logic for the menu and theme toggling.
   ========================================================================== */

document.addEventListener("DOMContentLoaded", function () {
    const bodyTag = document.body;
    const htmlTag = document.documentElement;

    // === [ THEME TOGGLE LOGIC ] ===
    const themeToggle = document.getElementById("themeToggle");
    const themeToggleOverlay = document.getElementById("themeToggleOverlay");
    const themeIcon = document.getElementById("themeIcon");
    const themeIconOverlay = document.getElementById("themeIconOverlay");
    
    const userIcon = document.getElementById("userIcon");
    const userIconOverlay = document.getElementById("userIconOverlay");
    const userAuthLink = document.getElementById("userAuthLink");
    const userAuthLinkOverlay = document.getElementById("userAuthLinkOverlay");

    const icons = {
        sun: 'static/icons/svg/light/sun-light.svg',
        moon: 'static/icons/svg/light/moon-light.svg',
        user: 'static/icons/svg/light/user-circle-light.svg',
        userChecked: 'static/icons/svg/light/user-circle-check-light.svg'
    };

    const setTheme = (isDark) => {
        htmlTag.classList.toggle('dark', isDark);
        if (themeIcon) themeIcon.src = isDark ? icons.sun : icons.moon;
        if (themeIconOverlay) themeIconOverlay.src = isDark ? icons.sun : icons.moon;
        localStorage.setItem('darkMode', isDark);
    };

    const savedThemeIsDark = localStorage.getItem('darkMode') === 'true';
    setTheme(savedThemeIsDark);

    const toggleTheme = () => {
        const isCurrentlyDark = htmlTag.classList.contains('dark');
        setTheme(!isCurrentlyDark);
    };

    if (themeToggle) themeToggle.addEventListener('click', toggleTheme);
    if (themeToggleOverlay) themeToggleOverlay.addEventListener('click', toggleTheme);
    
    let isLoggedIn = false;
    const toggleLogin = (e) => {
        e.preventDefault();
        isLoggedIn = !isLoggedIn;
        if (userIcon) userIcon.src = isLoggedIn ? icons.userChecked : icons.user;
        if (userIconOverlay) userIconOverlay.src = isLoggedIn ? icons.userChecked : icons.user;
    };

    if (userAuthLink) userAuthLink.addEventListener('click', toggleLogin);
    if (userAuthLinkOverlay) userAuthLinkOverlay.addEventListener('click', toggleLogin);


    // === [ OVERLAY MENU LOGIC ] ===
    const menuToggle = document.getElementById("menuToggle");
    const menuToggleOverlay = document.getElementById("menuToggleOverlay");
    const overlayMenu = document.getElementById("overlayMenu");

    const openMenu = () => {
        if (!overlayMenu) return;
        overlayMenu.classList.add("is-active");
        bodyTag.style.overflow = 'hidden';
    };

    const closeMenu = () => {
        if (!overlayMenu) return;
        overlayMenu.classList.remove("is-active");
        bodyTag.style.overflow = '';
    };

    if (menuToggle) menuToggle.addEventListener("click", openMenu);
    if (menuToggleOverlay) menuToggleOverlay.addEventListener("click", closeMenu);

    if (overlayMenu) {
      overlayMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', closeMenu);
      });
        overlayMenu.addEventListener('click', (event) => {
            // This checks if the click was on the overlay background itself,
            // and NOT on any of its children (like the content or header).
            if (event.target === overlayMenu) {
                closeMenu();
            }
        });
    }

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && overlayMenu.classList.contains('is-active')) {
            closeMenu();
        }
    });
});
```
