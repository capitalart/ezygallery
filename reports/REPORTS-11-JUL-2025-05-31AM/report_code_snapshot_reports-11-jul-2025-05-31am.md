# 🧠 EzyGallery Code Snapshot — REPORTS-11-JUL-2025-05-31AM


---
## 📄 config.py

```py
import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'changeme'

```

---
## 📄 git-update-push.sh

```sh
#!/bin/bash

# =====================================================
# 🔁 EzyGallery Git Update + Commit + Push + Backup
# 💥 Robbie Mode™ Gitflow Commander + Backup Engine + Cloud Upload
# Run Auto Mode:    ./git-update-push.sh --full-auto
# Options:
# Run:    ./git-update-push.sh --just git       Skip everything else
# Run:    ./git-update-push.sh --full-auto      Does everything
# Run:    ./git-update-push.sh --no-zip         Skip local ZIP backup
# Run:    ./git-update-push.sh --no-cloud       Skip rclone upload to Google Drive
# Run:    ./git-update-push.sh --no-retention   Skip retention cleanup in Google Drive
# Run:    ./git-update-push.sh --no-git         Skip git pull/push sync
# =====================================================

set -euo pipefail

LOG_DIR="git-update-push-logs"
BACKUP_DIR="backups"
mkdir -p "$LOG_DIR" "$BACKUP_DIR"

NOW=$(date '+%Y-%m-%d-%H-%M-%p')
LOG_FILE="$LOG_DIR/git-update-push-${NOW}.log"
BACKUP_ZIP="$BACKUP_DIR/${NOW}_backup.zip"
DIFF_RAW="$BACKUP_DIR/diff-raw.txt"
DIFF_REPORT="$BACKUP_DIR/backup-diff-REPORT.md"
COMMIT_MSG_FILE=".codex-commit-msg.txt"
GDRIVE_REMOTE="gdrive"
GDRIVE_FOLDER="ezygallery-backups"

# Default flags
AUTO_MODE=false
ENABLE_ZIP=true
ENABLE_CLOUD=true
ENABLE_RETENTION=true
ENABLE_GIT=true
JUST_GIT=false

# Flag parser
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

function log() {
  local msg="$1"
  local ts
  ts=$(date '+%Y-%m-%d %H:%M:%S')
  echo "[$ts] $msg" | tee -a "$LOG_FILE"
}

log "=== 🟢 EzyGallery Git + Backup Script Started ==="

# Git staging/commit
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

# === RUN total-rundown ===
if [ -f "./ezygallery-total-rundown.py" ]; then
  log "🧠 Running EzyGallery Total Rundown..."
  python3 ezygallery-total-rundown.py >> "$LOG_FILE" 2>&1 || log "⚠️ Rundown script failed."
else
  log "ℹ️ Rundown script not found."
fi

# Skip backup/cloud if JUST_GIT
if $JUST_GIT; then
  log "⏹️ JUST GIT MODE: Skipping all backup & cloud steps."
  exit 0
fi

# Create backup ZIP
if $ENABLE_ZIP; then
  log "📦 Creating full backup ZIP archive..."
  zip -r "$BACKUP_ZIP" . \
    -x ".git/*" "*.git*" "__pycache__/*" "node_modules/*" "venv/*" "outputs/*" "inputs/*" ".cache/*" ".mypy_cache/*" ".pytest_cache/*" "$BACKUP_DIR/*" "$LOG_DIR/*" "*.DS_Store" "*.pyc" "*.pyo" ".env" "*.sqlite3" >> "$LOG_FILE"
  log "✅ Backup ZIP created: $BACKUP_ZIP"
else
  log "⏭️ Skipping ZIP backup (flag --no-zip)"
fi

# Markdown diff report
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

# Git pull + push
if $ENABLE_GIT; then
  log "🔄 Pulling latest from origin/main..."
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
  log "⏭️ Skipping git pull/push (flag --no-git)"
fi

# Cloud backup with rclone
if $ENABLE_CLOUD; then
  log "☁️ Uploading to Google Drive ($GDRIVE_REMOTE:$GDRIVE_FOLDER)..."
  if command -v rclone >/dev/null 2>&1; then
    if rclone copy "$BACKUP_ZIP" "$GDRIVE_REMOTE:$GDRIVE_FOLDER" >> "$LOG_FILE" 2>&1; then
      log "✅ Uploaded to Drive folder: $GDRIVE_FOLDER"
    else
      log "❌ Rclone upload failed."
    fi
  else
    log "⚠️ rclone not found — skipping upload."
  fi
else
  log "⏭️ Skipping cloud upload (flag --no-cloud)"
fi

# Retention
if $ENABLE_RETENTION && $ENABLE_CLOUD; then
  log "🧹 Applying cloud retention policy (max 30 backups)..."
  if command -v rclone >/dev/null 2>&1 && command -v jq >/dev/null 2>&1; then
    OLD_FILES=$(rclone lsjson "$GDRIVE_REMOTE:$GDRIVE_FOLDER" \
      | jq -r '.[] | select(.IsDir == false) | "\(.ModTime) \(.Path)"' \
      | sort \
      | head -n -30 | cut -d' ' -f2-)
    if [[ -n "$OLD_FILES" ]]; then
      while IFS= read -r file; do
        log "🗑️ Deleting old backup: $file"
        rclone delete "$GDRIVE_REMOTE:$GDRIVE_FOLDER/$file" >> "$LOG_FILE" 2>&1 || true
      done <<< "$OLD_FILES"
      log "✅ Cloud cleanup complete."
    else
      log "ℹ️ Less than 30 cloud files — no cleanup needed."
    fi
  else
    log "⚠️ jq or rclone not found — skipping retention."
  fi
else
  log "⏭️ Skipping cloud retention (flag --no-retention or --no-cloud)"
fi

log "🎉 All done, Robbie! Git, ZIP, rundown, cloud and cleanup complete. 💚"

```

