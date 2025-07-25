# /app/blueprints/main/dashboard_routes.py

from flask import Blueprint, render_template, session, abort
from app.utils.decorators import login_required
from app.utils.db_utils import get_user_by_id, get_all_tactics

dashboard_bp = Blueprint(
    "dashboard_bp",
    __name__,
    url_prefix="/dashboard",
)

@dashboard_bp.route("/", methods=["GET"])
@login_required
def dashboard_home():
    """
    Dashboard home: show user info and all innovation tactics.
    Requires login.
    """
    user_id = session.get("user_id")
    user = get_user_by_id(user_id)

    if not user:
        # no such user in DB
        abort(404)

    tactics = get_all_tactics()

    return render_template(
        "main/dashboard.html",
        user=user,
        tactics=tactics
    )


