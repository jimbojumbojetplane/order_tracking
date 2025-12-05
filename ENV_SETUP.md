# Environment Variables Setup

Create a `.env` file in the project root with the following variables:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-this-in-production
SQLALCHEMY_DATABASE_URI=sqlite:///cellcom_orders.db
ADMIN_DEFAULT_PASSWORD=cellcom
```

## For Production (MySQL/PostgreSQL):

```env
FLASK_ENV=production
SECRET_KEY=your-very-secure-secret-key-here
SQLALCHEMY_DATABASE_URI=mysql+pymysql://user:password@localhost/cellcom_orders
# OR for PostgreSQL:
# SQLALCHEMY_DATABASE_URI=postgresql://user:password@localhost/cellcom_orders
ADMIN_DEFAULT_PASSWORD=cellcom
```

Note: Make sure to install the appropriate database driver:
- For MySQL: `pip install pymysql` or `pip install mysqlclient`
- For PostgreSQL: `pip install psycopg2-binary`

Add these to `requirements.txt` for production deployments.

