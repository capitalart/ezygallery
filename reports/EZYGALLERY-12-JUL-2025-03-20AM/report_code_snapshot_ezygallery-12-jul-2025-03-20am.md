# 🧠 EzyGallery Code Snapshot — EZYGALLERY-12-JUL-2025-03-20AM


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
echo "# ezy.py - Main app bootstrap" > ezy.py
echo "# Updated: 12 July 2025 — Added Codex snapshot awareness 💚" >> ezy.py

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

# Optional: Automatically detect latest snapshot folder (most recent by mod time)
LATEST_SNAPSHOT_DIR=$(ls -td reports/EZYGALLERY-* | head -n 1 || true)
if [[ -d "$LATEST_SNAPSHOT_DIR" ]]; then
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
  log "🔄 Pulling latest changes..."
  git pull origin main --rebase 2>>"$LOG_FILE" || {
    log "❌ git pull --rebase failed."
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
gunicorn
```

---
## 📄 `ezy.py`

```py
# ezy.py - Main app bootstrap
# Updated: 12 July 2025 — Added Codex snapshot awareness 💚

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

```

---
## 📄 `templates/gallery_page.html`

```html
{% extends 'base.html' %}
{% block title %}Gallery - EzyGallery{% endblock %}
{% block content %}
<h2>Gallery</h2>
<p>Gallery content coming soon.</p>
{% endblock %}

```

---
## 📄 `templates/home.html`

```html
{% extends 'base.html' %}
{% block title %}Home - EzyGallery{% endblock %}
{% block content %}
<h2>Welcome to EzyGallery</h2>
<p>This is the home page.</p>
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
{% block content %}
<h1>Hello World from Gallery</h1>
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
{% extends 'layout.html' %}
{% block content %}
<h1>Hello World from Home</h1>
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
    <title>{% block title %}EzyGallery{% endblock %}</title>
    <meta name="description" content="EzyGallery - a minimal Flask gallery.">
    <link rel="icon" href="{{ url_for('static', filename='img/favicon.svg') }}" type="image/svg+xml">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/theme.css') }}">
    {% block head %}{% endblock %}
</head>
<body>
<header>
    <h1><a href="{{ url_for('home') }}">EzyGallery</a></h1>
    <nav>
        <a href="{{ url_for('home') }}">Home</a> |
        <a href="{{ url_for('gallery') }}">Gallery</a> |
        <a href="{{ url_for('about') }}">About</a> |
        <a href="{{ url_for('contact') }}">Contact</a>
    </nav>
</header>
<main>
    {% block content %}{% endblock %}
</main>
<script src="{{ url_for('static', filename='js/base.js') }}"></script>
{% block scripts %}{% endblock %}
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
<!-- Main layout template -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>EzyGallery</title>
    <link rel="stylesheet" href="{{ static_url('css/theme.css') }}">
</head>
<body>
    {% include 'components/header.html' %}
    {% block content %}{% endblock %}
    <script src="{{ static_url('js/base.js') }}"></script>
</body>
</html>

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
## 📄 `templates/home/home.html`

```html
{% extends 'layout.html' %}
{% block content %}
<h2>Welcome to EzyGallery</h2>
<nav>
  <a href="/gallery">Gallery</a> |
  <a href="/uploads">Uploads</a> |
  <a href="/docs">Docs</a>
</nav>
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
# Artwork model placeholder

```

---
## 📄 `models/review.py`

```py
# Review model placeholder

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
## 📄 `routes/account.py`

```py
from flask import Blueprint, render_template

account_bp = Blueprint('account', __name__, url_prefix='/account')

@account_bp.route('/')
def account():
    return render_template('account.html')

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
from flask import Blueprint, render_template

art_bp = Blueprint('art', __name__, url_prefix='/art')

@art_bp.route('/<int:art_id>')
def art_detail(art_id):
    return render_template('art_detail.html', art_id=art_id)

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
    return render_template('home/home.html')

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
