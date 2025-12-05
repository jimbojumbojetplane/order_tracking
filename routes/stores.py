from flask import Blueprint, render_template, request
from models import db, Store
from auth import login_required

stores_bp = Blueprint('stores', __name__)

@stores_bp.route('', methods=['GET'])
@login_required
def list_stores():
    """List all stores"""
    search = request.args.get('search', '').strip()
    province_filter = request.args.get('province', '')
    
    query = Store.query.filter_by(is_active=True)
    
    if search:
        query = query.filter(
            db.or_(
                Store.name.ilike(f'%{search}%'),
                Store.city.ilike(f'%{search}%'),
                Store.street.ilike(f'%{search}%')
            )
        )
    
    if province_filter:
        query = query.filter(Store.province == province_filter)
    
    stores = query.order_by(Store.province, Store.city, Store.name).all()
    
    # Get unique provinces for filter
    provinces = db.session.query(Store.province).distinct().order_by(Store.province).all()
    provinces = [p[0] for p in provinces if p[0]]
    
    return render_template('stores/list.html', stores=stores, search=search, provinces=provinces, current_province=province_filter)

@stores_bp.route('/<int:store_id>', methods=['GET'])
@login_required
def store_detail(store_id):
    """Show store details"""
    store = Store.query.get_or_404(store_id)
    # Get orders for this store
    from models import Order
    orders = Order.query.filter_by(store_id=store_id).order_by(Order.created_at.desc()).limit(20).all()
    
    return render_template('stores/detail.html', store=store, orders=orders)

