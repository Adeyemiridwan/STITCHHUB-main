import os
import uuid

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    current_app,
)
from flask_login import current_user, login_required

from app.extensions import db
from app.models import TailorProfile
from app.forms import TailorForm

profile_bp = Blueprint("profile", __name__)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


@profile_bp.route("/")
@login_required
def profile():
    return render_template("profile/view.html")


@profile_bp.route("/tailor/<int:tailor_id>")
def view_tailor(tailor_id):
    """View a tailor's profile."""
    tailor = TailorProfile.query.get_or_404(tailor_id)
    listings = tailor.listings
    return render_template(
        "profile/tailor_profile.html", tailor=tailor, listings=listings
    )


@profile_bp.route("/become_tailor", methods=["GET", "POST"])
@login_required
def become_tailor():
    if current_user.tailor_profile:
        return redirect(url_for("dashboard.dashboard"))

    form = TailorForm()
    if form.validate_on_submit():
        try:
            # Handle file uploads
            certificate_filename = None
            document_filename = None

            if form.certificate.data:
                if allowed_file(form.certificate.data.filename):
                    ext = form.certificate.data.filename.rsplit(".", 1)[1].lower()
                    filename = f"cert_{uuid.uuid4().hex}.{ext}"
                    filepath = os.path.join(
                        current_app.config["UPLOAD_FOLDER"], "certificates", filename
                    )
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    form.certificate.data.save(filepath)
                    certificate_filename = filename

            if form.document.data:
                if allowed_file(form.document.data.filename):
                    ext = form.document.data.filename.rsplit(".", 1)[1].lower()
                    filename = f"id_{uuid.uuid4().hex}.{ext}"
                    filepath = os.path.join(
                        current_app.config["UPLOAD_FOLDER"], "documents", filename
                    )
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    form.document.data.save(filepath)
                    document_filename = filename

            # Create tailor profile
            new_tailor = TailorProfile(
                user_id=current_user.id,
                bio=form.bio.data,
                location=form.location.data,
                certificate_filename=certificate_filename,
                document_filename=document_filename,
            )

            # Update user role
            current_user.role = "tailor"

            db.session.add(new_tailor)
            db.session.commit()

            flash("Tailor profile submitted for verification!", "success")
            return redirect(url_for("dashboard.dashboard"))

        except Exception as e:
            db.session.rollback()
            print("TAILOR PROFILE ERROR:", e)
            flash(str(e), "danger")

    return render_template("profile/become_tailor.html", form=form)
