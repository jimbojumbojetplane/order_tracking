"""Seed script for orders"""
import random
from datetime import datetime, timedelta
from app import create_app
from models import db, Order, OrderStatusHistory, Customer, User, Phone, RatePlan, Store

def seed_orders():
    """Create mock orders"""
    app = create_app()
    with app.app_context():
        # Check if orders already exist
        if Order.query.first():
            print("Orders already exist. Skipping seed.")
            return
        
        # Get seeded data
        customers = Customer.query.all()
        users = User.query.filter(User.role == 'rep').all()  # Only use rep users
        phones = Phone.query.all()
        rate_plans = RatePlan.query.all()
        stores = Store.query.filter_by(is_active=True).all()
        
        if not all([customers, users, phones, rate_plans, stores]):
            print("Error: Make sure to seed stores, customers, users, phones, and rate plans first!")
            return
        
        statuses = ['New', 'Pending Activation', 'Activated', 'Cancelled', 'Returned']
        stores = Store.query.filter_by(is_active=True).all()
        
        if not stores:
            print("Error: No stores found. Please seed stores first!")
            return
        
        # Generate 12 mock orders
        year = datetime.now().year
        for i in range(1, 13):
            # Generate order number
            order_number = f"CEL-{year}-{i:04d}"
            
            # Random selections
            customer = random.choice(customers)
            user = random.choice(users)
            phone = random.choice(phones)
            rate_plan = random.choice(rate_plans)
            status = random.choice(statuses)
            store = random.choice(stores)
            
            # Random creation date (within last 60 days)
            days_ago = random.randint(0, 60)
            created_at = datetime.now() - timedelta(days=days_ago)
            
            # If activated, set activation date (after creation)
            activation_date = None
            if status == 'Activated':
                activation_days_ago = random.randint(0, days_ago - 1) if days_ago > 1 else 0
                activation_date = datetime.now() - timedelta(days=activation_days_ago)
            
            order = Order(
                order_number=order_number,
                customer_id=customer.id,
                user_id=user.id,
                phone_id=phone.id,
                rate_plan_id=rate_plan.id,
                store_id=store.id,
                store_location=store.display_name,  # Store display name for compatibility
                status=status,
                created_at=created_at,
                updated_at=created_at,
                activation_date=activation_date,
                notes=f'Mock order #{i} - {random.choice(["Standard order", "Priority customer", "Regular order", ""])}'.strip()
            )
            
            db.session.add(order)
            db.session.flush()  # Get order ID
            
            # Create initial status history entry
            history = OrderStatusHistory(
                order_id=order.id,
                old_status='',
                new_status=status,
                changed_by_user_id=user.id,
                changed_at=created_at,
                comment='Order created'
            )
            db.session.add(history)
            
            # Add a status change history entry if status changed
            if status != 'New':
                change_days_ago = random.randint(0, days_ago - 1) if days_ago > 1 else 0
                change_at = datetime.now() - timedelta(days=change_days_ago)
                
                history2 = OrderStatusHistory(
                    order_id=order.id,
                    old_status='New',
                    new_status=status,
                    changed_by_user_id=user.id,
                    changed_at=change_at,
                    comment=f'Status updated to {status}'
                )
                db.session.add(history2)
        
        db.session.commit()
        print(f"Seeded 12 orders successfully!")

if __name__ == '__main__':
    seed_orders()

