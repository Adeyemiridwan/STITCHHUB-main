from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    current_app,
)
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app.forms import LoginForm, RegistrationForm
from app.models import User
from app.extensions import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Logged in successfully!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard.dashboard"))
        flash("Invalid username or password", "danger")
    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Check if username already exists
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash("Username already exists. Please choose another.", "danger")
                return render_template("auth/register.html", form=form)

            # Check if email already exists
            existing_email = User.query.filter_by(email=form.email.data).first()
            if existing_email:
                flash(
                    "Email already registered. Please use another or login.", "danger"
                )
                return render_template("auth/register.html", form=form)

            # Create new user
            hashed_password = generate_password_hash(form.password.data)
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password,
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully! Please login.", "success")
            return redirect(url_for("auth.login"))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Registration error: {str(e)}")
            flash("An error occurred during registration. Please try again.", "danger")
            return render_template("auth/register.html", form=form)

    return render_template("auth/register.html", form=form)


@auth_bp.route("/register/tailor", methods=["POST"])
def register_tailor():
    try:
        # Check if email already exists
        existing_email = User.query.filter_by(email=request.form["email"]).first()
        if existing_email:
            flash("Email already registered", "danger")
            return redirect(url_for("auth.login"))

        hashed_password = generate_password_hash(request.form["password"])
        new_user = User(
            username=request.form["name"],
            email=request.form["email"],
            password=hashed_password,
            role="tailor",
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Tailor account created! Please login.", "success")
        return redirect(url_for("auth.login"))
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Tailor registration error: {str(e)}")
        flash("Error creating tailor account. Please try again.", "danger")
        return redirect(url_for("auth.register"))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
