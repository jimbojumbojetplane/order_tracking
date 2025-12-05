#!/usr/bin/env python3
"""
Test script to verify the Flask app is working
"""
import requests
import time
import sys

def test_server():
    """Test if server is responding"""
    url = "http://localhost:5001"
    login_url = "http://localhost:5001/login"
    
    print("Testing Flask server...")
    print(f"Base URL: {url}")
    print(f"Login URL: {login_url}")
    print()
    
    try:
        # Test root redirect
        print("1. Testing root URL (/)...")
        response = requests.get(url, timeout=5, allow_redirects=True)
        print(f"   Status: {response.status_code}")
        print(f"   Final URL: {response.url}")
        print(f"   Response length: {len(response.text)} bytes")
        
        # Test login page
        print("\n2. Testing login page (/login)...")
        response = requests.get(login_url, timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response length: {len(response.text)} bytes")
        
        if "Cellcom Order Tracker" in response.text:
            print("   ✓ Login page contains expected content")
        else:
            print("   ✗ Login page missing expected content")
            print(f"   First 200 chars: {response.text[:200]}")
        
        # Check for form
        if 'name="first_name"' in response.text:
            print("   ✓ Login form found")
        else:
            print("   ✗ Login form NOT found")
            
        print("\n✅ Server is responding correctly!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("   ✗ Connection refused - server is not running")
        print("   Start the server with: python3 app.py")
        return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

if __name__ == '__main__':
    print("Waiting 2 seconds for server to be ready...")
    time.sleep(2)
    success = test_server()
    sys.exit(0 if success else 1)

