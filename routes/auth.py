from flask import (Blueprint, render_template, redirect, request, url_for, flash) #Importing necessary modules from Flask
from flask_login import (login_user, logout_user, current_user) #To Handle login, logout, and gives access to the currently logged-in user
from flask_bcrypt import Bcrypt #Provides secure password hashing
from models.models import db, User #Importing the db instance and User model for database interaction

bcrypt = Bcrypt() #Initialize Bcrypt for hashing passwords
auth = Blueprint("auth", __name__) #Create Blueprint for authentication routes

@auth.route("/register", methods=["GET", "POST"]) #Defining the route for the register page
def register():
    if current_user.is_authenticated:
        return redirect(url_for("tasks.tasks_page"))
    
    if request.method == "POST": # Check if the request is a POST request (form submission)
        email = request.form.get('email').strip().lower()
        password =request.form.get('password')
        first = request.form.get('firstName')
        last = request.form.get('lastName')
        
        #Check if the email already exists in database
        if User.query.filter_by(email=email).first():
            flash("Email already exists. Please login", 'warning')
            return redirect(url_for('auth.login'))
        
        #Hash the password
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        
        #Create new user object
        user = User(email=email, password=hashed, first_name=first, last_name=last)
        db.session.add(user)
        db.session.commit() #save the changes in database
        
        flash("Account created. Please Login", 'success')
        return redirect(url_for("auth.login")) #Redirect user to login page after creating account
    
    return render_template("register.html")



@auth.route("/login", methods=["POST", "GET"]) # Defining the route for the login page
def login():
    if current_user.is_authenticated:
        return redirect(url_for("tasks.tasks_page"))
    
    if request.method == "POST":
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first() #Verify password using Bcrypt
    
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in success", 'success')
            return redirect(url_for("tasks.tasks_page")) #redirecting user to task_page after log-in
        flash("Invalide credentials", 'danger')
    
    return render_template("login.html")


@auth.route("/logout")  #Defining the route for the logout page
def logout():
    logout_user()   #Log out the current user (clears session)
    flash("Logged out", 'info')
    return redirect(url_for("main.index")) # redirect to home page after logged-out

        