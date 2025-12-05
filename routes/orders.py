from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from models import db, Order, Customer, Phone, RatePlan, User, Store
from auth import login_required
from datetime import datetime

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('', methods=['GET'])
@login_required
def list_orders():
    """List all orders with filters"""
    # Get filter parameters
    status_filter = request.args.get('status', '')
    owner_filter = request.args.get('owner', '')
    store_filter = request.args.get('store', '')
    
    # Build query
    query = Order.query
    
    if status_filter:
        query = query.filter(Order.status == status_filter)
    
    if owner_filter:
        query = query.filter(Order.user_id == int(owner_filter))
    
    if store_filter:
        # Filter by store_id if numeric, otherwise search by store name/location
        try:
            store_id = int(store_filter)
            query = query.filter(Order.store_id == store_id)
        except ValueError:
            # Legacy: search by store_location string
            query = query.filter(Order.store_location.ilike(f'%{store_filter}%'))
    
    # Order by created date (newest first)
    orders = query.order_by(Order.created_at.desc()).all()
    
    # Get all users for owner filter dropdown
    users = User.query.all()
    
    # Get all stores for store filter dropdown
    stores = Store.query.filter_by(is_active=True).order_by(Store.city, Store.name).all()
    
    # Get unique statuses for filter dropdown
    statuses = db.session.query(Order.status).distinct().all()
    statuses = [s[0] for s in statuses]
    
    return render_template('orders/list.html', 
                         orders=orders,
                         users=users,
                         stores=stores,
                         statuses=statuses,
                         current_status=status_filter,
                         current_owner=owner_filter,
                         current_store=store_filter)

@orders_bp.route('/<int:order_id>', methods=['GET'])
@login_required
def order_detail(order_id):
    """Show order details"""
    order = Order.query.get_or_404(order_id)
    # Sort status history by most recent first (already ordered in relationship, but ensure desc)
    if order.status_history:
        order.status_history = sorted(order.status_history, key=lambda x: x.changed_at, reverse=True)
    return render_template('orders/detail.html', order=order)

@orders_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_order():
    """Create a new order"""
    if request.method == 'POST':
        try:
            # Generate order number (CEL-YYYY-XXXX)
            year = datetime.now().year
            last_order = Order.query.order_by(Order.id.desc()).first()
            if last_order and last_order.order_number:
                try:
                    last_num = int(last_order.order_number.split('-')[-1])
                    next_num = last_num + 1
                except (ValueError, IndexError):
                    next_num = 1
            else:
                next_num = 1
            
            order_number = f"CEL-{year}-{next_num:04d}"
            
            # Get store and set store_location from store data
            store_id = int(request.form['store_id'])
            store = Store.query.get(store_id)
            if not store:
                flash('Invalid store selected.', 'error')
                return redirect(url_for('orders.new_order'))
            
            # Create order
            order = Order(
                order_number=order_number,
                customer_id=int(request.form['customer_id']),
                user_id=session['user_id'],
                phone_id=int(request.form['phone_id']),
                rate_plan_id=int(request.form['rate_plan_id']),
                store_id=store_id,
                store_location=store.display_name,  # Store display name for legacy compatibility
                status='New',
                notes=request.form.get('notes', '')
            )
            
            db.session.add(order)
            db.session.flush()  # Get order ID
            
            # Create initial status history entry
            from models import OrderStatusHistory
            history = OrderStatusHistory(
                order_id=order.id,
                old_status='',
                new_status='New',
                changed_by_user_id=session['user_id'],
                comment='Order created'
            )
            db.session.add(history)
            db.session.commit()
            
            flash(f'Order {order_number} created successfully!', 'success')
            return redirect(url_for('orders.order_detail', order_id=order.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating order: {str(e)}', 'error')
    
    # GET request - show form
    customers = Customer.query.order_by(Customer.last_name, Customer.first_name).all()
    # Order phones by brand, then model, with featured first
    phones = Phone.query.order_by(Phone.brand, Phone.is_featured.desc(), Phone.model).all()
    # Order rate plans by price (lowest first)
    rate_plans = RatePlan.query.order_by(RatePlan.monthly_price).all()
    # Get all active stores, ordered by city and name
    stores = Store.query.filter_by(is_active=True).order_by(Store.city, Store.name).all()
    
    # If user has a default store, select it
    current_user = User.query.get(session['user_id'])
    default_store_id = current_user.store_id if current_user and current_user.store_id else None
    
    return render_template('orders/new.html',
                         customers=customers,
                         phones=phones,
                         rate_plans=rate_plans,
                         stores=stores,
                         default_store_id=default_store_id)

@orders_bp.route('/<int:order_id>/status', methods=['POST'])
@login_required
def update_status(order_id):
    """Update order status"""
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    comment = request.form.get('comment', '')
    
    if not new_status:
        flash('Status is required.', 'error')
        return redirect(url_for('orders.order_detail', order_id=order_id))
    
    valid_statuses = ['New', 'Pending Activation', 'Activated', 'Cancelled', 'Returned']
    if new_status not in valid_statuses:
        flash(f'Invalid status. Must be one of: {", ".join(valid_statuses)}', 'error')
        return redirect(url_for('orders.order_detail', order_id=order_id))
    
    try:
        order.update_status(new_status, session['user_id'], comment)
        flash(f'Order status updated to {new_status}.', 'success')
    except Exception as e:
        flash(f'Error updating status: {str(e)}', 'error')
    
    return redirect(url_for('orders.order_detail', order_id=order_id))

