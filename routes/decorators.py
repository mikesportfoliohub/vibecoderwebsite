# blueprints/decorators.py
from functools import wraps
from flask import session, redirect, url_for, jsonify, request

def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            if request.is_json:
                return jsonify(error="Authentication required"), 401
            return redirect(url_for("auth_bp.login_view")) 
        return f(*args, **kwargs)
    return wrapped
