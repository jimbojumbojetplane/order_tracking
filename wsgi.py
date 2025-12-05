"""
WSGI entry point for production deployment
Compatible with Railway, HostPapa, and other hosting platforms
"""
import os
import sys

# Add the application directory to Python path
basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, basedir)

# Activate virtual environment if it exists (for local/testing)
venv_path = os.path.join(basedir, 'venv')
if os.path.exists(venv_path):
    activate_this = os.path.join(venv_path, 'bin', 'activate_this.py')
    if os.path.exists(activate_this):
        try:
            with open(activate_this) as file_:
                exec(file_.read(), dict(__file__=activate_this))
        except Exception:
            pass  # Ignore venv activation errors (Railway doesn't need this)

from app import create_app

# Get environment from environment variable or default to production
env = os.environ.get('FLASK_ENV', 'production')
application = create_app(env)

# Railway, Heroku, and other platforms expect 'application' variable
# Some platforms also accept 'app'
app = application

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port)
