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
