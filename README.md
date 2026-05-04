# FoodExpress

A full-stack food delivery web app — Flask + SQLAlchemy backend with a single-page vanilla-JS frontend. Browse restaurants, filter by category, build a cart, place an order, track its status — everything is wired up to a real REST API.

## What's inside

- **Backend**: Flask 3 application factory, Flask-RESTful API, Flask-Admin dashboard, SQLAlchemy models, custom error handling and validation.
- **Frontend**: Single page (`app/templates/index.html`) that fetches restaurants and menu items from the API, has a working cart (with quantity controls and persistence), checkout flow that creates customers and orders, and a live order tracker.
- **Database**: PostgreSQL in production, SQLite by default for zero-config local dev. A rich sample dataset (6 restaurants, 30 menu items, sample customers, partners, and orders) is loaded automatically on first run.

## Quick start (zero config)

```bash
python3 -m venv venv
source venv/bin/activate            # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

That's it. Open `http://127.0.0.1:5000`. On first launch the app creates a SQLite database (`foodexpress.db`) and seeds it with sample restaurants, menu items, customers, and a few orders, so the page is fully populated immediately.

The Flask-Admin dashboard is at `http://127.0.0.1:5000/admin`.

## Using PostgreSQL instead

If you want to run against PostgreSQL:

```bash
# 1. Create DB and user
psql postgres -c "CREATE USER foodexpress WITH PASSWORD 'your_password';"
psql postgres -c "CREATE DATABASE foodexpress OWNER foodexpress;"

# 2. Configure env
cp .env.example .env
#   then edit DATABASE_URL in .env to match your Postgres credentials

# 3. Run
python run.py
```

The same automatic seeder runs on first launch, so you don't need to load the SQL files manually. (`schema.sql` and `sample_data.sql` are still included for reference.)

## Project structure

```
.
├── app/
│   ├── __init__.py            # App factory, CORS, blueprints
│   ├── api/
│   │   ├── routes.py          # Resource registration (/api/v1/*)
│   │   └── resources/         # CustomerList, RestaurantList, OrderList, ...
│   ├── models/                # SQLAlchemy models
│   ├── services/order_service.py  # Order creation business logic
│   ├── utils/                 # Validators + error handlers
│   └── templates/index.html   # Single-page frontend
├── config.py                  # Config classes (dev/prod/testing)
├── run.py                     # Dev entrypoint (auto-seeds DB)
├── wsgi.py                    # Prod WSGI entrypoint (gunicorn)
├── init_db.py                 # Standalone seeder (also called from run.py)
├── make_zip.py                # Build a clean deployable zip
├── requirements.txt
├── schema.sql / sample_data.sql   # Reference SQL (Postgres)
├── .env.example               # Copy to .env and fill in
├── .gitignore
├── LICENSE                    # MIT
└── README.md
```

## REST API

All endpoints are prefixed with `/api/v1`.

| Method | Path                                     | Purpose                          |
|--------|------------------------------------------|----------------------------------|
| GET    | `/restaurants[?cuisine=…&include_menu=true]` | List restaurants             |
| GET    | `/restaurants/<id>?include_menu=true`    | Restaurant detail + menu         |
| POST   | `/restaurants`                           | Create restaurant                |
| PUT    | `/restaurants/<id>`                      | Update restaurant                |
| DELETE | `/restaurants/<id>`                      | Delete restaurant                |
| GET    | `/menu-items?available_only=true`        | List menu items                  |
| GET    | `/menu-items/<id>`                       | Menu item detail                 |
| POST   | `/menu-items`                            | Create menu item                 |
| GET    | `/customers`                             | List customers                   |
| POST   | `/customers`                             | Create customer                  |
| GET    | `/customers/<id>`                        | Customer detail                  |
| POST   | `/orders`                                | Place an order                   |
| GET    | `/orders/<id>?include_items=true`        | Order detail with items          |
| PUT    | `/orders/<id>/status`                    | Update order status              |
| GET    | `/delivery-partners`                     | List delivery partners           |
| GET    | `/payments`                              | List payments                    |

### Place-order payload

```json
{
  "customer_id": 1,
  "restaurant_id": 1,
  "items": [
    { "menu_item_id": 1, "quantity": 2 },
    { "menu_item_id": 2, "quantity": 1 }
  ]
}
```

All items in a single order must be from the same restaurant — the frontend enforces this, and the backend validates it.

## Running in production

```bash
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

Set `FLASK_ENV=production`, a strong `SECRET_KEY`, and a real Postgres `DATABASE_URL` in your environment.

## Building a deploy zip

```bash
python make_zip.py
```

Produces `../FoodExpress.zip` (one directory above the project), excluding `venv/`, caches, the local SQLite file, `.env`, and other build artefacts. Drop the zip into VS Code on any machine and follow Quick Start above.

## License

Released under the [MIT License](LICENSE).
