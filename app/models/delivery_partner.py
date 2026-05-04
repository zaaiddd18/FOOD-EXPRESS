"""
Delivery Partner Model
"""
from app import db
from sqlalchemy.orm import relationship


class DeliveryPartner(db.Model):
    """Delivery partner model representing delivery personnel."""
    __tablename__ = 'delivery_partners'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), index=True)
    vehicle_type = db.Column(db.String(50))
    status = db.Column(db.String(20), default='available', nullable=False, index=True)
    
    # Relationships
    orders = relationship('Order', back_populates='delivery_partner')
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'vehicle_type': self.vehicle_type,
            'status': self.status
        }
    
    def __repr__(self):
        return f'<DeliveryPartner {self.name} ({self.status})>'

