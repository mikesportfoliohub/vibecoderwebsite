# routes/admin_routes.py

import sqlite3
from flask import (
    Blueprint,
    session,
    redirect,
    url_for,
    flash,
    render_template,
    jsonify,
    current_app
)

# ─── Blueprint Setup ──────────────────────────────────────────────────────
admin_bp = Blueprint(
    'admin',
    __name__,
    url_prefix='/admin',
    template_folder='../templates'
)

# ─── 3. Blueprint‐Level Protection ────────────────────────────────────────
@admin_bp.before_request
def ensure_admin():
    # 1) Must be logged in
    if not session.get('user_id'):
        flash("Please log in first.", "warning")
        return redirect(url_for('main.home'))
    # 2) Must have admin flag in session
    if not session.get('is_admin'):
        flash("Access denied: Admins only.", "danger")
        return redirect(url_for('main.home'))

# ─── GET /admin ────────────────────────────────────────────────────────────
@admin_bp.route("/", methods=["GET"])
def admin_dashboard():
    user_id = session["user_id"]
    users = []
    tactics = []
    conn = None

    try:
        conn = sqlite3.connect(current_app.config['DB_PATH'])
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Fetch current user’s info
        cur.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        username = row["username"] if row else "Admin"

        # Fetch all users
        cur.execute("SELECT id, username, is_admin FROM users;")
        users = cur.fetchall()

        # Fetch all tactics
        cur.execute("""
            SELECT id, title, summary, purpose
              FROM innovation_tactics;
        """)
        tactics = cur.fetchall()

    except sqlite3.Error as e:
        current_app.logger.error(f"Error loading admin dashboard: {e}")
        flash("Could not load dashboard data. Try again later.", "danger")
        username = "Admin"   # fallback

    finally:
        if conn:
            conn.close()

    return render_template(
        "admin.html",
        username=username,
        users=users,
        tactics=tactics
    )


# ─── GET /admin/users_api ─────────────────────────────────────────────────
@admin_bp.route('/users_api', methods=['GET'])
def admin_users_api():
    """
    JSON endpoint: returns list of users for async admin UI.
    """
    conn = None
    try:
        conn = sqlite3.connect(current_app.config['DB_PATH'])
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT id, username, is_admin FROM users;")
        rows = cur.fetchall()

        users = [
            {
                "id": r["id"],
                "username": r["username"],
                "is_admin": bool(r["is_admin"])
            }
            for r in rows
        ]
        return jsonify(users=users), 200

    except sqlite3.Error as e:
        current_app.logger.error(f"Error fetching users_api: {e}")
        return jsonify(error="Failed to fetch users"), 500

    finally:
        if conn:
            conn.close()

# ─── GET /admin/get_users ─────────────────────────────────────────────────
@admin_bp.route('/get_users', methods=['GET'])
def get_users():
    """
    Admin‐only JSON endpoint listing every user (id, username, email).
    """
    conn = None
    try:
        conn = sqlite3.connect(current_app.config['DB_PATH'])
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT id, username, email FROM users;")
        rows = cur.fetchall()

        users = [
            {"id": r["id"], "username": r["username"], "email": r["email"]}
            for r in rows
        ]
        return jsonify(users=users), 200

    except sqlite3.Error as e:
        current_app.logger.error(f"Error fetching users: {e}")
        return jsonify(error="Error fetching users"), 500

    finally:
        if conn:
            conn.close()
