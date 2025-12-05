# HostPapa Quick Start Deployment

## Quick Deployment Checklist

### 1. Pre-Deployment (Local)
- [ ] All code committed to GitHub
- [ ] Tested locally
- [ ] `requirements.txt` updated
- [ ] `.env.example` created (if needed)

### 2. HostPapa Server Setup

#### Via SSH (Fastest Method):
```bash
# Connect to HostPapa
ssh username@yourdomain.com

# Navigate to web root
cd ~/public_html

# Clone your repository (or create directory and upload files)
git clone https://github.com/yourusername/celllcom_ticket_tool.git cellcom-app
cd cellcom-app

# Run setup script
chmod +x deployment/hostpapa-setup.sh
./deployment/hostpapa-setup.sh

# Initialize database
source venv/bin/activate
python3 init_db.py
```

#### Via cPanel File Manager:
1. Upload all files via File Manager or FTP
2. Create virtual environment via Terminal in cPanel
3. Install dependencies
4. Initialize database

### 3. Database Setup

#### Using MySQL (Recommended):
1. cPanel → MySQL Databases
2. Create database: `cellcom_orders`
3. Create user and grant privileges
4. Update `.env`:
   ```env
   SQLALCHEMY_DATABASE_URI=mysql+pymysql://user:password@localhost/cellcom_orders
   ```

#### Using PostgreSQL:
1. Create database via cPanel or command line
2. Update `.env`:
   ```env
   SQLALCHEMY_DATABASE_URI=postgresql://user:password@localhost/cellcom_orders
   ```

### 4. Configure Web Server

#### If using Passenger:
- `.htaccess` in `public/` directory should handle this automatically
- Ensure `PassengerEnabled On` is set

#### If using mod_wsgi:
- May need to configure in Apache config or `.htaccess`
- Contact HostPapa support for mod_wsgi setup

#### If using CGI:
- May need special configuration
- Contact HostPapa support

### 5. Environment Variables

Create `.env` file with:
```env
FLASK_ENV=production
SECRET_KEY=<generate-strong-random-key>
SQLALCHEMY_DATABASE_URI=<your-database-uri>
```

Generate secret key:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 6. File Permissions

```bash
chmod 755 ~/public_html/cellcom-app
chmod 644 ~/public_html/cellcom-app/*.py
chmod 644 ~/public_html/cellcom-app/.htaccess
chmod 755 ~/public_html/cellcom-app/wsgi.py
```

### 7. Test

1. Visit: `https://yourdomain.com`
2. Should see login page
3. Login with: `Anthony` / `cellcom`
4. Change default passwords in production!

## Common HostPapa-Specific Issues

### Python Version
Check available Python version:
```bash
python3 --version
which python3
```

### Virtual Environment Location
HostPapa may require venv in specific location:
```bash
# In your app directory
python3 -m venv venv
```

### Database Connection
- MySQL: Usually `localhost` or `127.0.0.1`
- PostgreSQL: Check HostPapa documentation
- User credentials from cPanel MySQL setup

### Static Files
Ensure static files are accessible:
- `/static/css/styles.css`
- `/static/js/main.js`

## Support

If you need HostPapa-specific help:
- Check HostPapa Knowledge Base
- Contact HostPapa Support (mention Python/Flask hosting)
- HostPapa Community Forums

## Production Security Checklist

- [ ] Changed default admin password
- [ ] Strong SECRET_KEY in .env
- [ ] Database credentials secure
- [ ] HTTPS/SSL enabled
- [ ] File permissions correct
- [ ] Error logging enabled
- [ ] Backups configured

