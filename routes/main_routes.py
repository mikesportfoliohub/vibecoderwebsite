# routes/main_routes.py

from flask import Blueprint, session, render_template, redirect, url_for, request, jsonify, current_app
import logging

# ─── Blueprint Setup ──────────────────────────────────────────────────────
main_bp = Blueprint('main', __name__)

# set up a logger for this module
logger = logging.getLogger(__name__)

# ─── GET / ────────────────────────────────────────────────────────────────
@main_bp.route('/', methods=['GET'])
def home():
    """
    Homepage: if logged in, redirect to dashboard/admin.
    Otherwise render the public landing page.
    """
    user_id = session.get('user_id')
    if user_id:
        # role‐based redirect
        if session.get('is_admin'):
            return redirect(url_for('admin.admin_dashboard'))
        return redirect(url_for('dashboard_bp.dashboard_home'))

    # Guest view
    username = 'Guest'
    logger.debug("Rendering public home page for Guest")
    return render_template('index.html', username=username)


# ─── POST / ──────────────────────────────────────────────────────────────
@main_bp.route('/', methods=['POST'])
def process_input():
    """
    Endpoint to receive user_input from a form and echo it back as JSON.
    """
    user_input = request.form.get('user_input', '').strip()
    logger.debug(f"Received user_input: {user_input}")

    if not user_input:
        logger.warning("Empty user_input received")
        return jsonify({"error": "No input provided"}), 400

    return jsonify({"message": f"You entered: {user_input}"})


@main_bp.route('/about', methods=['GET'])
def about():
    """
    Public About page describing Vibe Coder Hub’s mission, sandbox, and LLM innovations.
    """
    return render_template('about.html')  # make sure about.html lives under templates/

# ─── (Optional) Health Check ──────────────────────────────────────────────
@main_bp.route('/healthz', methods=['GET'])
def health_check():
    """
    Simple health endpoint to verify the app is up.
    """
    return jsonify(status="ok", app=current_app.name), 200
