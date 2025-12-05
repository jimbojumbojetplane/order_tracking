# HostPapa Deployment Guide

This guide will help you deploy the Cellcom Order Tracker Flask application to HostPapa hosting.

## Prerequisites

1. **HostPapa Account**: Ensure you have:
   - A HostPapa hosting plan that supports Python applications (VPS, Business, or Developer plan)
   - SSH access enabled (for VPS)
   - Python 3.x support
   - Database access (MySQL/PostgreSQL recommended for production)

2. **Required Access**:
   - cPanel access (for shared hosting)
   - SSH access (recommended for easier deployment)
   - FTP/SFTP credentials

## HostPapa Setup Options

### Option 1: VPS Hosting (Recommended)
Best for full control and Python/Flask support.

### Option 2: Python Hosting
If HostPapa offers Python-specific hosting.

### Option 3: Shared Hosting (Limited)
May require special configuration; check with HostPapa support.

## Deployment Steps

### Step 1: Prepare Your Repository

1. Ensure your code is pushed to GitHub:
```bash
git add .
git commit -m "Prepare for HostPapa deployment"
git push origin main
```

2. Verify all files are in the repository:
- `wsgi.py` (WSGI entry point)
- `.htaccess` (Apache configuration)
- `requirements.txt` (Python dependencies)
- `config.py` (Configuration)

### Step 2: Connect to HostPapa Server

#### Via SSH (Recommended):
```bash
ssh username@yourdomain.com
# or
ssh username@your-server-ip
```

#### Via cPanel File Manager:
- Log into cPanel
- Navigate to File Manager
- Go to `public_html` directory

### Step 3: Deploy Application Files

#### Method A: Clone from GitHub (Recommended)
```bash
cd ~/public_html
# Or create a subdirectory
mkdir -p ~/cellcom-app
cd ~/cellcom-app

# Clone your repository
git clone https://github.com/yourusername/celllcom_ticket_tool.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### Method B: Upload via FTP/SFTP
1. Use FileZilla or similar FTP client
2. Upload all files to your `public_html` directory (or subdirectory)
3. Ensure file permissions are correct (755 for directories, 644 for files)

### Step 4: Set Up Virtual Environment

```bash
# Create virtual environment in your app directory
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Verify installation
pip list
```

### Step 5: Configure Environment Variables

Create a `.env` file in your application root:

```bash
cd ~/public_html/cellcom-app
nano .env
```

Add the following (adjust values for production):
```env
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-change-this-in-production
SQLALCHEMY_DATABASE_URI=mysql+pymysql://username:password@localhost/cellcom_orders
# Or for PostgreSQL:
# SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost/cellcom_orders
```

**Important**: 
- Change `SECRET_KEY` to a strong random string
- Use environment variables in cPanel if available
- Never commit `.env` to Git

### Step 6: Set Up Database

#### Option A: MySQL (via cPanel)
1. Log into cPanel
2. Go to "MySQL Databases"
3. Create a new database: `cellcom_orders`
4. Create a database user
5. Grant all privileges to the user
6. Update `SQLALCHEMY_DATABASE_URI` in `.env`

#### Option B: PostgreSQL (if available)
1. Create database via cPanel or command line
2. Update connection string in `.env`

#### Option C: SQLite (for testing only - not recommended for production)
- The default SQLite database will be created automatically
- **Warning**: SQLite doesn't work well with multiple processes/mod_wsgi

### Step 7: Initialize Database

```bash
cd ~/public_html/cellcom-app
source venv/bin/activate

# Initialize and seed database
python3 init_db.py
```

### Step 8: Configure Web Server

#### For mod_wsgi (Apache):
If HostPapa supports mod_wsgi, update `.htaccess`:

```apache
WSGIScriptAlias / /home/username/public_html/cellcom-app/wsgi.py
WSGIDaemonProcess flaskapp python-path=/home/username/public_html/cellcom-app:/home/username/public_html/cellcom-app/venv/lib/python3.x/site-packages
WSGIProcessGroup flaskapp
WSGIApplicationGroup %{GLOBAL}
```

#### For Passenger (if HostPapa uses Passenger):
Ensure `public/.htaccess` is correctly configured with Passenger settings.

#### For FastCGI or CGI:
You may need to create a Python CGI wrapper - contact HostPapa support for specific instructions.

### Step 9: Set File Permissions

```bash
# Make directories writable (for database, logs, etc.)
chmod 755 ~/public_html/cellcom-app
chmod 755 ~/public_html/cellcom-app/instance
chmod 644 ~/public_html/cellcom-app/.htaccess
chmod 755 ~/public_html/cellcom-app/wsgi.py

# If using SQLite (not recommended):
chmod 666 ~/public_html/cellcom-app/instance/*.db
```

### Step 10: Test Application

1. Visit your domain: `https://yourdomain.com`
2. You should see the login page
3. Test login with default credentials:
   - Username: `Anthony`
   - Password: `cellcom`

## Troubleshooting

### Common Issues

1. **Import Errors**:
   - Verify virtual environment is activated
   - Check Python path in WSGI configuration
   - Ensure all dependencies are installed

2. **Database Connection Errors**:
   - Verify database credentials in `.env`
   - Check database server is running
   - Ensure database user has correct permissions

3. **500 Internal Server Error**:
   - Check error logs in cPanel
   - Verify file permissions
   - Check WSGI/Python configuration

4. **Static Files Not Loading**:
   - Verify `static/` directory exists and is accessible
   - Check `.htaccess` configuration
   - Clear browser cache

### Viewing Logs

```bash
# Application logs (if configured)
tail -f ~/logs/cellcom-app.log

# Apache error logs
tail -f ~/logs/error_log

# Access logs
tail -f ~/logs/access_log
```

## Production Recommendations

1. **Security**:
   - Change all default passwords
   - Use strong `SECRET_KEY`
   - Enable HTTPS/SSL certificate (free via Let's Encrypt in cPanel)
   - Keep dependencies updated

2. **Performance**:
   - Use MySQL/PostgreSQL instead of SQLite
   - Enable caching if available
   - Optimize database queries

3. **Backups**:
   - Set up automated database backups in cPanel
   - Regular file backups

4. **Monitoring**:
   - Monitor error logs regularly
   - Set up uptime monitoring
   - Track database size

## Contact HostPapa Support

If you encounter issues specific to HostPapa hosting:
- Support tickets via cPanel
- Live chat support
- Documentation: Check HostPapa's Python/Flask hosting documentation

## Additional Configuration

### Custom Domain Setup
1. Point domain DNS to HostPapa nameservers
2. Add domain in cPanel
3. Update application URL if needed

### SSL Certificate
1. Use Let's Encrypt (free) via cPanel
2. Enable "Force HTTPS Redirect"
3. Update Flask configuration if needed

### Cron Jobs (if needed)
Set up in cPanel → Cron Jobs for scheduled tasks

## Notes

- HostPapa shared hosting may have limitations on:
  - Python version
  - Module availability
  - Execution time limits
  - Memory limits

- For best results, consider HostPapa VPS or Business plan
- Always test in a staging environment first

