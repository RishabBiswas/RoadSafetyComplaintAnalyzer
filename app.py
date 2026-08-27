from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import pandas as pd
from dotenv import load_dotenv
import os

from extensions import db   # 👈 import db from extensions

load_dotenv()

category_model = joblib.load("model/category_model.pkl")
priority_model = joblib.load("model/priority_model.pkl")
vectorizer = joblib.load("model/tfidf.pkl")

app = Flask(__name__)

import uuid

def generate_complaint_no():
    return "CMP-" + uuid.uuid4().hex[:8].upper()


db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise RuntimeError("DATABASE_URL not loaded")

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# 🔑 IMPORTANT: initialize db with app
db.init_app(app)

# import models AFTER db.init_app
import models

def mask_govt_id(govt_id):
    return "XXXX-XXXX-" + govt_id[-4:]

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        govt_id = mask_govt_id(request.form["govt_id"])
        password = generate_password_hash(request.form["password"])

        user = User(
            name=name,
            email=email,
            mobile=mobile,
            govt_id_masked=govt_id,
            password_hash=password,
            role="user"
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            session["role"] = user.role

            if user.role == "admin":
                return redirect("/admin/dashboard")
            else:
                return redirect("/user/dashboard")

        return "Invalid credentials"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

from werkzeug.security import generate_password_hash
from models import User

@app.route("/create-admin")
def create_admin():
    with app.app_context():
        admin_exists = User.query.filter_by(email="admin@roadsafety.com").first()
        if admin_exists:
            return "Admin already exists"

        admin = User(
            name="Admin",
            email="admin@roadsafety.com",
            mobile="9999999999",
            govt_id_masked="XXXX-XXXX-0000",
            password_hash=generate_password_hash("admin123"),
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        return "Admin user created successfully"
    


from models import Complaint, User

@app.route("/user/dashboard")
def user_dashboard():
    if "user_id" not in session or session.get("role") != "user":
        return redirect("/login")

    user_id = session["user_id"]

    open_complaints = Complaint.query.filter_by(
        user_id=user_id, status="OPEN"
    ).order_by(Complaint.created_at.desc()).all()

    closed_complaints = Complaint.query.filter_by(
        user_id=user_id, status="CLOSED"
    ).order_by(Complaint.created_at.desc()).all()

    user = User.query.get(user_id)

    return render_template(
        "user_dashboard.html",
        user=user,
        open_complaints=open_complaints,
        closed_complaints=closed_complaints
    )

@app.route("/raise-complaint", methods=["GET", "POST"])
def raise_complaint():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        text = request.form["complaint"]

        X = vectorizer.transform([text])
        category = category_model.predict(X)[0]
        priority = priority_model.predict(X)[0]

        complaint_no = generate_complaint_no()

        complaint = Complaint(
            complaint_no=complaint_no,
            user_id=session["user_id"],
            complaint_text=text,
            category=category,
            priority=priority,
            status="OPEN"
        )

        db.session.add(complaint)
        db.session.commit()

        return render_template(
            "complaint_result.html",
            complaint_no=complaint_no,
            category=category,
            priority=priority
        )

    return render_template("raise_complaint.html")


from sqlalchemy import case
from models import Complaint, User

@app.route("/admin/dashboard")
def admin_dashboard():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect("/login")

    # Priority order: High -> Medium -> Low
    priority_order = case(
        (Complaint.priority == "High", 1),
        (Complaint.priority == "Medium", 2),
        (Complaint.priority == "Low", 3),
        else_=4
    )

    complaints = Complaint.query.order_by(
        priority_order,
        Complaint.created_at.desc()
    ).all()

    # Chart data
    category_counts = {}
    priority_counts = {}

    for c in complaints:
        category_counts[c.category] = category_counts.get(c.category, 0) + 1
        priority_counts[c.priority] = priority_counts.get(c.priority, 0) + 1

    return render_template(
        "admin_dashboard.html",
        complaints=complaints,
        category_counts=category_counts,
        priority_counts=priority_counts
    )

from datetime import datetime

@app.route("/admin/close/<int:complaint_id>")
def close_complaint(complaint_id):
    if "user_id" not in session or session.get("role") != "admin":
        return redirect("/login")

    complaint = Complaint.query.get(complaint_id)
    if complaint and complaint.status == "OPEN":
        complaint.status = "CLOSED"
        complaint.closed_at = datetime.utcnow()
        db.session.commit()

    return redirect("/admin/dashboard")



@app.route("/")
def home():
    return "Flask + PostgreSQL Connected Successfully!"

if __name__ == "__main__":
    app.run(debug=True)
