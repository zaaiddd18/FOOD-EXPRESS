"""
FoodExpress Application Factory
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_cors import CORS
from config import config
import os
import logging
from pathlib import Path

# Initialize extensions
db = SQLAlchemy()
admin = Admin(name='FoodExpress Admin', template_mode='bootstrap4')


def create_app(config_name=None):
    """
    Application factory pattern.
    Creates and configures the Flask application.
    """
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    admin.init_app(app)
    
    # Setup logging
    setup_logging(app)
    
    # Register blueprints FIRST - Flask-RESTful needs to handle responses
    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix=app.config['API_PREFIX'])
    
    # Configure CORS AFTER blueprints are registered
    # This ensures Flask-RESTful processes tuple responses before CORS
    CORS(app, resources={r"/api/*": {
        "origins": app.config['CORS_ORIGINS'],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }}, supports_credentials=True)
    
    # Register home route
    @app.route('/')
    def home():
        from flask import render_template
        return render_template('index.html')
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register admin views (must be after app context is available)
    with app.app_context():
        register_admin_views()
        # Create database tables
        db.create_all()
    
    return app


def setup_logging(app):
    """Configure application logging."""
    log_level = getattr(logging, app.config['LOG_LEVEL'].upper(), logging.INFO)
    
    # Create logs directory if it doesn't exist
    log_file = app.config['LOG_FILE']
    log_dir = Path(log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s %(levelname)s %(name)s %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    app.logger.setLevel(log_level)


def register_admin_views():
    """Register Flask-Admin views."""
    from app.models import (
        Customer, Restaurant, MenuItem, DeliveryPartner,
        Order, OrderItem, Payment
    )
    from flask_admin.contrib.sqla import ModelView
    
    admin.add_view(ModelView(Customer, db.session, name='Customers', category='Entities'))
    admin.add_view(ModelView(Restaurant, db.session, name='Restaurants', category='Entities'))
    admin.add_view(ModelView(MenuItem, db.session, name='Menu Items', category='Entities'))
    admin.add_view(ModelView(DeliveryPartner, db.session, name='Delivery Partners', category='Entities'))
    admin.add_view(ModelView(Order, db.session, name='Orders', category='Orders'))
    admin.add_view(ModelView(OrderItem, db.session, name='Order Items', category='Orders'))
    admin.add_view(ModelView(Payment, db.session, name='Payments', category='Orders'))


def register_error_handlers(app):
    """Register error handlers."""
    from app.utils.errors import register_error_handlers as reg_handlers
    reg_handlers(app)

