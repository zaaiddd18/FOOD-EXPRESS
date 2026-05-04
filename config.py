"""
Configuration management for FoodExpress application.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Base configuration class."""
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # Database Configuration
    # Falls back to a local SQLite file so the app works zero-config.
    # Set DATABASE_URL in .env to point at PostgreSQL for production.
    BASE_DIR = Path(__file__).resolve().parent
    DATABASE_URL = os.environ.get('DATABASE_URL') or \
                   os.environ.get('SQLALCHEMY_DATABASE_URI') or \
                   f'sqlite:///{BASE_DIR / "foodexpress.db"}'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    
    # API Configuration
    API_PREFIX = os.environ.get('API_PREFIX', '/api/v1')
    
    # Admin Configuration
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
    
    # Pagination
    ITEMS_PER_PAGE = 20
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/app.log')
    
    # CORS
    CORS_ORIGINS = ['*']  # Configure appropriately for production


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    FLASK_ENV = 'production'
    # Override with secure values in production
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in production environment")


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

