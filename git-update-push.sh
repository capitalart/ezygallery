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
