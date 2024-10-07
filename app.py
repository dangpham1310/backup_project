import threading
import time
import os
from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from routes import routes, limiter, threading_resync_scheduler_loop
from routes.db import db, Config
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.secret_key = 'n9b9monkey123456789'
app.register_blueprint(routes)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeCeiIqAAAAAJ8s8w4IVyIxmYTf6oMt3JQUC0iT'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeCeiIqAAAAAKwd4iOukpw5ujUOs2iZeUeSeE1W'
app.config.from_object(Config)
db.init_app(app)

# Initialize rate limiter with Redis as storage backend
# limiter.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'routes.login'
migrate = Migrate(app, db)

# Import the User model here
from routes.db import User

# Define the user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# threading_resync_scheduler_loop(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=4090)
