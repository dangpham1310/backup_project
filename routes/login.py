import os
import uuid
from flask import Blueprint, current_app, flash, jsonify, render_template, redirect, send_file, send_from_directory, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
import requests
from .db import User,db
from . import routes
from werkzeug.utils import secure_filename
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm, RecaptchaField


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    # recaptcha = RecaptchaField()
    submit = SubmitField('Login')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            print("Đăng Nhập Thành Công")

            if current_user.role == "SA" or current_user.role == "user":
                return redirect(url_for('routes.dashboard'))
            else:

                return redirect(url_for('routes.home'))
        else:
            

            flash("Sai Tên Đăng Nhập hoặc mật khẩu")
            return render_template('login.html', form=form)
    
    return render_template('login.html', form=form)

@routes.route('/dashboard')
@login_required
def dashboard():
    all_users = User.query.all()
    if current_user.role == "SA" or current_user.role == "user":
        return render_template("./dashboard/dashboard_main.html", users = all_users)
    else:
        return redirect(url_for('routes.home'))


@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.login'))


@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return 'Username already exists'
        new_user = User(username=username, name=name)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('routes.dashboard'))
    return render_template('register.html')









