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
