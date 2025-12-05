"""Seed script for users"""
from app import create_app
from models import db, User
from config import Config

def seed_users():
    """Create demo users"""
    app = create_app()
    with app.app_context():
        # Check if users already exist
        if User.query.first():
            print("Users already exist. Skipping seed.")
            return
        
        users_data = [
            {'first_name': 'Anthony', 'role': 'rep', 'password': 'cellcom'},
            {'first_name': 'Dominic', 'role': 'rep', 'password': 'cellcom'},
            {'first_name': 'Rene', 'role': 'manager', 'password': 'cellcom'},
            {'first_name': 'Admin', 'role': 'admin', 'password': 'cellcom'},
        ]
        
        for user_data in users_data:
            user = User(
                first_name=user_data['first_name'],
                role=user_data['role']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
        
        db.session.commit()
        print(f"Seeded {len(users_data)} users successfully!")

if __name__ == '__main__':
    seed_users()

