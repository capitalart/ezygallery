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
