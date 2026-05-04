"""
Customer Model
"""
from app import db
from datetime import datetime
from sqlalchemy.orm import relationship


class Customer(db.Model):
    """Customer model representing food delivery customers."""
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), index=True)
    address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    
    # Relationships
    orders = relationship('Order', back_populates='customer', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Customer {self.name} ({self.email})>'

