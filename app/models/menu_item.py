"""
Menu Item Model
"""
from app import db
from sqlalchemy.orm import relationship


class MenuItem(db.Model):
    """Menu item model representing restaurant menu items."""
    __tablename__ = 'menu_items'
    
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id', ondelete='CASCADE'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(8, 2), nullable=False)
    available = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships
    restaurant = relationship('Restaurant', back_populates='menu_items')
    order_items = relationship('OrderItem', back_populates='menu_item', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'restaurant_id': self.restaurant_id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price) if self.price else None,
            'available': self.available
        }
    
    def __repr__(self):
        return f'<MenuItem {self.name} (${self.price})>'