---
## 📄 ezygallery-total-rundown.py

```py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ===========================================
# 🔥 EzyGallery Total Nuclear Snapshot v2.2
# 🚀 Ultimate Dev Toolkit by Robbie Mode™
# All errors & output logged to DEV_LOGS_DIR/snapshot-YYYY-MM-DD-HHMMSS.log
#
# USAGE EXAMPLES:
#   python3 ezygallery-total-rundown.py
#   python3 ezygallery-total-rundown.py --no-zip
#   python3 ezygallery-total-rundown.py --skip-git --skip-env
# ===========================================

import os
import sys
import datetime
import subprocess
import zipfile
import py_compile
from pathlib import Path
from typing import Generator
import argparse
import traceback

# --- You may want to set DEV_LOGS_DIR to a local path in ezygallery! ---
DEV_LOGS_DIR = Path("./git-update-push-logs")

# -------------------------------------------
ALLOWED_EXTENSIONS = {".py", ".sh", ".jsx", ".txt", ".html", ".js", ".css"}
EXCLUDED_EXTENSIONS = {".json"}
EXCLUDED_FOLDERS = {
    "venv", ".venv", "__MACOSX", ".git", ".vscode", "reports",
    "backups", "node_modules", ".idea", "__pycache__"
}
EXCLUDED_FILES = {".DS_Store"}
LOGS_DIR = DEV_LOGS_DIR
LOGS_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH = LOGS_DIR / f"snapshot-{datetime.datetime.now():%Y-%m-%d-%H%M%S}.log"


def log(msg):
    print(msg)
    with open(LOG_PATH, "a", encoding="utf-8") as logf:
        logf.write(f"{datetime.datetime.now():[%Y-%m-%d %H:%M:%S]} {msg}\n")


def log_error(msg):
    print(f"\033[91m{msg}\033[0m")  # Red in terminal
    with open(LOG_PATH, "a", encoding="utf-8") as logf:
        logf.write(f"{datetime.datetime.now():[%Y-%m-%d %H:%M:%S]} ERROR: {msg}\n")


def get_timestamp() -> str:
    return datetime.datetime.now().strftime("REPORTS-%d-%b-%Y-%I-%M%p").upper()


def create_reports_folder() -> Path:
    timestamp = get_timestamp()
    folder_path = Path("reports") / timestamp
    folder_path.mkdir(parents=True, exist_ok=True)
    log(f"📁 Created report folder: {folder_path}")
    return folder_path


def get_included_files() -> Generator[Path, None, None]:
    for path in Path(".").rglob("*"):
        if (
            path.is_file()
            and path.suffix in ALLOWED_EXTENSIONS
            and path.suffix not in EXCLUDED_EXTENSIONS
            and path.name not in EXCLUDED_FILES
            and not any(str(part).lower() in EXCLUDED_FOLDERS for part in path.parts)
        ):
            try:
                path.stat()
                yield path
            except Exception:
                continue


def gather_code_snapshot(folder: Path) -> Path:
    md_path = folder / f"report_code_snapshot_{folder.name.lower()}.md"
    with open(md_path, "w", encoding="utf-8") as md_file:
        md_file.write(f"# 🧠 EzyGallery Code Snapshot — {folder.name}\n\n")
        for file in get_included_files():
            rel_path = file.relative_to(Path("."))
            log(f"📄 Including file: {rel_path}")
            md_file.write(f"\n---\n## 📄 {rel_path}\n\n```{file.suffix[1:] if file.suffix else ''}\n")
            try:
                with open(file, "r", encoding="utf-8") as f:
                    md_file.write(f.read())
            except Exception as e:
                md_file.write(f"[ERROR READING FILE: {e}]")
            md_file.write("\n```\n")
    log(f"✅ Code snapshot saved to: {md_path}")
    return md_path


