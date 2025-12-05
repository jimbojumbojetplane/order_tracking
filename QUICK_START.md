# Quick Start Guide

## ✅ Server is Now Running!

**Access the application at: http://localhost:5001**

> **Note:** Port 5001 is used instead of 5000 because macOS AirPlay Receiver uses port 5000.

## Login Credentials

- **Anthony** (Rep) - Password: `cellcom`
- **Dominic** (Rep) - Password: `cellcom`
- **Rene** (Manager) - Password: `cellcom`
- **Admin** (Admin) - Password: `cellcom`

## Starting the Server

### Option 1: Use the start script
```bash
cd /Users/jgf/coding/celllcom_ticket_tool
./START_APP.sh
```

### Option 2: Manual start
```bash
cd /Users/jgf/coding/celllcom_ticket_tool
source venv/bin/activate
python3 app.py
```

The server will start on **http://localhost:5001**

## What's Included

✅ **47 Real Handsets** from Canadian handsets database
- Apple (13 configurations)
- Samsung (10 configurations)
- Google (11 configurations)
- OnePlus (8 configurations)
- Motorola (5 configurations)

✅ **8 Bell Rate Plans** from extraction data
- Lite, Select, Max, Ultra (with 2-line variants)

✅ **10 Sample Customers**

✅ **12 Sample Orders**

## Testing

The server has been tested and verified working:
- ✅ Login page loads correctly
- ✅ All routes registered
- ✅ Database initialized
- ✅ Templates rendering

## Troubleshooting

If port 5001 is also in use, edit `app.py` and change:
```python
port = int(os.environ.get('PORT', 5002))  # Change to 5002 or any free port
```

Then access at: http://localhost:5002

