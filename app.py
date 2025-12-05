from flask import Flask
from config import config
from models import db
from routes.auth import auth_bp
from routes.orders import orders_bp
from routes.customers import customers_bp
from routes.phones import phones_bp
from routes.rate_plans import rate_plans_bp
from routes.stores import stores_bp
from routes.about import about_bp

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(phones_bp, url_prefix='/phones')
    app.register_blueprint(rate_plans_bp, url_prefix='/rate-plans')
    app.register_blueprint(stores_bp, url_prefix='/stores')
    app.register_blueprint(about_bp, url_prefix='')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Root route redirects to orders
    @app.route('/')
    def index():
        from flask import redirect, url_for, session
        if 'user_id' in session:
            return redirect(url_for('orders.list_orders'))
        return redirect(url_for('auth.login'))
    
    return app

if __name__ == '__main__':
    import os
    env = os.environ.get('FLASK_ENV', 'development')
    app = create_app(env)
    # Use port 5001 to avoid conflict with macOS AirPlay Receiver on port 5000
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)

