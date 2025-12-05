from flask import Blueprint, jsonify, render_template_string
from models import db, User, Store
import seed.seed_users as seed_users
import seed.seed_stores as seed_stores
import seed.seed_customers as seed_customers
import seed.seed_phones as seed_phones
import seed.seed_rate_plans as seed_rate_plans
import seed.seed_orders as seed_orders
import os

init_bp = Blueprint('init', __name__)

@init_bp.route('/init-db', methods=['GET'])
def init_database():
    """Initialize database via web interface - accessible without login for setup"""
    results = {
        'status': 'running',
        'steps': [],
        'error': None,
        'users_created': 0,
        'stores_created': 0
    }
    
    try:
        # Check environment
        results['steps'].append('Checking environment variables...')
        db_url = os.environ.get('DATABASE_URL', 'NOT SET')
        flask_env = os.environ.get('FLASK_ENV', 'NOT SET')
        results['steps'].append(f'DATABASE_URL: {"SET" if db_url != "NOT SET" else "NOT SET"}')
        results['steps'].append(f'FLASK_ENV: {flask_env}')
        
        # Create tables
        results['steps'].append('Creating database tables...')
        db.create_all()
        results['steps'].append('✓ Database tables created')
        
        # Check current state
        user_count_before = User.query.count()
        store_count_before = Store.query.count()
        results['steps'].append(f'Current state: {user_count_before} users, {store_count_before} stores')
        
        # Seed stores (if needed)
        if store_count_before == 0:
            results['steps'].append('Seeding stores...')
            seed_stores.seed_stores()
            store_count_after = Store.query.count()
            results['stores_created'] = store_count_after - store_count_before
            results['steps'].append(f'✓ Created {results["stores_created"]} stores')
        
        # Seed users (if needed)
        if user_count_before == 0:
            results['steps'].append('Seeding users...')
            seed_users.seed_users()
            user_count_after = User.query.count()
            results['users_created'] = user_count_after - user_count_before
            results['steps'].append(f'✓ Created {results["users_created"]} users')
        else:
            results['steps'].append(f'Skipping user seed (already {user_count_before} users exist)')
        
        # Seed other data if needed
        from models import Customer, Phone, RatePlan
        if Customer.query.count() == 0:
            results['steps'].append('Seeding customers...')
            seed_customers.seed_customers()
            results['steps'].append('✓ Customers seeded')
        
        if Phone.query.count() == 0:
            results['steps'].append('Seeding phones...')
            seed_phones.seed_phones()
            results['steps'].append('✓ Phones seeded')
        
        if RatePlan.query.count() == 0:
            results['steps'].append('Seeding rate plans...')
            seed_rate_plans.seed_rate_plans()
            results['steps'].append('✓ Rate plans seeded')
        
        # Final state
        final_user_count = User.query.count()
        final_store_count = Store.query.count()
        results['steps'].append(f'Final state: {final_user_count} users, {final_store_count} stores')
        
        results['status'] = 'success'
        results['steps'].append('✓ Database initialization complete!')
        
        # Get user list
        users = User.query.all()
        results['user_list'] = [f"{u.first_name} ({u.role})" for u in users]
        
    except Exception as e:
        results['status'] = 'error'
        results['error'] = str(e)
        results['steps'].append(f'✗ Error: {str(e)}')
    
    # Render as HTML for easy viewing
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Database Initialization</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            .success { color: green; }
            .error { color: red; }
            .step { margin: 5px 0; padding: 5px; background: #f5f5f5; }
            h1 { color: #333; }
            pre { background: #f0f0f0; padding: 10px; border-radius: 5px; overflow-x: auto; }
            .user-list { margin-top: 20px; }
            .user-list li { margin: 5px 0; }
        </style>
    </head>
    <body>
        <h1>Database Initialization Status</h1>
        <div class="status">
            <h2>Status: <span class="{{ status_class }}">{{ status|upper }}</span></h2>
        </div>
        
        <h3>Steps:</h3>
        <div class="steps">
            {% for step in steps %}
            <div class="step">{{ step }}</div>
            {% endfor %}
        </div>
        
        {% if error %}
        <div class="error">
            <h3>Error:</h3>
            <pre>{{ error }}</pre>
        </div>
        {% endif %}
        
        {% if users_created > 0 %}
        <div class="success user-list">
            <h3>Users Created:</h3>
            <ul>
                {% for user in user_list %}
                <li>{{ user }} - Password: <strong>cellcom</strong></li>
                {% endfor %}
            </ul>
            <p><strong>You can now <a href="/login">login here</a></strong></p>
        </div>
        {% elif user_list %}
        <div class="user-list">
            <h3>Existing Users:</h3>
            <ul>
                {% for user in user_list %}
                <li>{{ user }} - Password: <strong>cellcom</strong></li>
                {% endfor %}
            </ul>
            <p><strong><a href="/login">Go to login page</a></strong></p>
        </div>
        {% endif %}
        
        {% if stores_created > 0 %}
        <div class="success">
            <p>Created {{ stores_created }} stores</p>
        </div>
        {% endif %}
    </body>
    </html>
    """
    
    from flask import render_template_string
    status_class = 'success' if results['status'] == 'success' else 'error'
    return render_template_string(html_template, 
                                  status=results['status'],
                                  status_class=status_class,
                                  steps=results['steps'],
                                  error=results.get('error'),
                                  users_created=results.get('users_created', 0),
                                  stores_created=results.get('stores_created', 0),
                                  user_list=results.get('user_list', []))

