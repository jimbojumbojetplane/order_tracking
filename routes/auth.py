from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, User
from auth import login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        password = request.form.get('password', '').strip()
        
        if not first_name or not password:
            flash('Please enter both first name and password.', 'error')
            return render_template('login.html')
        
        # Find user by first name (case-insensitive match)
        # Try exact match first
        user = User.query.filter_by(first_name=first_name).first()
        
        # If not found, try case-insensitive search
        if not user:
            user = User.query.filter(
                db.func.lower(User.first_name) == db.func.lower(first_name)
            ).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_first_name'] = user.first_name
            session['user_role'] = user.role
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(url_for('orders.list_orders'))
        else:
            # Provide more helpful error message
            if not user:
                flash(f'User "{first_name}" not found. Please check the spelling.', 'error')
            else:
                flash('Invalid password. Password is case-sensitive.', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout and clear session"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

