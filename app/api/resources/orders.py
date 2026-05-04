"""
Order API Resources
"""
from flask_restful import Resource
from flask import request
from app import db
from app.models import Order
from app.services.order_service import OrderService
from app.utils.errors import NotFoundError


class OrderList(Resource):
    """Resource for listing and creating orders."""
    
    def get(self):
        """Get all orders."""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        customer_id = request.args.get('customer_id', type=int)
        restaurant_id = request.args.get('restaurant_id', type=int)
        status = request.args.get('status')
        include_items = request.args.get('include_items', 'false').lower() == 'true'
        
        query = Order.query
        
        if customer_id:
            query = query.filter_by(customer_id=customer_id)
        
        if restaurant_id:
            query = query.filter_by(restaurant_id=restaurant_id)
        
        if status:
            query = query.filter_by(status=status)
        
        orders = query.order_by(Order.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return {
            'status': 'success',
            'data': [order.to_dict(include_items=include_items) for order in orders.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': orders.total,
                'pages': orders.pages
            }
        }
    
    def post(self):
        """Create a new order."""
        data = request.get_json() or {}
        order = OrderService.create_order(data)
        
        return {
            'status': 'success',
            'message': 'Order created successfully',
            'data': order.to_dict(include_items=True)
        }, 201


class OrderDetail(Resource):
    """Resource for getting a specific order."""
    
    def get(self, order_id):
        """Get a specific order."""
        include_items = request.args.get('include_items', 'true').lower() == 'true'
        order = Order.query.get(order_id)
        if not order:
            raise NotFoundError(f'Order {order_id} not found')
        
        return {
            'status': 'success',
            'data': order.to_dict(
                include_items=include_items,
                include_customer=True,
                include_restaurant=True
            )
        }


class OrderStatusUpdate(Resource):
    """Resource for updating order status."""
    
    def put(self, order_id):
        """Update order status."""
        data = request.get_json() or {}
        status = data.get('status')
        
        if not status:
            return {
                'status': 'error',
                'message': 'Status is required'
            }, 400
        
        order = OrderService.update_order_status(order_id, status)
        
        return {
            'status': 'success',
            'message': 'Order status updated successfully',
            'data': order.to_dict(include_items=True)
        }

