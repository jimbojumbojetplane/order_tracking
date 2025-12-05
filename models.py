from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default='rep')  # rep, manager, admin
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=True)  # Store assignment
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='user', lazy=True)
    status_changes = db.relationship('OrderStatusHistory', backref='user', lazy=True)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.first_name}>'


class Store(db.Model):
    """Store location model"""
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    street = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(10), nullable=False)  # ON, QC, etc.
    postal_code = db.Column(db.String(10), nullable=True)
    latitude = db.Column(db.Numeric(10, 7), nullable=True)
    longitude = db.Column(db.Numeric(10, 7), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    users = db.relationship('User', backref='store', lazy=True)
    orders = db.relationship('Order', backref='store', lazy=True)
    
    def __repr__(self):
        return f'<Store {self.name}>'
    
    @property
    def full_address(self):
        """Return formatted full address"""
        parts = []
        if self.street:
            parts.append(self.street)
        if self.city:
            parts.append(self.city)
        if self.province:
            parts.append(self.province)
        if self.postal_code:
            parts.append(self.postal_code)
        return ', '.join(parts)
    
    @property
    def display_name(self):
        """Return display name with city"""
        return f"{self.name} - {self.city}, {self.province}"


class Customer(db.Model):
    """Customer model"""
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=True)
    preferred_store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='customer', lazy=True)
    preferred_store_rel = db.relationship('Store', foreign_keys=[preferred_store_id], backref='preferred_customers')
    
    def __repr__(self):
        return f'<Customer {self.first_name} {self.last_name}>'
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Phone(db.Model):
    """Phone/Device model"""
    __tablename__ = 'phones'
    
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    storage = db.Column(db.String(50), nullable=False)  # e.g., "128 GB"
    colour = db.Column(db.String(50), nullable=False)
    bell_sku = db.Column(db.String(100), nullable=False)
    full_price = db.Column(db.Numeric(10, 2), nullable=False)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='phone', lazy=True)
    
    def __repr__(self):
        return f'<Phone {self.brand} {self.model}>'
    
    @property
    def display_name(self):
        return f"{self.brand} {self.model}"


class RatePlan(db.Model):
    """Rate plan model for Bell plans"""
    __tablename__ = 'rate_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    monthly_price = db.Column(db.Numeric(10, 2), nullable=False)
    data_gb = db.Column(db.Integer, nullable=True)  # Can be null for unlimited
    unlimited_canada = db.Column(db.Boolean, default=True)
    unlimited_us = db.Column(db.Boolean, default=False)
    roaming_notes = db.Column(db.Text, nullable=True)
    bell_plan_code = db.Column(db.String(100), nullable=True)
    segment = db.Column(db.String(50), default='consumer')  # consumer or business
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='rate_plan', lazy=True)
    
    def __repr__(self):
        return f'<RatePlan {self.name}>'


class Order(db.Model):
    """Order model"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    phone_id = db.Column(db.Integer, db.ForeignKey('phones.id'), nullable=False)
    rate_plan_id = db.Column(db.Integer, db.ForeignKey('rate_plans.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    store_location = db.Column(db.String(255), nullable=True)  # Keep for backwards compatibility, can be derived from store
    status = db.Column(db.String(50), nullable=False, default='New')
    # Valid statuses: New, Pending Activation, Activated, Cancelled, Returned
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    activation_date = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    # Relationships
    status_history = db.relationship('OrderStatusHistory', backref='order', lazy=True, order_by='OrderStatusHistory.changed_at')
    
    def __repr__(self):
        return f'<Order {self.order_number}>'
    
    def update_status(self, new_status, user_id, comment=None):
        """Update order status and create history entry"""
        old_status = self.status
        self.status = new_status
        self.updated_at = datetime.utcnow()
        
        # Set activation_date if status becomes Activated
        if new_status == 'Activated' and not self.activation_date:
            self.activation_date = datetime.utcnow()
        
        # Create history entry
        history = OrderStatusHistory(
            order_id=self.id,
            old_status=old_status,
            new_status=new_status,
            changed_by_user_id=user_id,
            comment=comment
        )
        db.session.add(history)
        db.session.commit()
        
        return history


class OrderStatusHistory(db.Model):
    """Order status change history"""
    __tablename__ = 'order_status_history'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    old_status = db.Column(db.String(50), nullable=False)
    new_status = db.Column(db.String(50), nullable=False)
    changed_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<OrderStatusHistory {self.old_status} -> {self.new_status}>'

