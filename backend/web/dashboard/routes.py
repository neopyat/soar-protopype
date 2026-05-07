from flask import Blueprint, render_template

from flask_login import login_required, current_user

from web.models.incident import Incident


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    incidents = (
        Incident.query
        .order_by(Incident.timestamp.desc())
        .limit(20)
        .all()
    )

    total_incidents = Incident.query.count()

    return render_template(
        "dashboard/index.html",
        username=current_user.username,
        incidents=incidents,
        total_incidents=total_incidents
    )