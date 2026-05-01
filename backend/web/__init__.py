from flask import Flask

from web.extensions import db, login_manager

from web.auth.routes import auth_bp
from web.dashboard.routes import dashboard_bp
from web.incidents.routes import incidents_bp
from web.settings.routes import settings_bp

from web.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(incidents_bp)
    app.register_blueprint(settings_bp)

    return app