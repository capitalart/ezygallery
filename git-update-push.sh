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
  git pull origin master --rebase --autostash 2>>"$LOG_FILE" || {
    log "❌ git pull --rebase failed. Please resolve manually."
    exit 1
  }
  log "🚀 Pushing to origin/master..."
  git push origin master 2>>"$LOG_FILE" || {
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