def generate_file_summary(folder: Path) -> None:
    summary_path = folder / "file_summary.md"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("# 📊 File Summary\n\n")
        f.write("| File | Size (KB) | Last Modified |\n")
        f.write("|------|------------|----------------|\n")
        for file in get_included_files():
            try:
                size_kb = round(file.stat().st_size / 1024, 1)
                mtime = datetime.datetime.fromtimestamp(file.stat().st_mtime)
                rel = file.relative_to(Path("."))
                f.write(f"| `{rel}` | {size_kb} KB | {mtime:%Y-%m-%d %H:%M} |\n")
            except Exception:
                continue
    log(f"📋 File summary written to: {summary_path}")


def validate_python_files() -> None:
    log("\n🧪 Validating Python syntax...")
    for file in get_included_files():
        if file.suffix == ".py":
            try:
                py_compile.compile(file, doraise=True)
                log(f"✅ {file}")
            except py_compile.PyCompileError as e:
                log_error(f"❌ {file} → {e.msg}")


def log_git_status(folder: Path) -> None:
    git_path = folder / "git_snapshot.txt"
    try:
        with open(git_path, "w", encoding="utf-8") as f:
            f.write("🔧 Git Status:\n")
            subprocess.run(["git", "status"], stdout=f, stderr=subprocess.STDOUT, check=False)
            f.write("\n🔁 Last Commit:\n")
            subprocess.run(["git", "log", "-1"], stdout=f, stderr=subprocess.STDOUT, check=False)
            f.write("\n🧾 Diff Summary:\n")
            subprocess.run(["git", "diff", "--stat"], stdout=f, stderr=subprocess.STDOUT, check=False)
        log(f"📘 Git snapshot written to: {git_path}")
    except Exception as e:
        log_error(f"Could not write git snapshot: {e}")


def log_environment_details(folder: Path) -> None:
    env_path = folder / "env_metadata.txt"
    try:
        with open(env_path, "w", encoding="utf-8") as f:
            f.write("🐍 Python Version:\n")
            subprocess.run(["python3", "--version"], stdout=f, stderr=subprocess.STDOUT, check=False)
            f.write("\n🖥️ Platform Info:\n")
            if sys.platform != "win32":
                subprocess.run(["uname", "-a"], stdout=f, stderr=subprocess.STDOUT, check=False)
            f.write("\n📦 Installed Packages:\n")
            subprocess.run(["pip", "freeze"], stdout=f, stderr=subprocess.STDOUT, check=False)
        log(f"📚 Environment metadata saved to: {env_path}")
    except Exception as e:
        log_error(f"Failed environment details: {e}")


def show_dependency_issues() -> None:
    log("\n🔍 Running pip check...")
    try:
        subprocess.run(["pip", "check"])
        log("\n📦 Outdated packages:")
        subprocess.run(["pip", "list", "--outdated"])
    except Exception as e:
        log_error(f"pip not found or check failed: {e}")


def zip_report_folder(folder: Path) -> Path:
    zip_path = folder.with_suffix(".zip")
    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in folder.rglob("*"):
                zipf.write(file, file.relative_to(folder.parent))
        log(f"📦 Report zipped to: {zip_path}")
        return zip_path
    except Exception as e:
        log_error(f"Zipping report failed: {e}")
        return zip_path


