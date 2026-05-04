"""
Restaurant API Resources
"""
from flask_restful import Resource
from flask import request
from app import db
from app.models import Restaurant
from app.utils.errors import NotFoundError, ValidationError
from app.utils.validators import validate_required, validate_positive_number


class RestaurantList(Resource):
    """Resource for listing and creating restaurants."""
    
    def get(self):
        """Get all restaurants."""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        cuisine = request.args.get('cuisine')
        include_menu = request.args.get('include_menu', 'false').lower() == 'true'
        
        query = Restaurant.query
        
        if cuisine:
            query = query.filter_by(cuisine=cuisine)
        
        restaurants = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return {
            'status': 'success',
            'data': [r.to_dict(include_menu=include_menu) for r in restaurants.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': restaurants.total,
                'pages': restaurants.pages
            }
        }
    
    def post(self):
        """Create a new restaurant."""
        data = request.get_json() or {}
        
        validate_required(data, ['name', 'address'])
        
        if 'rating' in data and data['rating']:
            rating = validate_positive_number(data['rating'], 'rating')
            if rating > 5:
                raise ValidationError('Rating cannot exceed 5')
        
        restaurant = Restaurant(
            name=data['name'],
            address=data['address'],
            phone=data.get('phone'),
            cuisine=data.get('cuisine'),
            rating=data.get('rating')
        )
        
        db.session.add(restaurant)
        db.session.commit()
        
        return {
            'status': 'success',
            'message': 'Restaurant created successfully',
            'data': restaurant.to_dict()
        }, 201


class RestaurantDetail(Resource):
    """Resource for getting, updating, and deleting a specific restaurant."""
    
    def get(self, restaurant_id):
        """Get a specific restaurant."""
        include_menu = request.args.get('include_menu', 'false').lower() == 'true'
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            raise NotFoundError(f'Restaurant {restaurant_id} not found')
        
        return {
            'status': 'success',
            'data': restaurant.to_dict(include_menu=include_menu)
        }
    
    def put(self, restaurant_id):
        """Update a restaurant."""
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            raise NotFoundError(f'Restaurant {restaurant_id} not found')
        
        data = request.get_json() or {}
        
        if 'name' in data:
            restaurant.name = data['name']
        
        if 'address' in data:
            restaurant.address = data['address']
        
        if 'phone' in data:
            restaurant.phone = data['phone']
        
        if 'cuisine' in data:
            restaurant.cuisine = data['cuisine']
        
        if 'rating' in data:
            if data['rating']:
                rating = validate_positive_number(data['rating'], 'rating')
                if rating > 5:
                    raise ValidationError('Rating cannot exceed 5')
                restaurant.rating = rating
            else:
                restaurant.rating = None
        
        db.session.commit()
        
        return {
            'status': 'success',
            'message': 'Restaurant updated successfully',
            'data': restaurant.to_dict()
        }
    
    def delete(self, restaurant_id):
        """Delete a restaurant."""
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            raise NotFoundError(f'Restaurant {restaurant_id} not found')
        
        db.session.delete(restaurant)
        db.session.commit()
        
        return {
            'status': 'success',
            'message': 'Restaurant deleted successfully'
        }, 200

