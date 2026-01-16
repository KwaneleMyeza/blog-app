from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier')
        password = request.form.get('password')

        if not identifier or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('auth.login'))

        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier)
        ).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash('Invalid credentials.', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user)
        flash('Logged in successfully.', 'success')
        return redirect(url_for('main.home'))

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))
