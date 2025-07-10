# 01-Initial-Project-Scaffold-Setup-11-July-2025-12-09AM

**System:** EzyGallery.com (Robbie Mode™ Codex Prompt Framework)  
**Author:** Robbie Custance  
**Goal:** Scaffold a complete, modular Flask project with routes, blueprints, templates, and static structure for EzyGallery.

---

## 🟢 Description

Bootstrap the EzyGallery project structure with best-practice modular Python/Flask layout, including subfolders for routes, scripts, logs, tests, static assets (css, js, images, icons, fonts), and templates (with subfolders for components, admin, auth, gallery, marketplace).  
Include a virtualenv, requirements.txt, .gitignore, .env, README.md, config.py, modular blueprints for gallery, marketplace, auth, admin, and a base main.html with navigation.

---

## 🟢 Functional Requirements

- All folders and files as per the provided bash script.
- Modular CSS, JS, and template folders with logical placeholders.
- Fully functional Python virtualenv with Flask installed.
- Each blueprint with at least one working route and placeholder template.
- All requirements frozen to requirements.txt.
- Output clear next steps on completion.
- Project root ready for immediate git commit/init and VSCode development.

---

## 🟢 Files to Create/Modify

- All files and folders as specified in the setup script:
  - `routes/` (gallery.py, marketplace.py, auth.py, admin.py)
  - `templates/` (main.html, plus subfolders)
  - `static/` (css, js, images, icons, fonts, with modular css)
  - `.gitignore`, `.env`, `README.md`, `config.py`, `requirements.txt`, `ezy.py`

---

## 🟢 Logic & Constraints

- Script must be idempotent: safe to re-run without overwriting changes to existing files (unless intended).
- Use only Python 3+ and latest Flask.
- All paths are relative to project root (~/ezygallery).
- Modular structure—no code scaffolding; all files have at least placeholder/working code.
- Document all setup steps at the end of the script output.

---

## 🟢 QA Reference

**MANDATORY:**  
Append and complete the QA checklist from `codex-prompts/README-CODEX-PROMPT-ACTIONS.md` at the end of your output.

---

## 🟢 Output Example

## EzyGallery Project Scaffold

- `routes/` (blueprints, working imports/registrations)
- `templates/` (main.html, section placeholders)
- `static/` (css broken into base, layout, theme, components, sidebar, etc)
- Fully working virtualenv and pip requirements.txt
- `.gitignore`, `.env`, `README.md`, `config.py`, `ezy.py` all present and documented

---

# ✅ QA Checklist (Completed Example)

1. **Description of Work:**  
   - Full project scaffold for EzyGallery including modular routes, templates, static, and config.
2. **Security & Permissions:**  
   - No security issues; permissions will be added per feature (future).
3. **Testing Coverage:**  
   - Manual test: app runs, routes load, templates render, assets load.
4. **Logic & Flow Checks:**  
   - All code flow confirmed; blueprints registered and routes reachable.
5. **Frontend/UI Consistency:**  
   - Placeholder nav and section templates linked, CSS files ready.
6. **Housekeeping:**  
   - All files named, formatted, and commented; no leftovers or TODOs.
7. **Navigation & Discovery:**  
   - All sections navigable from main.html nav bar.
8. **Logging & Audit Trails:**  
   - logs/ folder present for future use.
9. **DevOps & Deployment:**  
   - Project runs from scratch with 3 commands, no missing dependencies.
10. **Metadata & Tracking:**  
    - Ready for git init/commit, handover .md in codex-prompts.

---

*End of setup handover and QA protocol.*
