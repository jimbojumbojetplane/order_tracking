from flask import Blueprint, render_template, request
from models import db, Phone
from auth import login_required

phones_bp = Blueprint('phones', __name__)

@phones_bp.route('', methods=['GET'])
@login_required
def list_phones():
    """List all phones with filters"""
    brand_filter = request.args.get('brand', '')
    featured_only = request.args.get('featured', '') == 'on'
    
    query = Phone.query
    
    if brand_filter:
        query = query.filter(Phone.brand == brand_filter)
    
    if featured_only:
        query = query.filter(Phone.is_featured == True)
    
    phones = query.order_by(Phone.brand, Phone.model).all()
    
    # Get unique brands for filter dropdown
    brands = db.session.query(Phone.brand).distinct().order_by(Phone.brand).all()
    brands = [b[0] for b in brands]
    
    return render_template('phones/list.html',
                         phones=phones,
                         brands=brands,
                         current_brand=brand_filter,
                         featured_only=featured_only)

