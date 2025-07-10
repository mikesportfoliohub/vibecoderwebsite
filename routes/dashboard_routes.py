from flask import Blueprint, render_template, session, abort
import os
import sqlite3

from decorators import login_required

dashboard_bp = Blueprint(
    "dashboard_bp", __name__, url_prefix="/dashboard"
)

@dashboard_bp.route("/", methods=["GET"])
@login_required
def dashboard_home():
    user_id = session["user_id"]
    db_path = "/content/drive/MyDrive/colab-web-app/database/site.db"

    # Quick debug
    print("👉 DB exists? ", os.path.exists(db_path))

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Fetch user
    cur.execute("SELECT username, email FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    if not user:
        conn.close()
        abort(404)

    # Count and fetch tactics
    cur.execute("SELECT COUNT(*) FROM innovation_tactics")
    print("tactics count:", cur.fetchone()[0])

    cur.execute("""
        SELECT title, summary, details, purpose
          FROM innovation_tactics
    """)
    tactics = cur.fetchall()
    print("👉 fetched", len(tactics), "tactics")

    conn.close()
    return render_template("dashboard.html", user=user, tactics=tactics)

