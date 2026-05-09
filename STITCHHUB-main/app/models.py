from datetime import datetime

from flask_login import UserMixin

from .extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default="customer")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tailor_profile = db.relationship(
        "TailorProfile", back_populates="user", uselist=False
    )
    orders = db.relationship(
        "Order", back_populates="customer", foreign_keys="Order.customer_id"
    )


class TailorProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    certificate_filename = db.Column(db.String(200), nullable=True)
    document_filename = db.Column(db.String(200), nullable=True)
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="tailor_profile")
    listings = db.relationship("Listing", back_populates="tailor")
    orders = db.relationship("Order", back_populates="tailor")


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    turnaround_time = db.Column(db.String(50))
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tailor_id = db.Column(
        db.Integer, db.ForeignKey("tailor_profile.id"), nullable=False
    )

    tailor = db.relationship("TailorProfile", back_populates="listings")
    orders = db.relationship("Order", back_populates="listing")


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    status = db.Column(db.String(20), default="requested")

    notes = db.Column(db.Text)

    measurements = db.Column(db.Text)

    special_requests = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    estimated_completion = db.Column(db.DateTime)

    # NEW
    confirmed_date = db.Column(db.DateTime)

    # NEW
    completed_date = db.Column(db.DateTime)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    tailor_id = db.Column(
        db.Integer,
        db.ForeignKey("tailor_profile.id"),
        nullable=False
    )

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey("listing.id"),
        nullable=True
    )

    customer = db.relationship(
        "User",
        back_populates="orders"
    )

    tailor = db.relationship(
        "TailorProfile",
        back_populates="orders"
    )

    listing = db.relationship(
        "Listing",
        back_populates="orders"
    )


class TailorRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Customer who made the request
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    tailor_id = db.Column(
        db.Integer,
        db.ForeignKey("tailor_profile.id"),
        nullable=False
    )

    # Listing requested
    listing_id = db.Column(
        db.Integer,
        db.ForeignKey("listing.id"),
        nullable=False
    )

    cloth_type = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text)

    location = db.Column(db.String(150), nullable=False)

    urgency = db.Column(db.String(20), default="normal")

    status = db.Column(db.String(20), default="pending")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    accepted_at = db.Column(db.DateTime)

    # Relationships
    requester = db.relationship("User")

    tailor = db.relationship("TailorProfile")

    listing = db.relationship("Listing")