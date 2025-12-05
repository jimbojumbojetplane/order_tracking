#!/bin/bash
# Quick start script for Cellcom Order Tracker

cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Set Flask environment variables
export FLASK_APP=app.py
export FLASK_ENV=development
export PORT=5001

echo "🚀 Starting Cellcom Order Tracker..."
echo ""
echo "📱 Application will be available at: http://localhost:5001"
echo ""
echo "👤 Login credentials:"
echo "   - Anthony (Rep) / cellcom"
echo "   - Dominic (Rep) / cellcom"
echo "   - Rene (Manager) / cellcom"
echo "   - Admin (Admin) / cellcom"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run with explicit host binding on port 5001 (5000 is used by macOS AirPlay)
python3 app.py

