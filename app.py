#Importing Flask core modules, configuration, database ORM, authentication manager, route blueprints, and password hashing utilities
from flask import Flask
from config import Config
from models.models import db
from flask_login import LoginManager
from routes.auth import auth
from routes.tasks import tasks
from routes.main import main
from flask_bcrypt import Bcrypt
from os import environ

app = Flask(__name__) #Creates main Flask application instance.
app.config.from_object(Config) #Loads configuration values from Config class

db.init_app(app) #Initializes the SQLAlchemy database obj with Flask app. Connects the database instance to flask application.
bcrypt = Bcrypt(app) #Connects Bcrypt(password encryption) to the app

# Login Manager
login_manager = LoginManager() #Creates a LoginManager object
login_manager.init_app(app) #Connects the LoginManager to Flask app
login_manager.login_view = "auth.login" #Tells Flask Login which route to redirect to when an unauthorized user tries to access any protected page.

from models.models import User # Import the User model for database access and authentication

@login_manager.user_loader #loads user from the session
def load_user(user_id):
    return User.query.get(int(user_id))

#Register blueprints
app.register_blueprint(main)   #Registers the main blueprint with app
app.register_blueprint(auth)   # Registers the authentication routes
app.register_blueprint(tasks)  # Registers the task-related routes

#Run the app and create database tables when executed
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(
        host="0.0.0.0",
        port=int(environ.get("PORT", 8080)),
        debug=False
    )