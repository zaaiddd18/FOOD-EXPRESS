"""
Order Item Model
"""
from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint

class OrderItem(db.Model):
    """Order item model representing items in an order."""
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, CheckConstraint('quantity > 0'), nullable=False)
    price = db.Column(db.Numeric(8, 2), nullable=False)

    # Relationships
    order = relationship('Order', back_populates='order_items')
    menu_item = relationship('MenuItem', back_populates='order_items')

    def to_dict(self, include_menu_item=False):
        """Convert model to dictionary."""
        data = {
            'id': self.id,
            'order_id': self.order_id,
            'menu_item_id': self.menu_item_id,
            'menu_item_name': self.menu_item.name if self.menu_item else None,
            'quantity': self.quantity,
            'price': float(self.price) if self.price else None,
            'subtotal': float(self.price * self.quantity) if self.price else None
        }

        if include_menu_item and self.menu_item:
            data['menu_item'] = self.menu_item.to_dict()

        return data

    def __repr__(self):
        return f'<OrderItem {self.menu_item_id} x{self.quantity}>'