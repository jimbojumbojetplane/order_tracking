#!/usr/bin/env python3
"""
Database initialization and seeding script
Run this once to set up the database with all seed data
"""
import sys
from app import create_app
from models import db
import seed.seed_users as seed_users
import seed.seed_stores as seed_stores
import seed.seed_customers as seed_customers
import seed.seed_phones as seed_phones
import seed.seed_rate_plans as seed_rate_plans
import seed.seed_orders as seed_orders

def init_database():
    """Initialize database and run all seed scripts"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created\n")
        
        print("Seeding database...\n")
        
        try:
            seed_stores.seed_stores()
            seed_users.seed_users()
            seed_customers.seed_customers()
            seed_phones.seed_phones()
            seed_rate_plans.seed_rate_plans()
            seed_orders.seed_orders()
            
            print("\n✓ Database initialization complete!")
            print("\nYou can now start the app with: flask run")
            print("\nDemo accounts:")
            print("  - Anthony (Rep) - Password: cellcom")
            print("  - Dominic (Rep) - Password: cellcom")
            print("  - Rene (Manager) - Password: cellcom")
            print("  - Admin (Admin) - Password: cellcom")
            
        except Exception as e:
            print(f"\n✗ Error during seeding: {e}")
            sys.exit(1)

if __name__ == '__main__':
    init_database()

