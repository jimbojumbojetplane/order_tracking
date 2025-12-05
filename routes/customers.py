from flask import Blueprint, render_template, request
from models import db, Customer, Order
from auth import login_required

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('', methods=['GET'])
@login_required
def list_customers():
    """List all customers with search"""
    search = request.args.get('search', '').strip()
    
    query = Customer.query
    
    if search:
        query = query.filter(
            db.or_(
                Customer.first_name.ilike(f'%{search}%'),
                Customer.last_name.ilike(f'%{search}%'),
                Customer.phone_number.ilike(f'%{search}%'),
                Customer.email.ilike(f'%{search}%')
            )
        )
    
    customers = query.order_by(Customer.last_name, Customer.first_name).all()
    
    return render_template('customers/list.html', customers=customers, search=search)

@customers_bp.route('/<int:customer_id>', methods=['GET'])
@login_required
def customer_detail(customer_id):
    """Show customer details and their orders"""
    customer = Customer.query.get_or_404(customer_id)
    orders = Order.query.filter_by(customer_id=customer_id).order_by(Order.created_at.desc()).all()
    
    return render_template('customers/detail.html', customer=customer, orders=orders)

