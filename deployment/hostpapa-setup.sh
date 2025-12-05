#!/bin/bash
# HostPapa Deployment Setup Script
# Run this on your HostPapa server after uploading files

echo "Setting up Cellcom Order Tracker on HostPapa..."

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

cd "$APP_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create instance directory if it doesn't exist
mkdir -p instance

# Set permissions
echo "Setting file permissions..."
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;
chmod 755 wsgi.py
chmod 755 deployment/hostpapa-setup.sh

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file template..."
    cat > .env << EOF
FLASK_ENV=production
SECRET_KEY=$(openssl rand -hex 32)
SQLALCHEMY_DATABASE_URI=sqlite:///instance/celldb.db
EOF
    echo ".env file created. Please update with your production values!"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env file with your production database URI and secret key"
echo "2. Run: python3 init_db.py (to initialize the database)"
echo "3. Configure your .htaccess file for your HostPapa setup"
echo "4. Test your application"

