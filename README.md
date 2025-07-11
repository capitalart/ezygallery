# 🎨 EzyGallery Dev Toolkit — Robbie Mode™ Edition

Welcome, Codex (and curious devs)! This is the official **developer toolkit** for the `ezygallery.com` project — built with 💚 by Robin Custance. Everything here is structured for AI-powered automation, backup, commit safety, and smooth collaboration between humans and machines alike.

---

## 🗂️ Project Structure Overview

| Folder / File            | Description |
|--------------------------|-------------|
| `dev_logs/`              | Live logs from `ezygallery-total-rundown.py` snapshots. |
| `reports/`               | Markdown-formatted developer snapshots (code, env, git, etc). One folder per run. |
| `backups/`               | ZIP archives of the project, created by `git-update-push.sh`. |
| `git-update-push-logs/`  | Logs for all Git+Backup sessions. Useful for debugging or reviewing push failures. |
| `codex-prompts/`         | Codex prompt files (used during AI sessions or patch prep). |
| `.codex-commit-msg.txt`  | Optional file used to preload Codex-generated commit messages. |

---

## 🧠 Codex Snapshot System (How It Works)

### 1. `ezygallery-total-rundown.py`  
This is your **main dev snapshot tool**. It gathers:

- 📜 All source code and templates (`.py`, `.html`, `.js`, etc)
- 📊 A full file summary (size, last modified)
- 🧪 Python syntax validation
- 🌐 Git snapshot (`status`, `log`, `diff`)
- 🧬 Env info (`python`, `pip`, system info)
- ⚠️ Optional `pip check` + outdated packages

> 💾 Reports are stored in: `./reports/EZYGALLERY-DD-MMM-YYYY-HH-MMAM/`  
> 📓 Log file saved in: `./dev_logs/snapshot-YYYY-MM-DD-HHMMSS.log`

---

## 🚀 Git Backup Script (git-update-push.sh)

Your **main deploy + commit + backup + cloud uploader**. It handles:

- Git commit / push
- ZIP backups to `./backups/`
- Markdown diff report (`backup-diff-REPORT.md`)
- Uploads to Google Drive: `ezygallery-backups`
- Cache busting static assets
- Retention cleanup (keeps 30 most recent cloud backups)

> 🎯 Primary log: `./git-update-push-logs/git-update-push-YYYY-MM-DD-HH-MM.log`  
> 🗂️ Diff report: `./backups/backup-diff-REPORT.md`  
> 📦 ZIP: `./backups/YYYY-MM-DD-HH-MM_backup.zip`

---

## 🔍 Codex Integration Points

### 📁 Snapshot Reports:
- Codex can access full markdown snapshots in `./reports/` for:
  - Code file context
  - System info (Python, pip, OS)
  - Git history

### 🧪 Diff Reference:
- Codex should reference `./backups/backup-diff-REPORT.md` to understand:
  - What changed since last commit
  - Which files to prioritize in reviews or patches

### 🔎 Live Logs:
- For debugging AI sessions, use:
  - `./dev_logs/` → snapshot logs
  - `./git-update-push-logs/` → git/backup sessions

---

## 🛡️ Security & Ignored Files

This repo uses a strict `.gitignore` to protect:

- Secrets (`.env`, `.secret`)
- Virtualenv (`venv/`, `.venv/`)
- Heavy or untracked files (e.g. `node_modules/`, `__pycache__/`)
- Dev folders (e.g. `outputs/`, `inputs/`, `logs/`)

> 🧠 Codex and devs should **not** rely on ignored files — use snapshots instead.

---

## ✅ Quick Start Commands

```bash
# Generate a new dev snapshot
python3 ezygallery-total-rundown.py

# Commit + push + zip + upload
./git-update-push.sh --full-auto

# Just Git changes (skip backup & cloud)
./git-update-push.sh --just-git
