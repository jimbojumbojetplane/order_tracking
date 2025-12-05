from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(required_role):
    """Decorator to require specific role for routes"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_role' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            if session['user_role'] != required_role and session['user_role'] != 'admin':
                flash('You do not have permission to access this page.', 'error')
                return redirect(url_for('orders.list_orders'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

