"""
Restaurant Model
"""
from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint


class Restaurant(db.Model):
    """Restaurant model representing food delivery restaurants."""
    __tablename__ = 'restaurants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20))
    cuisine = db.Column(db.String(50), index=True)
    rating = db.Column(db.Numeric(2, 1), CheckConstraint('rating >= 0 AND rating <= 5'))
    
    # Relationships
    menu_items = relationship('MenuItem', back_populates='restaurant', cascade='all, delete-orphan')
    orders = relationship('Order', back_populates='restaurant', cascade='all, delete-orphan')
    
    def to_dict(self, include_menu=False):
        """Convert model to dictionary."""
        data = {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'cuisine': self.cuisine,
            'rating': float(self.rating) if self.rating else None
        }
        if include_menu:
            data['menu_items'] = [item.to_dict() for item in self.menu_items]
        return data
    
    def __repr__(self):
        return f'<Restaurant {self.name}>'

