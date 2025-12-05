# Cellcom Order Tracker

An internal web application for tracking mobile phone orders, managing customers, devices, and rate plans across Cellcom store locations.

## Overview

Cellcom Order Tracker is a Flask-based web application designed to help store representatives and managers track mobile phone orders from creation through activation. The system provides:

- Multi-user authentication with role-based access
- Order lifecycle management (New → Pending Activation → Activated → Cancelled/Returned)
- Customer relationship management
- Device catalog (20+ Bell mobile devices)
- Bell rate plan reference
- Order status history and timeline
- Professional UI with Cellcom-inspired branding

## Tech Stack

- **Backend**: Python 3, Flask, SQLAlchemy
- **Frontend**: Jinja2 templates, vanilla JavaScript, custom CSS
- **Database**: SQLite (development), MySQL/PostgreSQL (production)
- **Authentication**: Flask sessions with bcrypt password hashing
- **Deployment**: Gunicorn WSGI server, Nginx reverse proxy

## Project Structure

```
cellcom-order-tracker/
├── app.py                  # Flask app factory / main entry
├── config.py               # Configuration classes
├── models.py               # SQLAlchemy models
├── auth.py                 # Authentication decorators
├── routes/                 # Route blueprints
│   ├── __init__.py
│   ├── auth.py
│   ├── orders.py
│   ├── customers.py
│   ├── phones.py
│   ├── rate_plans.py
│   └── about.py
├── templates/              # Jinja2 templates
│   ├── base.html
│   ├── login.html
│   ├── orders/
│   ├── customers/
│   ├── phones/
│   ├── rate_plans/
│   └── about.html
├── static/                 # Static assets
│   ├── css/styles.css
│   ├── js/main.js
│   └── img/
├── seed/                   # Database seed scripts
│   ├── seed_users.py
│   ├── seed_customers.py
│   ├── seed_phones.py
│   ├── seed_rate_plans.py
│   └── seed_orders.py
├── deployment/             # Deployment configs
│   ├── gunicorn.service.example
│   └── nginx.conf.example
├── requirements.txt
├── .env.example
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool (venv or virtualenv)

### Local Development Setup

1. **Clone or navigate to the project directory**
   ```bash
   cd cellcom-order-tracker
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create `.env` file**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set appropriate values:
   ```env
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-change-this-in-production
   SQLALCHEMY_DATABASE_URI=sqlite:///cellcom_orders.db
   ADMIN_DEFAULT_PASSWORD=cellcom
   ```

6. **Initialize the database**
   The database will be created automatically when you first run the app. Tables are created via `db.create_all()` in `app.py`.

7. **Seed the database**
   Run the seed scripts in order:
   ```bash
   python seed/seed_users.py
   python seed/seed_customers.py
   python seed/seed_phones.py
   python seed/seed_rate_plans.py
   python seed/seed_orders.py
   ```

8. **Run the application**
   ```bash
   flask run
   ```
   
   Or directly:
   ```bash
   python app.py
   ```

9. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

## Demo Accounts

The following demo accounts are seeded:

- **Anthony** (Rep) - Password: `cellcom`
- **Dominic** (Rep) - Password: `cellcom`
- **Rene** (Manager) - Password: `cellcom`
- **Admin** (Admin) - Password: `cellcom`

## Usage

### Logging In

1. Navigate to the login page
2. Enter your first name and password
3. You'll be redirected to the Orders dashboard

### Main Features

#### Orders Dashboard
- View all orders with filtering by status, owner, or store
- Click on an order number to view details
- Create new orders from the "New Order" button

#### Order Details
- View complete order information
- Update order status with comments
- View status history timeline

#### Customers
- Browse and search customers
- View customer details and their order history

#### Phone Catalog
- Browse available devices
- Filter by brand or featured status

#### Rate Plans
- View Bell rate plan reference catalog
- See pricing, data allowances, and features

#### About Page
- View system architecture diagram
- Read current features and roadmap

## Production Deployment (HostPapa VPS)

### Database Configuration

For production, switch from SQLite to MySQL or PostgreSQL:

1. **Update `.env` file:**
   ```env
   SQLALCHEMY_DATABASE_URI=mysql+pymysql://user:password@localhost/cellcom_orders
   # OR for PostgreSQL:
   # SQLALCHEMY_DATABASE_URI=postgresql://user:password@localhost/cellcom_orders
   ```

2. **Install database driver:**
   - For MySQL: Add `pymysql` or `mysqlclient` to `requirements.txt`
   - For PostgreSQL: Add `psycopg2-binary` to `requirements.txt`

3. **Create database:**
   ```sql
   CREATE DATABASE cellcom_orders;
   ```

4. **Run migrations/seed:**
   - The tables will be created on first run
   - Run seed scripts as in development setup

### Gunicorn Setup

1. **Create systemd service file:**
   ```bash
   sudo cp deployment/gunicorn.service.example /etc/systemd/system/cellcom-order-tracker.service
   sudo nano /etc/systemd/system/cellcom-order-tracker.service
   ```
   
   Update paths and user as needed.

2. **Start and enable service:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start cellcom-order-tracker
   sudo systemctl enable cellcom-order-tracker
   ```

### Nginx Configuration

1. **Copy nginx config:**
   ```bash
   sudo cp deployment/nginx.conf.example /etc/nginx/sites-available/cellcom-order-tracker
   sudo ln -s /etc/nginx/sites-available/cellcom-order-tracker /etc/nginx/sites-enabled/
   ```

2. **Update configuration:**
   - Update `server_name` with your domain
   - Adjust paths as needed
   - Configure SSL certificates if using HTTPS

3. **Test and reload nginx:**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

### Environment Variables

Ensure your production `.env` file has:
- Strong `SECRET_KEY`
- Production database URI
- `FLASK_ENV=production`

## Updating Rate Plans

### Using Real Bell Rate Plan Data

The project includes a script to parse Bell rate plan data from the extraction pipeline:

1. **Parse Bell JSON data** (if you have updated rate plan data):
   ```bash
   python3 seed/parse_bell_plans.py
   ```
   
   This script reads from `/Users/jgf/coding/rate_plan_pricing_extractor_v2/data/bell/output/bell_llm_output_all_plans_*.json` 
   and generates `seed/rate_plans.json` with the proper format.

2. **Seed the database** with the parsed plans:
   ```bash
   python3 seed/seed_rate_plans.py
   ```

The seed script automatically uses `seed/rate_plans.json` if it exists, otherwise falls back to placeholder plans.

### Manual Rate Plan Updates

You can also manually create/update `seed/rate_plans.json` with the following structure:
```json
[
  {
    "name": "Lite",
    "monthly_price": 70.00,
    "data_gb": 60,
    "unlimited_canada": true,
    "unlimited_us": false,
    "roaming_notes": "Unlimited Canada-wide calling | Unlimited Canada texting",
    "bell_plan_code": "LITE",
    "segment": "consumer"
  }
]
```

Then re-run the seed script:
```bash
python3 seed/seed_rate_plans.py
```

**Note:** The current `seed/rate_plans.json` contains 8 Bell plans extracted from the latest rate plan data:
- Lite ($70/mo - 60 GB)
- Select ($75/mo - 100 GB)
- Max ($85/mo - 200 GB)
- Ultra ($105/mo - 250 GB)
- Plus 2-line variants of each

## Development Notes

- The app uses Flask's built-in session management for authentication
- Passwords are hashed using Werkzeug's password hashing
- Order numbers are auto-generated in format: `CEL-YYYY-XXXX`
- Status changes are automatically tracked in `order_status_history`
- The database schema supports easy migration to MySQL/PostgreSQL

## Troubleshooting

### Database Issues
- Ensure SQLite file permissions if using SQLite in production
- Check database connection string format for MySQL/PostgreSQL
- Verify database user has proper permissions

### Import Errors
- Ensure virtual environment is activated
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python path and project structure

### Port Already in Use
- Change Flask port: `flask run --port 5001`
- Or stop the process using port 5000

## License

Internal use only - Cellcom Order Tracker

## Support

For issues or questions, contact the development team.

