# routes/auth_routes.py

import sqlite3
import random
import logging

from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    current_app
)
from werkzeug.security import generate_password_hash, check_password_hash

# ─── Blueprint Setup ──────────────────────────────────────────────────────
auth_bp = Blueprint(
    'auth',
    __name__,
    template_folder='../templates'
)

# ─── Module Logger ─────────────────────────────────────────────────────────
logger = logging.getLogger(__name__)

# ─── Goodbye Messages ───────────────────────────────────────────────────────
GOODBYES = [
    "Vibe offline, but spirit stays online. See you next time!",
    "Your coding couch misses you already. Drop by again soon!",
    "Our pixels part today, but the code remains. Until we ping again!",
]

# ─── DB HELPER ──────────────────────────────────────────────────────────────
def get_db_connection():
    """Open a SQLite connection using the app’s DB_PATH config."""
    db_path = current_app.config['DB_PATH']
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# ─── REGISTER ───────────────────────────────────────────────────────────────
@auth_bp.route('/register_page', methods=['GET'])
def show_register_form():
    """Render the user registration page."""
    return render_template('register.html')

@auth_bp.route('/register_user', methods=['POST'])
def register_user():
    """
    Expects JSON: { username, email, password }
    Creates a new user (non-admin) or returns 400 on dup.
    """
    data = request.get_json(force=True)
    username = data.get("username", "").strip()
    email    = data.get("email", "").strip()
    password = data.get("password", "")

    if not username or not email or not password:
        logger.warning("Missing fields in registration payload")
        return jsonify({"error": "username, email & password required"}), 400

    hashed_password = generate_password_hash(password)
    try:
        conn = get_db_connection()
        cur  = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_password)
        )
        conn.commit()
        conn.close()
        logger.info(f"New user registered: {username}")
        return jsonify({"message": "User registered successfully!"}), 201

    except sqlite3.IntegrityError:
        logger.warning(f"Registration conflict for {username} / {email}")
        return jsonify({"error": "Username or Email already exists!"}), 400

# ─── LOGIN ──────────────────────────────────────────────────────────────────
@auth_bp.route('/login_page', methods=['GET'])
def show_login_form():
    """Render the login page."""
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Expects JSON: { email, password }
    On success: stores session and returns { message, username }
    On failure: 401 + { error }.
    """
    data  = request.get_json(force=True)
    email = data.get("email", "").strip()
    pwd   = data.get("password", "")

    if not email or not pwd:
        return jsonify({"error": "Email and password required"}), 400

    conn = get_db_connection()
    cur  = conn.cursor()
    cur.execute(
        "SELECT id, username, password FROM users WHERE email = ?",
        (email,)
    )
    user = cur.fetchone()
    conn.close()

    if user and check_password_hash(user["password"], pwd):
        session.clear()
        session["user_id"]   = user["id"]
        session["username"]  = user["username"]
        logger.info(f"User logged in: {user['username']}")
        return jsonify({
            "message":  "Login successful!",
            "username": user["username"]
        })

    logger.warning(f"Failed login attempt for {email}")
    return jsonify({"error": "Invalid credentials!"}), 401

# ─── LOGOUT ─────────────────────────────────────────────────────────────────
@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    Clears the session.
    If JSON/POST: returns JSON.
    Otherwise: renders a goodbye page.
    """
    session.pop("user_id", None)
    session.pop("username", None)
    logger.info("User logged out")

    if request.is_json or request.method == 'POST':
        return jsonify({"message": "Logged out successfully."})

    goodbye = random.choice(GOODBYES)
    return render_template('logout.html', goodbye=goodbye)
