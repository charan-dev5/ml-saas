from flask import render_template,request, redirect, url_for
from app import app, db
from app.models import User
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import joblib
import razorpay
import os


@app.route("/")
def index():
    return redirect(url_for('register'))

@app.route("/register", methods=["GET" , "POST"])
def register():
    if request.method== "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username,
                        email=email,
                        password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route("/login", methods=["GET" , "POST"])    
def login():
    if request.method=="POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
            
    return render_template('login.html')

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    predictions = None
    if not current_user.is_paid:
        return redirect(url_for('subscribe'))
    if request.method=="POST":
        try:
            file = request.files['file']
            df = pd.read_csv(file)
            df = df.head(100)
            model = joblib.load('telco_model.pkl')
            columns = joblib.load('telco_columns.pkl')
            X = df[["Tenure Months", "Monthly Charges", "Total Charges", "Contract", "Internet Service", "Payment Method"]]
            X = pd.get_dummies(X)
            X = X.reindex(columns=columns,fill_value=0)
            predictions = model.predict(X).tolist()
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template('dashboard.html', predictions=predictions)    

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/subscribe")
@login_required
def subscribe():
    client = razorpay.Client(auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET")))
    order = client.order.create({"amount": 49900, "currency": "INR"})
    return render_template('subscribe.html', order=order, key=os.getenv("RAZORPAY_KEY_ID"))

@app.route("/payment-success")
@login_required
def payment_success():
    current_user.is_paid = True
    db.session.commit()
    return redirect(url_for('dashboard'))



