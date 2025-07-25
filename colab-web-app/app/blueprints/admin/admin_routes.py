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
    request,
    current_app
)

from app.utils.db_utils import (
    get_username_by_id,
    get_all_users,
    get_all_tactics,
    get_user_by_id,
    update_user,
    delete_user_db
)

# ─── Blueprint Setup ──────────────────────────────────────────────────────
admin_bp = Blueprint(
    'admin_bp',
    __name__,
    url_prefix='/admin'
)


# ─── Blueprint‐Level Protection ────────────────────────────────────────────
@admin_bp.before_request
def ensure_admin():
    # 1) Must be logged in
    if not session.get('user_id'):
        flash("Please log in first.", "warning")
        return redirect(url_for('main_bp.home'))

    # 2) Must have admin privileges
    if not session.get('is_admin'):
        flash("Access denied: Admins only.", "danger")
        return redirect(url_for('main_bp.home'))

# ─── GET /admin (Dashboard) ───────────────────────────────────────────────
@admin_bp.route("/", methods=["GET"])
def admin_dashboard():
    user_id = session["user_id"]

    # Fetch current user’s name
    username = get_username_by_id(user_id) or "Admin"

    # Fetch data for tables
    users = get_all_users()
    tactics = get_all_tactics()

    return render_template(
        "admin/admin.html",
        username=username,
        users=users,
        tactics=tactics
    )

# ─── GET /admin/users/<id>/edit ────────────────────────────────────────────
@admin_bp.route("/users/<int:user_id>/edit", methods=["GET"])
def edit_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        flash("User not found.", "warning")
        return redirect(url_for("admin_bp.admin_dashboard"))

    return render_template("edit_user.html", user=user)

# ─── POST /admin/users/<id>/update ────────────────────────────────────────
@admin_bp.route("/users/<int:user_id>/update", methods=["POST"])
def update_user_route(user_id):
    new_username = request.form.get("username", "").strip()
    new_role = 1 if request.form.get("is_admin") else 0

    try:
        update_user(user_id, new_username, new_role)
        flash("User updated successfully.", "success")
    except Exception as e:
        current_app.logger.error(f"Update failed: {e}")
        flash("Could not update user.", "danger")

    return redirect(url_for("admin_bp.admin_dashboard"))

# ─── POST /admin/users/<id>/delete ────────────────────────────────────────
@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    try:
        delete_user_db(user_id)
        flash("User deleted.", "success")
    except Exception as e:
        current_app.logger.error(f"Delete failed: {e}")
        flash("Could not delete user.", "danger")

    return redirect(url_for("admin_bp.admin_dashboard"))

# ─── GET /admin/users_api ─────────────────────────────────────────────────
@admin_bp.route("/users_api", methods=["GET"])
def admin_users_api():
    try:
        rows = get_all_users()
        users = [
            {"id": r["id"], "username": r["username"], "is_admin": bool(r["is_admin"])}
            for r in rows
        ]
        return jsonify(users=users), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching users_api: {e}")
        return jsonify(error="Failed to fetch users"), 500

# ─── GET /admin/get_users ─────────────────────────────────────────────────
@admin_bp.route("/get_users", methods=["GET"])
def get_users():
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

    except sqlite3.Error as e:
        current_app.logger.error(f"Error fetching get_users: {e}")
        return jsonify(error="Error fetching users"), 500
