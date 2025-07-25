# app/blueprints/auth/auth_routes.py

import random
import logging
import sqlite3

from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    current_app,
)

from app.utils.db_utils import get_all_users

from werkzeug.security import generate_password_hash, check_password_hash

from app.utils.db_utils import get_connection

# ─── Blueprint Setup ──────────────────────────────────────────────────────
auth_bp = Blueprint(
    "auth_bp",
    __name__,
    url_prefix="/auth"
)

logger = logging.getLogger(__name__)

GOODBYES = [
    "Vibe offline, but spirit stays online. See you next time!",
    "Your coding couch misses you already. Drop by again soon!",
    "Our pixels part today, but the code remains. Until we ping again!",
    "Logging out now. May your exit code always be 0.",
    "Terminal closed, but the vibe lives on. Reboot with us again soon!",
    "Farewell, coder. May your uptime be high and your load average low.",
    "This TTY is closing—catch you on the next virtual console!",
    "Reached EOF on today's session. Compile your dreams until next time!",
    "Unmounting Vibe Coder Hub… see you when you mount a new project!",
    "Session terminated. Don’t forget to git push your brilliance!",
    "Live long and prosper."
]

@auth_bp.route("/login", methods=["GET"])
def show_login_form():
    next_page = request.args.get("next", "")
    return render_template("auth/login.html", next_page=next_page)


@auth_bp.route("/get_users", methods=["GET"])
def get_users():
    """
    Returns JSON list of all users:
      GET /auth/get_users → [{id, username, is_admin}, …]
    """
    users = get_all_users()                # returns sqlite3.Row list
    # convert each Row into a plain dict
    payload = [dict(u) for u in users]
    return jsonify(payload), 200

# ─── REGISTER ───────────────────────────────────────────────────────────────
@auth_bp.route("/register_page", methods=["GET"])
def show_register_form():
    """Render the user registration page."""
    return render_template("auth/register.html")


@auth_bp.route("/register_user", methods=["POST"])
def register_user():
    """
    Expects JSON: { username, email, password }.
    Creates a new user or returns 400 on missing fields or duplicate.
    """
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not (username and email and password):
        logger.warning("Registration failed: missing fields")
        return jsonify(error="username, email & password required"), 400

    hashed = generate_password_hash(password)
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed)
        )
        conn.commit()
        logger.info("Registered new user: %s", username)
        return jsonify(message="User registered successfully!"), 201

    except sqlite3.IntegrityError:
        logger.warning("Registration conflict for %s / %s", username, email)
        return jsonify(error="Username or Email already exists!"), 400

    finally:
        conn.close()


# ─── LOGIN ──────────────────────────────────────────────────────────────────
@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Expects JSON: { email, password }.
    On success: sets session and returns { message, username, is_admin, next }.
    """
    if not request.is_json:
        return jsonify(error="Request must be JSON"), 400

    data = request.get_json()
    email = data.get("email", "").strip()
    pwd   = data.get("password", "")

    if not (email and pwd):
        return jsonify(error="Email and password required"), 400

    # Grab the `next` param out of the query string
    next_page = request.args.get("next", "")

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username, password, is_admin FROM users WHERE email = ?",
            (email,)
        )
        user = cur.fetchone()
    finally:
        conn.close()

    if user and check_password_hash(user["password"], pwd):
        session.clear()
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["is_admin"]  = bool(user["is_admin"])

        logger.info("User logged in: %s (admin=%s)", user["username"], session["is_admin"])

        payload = {
            "message":  "Login successful!",
            "username": user["username"],
            "is_admin": session["is_admin"],
        }
        if next_page:
            payload["next"] = next_page

        return jsonify(payload), 200

    logger.warning("Failed login attempt for %s", email)
    return jsonify(error="Invalid credentials!"), 401



# ─── LOGOUT ─────────────────────────────────────────────────────────────────
@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    """
    Clears the session. Returns JSON on POST/JSON
    or renders a goodbye page on GET.
    """
    session.clear()
    logger.info("User logged out")

    if request.is_json or request.method == "POST":
        return jsonify(message="Logged out successfully."), 200

    goodbye = random.choice(GOODBYES)
    return render_template("auth/logout.html", goodbye=goodbye)
