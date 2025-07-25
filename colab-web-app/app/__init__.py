# app/__init__.py

import os
import logging
from flask import Flask

def create_app(test_config=None):
    """
    Application factory: configures and returns a Flask app instance.
    """

    # ─── Flask App Setup ────────────────────────────────────────────────
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="templates",
        static_folder="static",
    )

    # ─── Default Configuration ───────────────────────────────────────────
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-key"),
        DB_PATH=os.getenv(
            "DB_PATH",
            os.path.join(app.instance_path, "site.db"),
        ),
    )

    # ─── Load Test or Instance Config ───────────────────────────────────
    if test_config:
        app.config.update(test_config)
    else:
        # looks for instance/config.py if present
        app.config.from_pyfile("config.py", silent=True)

    # ─── Ensure Instance Folder Exists ──────────────────────────────────
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        app.logger.exception("Could not create instance folder")

    # ─── Logging Configuration ──────────────────────────────────────────
    logging.basicConfig(level=logging.INFO)
    app.logger.info("App initialized; DB_PATH=%s", app.config["DB_PATH"])

    # ─── Register Blueprints ────────────────────────────────────────────
    from app.blueprints.main.main_routes      import main_bp
    from app.blueprints.main.dashboard_routes import dashboard_bp
    from app.blueprints.auth.auth_routes      import auth_bp
    from app.blueprints.admin.admin_routes    import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp,      url_prefix="/auth")
    app.register_blueprint(admin_bp,     url_prefix="/admin")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    return app
