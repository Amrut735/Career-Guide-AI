import io
import json
from datetime import datetime

from flask import Blueprint, current_app, jsonify, redirect, render_template, send_file, session, url_for

from services.report_service import create_pdf_report


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/results")
def results():
    if "guidance_text" not in session or "json_output" not in session:
        return redirect(url_for("main.index"))
    return render_template("results.html", no_data=False)


@main_bp.route("/download/<format>")
def download(format):
    if "guidance_text" not in session or "json_output" not in session:
        return jsonify({"error": "No results available"}), 404

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    user_name = session.get("user_profile", {}).get("name", "user")
    safe_name = "".join(c for c in user_name if c.isalnum() or c in (" ", "-", "_")).rstrip()
    safe_name = safe_name.replace(" ", "_")

    if format.lower() == "pdf":
        filename = f"career_guidance_{safe_name}_{timestamp}.pdf"
        pdf_buffer = create_pdf_report(session.get("user_profile", {}), session.get("json_output", {}))
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype="application/pdf",
        )
    if format.lower() == "json":
        filename = f"career_guidance_{safe_name}_{timestamp}.json"
        return send_file(
            io.BytesIO(json.dumps(session["json_output"], indent=2).encode()),
            as_attachment=True,
            download_name=filename,
            mimetype="application/json",
        )

    return jsonify({"error": "Unsupported format"}), 400


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/contact")
def contact():
    return render_template("contact.html")


@main_bp.route("/sitemap.xml")
def sitemap():
    return send_file("static/sitemap.xml", mimetype="application/xml")


@main_bp.route("/robots.txt")
def robots():
    robots_content = """User-agent: *
Allow: /
Sitemap: https://career-guide-ai.onrender.com/sitemap.xml"""
    return current_app.response_class(robots_content, mimetype="text/plain")


@main_bp.route("/debug")
def debug():
    return render_template("debug.html")
