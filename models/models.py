from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
#from datetime import datetime

db = SQLAlchemy() #creates a SQLAlchemy object

#define the User model (a table in the database)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50))
    tasks = db.relationship("Task", backref="user", lazy=True) #creates a relationship between User and Task
    
    #return the first letter of user email(will be used as user icon in navbar section).
    def display_initial(self):
        if self.email:
            return self.email[0].upper()
        return "E"
    
#define the Task model (a task table created by user)  
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(500))
    timestamp = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))    