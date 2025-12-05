#!/usr/bin/env python3
"""Quick script to check database connection and verify users exist"""
from app import create_app
from models import db, User
import os

def check_database():
    """Check database connection and user count"""
    app = create_app()
    
    print("=" * 50)
    print("DATABASE CONNECTION CHECK")
    print("=" * 50)
    
    # Check environment variables
    print("\n1. Environment Variables:")
    print(f"   FLASK_ENV: {os.environ.get('FLASK_ENV', 'NOT SET')}")
    print(f"   DATABASE_URL: {os.environ.get('DATABASE_URL', 'NOT SET')[:50] if os.environ.get('DATABASE_URL') else 'NOT SET'}...")
    print(f"   SQLALCHEMY_DATABASE_URI: {os.environ.get('SQLALCHEMY_DATABASE_URI', 'NOT SET')[:50] if os.environ.get('SQLALCHEMY_DATABASE_URI') else 'NOT SET'}...")
    
    with app.app_context():
        # Check database URI
        print(f"\n2. Database URI (from config):")
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', 'NOT SET')
        # Hide password in URI for security
        if db_uri and db_uri != 'NOT SET':
            if '@' in db_uri:
                # Hide password
                parts = db_uri.split('@')
                if '://' in parts[0]:
                    protocol_user = parts[0].split('://')[0] + '://' + parts[0].split('://')[1].split(':')[0] + ':***'
                    print(f"   {protocol_user}@{parts[1]}")
                else:
                    print(f"   {db_uri[:50]}...")
            else:
                print(f"   {db_uri}")
        else:
            print(f"   {db_uri}")
        
        # Try to connect
        print("\n3. Testing Database Connection...")
        try:
            db.engine.connect()
            print("   ✅ Database connection successful!")
        except Exception as e:
            print(f"   ❌ Database connection failed: {e}")
            return False
        
        # Check if tables exist
        print("\n4. Checking Tables...")
        try:
            # Try to query users table
            user_count = User.query.count()
            print(f"   ✅ Users table exists!")
            print(f"   ✅ Found {user_count} users in database")
            
            if user_count > 0:
                users = User.query.all()
                print("\n5. Users in database:")
                for user in users:
                    print(f"   - {user.first_name} ({user.role})")
                return True
            else:
                print("\n   ⚠️  No users found! Database needs to be initialized.")
                print("   Run: railway run python3 init_db.py")
                return False
                
        except Exception as e:
            print(f"   ❌ Error querying database: {e}")
            print("   ⚠️  Tables might not exist yet.")
            print("   Run: railway run python3 init_db.py")
            return False

if __name__ == '__main__':
    success = check_database()
    if not success:
        print("\n" + "=" * 50)
        print("ACTION NEEDED: Initialize database with init_db.py")
        print("=" * 50)

