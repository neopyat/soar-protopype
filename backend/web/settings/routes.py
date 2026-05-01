from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from web.extensions import db
from web.models.setting import Setting

settings_bp = Blueprint("settings", __name__)


@settings_bp.route("/settings", methods=["GET", "POST"])
@login_required
def index():
    settings = Setting.query.first()

    if not settings:
        settings = Setting()
        db.session.add(settings)
        db.session.commit()

    if request.method == "POST":
        settings.debug = bool(request.form.get("debug"))
        settings.ml_enabled = bool(request.form.get("ml_enabled"))
        settings.blocking = bool(request.form.get("blocking"))
        settings.loop_interval = int(request.form.get("loop_interval", 2))
        settings.siem = request.form.get("siem", "none")

        db.session.commit()

        flash("Settings updated.")
        return redirect(url_for("settings.index"))

    return render_template(
        "settings/index.html",
        settings=settings
    )