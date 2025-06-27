# routes/main_routes.py

from flask import Blueprint, session, render_template, request, jsonify, current_app
import logging

# ─── Blueprint Setup ──────────────────────────────────────────────────────
main_bp = Blueprint('main', __name__)

# set up a logger for this module
logger = logging.getLogger(__name__)

# ─── GET / ────────────────────────────────────────────────────────────────
@main_bp.route('/', methods=['GET'])
def home():
    """
    Homepage: shows a welcome message to the logged-in user (or Guest).
    """
    username = session.get('username', 'Guest')
    logger.debug(f"Rendering home for user: {username}")
    return render_template('index.html', username=username)


# ─── POST / ───────────────────────────────────────────────────────────────
@main_bp.route('/', methods=['POST'])
def process_input():
    """
    Endpoint to receive user_input from a form and echo it back as JSON.
    """
    user_input = request.form.get('user_input', '').strip()
    logger.debug(f"Received user_input: {user_input}")

    if not user_input:
        logger.warning("Empty user_input received")
        return jsonify({
            "error": "No input provided"
        }), 400

    return jsonify({
        "message": f"You entered: {user_input}"
    })


# ─── (Optional) Health Check ──────────────────────────────────────────────
@main_bp.route('/healthz', methods=['GET'])
def health_check():
    """
    Simple health endpoint to verify the app is up.
    """
    return jsonify(status="ok", app=current_app.name), 200
