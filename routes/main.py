from flask import Blueprint, render_template, flash, redirect, url_for #Importing necessary modules from Flask
from flask_login import current_user #Gives access to the currently logged-in user data

main = Blueprint("main", __name__) #Create Blueprint for main routes

@main.route("/") # Defining the route for the home page
def index():
    return render_template("index.html") 

@main.route("/start") # Defining the route for the 'start adding task button'
def start():
    if current_user.is_authenticated:
        return redirect(url_for("tasks.tasks_page"))
    
    flash("Please login first", 'warning')
    return redirect(url_for("auth.login"))
