from datetime import datetime

from flask import Flask, app, flash, redirect, url_for
from flask_wtf.csrf import CSRFError, generate_csrf

from .config import Config
from .extensions import db, login_manager, migrate, csrf
from .errors import page_not_found, internal_error, csrf_error


def time_ago(dt):
    """Convert datetime to 'time ago' format."""
    if not dt:
        return "Unknown"
    now = datetime.utcnow()
    diff = now - dt

    seconds = diff.total_seconds()
    if seconds < 60:
        return "Just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    else:
        weeks = int(seconds / 604800)
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register custom filters
    app.jinja_env.filters["time_ago"] = time_ago

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.profile import profile_bp
    from app.routes.listings import listings_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.orders import orders_bp
    from app.routes.request.routes import request_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp, url_prefix="")
    app.register_blueprint(listings_bp, url_prefix="/listings")
    app.register_blueprint(orders_bp, url_prefix="/orders")
    app.register_blueprint(profile_bp, url_prefix="/profile")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(request_bp, url_prefix="/request")

    # Error handlers
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(403, page_not_found)
    app.register_error_handler(500, internal_error)
    app.register_error_handler(CSRFError, csrf_error)

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User

        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        flash("Please log in to continue.", "warning")
        return redirect(url_for("auth.login"))

    @app.errorhandler(403)
    def forbidden(e):
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for("listings.marketplace"))

    # Context processor
    @app.context_processor
    def inject_user():
        from flask_login import current_user

        return dict(current_user=current_user)

    return app
