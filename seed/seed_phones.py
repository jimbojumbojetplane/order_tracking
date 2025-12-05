"""Seed script for phones - Canadian handsets database"""
import json
import os
from app import create_app
from models import db, Phone

def seed_phones():
    """Create phone catalog - loads from JSON file if available, otherwise uses defaults"""
    app = create_app()
    with app.app_context():
        # Check if phones already exist
        if Phone.query.first():
            print("Phones already exist. Skipping seed.")
            return
        
        # Try to load from JSON file if it exists
        json_file = os.path.join(os.path.dirname(__file__), 'handsets.json')
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                phones_data = json.load(f)
            print(f"✓ Loading handsets from {json_file}")
            print(f"  Found {len(phones_data)} handset configurations")
        else:
            # Fallback to default placeholder phones
            print("No handsets.json found. Using default placeholder phones.")
            phones_data = [
            # Apple iPhone models
            {'brand': 'Apple', 'model': 'iPhone 16 Pro Max', 'storage': '256 GB', 'colour': 'Natural Titanium', 'bell_sku': 'IPH16PM256NT', 'full_price': 1649.99, 'is_featured': True},
            {'brand': 'Apple', 'model': 'iPhone 16 Pro', 'storage': '256 GB', 'colour': 'Natural Titanium', 'bell_sku': 'IPH16P256NT', 'full_price': 1449.99, 'is_featured': True},
            {'brand': 'Apple', 'model': 'iPhone 16', 'storage': '128 GB', 'colour': 'Blue', 'bell_sku': 'IPH16128BL', 'full_price': 1129.99, 'is_featured': True},
            {'brand': 'Apple', 'model': 'iPhone 15 Pro Max', 'storage': '256 GB', 'colour': 'Natural Titanium', 'bell_sku': 'IPH15PM256NT', 'full_price': 1549.99, 'is_featured': False},
            {'brand': 'Apple', 'model': 'iPhone 15', 'storage': '128 GB', 'colour': 'Blue', 'bell_sku': 'IPH15128BL', 'full_price': 1029.99, 'is_featured': False},
            {'brand': 'Apple', 'model': 'iPhone 14', 'storage': '128 GB', 'colour': 'Midnight', 'bell_sku': 'IPH14128MD', 'full_price': 899.99, 'is_featured': False},
            
            # Samsung Galaxy models
            {'brand': 'Samsung', 'model': 'Galaxy S24 Ultra', 'storage': '256 GB', 'colour': 'Titanium Black', 'bell_sku': 'SGS24U256TB', 'full_price': 1549.99, 'is_featured': True},
            {'brand': 'Samsung', 'model': 'Galaxy S24+', 'storage': '256 GB', 'colour': 'Marble Gray', 'bell_sku': 'SGS24P256MG', 'full_price': 1249.99, 'is_featured': True},
            {'brand': 'Samsung', 'model': 'Galaxy S24', 'storage': '128 GB', 'colour': 'Marble Gray', 'bell_sku': 'SGS24128MG', 'full_price': 1049.99, 'is_featured': False},
            {'brand': 'Samsung', 'model': 'Galaxy Z Fold5', 'storage': '256 GB', 'colour': 'Phantom Black', 'bell_sku': 'SGZF5256PB', 'full_price': 2249.99, 'is_featured': True},
            {'brand': 'Samsung', 'model': 'Galaxy Z Flip5', 'storage': '256 GB', 'colour': 'Mint', 'bell_sku': 'SGZF5256MT', 'full_price': 1249.99, 'is_featured': False},
            {'brand': 'Samsung', 'model': 'Galaxy A54 5G', 'storage': '128 GB', 'colour': 'Awesome Black', 'bell_sku': 'SGA54128AB', 'full_price': 549.99, 'is_featured': False},
            
            # Google Pixel models
            {'brand': 'Google', 'model': 'Pixel 9 Pro', 'storage': '256 GB', 'colour': 'Obsidian', 'bell_sku': 'PIX9P256OB', 'full_price': 1249.99, 'is_featured': True},
            {'brand': 'Google', 'model': 'Pixel 9', 'storage': '128 GB', 'colour': 'Obsidian', 'bell_sku': 'PIX9128OB', 'full_price': 949.99, 'is_featured': False},
            {'brand': 'Google', 'model': 'Pixel 8 Pro', 'storage': '256 GB', 'colour': 'Obsidian', 'bell_sku': 'PIX8P256OB', 'full_price': 1099.99, 'is_featured': False},
            
            # Other brands
            {'brand': 'Motorola', 'model': 'Edge 50 Ultra', 'storage': '256 GB', 'colour': 'Peach Fuzz', 'bell_sku': 'MTE50U256PF', 'full_price': 899.99, 'is_featured': False},
            {'brand': 'Motorola', 'model': 'Razr 50 Ultra', 'storage': '256 GB', 'colour': 'Spring Green', 'bell_sku': 'MTR50U256SG', 'full_price': 1099.99, 'is_featured': False},
            {'brand': 'OnePlus', 'model': '12', 'storage': '256 GB', 'colour': 'Silky Black', 'bell_sku': 'OP12256SB', 'full_price': 999.99, 'is_featured': False},
            {'brand': 'Nothing', 'model': 'Phone (2a)', 'storage': '128 GB', 'colour': 'White', 'bell_sku': 'NOT2A128WH', 'full_price': 549.99, 'is_featured': False},
            ]
        
        for phone_data in phones_data:
            phone = Phone(**phone_data)
            db.session.add(phone)
        
        db.session.commit()
        print(f"✓ Seeded {len(phones_data)} phones successfully!")

if __name__ == '__main__':
    seed_phones()

