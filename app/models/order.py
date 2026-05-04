"""
Order Model
"""
from app import db
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint


class Order(db.Model):
    """Order model representing customer orders."""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='CASCADE'), nullable=False, index=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id', ondelete='CASCADE'), nullable=False, index=True)
    delivery_partner_id = db.Column(db.Integer, db.ForeignKey('delivery_partners.id', ondelete='SET NULL'), index=True)
    status = db.Column(db.String(20), default='placed', nullable=False, index=True)
    total_amount = db.Column(db.Numeric(10, 2))
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    
    # Relationships
    customer = relationship('Customer', back_populates='orders')
    restaurant = relationship('Restaurant', back_populates='orders')
    delivery_partner = relationship('DeliveryPartner', back_populates='orders')
    order_items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    payment = relationship('Payment', back_populates='order', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self, include_items=False, include_customer=False, include_restaurant=False):
        """Convert model to dictionary."""
        data = {
            'id': self.id,
            'customer_id': self.customer_id,
            'restaurant_id': self.restaurant_id,
            'delivery_partner_id': self.delivery_partner_id,
            'status': self.status,
            'total_amount': float(self.total_amount) if self.total_amount else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_items:
            data['order_items'] = [item.to_dict() for item in self.order_items]
        
        if include_customer and self.customer:
            data['customer'] = self.customer.to_dict()
        
        if include_restaurant and self.restaurant:
            data['restaurant'] = self.restaurant.to_dict()
        
        if self.delivery_partner:
            data['delivery_partner'] = self.delivery_partner.to_dict()
        
        if self.payment:
            data['payment'] = self.payment.to_dict()
        
        return data
    
    def calculate_total(self):
        """Calculate total amount from order items."""
        total = sum(item.price * item.quantity for item in self.order_items)
        self.total_amount = total
        return total
    
    def __repr__(self):
        return f'<Order {self.id} - {self.status}>'

