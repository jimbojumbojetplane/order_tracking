# Railway Deployment Guide

Railway is an excellent choice for deploying Flask applications. It's simple, supports Python automatically, and offers PostgreSQL databases.

## Why Railway for Flask?

✅ **Automatic Python Detection** - Railway detects Python apps automatically  
✅ **PostgreSQL Database** - Built-in database support (free tier available)  
✅ **GitHub Integration** - Auto-deploy on every push  
✅ **Free Tier Available** - $5/month credit (enough for small apps)  
✅ **No Configuration Needed** - Works out of the box  
✅ **SSL/HTTPS Included** - Free SSL certificates  
✅ **Environment Variables** - Easy configuration  

## Quick Deployment Steps

### 1. Prepare Your Code

✅ Your code is already pushed to GitHub: `https://github.com/jimbojumbojetplane/order_tracking`

The repository already includes:
- `Procfile` - Tells Railway how to run your app
- `runtime.txt` - Specifies Python version
- `requirements.txt` - Python dependencies
- `wsgi.py` - WSGI entry point (updated for Railway)

### 2. Sign Up for Railway

1. Go to: **https://railway.app/**
2. Click **"Start a New Project"**
3. Sign up with GitHub (recommended - easiest integration)
4. Authorize Railway to access your GitHub repositories

### 3. Deploy from GitHub

1. In Railway dashboard, click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Find and select: `jimbojumbojetplane/order_tracking`
4. Railway will automatically:
   - Detect it's a Python app
   - Install dependencies from `requirements.txt`
   - Start the application using the `Procfile`

### 4. Set Up PostgreSQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway will create a PostgreSQL database
4. Copy the database URL from the **Variables** tab

### 5. Configure Environment Variables

In Railway project → **Variables** tab, add:

```env
FLASK_ENV=production
SECRET_KEY=<generate-a-strong-random-key>
SQLALCHEMY_DATABASE_URI=${{Postgres.DATABASE_URL}}
```

**To generate a secret key:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

**Note:** Railway automatically provides `DATABASE_URL` as an environment variable. The format is:
```
postgresql://user:password@host:port/database
```

### 6. Initialize Database

#### Option A: Using Railway CLI (Recommended)

1. Install Railway CLI:
   ```bash
   npm i -g @railway/cli
   ```

2. Login to Railway:
   ```bash
   railway login
   ```

3. Link to your project:
   ```bash
   railway link
   ```

4. Run database initialization:
   ```bash
   railway run python3 init_db.py
   ```

#### Option B: Using Railway Shell

1. In Railway dashboard, open your service
2. Click **"Deployments"** → Latest deployment
3. Click **"View Logs"** → **"Shell"**
4. Run:
   ```bash
   python3 init_db.py
   ```

### 7. Access Your Application

Railway automatically provides a URL like:
- `https://your-app-name.up.railway.app`

Your app should now be live! 🎉

## Railway-Specific Configuration

### Port Configuration

Railway automatically sets the `PORT` environment variable. The `Procfile` uses this:

```
web: gunicorn wsgi:application --bind 0.0.0.0:$PORT
```

### Database Connection

Railway provides `DATABASE_URL` automatically. Your `config.py` reads from `SQLALCHEMY_DATABASE_URI` environment variable.

**Important:** Update your `config.py` to handle Railway's `DATABASE_URL`:

```python
# In config.py, you can add:
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Railway provides postgres:// but SQLAlchemy needs postgresql://
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
```

Actually, this is already handled in your current config if you set:
```env
SQLALCHEMY_DATABASE_URI=${{Postgres.DATABASE_URL}}
```

### Static Files

Railway serves static files through Flask automatically. No additional configuration needed.

## Updating Your Application

Railway automatically redeploys when you push to GitHub:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Railway will:
1. Detect the push
2. Build your application
3. Run tests (if configured)
4. Deploy automatically

## Monitoring & Logs

- **View Logs**: Railway dashboard → Your service → **"View Logs"**
- **Metrics**: Railway dashboard → **"Metrics"** tab
- **Deployments**: Railway dashboard → **"Deployments"** tab

## Custom Domain (Optional)

1. In Railway project → **Settings** → **Networking**
2. Click **"Custom Domain"**
3. Add your domain
4. Follow DNS configuration instructions

## Pricing

- **Free Tier**: $5/month credit
- **Hobby Plan**: $5/month (after free credits)
- **Pro Plan**: $20/month

For your Flask app, the free tier should be sufficient for initial testing.

## Troubleshooting

### Application Won't Start

1. Check logs in Railway dashboard
2. Verify `Procfile` is correct
3. Ensure `requirements.txt` includes all dependencies
4. Check environment variables are set correctly

### Database Connection Issues

1. Verify `DATABASE_URL` is set in Variables
2. Check database is running (Railway dashboard)
3. Ensure database is initialized: `railway run python3 init_db.py`

### Static Files Not Loading

Railway serves static files through Flask. Ensure:
- `static/` directory exists
- Routes are configured correctly
- No hardcoded localhost URLs

## Useful Railway Commands

```bash
# Login to Railway
railway login

# Link to project
railway link

# View logs
railway logs

# Run commands
railway run python3 init_db.py

# Open shell
railway shell
```

## Next Steps

1. ✅ Deploy to Railway
2. ✅ Set up PostgreSQL database
3. ✅ Configure environment variables
4. ✅ Initialize database
5. ✅ Test your application
6. ✅ Share the URL with your team!

## Support

- Railway Docs: https://docs.railway.app/
- Railway Discord: https://discord.gg/railway
- Railway Status: https://status.railway.app/

