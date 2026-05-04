"""
Delivery Partner API Resources
"""
from flask_restful import Resource
from flask import request
from app import db
from app.models import DeliveryPartner
from app.utils.errors import NotFoundError, ValidationError
from app.utils.validators import validate_required


class DeliveryPartnerList(Resource):
    """Resource for listing and creating delivery partners."""
    
    def get(self):
        """Get all delivery partners."""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        
        query = DeliveryPartner.query
        
        if status:
            query = query.filter_by(status=status)
        
        partners = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return {
            'status': 'success',
            'data': [partner.to_dict() for partner in partners.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': partners.total,
                'pages': partners.pages
            }
        }
    
    def post(self):
        """Create a new delivery partner."""
        data = request.get_json() or {}
        
        validate_required(data, ['name'])
        
        partner = DeliveryPartner(
            name=data['name'],
            phone=data.get('phone'),
            vehicle_type=data.get('vehicle_type'),
            status=data.get('status', 'available')
        )
        
        db.session.add(partner)
        db.session.commit()
        
        return {
            'status': 'success',
            'message': 'Delivery partner created successfully',
            'data': partner.to_dict()
        }, 201


class DeliveryPartnerDetail(Resource):
    """Resource for getting, updating, and deleting a specific delivery partner."""
    
    def get(self, partner_id):
        """Get a specific delivery partner."""
        partner = DeliveryPartner.query.get(partner_id)
        if not partner:
            raise NotFoundError(f'Delivery partner {partner_id} not found')
        
        return {
            'status': 'success',
            'data': partner.to_dict()
        }
    
    def put(self, partner_id):
        """Update a delivery partner."""
        partner = DeliveryPartner.query.get(partner_id)
        if not partner:
            raise NotFoundError(f'Delivery partner {partner_id} not found')
        
        data = request.get_json() or {}
        
        if 'name' in data:
            partner.name = data['name']
        
        if 'phone' in data:
            partner.phone = data['phone']
        
        if 'vehicle_type' in data:
            partner.vehicle_type = data['vehicle_type']
        
        if 'status' in data:
            valid_statuses = ['available', 'busy', 'offline']
            if data['status'] not in valid_statuses:
                raise ValidationError(f'Status must be one of: {", ".join(valid_statuses)}')
            partner.status = data['status']
        
        db.session.commit()
        
        return {
            'status': 'success',
            'message': 'Delivery partner updated successfully',
            'data': partner.to_dict()
        }
    
    def delete(self, partner_id):
        """Delete a delivery partner."""
        partner = DeliveryPartner.query.get(partner_id)
        if not partner:
            raise NotFoundError(f'Delivery partner {partner_id} not found')
        
        db.session.delete(partner)
        db.session.commit()
        
        return {
            'status': 'success',
            'message': 'Delivery partner deleted successfully'
        }, 200

