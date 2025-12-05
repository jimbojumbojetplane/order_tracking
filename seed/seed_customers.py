"""Seed script for customers"""
from app import create_app
from models import db, Customer, Store

def seed_customers():
    """Create mock customers"""
    app = create_app()
    with app.app_context():
        # Check if customers already exist
        if Customer.query.first():
            print("Customers already exist. Skipping seed.")
            return
        
        # Get some stores for preferred_store assignment (if stores exist)
        all_stores = Store.query.all()
        montreal_stores = Store.query.filter(Store.city.ilike('%Montréal%')).limit(3).all()
        laval_stores = Store.query.filter(Store.city == 'Laval').limit(2).all()
        
        # Helper function to get store ID safely
        def get_store_id(stores_list, index):
            if stores_list and len(stores_list) > index:
                return stores_list[index].id
            return None
        
        customers_data = [
            {'first_name': 'John', 'last_name': 'Smith', 'phone_number': '514-555-0101', 'email': 'john.smith@email.com', 'preferred_store_id': get_store_id(montreal_stores, 0)},
            {'first_name': 'Sarah', 'last_name': 'Johnson', 'phone_number': '514-555-0102', 'email': 'sarah.j@email.com', 'preferred_store_id': get_store_id(montreal_stores, 0)},
            {'first_name': 'Michael', 'last_name': 'Chen', 'phone_number': '514-555-0103', 'email': 'mchen@email.com', 'preferred_store_id': get_store_id(laval_stores, 0)},
            {'first_name': 'Emily', 'last_name': 'Martinez', 'phone_number': '514-555-0104', 'email': 'emily.m@email.com', 'preferred_store_id': get_store_id(montreal_stores, 1)},
            {'first_name': 'David', 'last_name': 'Brown', 'phone_number': '514-555-0105', 'email': 'david.brown@email.com', 'preferred_store_id': get_store_id(all_stores, 5)},
            {'first_name': 'Jessica', 'last_name': 'Davis', 'phone_number': '514-555-0106', 'email': 'j.davis@email.com', 'preferred_store_id': get_store_id(montreal_stores, 0)},
            {'first_name': 'James', 'last_name': 'Wilson', 'phone_number': '514-555-0107', 'email': 'jwilson@email.com', 'preferred_store_id': get_store_id(all_stores, 3)},
            {'first_name': 'Maria', 'last_name': 'Garcia', 'phone_number': '514-555-0108', 'email': 'maria.g@email.com', 'preferred_store_id': get_store_id(laval_stores, 0)},
            {'first_name': 'Robert', 'last_name': 'Anderson', 'phone_number': '514-555-0109', 'email': 'robert.a@email.com', 'preferred_store_id': get_store_id(montreal_stores, 2)},
            {'first_name': 'Lisa', 'last_name': 'Thompson', 'phone_number': '514-555-0110', 'email': 'lisa.t@email.com', 'preferred_store_id': get_store_id(all_stores, 8)},
        ]
        
        for customer_data in customers_data:
            customer = Customer(**customer_data)
            db.session.add(customer)
        
        db.session.commit()
        print(f"Seeded {len(customers_data)} customers successfully!")

if __name__ == '__main__':
    seed_customers()

