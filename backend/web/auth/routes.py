from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user

from web.extensions import db
from web.models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/setup", methods=["GET", "POST"])
def setup():
    admin = User.query.first()

    if admin:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Fill all fields.")
            return redirect(url_for("auth.setup"))

        user = User(
            username=username,
            password_hash=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        flash("Administrator created.")
        return redirect(url_for("auth.login"))

    return render_template("auth/setup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    user = User.query.first()

    if not user:
        return redirect(url_for("auth.setup"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == user.username and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("dashboard.index"))

        flash("Invalid credentials.")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))