def parse_args():
    parser = argparse.ArgumentParser(description="EzyGallery Dev Snapshot Generator")
    parser.add_argument("--no-zip", action="store_true", help="Skip ZIP archive creation")
    parser.add_argument("--skip-env", action="store_true", help="Skip environment metadata logging")
    parser.add_argument("--skip-validate", action="store_true", help="Skip Python syntax validation")
    parser.add_argument("--skip-git", action="store_true", help="Skip Git snapshot logging")
    parser.add_argument("--skip-pip-check", action="store_true", help="Skip pip dependency checks")
    return parser.parse_args()


def main():
    args = parse_args()
    log("🎨 Generating EzyGallery Total Nuclear Snapshot (v2.2)...")
    try:
        report_folder = create_reports_folder()
        try:
            gather_code_snapshot(report_folder)
        except Exception:
            log_error(f"Code snapshot failed: {traceback.format_exc()}")
        try:
            generate_file_summary(report_folder)
        except Exception:
            log_error(f"File summary failed: {traceback.format_exc()}")
        if not args.skip_validate:
            try:
                validate_python_files()
            except Exception:
                log_error(f"Python validation failed: {traceback.format_exc()}")
        if not args.skip_env:
            try:
                log_environment_details(report_folder)
            except Exception:
                log_error(f"Env details failed: {traceback.format_exc()}")
        if not args.skip_git:
            try:
                log_git_status(report_folder)
            except Exception:
                log_error(f"Git snapshot failed: {traceback.format_exc()}")
        if not args.skip_pip_check:
            try:
                show_dependency_issues()
            except Exception:
                log_error(f"Pip checks failed: {traceback.format_exc()}")
        if not args.no_zip:
            try:
                zip_report_folder(report_folder)
            except Exception:
                log_error(f"Zip step failed: {traceback.format_exc()}")
        log("✅ Snapshot complete. All systems green, Robbie! 💚")
    except Exception:
        log_error(f"Top-level script failure: {traceback.format_exc()}")


if __name__ == "__main__":
    main()

```

---
## 📄 requirements.txt

```txt
alembic==1.16.4
amqp==5.3.1
aniso8601==10.0.1
async-timeout==5.0.1
bcrypt==4.3.0
billiard==4.2.1
blinker==1.9.0
cachelib==0.13.0
celery==5.5.3
certifi==2025.7.9
charset-normalizer==3.4.2
click==8.2.1
click-didyoumean==0.3.1
click-plugins==1.1.1.2
click-repl==0.3.0
Deprecated==1.2.18
Flask==3.1.1
Flask-Admin==1.6.1
Flask-Caching==2.3.1
Flask-Limiter==3.12
Flask-Login==0.6.3
Flask-Mail==0.10.0
Flask-Migrate==4.1.0
flask-paginate==2024.4.12
Flask-RESTful==0.3.10
Flask-SQLAlchemy==3.1.1
Flask-Uploads==0.2.1
Flask-WTF==1.2.2
greenlet==3.2.3
idna==3.10
iniconfig==2.1.0
itsdangerous==2.2.0
Jinja2==3.1.6
kombu==5.5.4
limits==5.4.0
Mako==1.3.10
Markdown==3.8.2
markdown-it-py==3.0.0
MarkupSafe==3.0.2
marshmallow==4.0.0
mdurl==0.1.2
ordered-set==4.1.0
packaging==25.0
pillow==11.3.0
pluggy==1.6.0
prompt_toolkit==3.0.51
Pygments==2.19.2
pytest==8.4.1
python-dateutil==2.9.0.post0
python-dotenv==1.1.1
pytz==2025.2
qrcode==8.2
redis==5.2.1
requests==2.32.4
rich==13.9.4
six==1.17.0
SQLAlchemy==2.0.41
stripe==12.3.0
typing_extensions==4.14.1
tzdata==2025.2
urllib3==2.5.0
vine==5.1.0
wcwidth==0.2.13
Werkzeug==3.1.3
wrapt==1.17.2
WTForms==3.2.1

```

---
## 📄 ezy.py

```py
from flask import Flask
from routes.gallery import gallery_bp
from routes.marketplace import marketplace_bp
from routes.auth import auth_bp
from routes.admin import admin_bp

app = Flask(__name__, static_folder='static')
app.config.from_pyfile('config.py', silent=True)

