"""
WSGI entry point for production deployment with HostPapa
This file is used by mod_wsgi or Passenger on HostPapa hosting
"""
import os
import sys

# Add the application directory to Python path
# Adjust these paths based on your HostPapa account structure
basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, basedir)

# Activate virtual environment if it exists
# HostPapa Python hosting may require virtual environment
venv_path = os.path.join(basedir, 'venv')
if os.path.exists(venv_path):
    activate_this = os.path.join(venv_path, 'bin', 'activate_this.py')
    if os.path.exists(activate_this):
        with open(activate_this) as file_:
            exec(file_.read(), dict(__file__=activate_this))

from app import create_app

# Get environment from environment variable or default to production
env = os.environ.get('FLASK_ENV', 'production')
application = create_app(env)

if __name__ == '__main__':
    application.run()
