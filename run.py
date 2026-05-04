"""
Application entry point for development.

On first run this also creates tables and loads sample data, so opening
the page shows real restaurants and menu items immediately.
"""
import os
from app import create_app

app = create_app(os.environ.get('FLASK_ENV', 'development'))


def _bootstrap_db():
    """Create tables and seed sample data if the DB is empty."""
    from app import db
    from init_db import seed
    with app.app_context():
        db.create_all()
        seed()


if __name__ == '__main__':
    _bootstrap_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
