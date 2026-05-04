"""
Customer API Resources
"""
from flask_restful import Resource
from flask import request
from app import db
from app.models import Customer
from app.utils.errors import NotFoundError, ValidationError, ConflictError
from app.utils.validators import validate_email, validate_phone, validate_required


class CustomerList(Resource):
    """Resource for listing and creating customers."""
    
    def get(self):
        """Get all customers."""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        customers = Customer.query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return {
            'status': 'success',
            'data': [customer.to_dict() for customer in customers.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': customers.total,
                'pages': customers.pages
            }
        }
    
    def post(self):
        """Create a new customer."""
        data = request.get_json() or {}
        
        validate_required(data, ['name', 'email', 'address'])
        validate_email(data['email'])
        
        if data.get('phone'):
            validate_phone(data['phone'])
        
        # Check if email already exists
        if Customer.query.filter_by(email=data['email']).first():
            raise ConflictError('Customer with this email already exists')
        
        customer = Customer(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone'),
            address=data['address']
        )
        
        db.session.add(customer)
        db.session.commit()
        
        return {
            'status': 'success',
            'message': 'Customer created successfully',
            'data': customer.to_dict()
        }, 201


class CustomerDetail(Resource):
    """Resource for getting, updating, and deleting a specific customer."""
    
    def get(self, customer_id):
        """Get a specific customer."""
        customer = Customer.query.get(customer_id)
        if not customer:
            raise NotFoundError(f'Customer {customer_id} not found')
        
        return {
            'status': 'success',
            'data': customer.to_dict()
        }
    
    def put(self, customer_id):
        """Update a customer."""
        customer = Customer.query.get(customer_id)
        if not customer:
            raise NotFoundError(f'Customer {customer_id} not found')
        
        data = request.get_json() or {}
        
        if 'email' in data:
            validate_email(data['email'])
            # Check if email is already taken by another customer
            existing = Customer.query.filter_by(email=data['email']).first()
            if existing and existing.id != customer_id:
                raise ConflictError('Email already in use')
            customer.email = data['email']
        
        if 'phone' in data and data['phone']:
            validate_phone(data['phone'])
            customer.phone = data['phone']
        
        if 'name' in data:
            customer.name = data['name']
        
        if 'address' in data:
            customer.address = data['address']
        
        db.session.commit()
        
        return {
            'status': 'success',
            'message': 'Customer updated successfully',
            'data': customer.to_dict()
        }
    
    def delete(self, customer_id):
        """Delete a customer."""
        customer = Customer.query.get(customer_id)
        if not customer:
            raise NotFoundError(f'Customer {customer_id} not found')
        
        db.session.delete(customer)
        db.session.commit()
        
        return {
            'status': 'success',
            'message': 'Customer deleted successfully'
        }, 200

