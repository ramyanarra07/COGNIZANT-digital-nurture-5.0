import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this-secret'
    # Defaulting to an in-memory or local SQLite database for local development
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///courses.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True