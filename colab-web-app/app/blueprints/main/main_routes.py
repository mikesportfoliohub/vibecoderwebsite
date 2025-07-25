# app/blueprints/main/main_routes.py

import logging

from flask import (
    Blueprint,
    session,
    render_template,
    redirect,
    url_for,
    request,
    jsonify,
    current_app,
)

# ─── Blueprint Setup ──────────────────────────────────────────────────────
main_bp = Blueprint(
    "main_bp",
    __name__,
    template_folder="templates/main",
    static_folder="static",
)

# module‐level logger
logger = logging.getLogger(__name__)


@main_bp.route("/", methods=["GET"])
def home():
    """
    GET / → if logged in, redirect based on role; otherwise show public landing.
    """
    user_id = session.get("user_id")
    if user_id:
        if session.get("is_admin"):
            logger.info(f"Admin (id={user_id}) accessing home; redirecting.")
            return redirect(url_for("admin_bp.admin_dashboard"))
        logger.info(f"User (id={user_id}) accessing home; redirecting.")
        return redirect(url_for("admin_bp.admin_dashboard"))

    logger.debug("Rendering public home page for Guest")
    return render_template("main/index.html", username="Guest")


@main_bp.route("/", methods=["POST"])
def process_input():
    """
    POST / → receive form input, validate, and echo back JSON.
    """
    user_input = request.form.get("user_input", "").strip()
    logger.debug(f"Received user_input: {user_input!r}")

    if not user_input:
        logger.warning("Empty user_input received")
        return jsonify(error="No input provided"), 400

    return jsonify(message=f"You entered: {user_input}"), 200


@main_bp.route("/about", methods=["GET"])
def about():
    """
    Public About page describing the app’s mission and features.
    """
    return render_template("main/about.html")


@main_bp.route("/healthz", methods=["GET"])
def health_check():
    """
    Health check endpoint → returns 200 and app name.
    """
    payload = {"status": "ok", "app": current_app.name}
    return jsonify(payload), 200
