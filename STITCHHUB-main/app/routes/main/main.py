from flask import Blueprint, render_template, request, send_from_directory

from app.models import TailorProfile

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    page = request.args.get("page", 1, type=int)
    verified_tailors = TailorProfile.query.filter_by(verified=True).paginate(
        page=page, per_page=6
    )
    return render_template("main/home.html", tailors=verified_tailors)


@main_bp.route("/uploads/<path:filename>")
def download_file(filename):
    """Serve uploaded files from secure_uploads folder."""
    from flask import current_app

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(upload_folder, filename)
