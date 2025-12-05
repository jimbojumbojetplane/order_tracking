"""Seed script for stores from Notion database"""
import json
import os
from app import create_app
from models import db, Store

def seed_stores():
    """Create stores from JSON file"""
    app = create_app()
    with app.app_context():
        # Check if stores already exist
        if Store.query.first():
            print("Stores already exist. Skipping seed.")
            return
        
        # Load stores from JSON file
        json_file = os.path.join(os.path.dirname(__file__), 'stores_from_notion.json')
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                stores_data = json.load(f)
            print(f"✓ Loading stores from {json_file}")
            print(f"  Found {len(stores_data)} stores")
        else:
            print("No stores_from_notion.json found. Skipping store seed.")
            return
        
        for store_data in stores_data:
            # Fix province typo
            if store_data.get('province') == 'Onatrio':
                store_data['province'] = 'ON'
            
            store = Store(**store_data)
            db.session.add(store)
        
        db.session.commit()
        print(f"✓ Seeded {len(stores_data)} stores successfully!")

if __name__ == '__main__':
    seed_stores()

