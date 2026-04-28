from flask import Flask

from web.config import Config
from web.extensions import db, login_manager


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from web.models.user import User
    from web.models.incident import Incident
    from web.models.setting import Setting
    from web.models.audit import AuditLog

    from web.auth.routes import auth_bp
    from web.dashboard.routes import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    return app