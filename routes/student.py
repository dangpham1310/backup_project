import os
import uuid
from flask import Blueprint, current_app, flash, jsonify, render_template, redirect, send_file, send_from_directory, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
import requests
from .db import User
from . import routes
from werkzeug.utils import secure_filename
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm, RecaptchaField
from werkzeug.security import generate_password_hash

