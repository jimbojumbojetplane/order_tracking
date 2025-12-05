# Troubleshooting Guide

## Localhost Access Denied

If you're getting "access denied" errors when trying to access http://localhost:5000:

### Solution 1: Kill existing processes
```bash
# Kill any Flask processes
pkill -f "flask run"
pkill -f "python.*app.py"

# Or kill specific port
lsof -ti:5000 | xargs kill -9
```

### Solution 2: Use the correct URL
Try these URLs:
- http://localhost:5000
- http://127.0.0.1:5000
- http://0.0.0.0:5000

### Solution 3: Check if app is running
```bash
# Check if port 5000 is in use
lsof -i:5000

# Check Flask processes
ps aux | grep flask
```

### Solution 4: Restart the app
```bash
cd /Users/jgf/coding/celllcom_ticket_tool
source venv/bin/activate
python3 app.py
```

### Solution 5: Try a different port
Edit `app.py` and change:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use port 5001
```

Then access at: http://localhost:5001

## Common Issues

### Database locked
If you see database errors:
```bash
rm cellcom_orders.db
python3 init_db.py
```

### Module not found
Make sure virtual environment is activated:
```bash
source venv/bin/activate
```

### Port already in use
```bash
# Find what's using the port
lsof -i:5000

# Kill it
kill -9 <PID>
```

