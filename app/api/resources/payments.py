"""
Payment API Resources
"""
from flask_restful import Resource
from flask import request
from app import db
from app.models import Payment, Order
from app.utils.errors import NotFoundError, ValidationError, ConflictError
from app.utils.validators import validate_required, validate_positive_number
from datetime import datetime


class PaymentList(Resource):
    """Resource for listing and creating payments."""
    
    def get(self):
        """Get all payments."""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        order_id = request.args.get('order_id', type=int)
        status = request.args.get('status')
        
        query = Payment.query
        
        if order_id:
            query = query.filter_by(order_id=order_id)
        
        if status:
            query = query.filter_by(status=status)
        
        payments = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return {
            'status': 'success',
            'data': [payment.to_dict() for payment in payments.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': payments.total,
                'pages': payments.pages
            }
        }
    
    def post(self):
        """Create a new payment."""
        data = request.get_json() or {}
        
        validate_required(data, ['order_id', 'amount', 'method'])
        
        # Verify order exists
        order = Order.query.get(data['order_id'])
        if not order:
            raise NotFoundError(f'Order {data["order_id"]} not found')
        
        # Check if payment already exists for this order
        existing_payment = Payment.query.filter_by(order_id=data['order_id']).first()
        if existing_payment:
            raise ConflictError('Payment already exists for this order')
        
        amount = validate_positive_number(data['amount'], 'amount')
        
        valid_methods = ['card', 'upi', 'cash', 'wallet']
        if data['method'] not in valid_methods:
            raise ValidationError(f'Payment method must be one of: {", ".join(valid_methods)}')
        
        payment = Payment(
            order_id=data['order_id'],
            amount=amount,
            method=data['method'],
            status=data.get('status', 'pending')
        )
        
        # If status is success, set paid_at
        if payment.status == 'success':
            payment.paid_at = datetime.utcnow()
        
        db.session.add(payment)
        db.session.commit()
        
        return {
            'status': 'success',
            'message': 'Payment created successfully',
            'data': payment.to_dict()
        }, 201


class PaymentDetail(Resource):
    """Resource for getting and updating a specific payment."""
    
    def get(self, payment_id):
        """Get a specific payment."""
        payment = Payment.query.get(payment_id)
        if not payment:
            raise NotFoundError(f'Payment {payment_id} not found')
        
        return {
            'status': 'success',
            'data': payment.to_dict()
        }
    
    def put(self, payment_id):
        """Update payment status."""
        payment = Payment.query.get(payment_id)
        if not payment:
            raise NotFoundError(f'Payment {payment_id} not found')
        
        data = request.get_json() or {}
        
        if 'status' in data:
            valid_statuses = ['pending', 'success', 'failed']
            if data['status'] not in valid_statuses:
                raise ValidationError(f'Status must be one of: {", ".join(valid_statuses)}')
            
            payment.status = data['status']
            
            # Update paid_at if status changes to success
            if payment.status == 'success' and not payment.paid_at:
                payment.paid_at = datetime.utcnow()
            elif payment.status != 'success':
                payment.paid_at = None
        
        if 'method' in data:
            valid_methods = ['card', 'upi', 'cash', 'wallet']
            if data['method'] not in valid_methods:
                raise ValidationError(f'Payment method must be one of: {", ".join(valid_methods)}')
            payment.method = data['method']
        
        if 'amount' in data:
            payment.amount = validate_positive_number(data['amount'], 'amount')
        
        db.session.commit()
        
        return {
            'status': 'success',
            'message': 'Payment updated successfully',
            'data': payment.to_dict()
        }

