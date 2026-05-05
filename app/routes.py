from flask import render_template,request, redirect, url_for
from app import app, db
from app.models import User
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import joblib

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
    if request.method=="POST":
        try:
            file = request.files['file']
            df = pd.read_csv(file)
            model = joblib.load('churn_model.pkl')
            X = df[["Age", "Salary", "Complaints"]]
            predictions = model.predict(X).tolist()
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template('dashboard.html', predictions=predictions)    

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))



