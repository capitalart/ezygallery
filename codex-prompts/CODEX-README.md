# EzyGallery CODEX-README.md

Welcome, Codex (or any AI dev working on EzyGallery)!  
**Before you do anything, read and follow ALL instructions in this document.**

---

## 🚩 Project Overview — What is EzyGallery?

**EzyGallery** is a next-generation, artist-first online marketplace and gallery platform.  
Built for scale, simplicity, and storytelling, it empowers artists to showcase, mock up, and sell their work—backed by the automation, quality control, and SEO mastery of Robbie Mode™.

> "Think of it as Etsy meets Shopify—but custom-built for professional artists who want creative control and zero fluff."

**Built by:** Robin Custance (Aboriginal Aussie Artist, developer, and dot art whisperer)  
**Powered by:** Flask, OpenAI, Jinja2, SQLite, Git, and beautifully modular architecture

---

## 🧱 Core Capabilities

- ✅ Artist accounts and gallery page setup
- ✅ Artwork upload, sorting, and batch prep
- ✅ AI-powered listing generation (Pulitzer-worthy SEO)
- ✅ Multi-category mockup selection and preview
- ✅ Finalisation flow: naming, foldering, QA
- ✅ Export tools for Sellbrite, Etsy, Gelato
- ✅ Modular extension system (routes, templates, tools)

**Key Tech Stack**  
- Python 3.11+  
- Flask (Blueprints)  
- Jinja2 templating  
- SQLite3  
- OpenAI API (GPT + Vision)  
- Shell tools (for audit/export/backup)

---

## 📂 File & Folder Layout

- `routes/` — Flask Blueprints (upload, analyze, review, approve, publish, export)
- `services/` — AI prompt builder, listing composer, export logic
- `utils/` — Reusable tools (file naming, folder prep, template blocks, QA scans)
- `templates/` — Jinja2 UI templates (auto-linked to menus by folder)
- `static/` — CSS, logos, JS, image assets
- `mockups/` — Categorised mockup library by aspect ratio (4:5, 3:4, etc.)
- `data/` — Local database (SQLite), config JSONs, profile settings
- `exports/` — Output CSVs, JSONs, error logs, Sellbrite-ready bundles

**Entry Point:**  
- `ezygallery.py` — Main Flask app runner (registers all routes, sets context/theme)

---

## 🔥 Collaboration & Coding Rules

**MANDATORY STANDARDS:**

- ✅ **Full file rewrites only** (no snippets or scaffolding)
- ✅ All code must be **production-grade** with **docstrings** and **clear comments**
- ✅ Use **TOC + permanent section codes** (e.g. `review-routes-py-2b`)
- ✅ Do not break, regress, or remove working logic
- ✅ If extending a flow, preserve QA, naming, and structure
- ✅ All AI prompt logic must log model, profile, and template used

**WHEN UNSURE: Ask first. Always.**

---

## 🧭 Core Workflows (Robbie Mode™ Protected)

1. **Artwork Upload**  
   → Files stored in temp folder, DB entry created

2. **AI Analysis**  
   → Uses OpenAI GPT + Vision to generate:  
     - SEO title  
     - Pulitzer-grade listing (400+ words)  
     - Description blocks (tags, size, palette)

3. **Mockup Generation**  
   → Mockups selected by category (e.g. Living Room, Nursery)  
   → Images renamed as `{seo_filename}-MU-01.jpg`, etc.

4. **Finalisation Flow**  
   → Files moved to `/finalised-artwork/{seo_folder}/`  
   → QA run (image size, mockup count, thumbnail check)  
   → Metadata JSON written alongside images

5. **Export**  
   → Artwork + mockups exported as CSV/JSON  
   → Compatible with Sellbrite, Etsy, Gelato  
   → URLs converted to public-ready format

---

## 📦 Folder & File Conventions

All finalized outputs must live under:  
`/finalised-artwork/{seo_folder}/`

### Image naming rules:
- Main artwork: `{seo_filename}.jpg`
- Mockups: `{seo_filename}-MU-01.jpg` to `-MU-10.jpg`
- Thumbnail: `{seo_filename}-thumb.jpg`
- AI-generated listing art: `{seo_filename}-openai.jpg`
- Metadata JSON: `{seo_filename}-listing.json`

Temporary files must never leak into final folders.  
Audit scripts will check for misnamed or misplaced files.

---

## ✍️ AI Prompt Engineering Guidelines

All OpenAI calls must:

- Use `etsy_master_template.txt` (text only, CSV-safe)
- Reference `settings.json` for correct profile
- Use content blocks from `utils/content_blocks.py` if required
- Respect tone, SEO, and Aboriginal cultural protocols
- Hit **400+ words**
- Use proper art curation terms (style, technique, color palette)
- Avoid banned phrases like “immerse yourself”, “step into”
- CTA: “Add to ya shopping basket” preferred over “Buy now”

---

## 🔐 Security, Roles & .env Discipline

- All delete, publish, and admin actions must check role  
- Multi-user artist support is coming—design accordingly  
- No API keys or passwords in code—use `.env` files only  
- Sessions must be isolated and logged properly

---

## 🧪 Testing & QA Flow

**Audit Requirements:**

- All export files must pass filename/structure validation
- Every listing must include:
  - Main image
  - 3–10 mockups
  - Thumbnail
  - OpenAI version
  - JSON metadata
- Audit logs are written to `/exports/logs/`
- Pytest coverage required for:
  - Prompt builder
  - Mockup finaliser
  - Export engine

---

## 🔧 Adding New Features

### ➕ Add New Route:
- Use Flask Blueprint in `routes/`
- Include TOC and permanent section headers
- Register in `ezygallery.py`

### 🎨 Add New Template:
- Place in appropriate `templates/` subfolder
- Sidebar auto-detects for nav menus

### 🧠 Add Prompt Template/Profile:
- Add prompt to `master_listing_templates/`
- Link profile in `data/settings.json`

---

## 🧠 Robbie’s Dev Tips

- “Structure is freedom—use it properly.”
- “If it isn’t QA’d, it’s not finished.”
- “Don’t be clever. Be clean, readable, and safe.”
- “Robbie Mode™ means full file rewrites, real comments, no short-cuts.”

---

# END OF CODEX-README

**Before starting, Codex must:**

1. Read this file fully  
2. Follow ALL naming, foldering, and QA rules  
3. Reference it before making any file changes  
4. Double-check your logic against every workflow section above

