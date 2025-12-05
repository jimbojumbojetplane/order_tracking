"""Seed script for rate plans"""
import json
import os
from app import create_app
from models import db, RatePlan

def seed_rate_plans():
    """Create rate plans - can read from JSON file if provided, otherwise uses defaults"""
    app = create_app()
    with app.app_context():
        # Check if rate plans already exist
        if RatePlan.query.first():
            print("Rate plans already exist. Skipping seed.")
            return
        
        # Try to load from JSON file if it exists
        json_file = os.path.join(os.path.dirname(__file__), 'rate_plans.json')
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                plans_data = json.load(f)
            print(f"✓ Loading rate plans from {json_file}")
            print(f"  Found {len(plans_data)} plans")
        else:
            # Default placeholder plans
            print("No rate_plans.json found. Using default placeholder plans.")
            plans_data = [
                {
                    'name': 'Canada 150',
                    'monthly_price': 65.00,
                    'data_gb': 150,
                    'unlimited_canada': True,
                    'unlimited_us': False,
                    'roaming_notes': 'Unlimited talk & text in Canada. 150GB data.',
                    'bell_plan_code': 'CAN150',
                    'segment': 'consumer'
                },
                {
                    'name': 'Canada + US 100',
                    'monthly_price': 85.00,
                    'data_gb': 100,
                    'unlimited_canada': True,
                    'unlimited_us': True,
                    'roaming_notes': 'Unlimited talk & text in Canada & US. 100GB data.',
                    'bell_plan_code': 'CAUS100',
                    'segment': 'consumer'
                },
                {
                    'name': 'Unlimited Canada',
                    'monthly_price': 75.00,
                    'data_gb': None,
                    'unlimited_canada': True,
                    'unlimited_us': False,
                    'roaming_notes': 'Unlimited talk, text, and data in Canada.',
                    'bell_plan_code': 'UNCAN',
                    'segment': 'consumer'
                },
                {
                    'name': 'Canada 75',
                    'monthly_price': 55.00,
                    'data_gb': 75,
                    'unlimited_canada': True,
                    'unlimited_us': False,
                    'roaming_notes': 'Unlimited talk & text in Canada. 75GB data.',
                    'bell_plan_code': 'CAN75',
                    'segment': 'consumer'
                },
                {
                    'name': 'Canada 50',
                    'monthly_price': 45.00,
                    'data_gb': 50,
                    'unlimited_canada': True,
                    'unlimited_us': False,
                    'roaming_notes': 'Unlimited talk & text in Canada. 50GB data.',
                    'bell_plan_code': 'CAN50',
                    'segment': 'consumer'
                },
                {
                    'name': 'Business Unlimited Canada',
                    'monthly_price': 95.00,
                    'data_gb': None,
                    'unlimited_canada': True,
                    'unlimited_us': False,
                    'roaming_notes': 'Business plan with unlimited talk, text, and data in Canada.',
                    'bell_plan_code': 'BIZUNCAN',
                    'segment': 'business'
                },
                {
                    'name': 'Business Canada + US 150',
                    'monthly_price': 115.00,
                    'data_gb': 150,
                    'unlimited_canada': True,
                    'unlimited_us': True,
                    'roaming_notes': 'Business plan with unlimited talk & text in Canada & US. 150GB data.',
                    'bell_plan_code': 'BIZCAUS150',
                    'segment': 'business'
                },
            ]
        
        for plan_data in plans_data:
            plan = RatePlan(**plan_data)
            db.session.add(plan)
        
        db.session.commit()
        print(f"Seeded {len(plans_data)} rate plans successfully!")
        print("Note: To use custom rate plans, create seed/rate_plans.json with the plan data.")

if __name__ == '__main__':
    seed_rate_plans()

