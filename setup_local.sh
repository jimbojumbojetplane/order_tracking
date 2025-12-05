#!/bin/bash
# Local development setup script for Cellcom Order Tracker

set -e  # Exit on error

echo "🚀 Setting up Cellcom Order Tracker for local development..."
echo ""

# Check Python version
echo "✓ Python version: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "✓ Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
FLASK_ENV=development
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
SQLALCHEMY_DATABASE_URI=sqlite:///cellcom_orders.db
ADMIN_DEFAULT_PASSWORD=cellcom
EOF
    echo "✓ .env file created"
else
    echo "✓ .env file already exists"
fi

# Initialize database
echo "💾 Initializing database..."
python3 init_db.py
echo "✓ Database initialized and seeded"

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run: flask run"
echo "  3. Open browser: http://localhost:5000"
echo ""
echo "Or run directly: python3 app.py"
echo ""
echo "Login credentials:"
echo "  - Anthony (Rep) / cellcom"
echo "  - Dominic (Rep) / cellcom"
echo "  - Rene (Manager) / cellcom"
echo "  - Admin (Admin) / cellcom"

