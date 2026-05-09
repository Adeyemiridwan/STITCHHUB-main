import os
import uuid

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    current_app,
    request,
)
from flask_login import current_user, login_required

from app.extensions import db
from app.forms import ListingForm, OrderForm
from app.models import Listing, TailorRequest

listings_bp = Blueprint("listings", __name__)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


@listings_bp.route("/marketplace")
def marketplace():
    """Display all available listings."""
    active_listing_ids = []

    if current_user.is_authenticated and current_user.role == "customer":

        active_listing_ids = [
            r.listing_id
            for r in TailorRequest.query.filter(
                TailorRequest.user_id == current_user.id,
                TailorRequest.status == "pending",
            ).all()
        ]

    listings = Listing.query.order_by(Listing.created_at.desc()).all()
    return render_template(
        "listings/marketplace.html",
        listings=listings,
        active_listing_ids=active_listing_ids,
    )


@listings_bp.route("/listing/<int:listing_id>", methods=["GET", "POST"])
def view_listing(listing_id):
    """View a single listing and place orders."""

    listing = Listing.query.get_or_404(listing_id)
    form = OrderForm()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to log in to place an order", "warning")
            return redirect(url_for("auth.login"))

        try:
            from app.models import Order

            new_order = Order(
                customer_id=current_user.id,
                tailor_id=listing.tailor.id,
                listing_id=listing.id,
                notes=form.notes.data,
                measurements=form.measurements.data,
                special_requests=form.special_requests.data,
            )
            db.session.add(new_order)
            db.session.commit()
            flash("Order placed successfully!", "success")
            return redirect(url_for("orders.view_orders"))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error placing order: {str(e)}")
            flash("Error placing order. Please try again.", "danger")

    return render_template("listings/view.html", listing=listing, form=form)


@listings_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_listing():
    if not current_user.tailor_profile:
        flash("You need to be a tailor to add listings", "warning")
        return redirect(url_for("dashboard.dashboard"))

    form = ListingForm()
    if form.validate_on_submit():
        try:
            # Handle image upload
            image_url = None
            if form.image_file.data:
                if allowed_file(form.image_file.data.filename):
                    ext = form.image_file.data.filename.rsplit(".", 1)[1].lower()
                    filename = f"listing_{uuid.uuid4().hex}.{ext}"
                    filepath = os.path.join(
                        current_app.config["UPLOAD_FOLDER"], "listings", filename
                    )
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    form.image_file.data.save(filepath)
                    image_url = f"/uploads/listings/{filename}"

            new_listing = Listing(
                tailor_id=current_user.tailor_profile.id,
                title=form.title.data,
                description=form.description.data,
                price=form.price.data,
                category=form.category.data,
                turnaround_time=form.turnaround_time.data,
                image_url=image_url,
            )
            db.session.add(new_listing)
            db.session.commit()
            flash("Listing created successfully!", "success")
            return redirect(url_for("dashboard.dashboard"))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating listing: {str(e)}")
            flash("Error creating listing. Please try again.", "danger")

    return render_template("listings/add.html", form=form)


@listings_bp.route("/listing/<int:listing_id>/edit", methods=["GET", "POST"])
@login_required
def edit_listing(listing_id):
    """Edit an existing listing."""
    listing = Listing.query.get_or_404(listing_id)

    # Ensure user owns this listing
    if listing.tailor.user_id != current_user.id:
        flash("You don't have permission to edit this listing", "danger")
        return redirect(url_for("dashboard.dashboard"))

    form = ListingForm()
    if form.validate_on_submit():
        try:
            # Handle image upload if provided
            if form.image_file.data:
                if allowed_file(form.image_file.data.filename):
                    ext = form.image_file.data.filename.rsplit(".", 1)[1].lower()
                    filename = f"listing_{uuid.uuid4().hex}.{ext}"
                    filepath = os.path.join(
                        current_app.config["UPLOAD_FOLDER"], "listings", filename
                    )
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    form.image_file.data.save(filepath)
                    listing.image_url = f"/uploads/listings/{filename}"

            # Update listing data
            listing.title = form.title.data
            listing.description = form.description.data
            listing.price = form.price.data
            listing.category = form.category.data
            listing.turnaround_time = form.turnaround_time.data

            db.session.commit()
            flash("Listing updated successfully!", "success")
            return redirect(url_for("dashboard.dashboard"))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating listing: {str(e)}")
            flash("Error updating listing. Please try again.", "danger")
    elif request.method == "GET":
        # Pre-fill form with existing data
        form.title.data = listing.title
        form.description.data = listing.description
        form.price.data = listing.price
        form.category.data = listing.category
        form.turnaround_time.data = listing.turnaround_time

    return render_template("listings/edit.html", form=form, listing=listing)


@listings_bp.route("/listing/<int:listing_id>/delete", methods=["POST"])
@login_required
def delete_listing(listing_id):
    """Delete a listing."""
    listing = Listing.query.get_or_404(listing_id)

    # Ensure user owns this listing
    if listing.tailor.user_id != current_user.id:
        flash("You don't have permission to delete this listing", "danger")
        return redirect(url_for("dashboard.dashboard"))

    try:
        db.session.delete(listing)
        db.session.commit()
        flash("Listing deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting listing: {str(e)}")
        flash("Error deleting listing. Please try again.", "danger")

    return redirect(url_for("dashboard.dashboard"))
