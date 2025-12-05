from flask import Blueprint, render_template
from models import RatePlan
from auth import login_required

rate_plans_bp = Blueprint('rate_plans', __name__)

@rate_plans_bp.route('', methods=['GET'])
@login_required
def list_rate_plans():
    """List all rate plans"""
    # TODO: Add filtering by segment (consumer/business) if needed
    rate_plans = RatePlan.query.order_by(RatePlan.monthly_price).all()
    return render_template('rate_plans/list.html', rate_plans=rate_plans)

