from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    FloatField,
    SelectField,
    SubmitField,
    FileField,
)
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=64)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password")],
    )


class ListingForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=100)])
    description = TextAreaField("Description", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired(), NumberRange(min=0.01)])
    category = SelectField(
        "Category",
        choices=[
            ("alterations", "Alterations"),
            ("custom", "Custom Clothing"),
            ("repair", "Repairs"),
            ("design", "Design Consultation"),
        ],
    )
    turnaround_time = SelectField(
        "Turnaround Time",
        choices=[
            ("24h", "24 Hours"),
            ("3d", "3 Days"),
            ("1w", "1 Week"),
            ("2w", "2 Weeks"),
            ("1m", "1 Month"),
        ],
    )
    image_file = FileField("Service Image")


class OrderForm(FlaskForm):
    notes = TextAreaField("Special Instructions")
    measurements = TextAreaField("Measurements")
    special_requests = TextAreaField("Special Requests")


class TailorForm(FlaskForm):
    bio = TextAreaField("Bio", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    certificate = FileField("Professional Certificate")
    document = FileField("ID Document")


class TailorRequestForm(FlaskForm):
    cloth_type = StringField("Cloth Type", validators=[DataRequired()])
    description = TextAreaField("Description")
    location = StringField("Location", validators=[DataRequired()])
    urgency = SelectField(
        "Urgency",
        choices=[
            ("normal", "Normal"),
            ("urgent", "Urgent"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Send Request")
