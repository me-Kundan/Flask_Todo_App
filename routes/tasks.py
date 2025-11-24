from flask import Blueprint, render_template, request, redirect, url_for, flash #Importing necessary modules from Flask
from flask_login import login_required, current_user # Protects routes and provides access to the logged-in user data
from models.models import db, Task #Importing the db instance and Task model for database interaction
from datetime import datetime 

tasks = Blueprint("tasks", __name__) #Create Blueprint for tasks routes

@tasks.route("/tasks", methods=["GET", "POST"]) #Defining the route for the tasks page
@login_required  #Ensure only logged-in users can access this page
def tasks_page():
    if request.method == "POST": # Check if the request is a POST request (form submission)
        title = request.form.get('title')
        desc = request.form.get('description', "")
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
        
        #Create a new Task linked to the logged-in user
        t = Task(title=title, description=desc, timestamp=timestamp, user_id=current_user.id)
        db.session.add(t)
        db.session.commit()
        
        flash("Task added", 'success')
        return redirect(url_for("tasks.tasks_page")) #redirect to task_page after adding task(to avoid resubmission of same task)
    
    user_tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.id.desc()).all() #Fetch all tasks belonging to the logged-in user (newest first)
    return render_template("tasks.html", tasks=user_tasks)


@tasks.route("/update/<int:task_id>", methods=["GET", "POST"]) #Defining the route for the update page
@login_required
def update(task_id):
    task = Task.query.get_or_404(task_id)
    
    #Prevent users from modifying tasks that are not theirs
    if task.user_id != current_user.id:
        flash("Unauthorized request", 'danger')
        return redirect(url_for("tasks.tasks_page")) 
    
    if request.method == "POST": #Check if the request is a POST request (form submission)
        task.title = request.form.get("title")
        task.description = request.form.get("description")
        db.session.commit()
        flash("Task updated", 'success')
        return redirect(url_for("tasks.tasks_page")) 
    
    # Render the update form with the current task data
    return render_template("update_task.html", task=task)


@tasks.route("/delete/<int:task_id>", methods=["POST"]) #Defining the route for the delete action
@login_required
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    
    #Prevent users from deleting tasks that are not theirs
    if task.user_id != current_user.id:
        flash("Unauthorized request", 'danger')
        return redirect(url_for("tasks.tasks_page"))
    
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted", 'info')
    return redirect(url_for("tasks.tasks_page"))