# Register blueprints
app.register_blueprint(gallery_bp)
app.register_blueprint(marketplace_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)

```

---
## 📄 setup_ezygallery_pro.sh

```sh
#!/bin/bash
set -e

# ---- Make Folders ----
cd ~
mkdir -p ezygallery/{routes,scripts,logs,tests}
mkdir -p ezygallery/static/{css,js,images,icons,fonts}
mkdir -p ezygallery/templates/{components,admin,auth,gallery,marketplace}

cd ezygallery
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip flask

# ---- Requirements ----
pip freeze > requirements.txt

# ---- .gitignore ----
cat <<EOL > .gitignore
venv/
__pycache__/
*.pyc
.env
logs/
EOL

# ---- .env ----
cat <<EOL > .env
FLASK_ENV=development
SECRET_KEY=$(openssl rand -hex 16)
EOL

# ---- README.md ----
echo "# EzyGallery.com — Digital Art Marketplace" > README.md

# ---- config.py ----
cat <<EOL > config.py
import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'changeme'
EOL

# ---- Placeholder CSS files ----
cat <<EOL > static/css/base.css
body { font-family: sans-serif; background: #faf9f6; margin:0; padding:0;}
EOL
touch static/css/components.css static/css/layout.css static/css/theme.css static/css/sidebar.css

# ---- Placeholder JS ----
touch static/js/base.js

# ---- Placeholder templates ----
# main.html with nav
cat <<'EOL' > templates/main.html
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{% block title %}EzyGallery.com{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/base.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/layout.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/theme.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/components.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/sidebar.css') }}">
</head>
<body>
    <nav>
        <a href="{{ url_for('gallery_bp.gallery_home') }}">Gallery</a> |
        <a href="{{ url_for('marketplace_bp.marketplace_home') }}">Marketplace</a> |
        <a href="{{ url_for('auth_bp.login') }}">Login</a> |
        <a href="{{ url_for('admin_bp.admin_home') }}">Admin</a>
    </nav>
    <div id="main-content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
EOL

# ---- Section templates ----
cat <<EOL > templates/gallery/gallery_home.html
{% extends "main.html" %}
{% block title %}Gallery — EzyGallery.com{% endblock %}
{% block content %}
<h1>Gallery</h1>
<p>This is the Gallery section. (Placeholder)</p>
{% endblock %}
EOL

cat <<EOL > templates/marketplace/marketplace_home.html
{% extends "main.html" %}
{% block title %}Marketplace — EzyGallery.com{% endblock %}
{% block content %}
<h1>Marketplace</h1>
<p>This is the Marketplace section. (Placeholder)</p>
{% endblock %}
EOL

cat <<EOL > templates/auth/login.html
{% extends "main.html" %}
{% block title %}Login — EzyGallery.com{% endblock %}
{% block content %}
<h1>Login</h1>
<p>Login form coming soon!</p>
{% endblock %}
EOL

cat <<EOL > templates/admin/admin_home.html
{% extends "main.html" %}
{% block title %}Admin — EzyGallery.com{% endblock %}
{% block content %}
<h1>Admin Dashboard</h1>
<p>Admin section placeholder.</p>
{% endblock %}
EOL

cat <<EOL > templates/components/header.html
<!-- Header component (you can {% include %} this anywhere) -->
<header><h2>EzyGallery Header</h2></header>
EOL

# ---- Blueprints in routes/ ----
cat <<EOL > routes/gallery.py
from flask import Blueprint, render_template

gallery_bp = Blueprint('gallery_bp', __name__, template_folder='../templates/gallery')

@gallery_bp.route('/')
def gallery_home():
    return render_template('gallery/gallery_home.html')
EOL

cat <<EOL > routes/marketplace.py
from flask import Blueprint, render_template

marketplace_bp = Blueprint('marketplace_bp', __name__, template_folder='../templates/marketplace')

@marketplace_bp.route('/marketplace')
def marketplace_home():
    return render_template('marketplace/marketplace_home.html')
EOL

cat <<EOL > routes/auth.py
from flask import Blueprint, render_template

auth_bp = Blueprint('auth_bp', __name__, template_folder='../templates/auth')

@auth_bp.route('/login')
def login():
    return render_template('auth/login.html')
EOL

cat <<EOL > routes/admin.py
from flask import Blueprint, render_template

admin_bp = Blueprint('admin_bp', __name__, template_folder='../templates/admin')

@admin_bp.route('/admin')
def admin_home():
    return render_template('admin/admin_home.html')
EOL

# ---- Main app ezy.py ----
cat <<EOL > ezy.py
from flask import Flask
from routes.gallery import gallery_bp
from routes.marketplace import marketplace_bp
from routes.auth import auth_bp
from routes.admin import admin_bp

app = Flask(__name__, static_folder='static')
app.config.from_pyfile('config.py', silent=True)

# Register blueprints
app.register_blueprint(gallery_bp)
app.register_blueprint(marketplace_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
EOL

echo "✅ EzyGallery project structure created with modular routes, templates, CSS, and nav!"
echo "1. cd ~/ezygallery"
echo "2. source venv/bin/activate"
echo "3. python ezy.py"
echo "4. Visit http://localhost:8001/ (Gallery), /marketplace, /login, /admin"


```

---
## 📄 templates/main.html

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{% block title %}EzyGallery.com{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/base.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/layout.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/theme.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/components.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/sidebar.css') }}">
</head>
<body>
    <nav>
        <a href="{{ url_for('gallery_bp.gallery_home') }}">Gallery</a> |
        <a href="{{ url_for('marketplace_bp.marketplace_home') }}">Marketplace</a> |
        <a href="{{ url_for('auth_bp.login') }}">Login</a> |
        <a href="{{ url_for('admin_bp.admin_home') }}">Admin</a>
    </nav>
    <div id="main-content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>

```

---
## 📄 templates/auth/login.html

```html
{% extends "main.html" %}
{% block title %}Login — EzyGallery.com{% endblock %}
{% block content %}
<h1>Login</h1>
<p>Login form coming soon!</p>
{% endblock %}

```

---
## 📄 templates/gallery/gallery_home.html

```html
{% extends "main.html" %}
{% block title %}Gallery — EzyGallery.com{% endblock %}
{% block content %}
<h1>Gallery</h1>
<p>This is the Gallery section. (Placeholder)</p>
{% endblock %}

```

---
## 📄 templates/marketplace/marketplace_home.html

```html
{% extends "main.html" %}
{% block title %}Marketplace — EzyGallery.com{% endblock %}
{% block content %}
<h1>Marketplace</h1>
<p>This is the Marketplace section. (Placeholder)</p>
{% endblock %}

```

---
## 📄 templates/components/header.html

```html
<!-- Header component (you can {% include %} this anywhere) -->
<header><h2>EzyGallery Header</h2></header>

```

---
## 📄 templates/admin/admin_home.html

```html
{% extends "main.html" %}
{% block title %}Admin — EzyGallery.com{% endblock %}
{% block content %}
<h1>Admin Dashboard</h1>
<p>Admin section placeholder.</p>
{% endblock %}

```

---
## 📄 routes/gallery.py

```py
from flask import Blueprint, render_template

gallery_bp = Blueprint('gallery_bp', __name__, template_folder='../templates/gallery')

@gallery_bp.route('/')
def gallery_home():
    return render_template('gallery/gallery_home.html')

```

---
## 📄 routes/auth.py

```py
from flask import Blueprint, render_template

auth_bp = Blueprint('auth_bp', __name__, template_folder='../templates/auth')

@auth_bp.route('/login')
def login():
    return render_template('auth/login.html')

```

---
## 📄 routes/admin.py

```py
from flask import Blueprint, render_template

admin_bp = Blueprint('admin_bp', __name__, template_folder='../templates/admin')

@admin_bp.route('/admin')
def admin_home():
    return render_template('admin/admin_home.html')

```

---
## 📄 routes/marketplace.py

```py
from flask import Blueprint, render_template

marketplace_bp = Blueprint('marketplace_bp', __name__, template_folder='../templates/marketplace')

@marketplace_bp.route('/marketplace')
def marketplace_home():
    return render_template('marketplace/marketplace_home.html')

```

---
## 📄 static/css/theme.css

```css

```

---
## 📄 static/css/components.css

```css

```

---
## 📄 static/css/layout.css

```css

```

---
## 📄 static/css/sidebar.css

```css

```

---
## 📄 static/css/base.css

```css
body { font-family: sans-serif; background: #faf9f6; margin:0; padding:0;}

```

---
## 📄 static/js/base.js

```js

```
