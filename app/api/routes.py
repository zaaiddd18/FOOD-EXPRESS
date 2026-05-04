"""
API Routes
"""
from flask import Blueprint
from app.api.resources.customers import CustomerList, CustomerDetail
from app.api.resources.restaurants import RestaurantList, RestaurantDetail
from app.api.resources.menu_items import MenuItemList, MenuItemDetail
from app.api.resources.orders import OrderList, OrderDetail, OrderStatusUpdate
from app.api.resources.delivery_partners import DeliveryPartnerList, DeliveryPartnerDetail
from app.api.resources.payments import PaymentList, PaymentDetail
from flask_restful import Api

api_bp = Blueprint('api', __name__)
# Configure Api to handle errors properly and work with CORS
# catch_all_404s ensures Flask-RESTful handles 404s instead of Flask
api = Api(api_bp, catch_all_404s=True, prefix='')

# Register resources
api.add_resource(CustomerList, '/customers')
api.add_resource(CustomerDetail, '/customers/<int:customer_id>')

api.add_resource(RestaurantList, '/restaurants')
api.add_resource(RestaurantDetail, '/restaurants/<int:restaurant_id>')

api.add_resource(MenuItemList, '/menu-items')
api.add_resource(MenuItemDetail, '/menu-items/<int:menu_item_id>')

api.add_resource(OrderList, '/orders')
api.add_resource(OrderDetail, '/orders/<int:order_id>')
api.add_resource(OrderStatusUpdate, '/orders/<int:order_id>/status')

api.add_resource(DeliveryPartnerList, '/delivery-partners')
api.add_resource(DeliveryPartnerDetail, '/delivery-partners/<int:partner_id>')

api.add_resource(PaymentList, '/payments')
api.add_resource(PaymentDetail, '/payments/<int:payment_id>')

