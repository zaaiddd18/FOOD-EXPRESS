"""
Menu Item API Resources
"""
from flask_restful import Resource
from flask import request
from app import db
from app.models import MenuItem, Restaurant
from app.utils.errors import NotFoundError, ValidationError
from app.utils.validators import validate_required, validate_positive_number


class MenuItemList(Resource):
    """Resource for listing and creating menu items."""
    
    def get(self):
        """Get all menu items."""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        restaurant_id = request.args.get('restaurant_id', type=int)
        available_only = request.args.get('available_only', 'false').lower() == 'true'
        
        query = MenuItem.query
        
        if restaurant_id:
            query = query.filter_by(restaurant_id=restaurant_id)
        
        if available_only:
            query = query.filter_by(available=True)
        
        menu_items = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return {
            'status': 'success',
            'data': [item.to_dict() for item in menu_items.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': menu_items.total,
                'pages': menu_items.pages
            }
        }
    
    def post(self):
        """Create a new menu item."""
        data = request.get_json() or {}
        
        validate_required(data, ['restaurant_id', 'name', 'price'])
        
        # Verify restaurant exists
        restaurant = Restaurant.query.get(data['restaurant_id'])
        if not restaurant:
            raise NotFoundError(f'Restaurant {data["restaurant_id"]} not found')
        
        price = validate_positive_number(data['price'], 'price')
        
        menu_item = MenuItem(
            restaurant_id=data['restaurant_id'],
            name=data['name'],
            description=data.get('description'),
            price=price,
            available=data.get('available', True)
        )
        
        db.session.add(menu_item)
        db.session.commit()
        
        return {
            'status': 'success',
            'message': 'Menu item created successfully',
            'data': menu_item.to_dict()
        }, 201


class MenuItemDetail(Resource):
    """Resource for getting, updating, and deleting a specific menu item."""
    
    def get(self, menu_item_id):
        """Get a specific menu item."""
        menu_item = MenuItem.query.get(menu_item_id)
        if not menu_item:
            raise NotFoundError(f'Menu item {menu_item_id} not found')
        
        return {
            'status': 'success',
            'data': menu_item.to_dict()
        }
    
    def put(self, menu_item_id):
        """Update a menu item."""
        menu_item = MenuItem.query.get(menu_item_id)
        if not menu_item:
            raise NotFoundError(f'Menu item {menu_item_id} not found')
        
        data = request.get_json() or {}
        
        if 'name' in data:
            menu_item.name = data['name']
        
        if 'description' in data:
            menu_item.description = data['description']
        
        if 'price' in data:
            menu_item.price = validate_positive_number(data['price'], 'price')
        
        if 'available' in data:
            menu_item.available = bool(data['available'])
        
        if 'restaurant_id' in data:
            restaurant = Restaurant.query.get(data['restaurant_id'])
            if not restaurant:
                raise NotFoundError(f'Restaurant {data["restaurant_id"]} not found')
            menu_item.restaurant_id = data['restaurant_id']
        
        db.session.commit()
        
        return {
            'status': 'success',
            'message': 'Menu item updated successfully',
            'data': menu_item.to_dict()
        }
    
    def delete(self, menu_item_id):
        """Delete a menu item."""
        menu_item = MenuItem.query.get(menu_item_id)
        if not menu_item:
            raise NotFoundError(f'Menu item {menu_item_id} not found')
        
        db.session.delete(menu_item)
        db.session.commit()
        
        return {
            'status': 'success',
            'message': 'Menu item deleted successfully'
        }, 200

