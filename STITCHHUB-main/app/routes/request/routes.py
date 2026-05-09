from flask import Blueprint, abort, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Listing, TailorRequest, Order
from app.forms import TailorRequestForm

request_bp = Blueprint("request", __name__)


# ===============================
# TAILOR REQUEST ROUTES
# ===============================
@request_bp.route("/request/<int:listing_id>", methods=["GET", "POST"])
@login_required
def request_tailor(listing_id):
    # 🚫 Tailors cannot make requests
    if current_user.role == "tailor":
        flash("Tailors cannot request services.", "danger")
        return redirect(url_for("listings.marketplace"))

    form = TailorRequestForm()
    listing = Listing.query.get_or_404(listing_id)

    if form.validate_on_submit():
        tailor_request = TailorRequest(
            user_id=current_user.id,
            tailor_id=listing.tailor_id,
            listing_id=listing.id,  # ✅ THIS FIXES EVERYTHING
            cloth_type=form.cloth_type.data,
            description=form.description.data,
            location=form.location.data,
            urgency=form.urgency.data,
        )

        db.session.add(tailor_request)
        db.session.commit()

        flash("Tailor request sent successfully.", "success")
        return redirect(url_for("dashboard.dashboard"))

    return render_template("request/request_tailor.html", form=form, listing=listing)


# ===============================
# AVAILABLE REQUEST ROUTES
# ===============================
@request_bp.route("/available_requests")
@login_required
def available_requests():

    if not current_user.tailor_profile:
        abort(403)

    requests = (
        TailorRequest.query.filter_by(
            tailor_id=current_user.tailor_profile.id, status="pending"
        )
        .order_by(TailorRequest.created_at.desc())
        .all()
    )

    return render_template("request/available_requests.html", requests=requests)


# ===============================
# ACCEPT REQUEST ROUTES
# ===============================
@request_bp.route("/request/<int:request_id>/accept", methods=["POST"])
@login_required
def accept_request(request_id):
    req = TailorRequest.query.get_or_404(request_id)

    if not current_user.tailor_profile:
        abort(403)

    # Prevent double action
    if req.status != "pending":
        flash("Request already handled", "warning")
        return redirect(url_for("request.available_requests"))

    req.status = "accepted"

    order = Order(
        customer_id=req.user_id,
        tailor_id=current_user.tailor_profile.id,
        listing_id=req.listing_id,  # ✅ NOW NOT NULL
        status="in_progress",
        notes=req.description,
    )

    db.session.add(order)
    db.session.commit()

    flash("Request accepted. Order created.", "success")
    return redirect(url_for("request.available_requests"))


# ===============================
# REJECT REQUEST ROUTES
# ===============================
@request_bp.route("/request/<int:request_id>/reject", methods=["POST"])
@login_required
def reject_request(request_id):
    req = TailorRequest.query.get_or_404(request_id)

    if (
        not current_user.tailor_profile
        or req.tailor_id != current_user.tailor_profile.id
    ):
        abort(403)

    req.status = "rejected"
    db.session.commit()

    flash("Request rejected", "info")
    return redirect(url_for("request.available_requests"))


@request_bp.route("/my-requests")
@login_required
def my_requests():

    # 🚫 Tailors should not access this page
    if current_user.role != "customer":
        abort(403)

    requests = (
        TailorRequest.query.filter_by(user_id=current_user.id)
        .order_by(TailorRequest.created_at.desc())
        .all()
    )

    return render_template("request/my_requests.html", requests=requests)


@request_bp.route("/cancel/<int:request_id>", methods=["POST"])
@login_required
def cancel_request(request_id):

    request_obj = TailorRequest.query.get_or_404(request_id)

    if request_obj.user_id != current_user.id:
        abort(403)

    if request_obj.status != "accepted":
        flash("You can only cancel after acceptance.", "warning")
        return redirect(url_for("request.my_requests"))

    request_obj.status = "cancelled"
    db.session.commit()

    flash("Request cancelled.", "info")
    return redirect(url_for("request.my_requests"))
