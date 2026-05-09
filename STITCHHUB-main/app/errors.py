from flask import render_template


def page_not_found(error):
    return render_template("errors/404.html"), 404


def internal_error(error):
    return render_template("errors/500.html"), 500


def csrf_error(error):
    return render_template("errors/csrf_error.html"), 400
