# app/utils/decorators.py

import functools
from urllib.parse import quote_plus
from flask import (
    session,
    redirect,
    url_for,
    request,
    jsonify,
    abort,
)


def login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            wants_json = (
                request.is_json
                or request.accept_mimetypes['application/json']
                   > request.accept_mimetypes['text/html']
                or request.path.startswith('/api/')
            )
            if wants_json:
                return jsonify(error='Authentication required'), 401

            next_url = quote_plus(request.url)
            login_url = url_for('auth_bp.show_login_form', next=next_url)
            return redirect(login_url)

        return view_func(*args, **kwargs)
    return wrapper


def admin_required(view_func):
    """
    Protect a view so only admins can access it.
    Automatically applies login_required first.
    """
    @login_required
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get('is_admin'):
            wants_json = (
                request.is_json
                or request.accept_mimetypes.best == 'application/json'
            )
            if wants_json:
                return jsonify(error='Admin access required'), 403

            # Redirect non-admins back to their dashboard or home
            return redirect(url_for('main.home'))

        return view_func(*args, **kwargs)

    return wrapper
