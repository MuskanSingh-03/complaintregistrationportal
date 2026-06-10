"""
Flask application factory.

Demonstrates: Functions, Decorators, OOP
"""

import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_login import LoginManager
from flask_mail import Mail

from app.config import config_registry, BaseConfig

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Extension singletons (initialised per-app via init_app pattern)
# ---------------------------------------------------------------------------
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
login_manager = LoginManager()
mail = Mail()


def create_app(config_name: str = "development") -> Flask:
    """
    Application factory — creates and configures a Flask instance.

    :param config_name: One of 'development', 'production', 'testing'.
    :returns: Configured Flask application.
    """
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # ------------------------------------------------------------------
    # Load configuration
    # ------------------------------------------------------------------
    cfg_class = config_registry.get(config_name, config_registry["development"])
    cfg = cfg_class()
    app.config.from_object(cfg)
    # Materialise property-based URI into the config dict
    app.config["SQLALCHEMY_DATABASE_URI"] = cfg.SQLALCHEMY_DATABASE_URI
    cfg.init_app(app)

    # ------------------------------------------------------------------
    # Initialise extensions
    # ------------------------------------------------------------------
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # ------------------------------------------------------------------
    # Register blueprints
    # ------------------------------------------------------------------
    from app.routes.auth import auth_bp
    from app.routes.complaints import complaints_bp
    from app.routes.admin import admin_bp
    from app.routes.reports import reports_bp
    from app.routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(complaints_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    # ------------------------------------------------------------------
    # User loader for Flask-Login
    # ------------------------------------------------------------------
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id: str):
        return User.query.get(int(user_id))

    logger.info("Flask app created with config: %s", config_name)
    return app
