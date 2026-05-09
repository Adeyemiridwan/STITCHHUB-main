from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.models import Listing, Order, TailorRequest

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def dashboard():

    # ===============================
    # TAILOR DASHBOARD
    # ===============================
    if current_user.tailor_profile:
        tailor_id = current_user.tailor_profile.id

        listings = (
            Listing.query.filter_by(tailor_id=tailor_id)
            .order_by(Listing.created_at.desc())
            .all()
        )

        orders = (
            Order.query.filter_by(tailor_id=current_user.tailor_profile.id)
            .order_by(Order.created_at.desc())
            .all()
        )

        requests = (
            TailorRequest.query.filter_by(tailor_id=tailor_id, status="pending")
            .order_by(TailorRequest.created_at.desc())
            .all()
        )

        return render_template(
            "dashboard/tailor.html",
            listings=listings,
            orders=orders,
            requests=requests,  # ✅ THIS WAS MISSING
        )

    # ===============================
    # CUSTOMER DASHBOARD
    # ===============================
    return render_template("dashboard/customer.html")


@dashboard_bp.route("/requests")
@login_required
def tailor_requests():
    if not current_user.tailor_profile:
        flash("Access denied", "danger")
        return redirect(url_for("dashboard.dashboard"))

    requests = (
        TailorRequest.query.filter_by(user_id=current_user.id)
        .order_by(TailorRequest.created_at.desc())
        .all()
    )

    return render_template("request/available_requests.html", requests=requests)
