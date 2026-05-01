from flask import Blueprint, render_template
from flask_login import login_required

from web.models.incident import Incident

incidents_bp = Blueprint("incidents", __name__)


@incidents_bp.route("/incidents")
@login_required
def index():
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()

    return render_template(
        "incidents/list.html",
        incidents=incidents
    )