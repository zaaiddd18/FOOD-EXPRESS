"""
Error handling utilities
"""
from flask import jsonify
from app import db
import logging

logger = logging.getLogger(__name__)


class APIError(Exception):
    """Base API exception class."""
    status_code = 400
    message = 'An error occurred'
    
    def __init__(self, message=None, status_code=None, payload=None):
        Exception.__init__(self)
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status'] = 'error'
        return rv


class ValidationError(APIError):
    """Validation error exception."""
    status_code = 400


class NotFoundError(APIError):
    """Resource not found exception."""
    status_code = 404


class ConflictError(APIError):
    """Resource conflict exception."""
    status_code = 409


def register_error_handlers(app):
    """Register error handlers for the application."""
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        """Handle API errors."""
        # Return a proper Response object, not a tuple
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        logger.error(f"API Error: {error.message}")
        return response
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle 404 errors."""
        response = jsonify({
            'status': 'error',
            'message': 'Resource not found'
        })
        response.status_code = 404
        return response
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        """Handle 500 errors."""
        db.session.rollback()
        response = jsonify({
            'status': 'error',
            'message': 'Internal server error'
        })
        response.status_code = 500
        logger.error(f"Internal Error: {str(error)}")
        return response
    
    @app.errorhandler(400)
    def handle_bad_request(error):
        """Handle 400 errors."""
        response = jsonify({
            'status': 'error',
            'message': 'Bad request'
        })
        response.status_code = 400
        return response

