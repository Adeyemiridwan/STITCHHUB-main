# StitchHub

### A Modern Tailoring & Fashion Services Marketplace

StitchHub is a web based fashion and tailoring marketplace built with **Python and Flask**. It connects customers with professional tailors, allowing users to discover tailoring services, view service listings, submit custom orders, and track their tailoring experience.

The platform also provides tailors with tools to create and manage professional service listings and build their presence within the StitchHub marketplace.

---

## 📌 Project Overview

StitchHub is designed around two primary user experiences:

### 👤 Customers

Customers can:

* Create an account
* Log in securely
* Browse tailoring services
* Search the marketplace
* View individual service listings
* View tailor information
* Place custom orders
* Provide measurements
* Add special instructions
* Track order progress
* Manage their profile

### ✂️ Tailors

Tailors can:

* Create a professional account
* Build a tailor profile
* Submit professional information
* Provide their service location
* Upload verification documents
* Create service listings
* Add pricing
* Add delivery/turnaround information
* Upload fashion/service images
* Edit existing listings
* Present their services to customers

---

# ✨ Features

## 🔐 Authentication

StitchHub includes an authentication system built with Flask.

Features include:

* User registration
* User login
* User logout
* Password hashing
* Session-based authentication
* Protected routes
* Flask-WTF form validation
* CSRF protection
* Duplicate username detection
* Duplicate email detection
* Authentication-aware navigation

Passwords are stored using Werkzeug password hashing rather than storing plain-text passwords.

---

# 👤 User Profiles

Users have profile pages containing account information.

Profile information includes:

* Username
* Account type
* Registration date
* Tailor information
* Tailor location
* Verification status
* Tailor biography

The profile interface follows StitchHub's modern dashboard design system.

---

# ✂️ Tailor Registration

Users can apply to become StitchHub tailors.

The tailor registration process allows applicants to provide:

* Professional biography
* Location
* Professional certificate
* Government-issued identification document

Uploaded verification files are stored separately from normal application data.

The system generates unique filenames for uploaded documents to reduce filename collisions.

Example:

```text
cert_<unique-id>.pdf
id_<unique-id>.jpg
```

---

# 🛍️ Marketplace

The StitchHub marketplace allows customers to discover tailoring services.

Users can browse listings containing information such as:

* Service title
* Category
* Description
* Price
* Tailor
* Tailor location
* Creation date
* Service image
* Turnaround time

The marketplace is designed to make service discovery simple and visually clear.

---

# 📦 Custom Orders

Customers can place an order from a service listing.

An order can contain:

### Notes

Additional information about the customer's desired design.

### Measurements

Customer measurements required for tailoring.

### Special Requests

Additional requirements such as:

* Fabric preferences
* Embroidery
* Design modifications
* Other tailoring instructions

The order system is designed to support the tailoring workflow from request through completion.

---

# 📋 Order Workflow

StitchHub uses order statuses to represent the progress of an order.

Current status concepts include:

```text
Requested
Confirmed
In Progress
Ready
Completed
Cancelled
```

This provides a foundation for displaying order progress through the dashboard and timeline interfaces.

---

# 🧵 Service Listings

Tailors can create professional service listings.

A listing can contain:

* Service title
* Category
* Description
* Price
* Delivery/turnaround time
* Fashion/service image

Tailors can also edit their existing listings.

The interface includes:

* Listing creation
* Listing editing
* Image preview
* Pricing input
* Category selection
* Service information
* Publishing controls

---

# 🎨 User Interface

StitchHub uses a modern responsive interface with a consistent visual design system.

The design includes:

* Dashboard-style cards
* Modern forms
* Responsive layouts
* Rounded components
* Professional typography
* Primary action buttons
* Status badges
* Timeline components
* Marketplace cards
* Profile cards
* Authentication cards
* Error pages
* Mobile-responsive layouts

The UI is designed around a consistent visual language instead of treating each page as a completely separate design.

---

# 🚨 Error Handling

StitchHub includes custom error pages for common application errors.

Supported interfaces include:

```text
403 - Access Denied
404 - Page Not Found
500 - Server Error
CSRF / Security Error
```

These pages maintain the same visual design language as the rest of the application.

---

# 🏗️ Technology Stack

## Backend

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Migrate
* Flask-Login
* Flask-WTF
* Werkzeug

## Frontend

* HTML5
* CSS3
* Bootstrap
* Jinja2
* Font Awesome

## Database

The application is designed to work with:

* SQLite for local development
* PostgreSQL for production environments

## Development Tools

Recommended development environment:

* Visual Studio Code
* Python 3.x
* Git
* GitHub
* Python virtual environment

---

# 📁 Project Structure

A simplified structure of the project looks like this:

```text
STITCHHUB/
│
├── app/
│   │
│   ├── models/
│   │
│   ├── routes/
│   │
│   ├── forms/
│   │
│   ├── templates/
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── profile/
│   │   ├── listings/
│   │   └── errors/
│   │
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   └── extensions.py
│
├── migrations/
│
├── uploads/
│
├── instance/
│
├── config.py
├── run.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

> The exact structure may vary depending on the current development version of the project.

---
