"""
Order service for business logic
"""
from app import db
from app.models import Order, OrderItem, MenuItem, Payment
from app.utils.errors import NotFoundError, ValidationError
from app.utils.validators import validate_required, validate_positive_number
from datetime import datetime


class OrderService:
    """Service for order operations."""
    
    @staticmethod
    def create_order(data):
        """Create a new order."""
        validate_required(data, ['customer_id', 'restaurant_id', 'items'])
        
        if not data.get('items') or len(data['items']) == 0:
            raise ValidationError('Order must contain at least one item')
        
        # Validate and fetch menu items
        menu_items = {}
        for item_data in data['items']:
            validate_required(item_data, ['menu_item_id', 'quantity'])
            menu_item_id = item_data['menu_item_id']
            quantity = validate_positive_number(item_data['quantity'], 'quantity')
            
            menu_item = MenuItem.query.get(menu_item_id)
            if not menu_item:
                raise NotFoundError(f'Menu item {menu_item_id} not found')
            if not menu_item.available:
                raise ValidationError(f'Menu item {menu_item.name} is not available')
            if menu_item.restaurant_id != data['restaurant_id']:
                raise ValidationError('All items must be from the same restaurant')
            
            menu_items[menu_item_id] = {
                'menu_item': menu_item,
                'quantity': int(quantity)
            }
        
        # Create order
        order = Order(
            customer_id=data['customer_id'],
            restaurant_id=data['restaurant_id'],
            delivery_partner_id=data.get('delivery_partner_id'),
            status=data.get('status', 'placed')
        )
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order items
        total_amount = 0
        for menu_item_id, item_data in menu_items.items():
            menu_item = item_data['menu_item']
            quantity = item_data['quantity']
            price = menu_item.price
            
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=menu_item_id,
                quantity=quantity,
                price=price
            )
            db.session.add(order_item)
            total_amount += float(price) * quantity
        
        order.total_amount = total_amount
        db.session.commit()
        
        return order
    
    @staticmethod
    def update_order_status(order_id, status):
        """Update order status."""
        order = Order.query.get(order_id)
        if not order:
            raise NotFoundError(f'Order {order_id} not found')
        
        valid_statuses = ['placed', 'confirmed', 'preparing', 'dispatched', 'delivered', 'cancelled']
        if status not in valid_statuses:
            raise ValidationError(f'Invalid status. Must be one of: {", ".join(valid_statuses)}')
        
        order.status = status
        db.session.commit()
        return order
    
    @staticmethod
    def assign_delivery_partner(order_id, delivery_partner_id):
        """Assign delivery partner to order."""
        order = Order.query.get(order_id)
        if not order:
            raise NotFoundError(f'Order {order_id} not found')
        
        from app.models import DeliveryPartner
        partner = DeliveryPartner.query.get(delivery_partner_id)
        if not partner:
            raise NotFoundError(f'Delivery partner {delivery_partner_id} not found')
        
        if partner.status != 'available':
            raise ValidationError('Delivery partner is not available')
        
        order.delivery_partner_id = delivery_partner_id
        partner.status = 'busy'
        db.session.commit()
        return order

