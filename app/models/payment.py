"""
Payment Model
"""
from app import db
from sqlalchemy.orm import relationship


class Payment(db.Model):
    """Payment model representing order payments."""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False, unique=True, index=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    method = db.Column(db.String(20), nullable=False, index=True)
    status = db.Column(db.String(20), default='pending', nullable=False, index=True)
    paid_at = db.Column(db.TIMESTAMP)
    
    # Relationships
    order = relationship('Order', back_populates='payment')
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'amount': float(self.amount) if self.amount else None,
            'method': self.method,
            'status': self.status,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None
        }
    
    def __repr__(self):
        return f'<Payment {self.id} - {self.status}>'

