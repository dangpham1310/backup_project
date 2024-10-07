from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False,default="user")


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password,password)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Config:
    UPLOAD_FOLDER = "uploads"

class RsyncJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_rent = db.Column(db.String(50), nullable=False)
    source_user = db.Column(db.String(50), nullable=False)
    source_host = db.Column(db.String(100), nullable=False)
    source_path = db.Column(db.String(200), nullable=False)
    dest_path = db.Column(db.String(200), nullable=False)
    ssh_port = db.Column(db.Integer, nullable=False)
    backuptime = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, default=False)

class StackRsyncJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commandLine = db.Column(db.String(1000), nullable=False)
    completed = db.Column(db.Boolean, default=False)


