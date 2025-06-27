# routes/admin_routes.py

import sqlite3
from functools import wraps
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

# ─── Decorator: Protect Admin Routes ──────────────────────────────────────
def admin_required(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        # 1) Ensure user is logged in
        if 'user_id' not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for('main.home'))

        # 2) Check is_admin flag in users table
        db_path = current_app.config['DB_PATH']
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(
            "SELECT is_admin FROM users WHERE id = ?",
            (session['user_id'],)
        )
        row = cur.fetchone()
        conn.close()

        if not row or row[0] != 1:
            flash("Access denied: Admins only.", "danger")
            return redirect(url_for('main.home'))

        # 3) All good → call the view
        return f(*args, **kwargs)

    return decorated_view

# ─── GET /admin ────────────────────────────────────────────────────────────
@admin_bp.route('/', methods=['GET'])
@admin_required
def admin_dashboard():
    """
    Admin dashboard: list all users (id, username, is_admin).
    """
    db_path = current_app.config['DB_PATH']
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT id, username, is_admin FROM users;")
    users = cur.fetchall()
    conn.close()

    return render_template('admin.html', users=users)

# ─── GET /admin/users_api ─────────────────────────────────────────────────
@admin_bp.route('/users_api', methods=['GET'])
@admin_required
def admin_users_api():
    """
    JSON endpoint: returns list of users for async admin UI.
    """
    db_path = current_app.config['DB_PATH']
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT id, username, is_admin FROM users;")
    rows = cur.fetchall()
    conn.close()

    users = [
        {"id": r["id"], "username": r["username"], "is_admin": bool(r["is_admin"])}
        for r in rows
    ]
    return jsonify(users=users)

@admin_bp.route('/get_users', methods=['GET'])
@admin_required
def get_users():
    """
    Admin‐only JSON endpoint listing every user (id, username, email).
    """
    try:
        conn = sqlite3.connect(current_app.config['DB_PATH'])
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT id, username, email FROM users;")
        rows = cur.fetchall()
        conn.close()

        users = [
            {"id": r["id"], "username": r["username"], "email": r["email"]}
            for r in rows
        ]
        return jsonify(users=users), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching users: {e}")
        return jsonify({"error": str(e)}), 500
