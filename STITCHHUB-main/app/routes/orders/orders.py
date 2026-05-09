from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    abort,
)
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Listing, Order

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/")
@login_required
def view_orders():
    if current_user.role == "tailor":
        orders = (
            Order.query.join(Listing)
            .filter(Listing.tailor_id == current_user.tailor_profile.id)
            .all()
        )
        return render_template("orders/tailor_orders.html", orders=orders)
    else:
        orders = current_user.orders
        return render_template("orders/customer_orders.html", orders=orders)


@orders_bp.route("/update/<int:order_id>", methods=["POST"])
@login_required
def update_order(order_id):
    order = Order.query.get_or_404(order_id)

    if (
        not current_user.tailor_profile
        or order.listing.tailor_id != current_user.tailor_profile.id
    ):
        abort(403)

    new_status = request.form.get("status")
    notes = request.form.get("notes", "")
    estimated_completion = request.form.get("estimated_completion")

    valid_statuses = [
        "requested",
        "confirmed",
        "in_progress",
        "ready",
        "completed",
        "cancelled",
    ]

    if new_status in valid_statuses:
        order.status = new_status
        order.notes = notes

        # Add estimated completion handling
        if estimated_completion:
            order.estimated_completion = datetime.strptime(
                estimated_completion, "%Y-%m-%d"
            )

        if new_status == "confirmed":
            order.confirmed_date = datetime.utcnow()
        elif new_status == "completed":
            order.completed_date = datetime.utcnow()

        db.session.commit()
        flash("Order status updated", "success")
    else:
        flash("Invalid status", "danger")

    return redirect(url_for("orders.view_orders"))

@orders_bp.route("/<int:order_id>")
@login_required
def order_detail(order_id):

    order = Order.query.get_or_404(order_id)

    # Customer owner
    if current_user.role == "customer":
        if order.customer_id != current_user.id:
            abort(403)

    # Tailor owner
    elif current_user.role == "tailor":
        if order.tailor_id != current_user.tailor_profile.id:
            abort(403)

    return render_template(
        "orders/detail.html",
        order=order
    )
