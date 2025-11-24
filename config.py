import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__)) #absolute path for the current project directory

class Config:
    SECRET_KEY = "my-secret-key"  #used for Securing sessions, Protecting cookies....
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False #disables SQLAlchemy event system that tracks object changes.
