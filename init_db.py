"""
Database initialization + seed script.

Creates tables (if missing) and loads a rich sample dataset of restaurants,
menu items, customers, delivery partners, orders, and payments — but only if
the database is empty. Safe to run multiple times.

Usage:
    python init_db.py            # create tables + seed if empty
    python init_db.py --reset    # DROP all tables, recreate, and re-seed

Works with any backend supported by the configured SQLAlchemy URL
(defaults to a local SQLite file — see config.py).
"""
import sys
from datetime import datetime

from app import create_app, db
from app.models import (
    Customer, Restaurant, MenuItem, DeliveryPartner,
    Order, OrderItem, Payment,
)


# ────────────────────────────────────────────────────────────────────
# Sample data
# ────────────────────────────────────────────────────────────────────

RESTAURANTS = [
    {
        "name": "Pizza Palace",
        "address": "Connaught Place, New Delhi",
        "phone": "011-2345-6789",
        "cuisine": "Italian",
        "rating": 4.9,
        "menu": [
            ("Margherita Pizza",      "Fresh mozzarella, tomato base, basil, extra virgin olive oil",     349),
            ("Pepperoni Pizza",       "Loaded with pepperoni and melted cheese",                          429),
            ("Veggie Supreme Pizza",  "Bell peppers, onions, olives, mushrooms, sweet corn",              399),
            ("BBQ Chicken Pizza",     "Smoky BBQ sauce, grilled chicken, red onion, cilantro",            479),
            ("Garlic Bread",          "Toasted bread with garlic butter and herbs",                       149),
        ],
    },
    {
        "name": "Burger Republic",
        "address": "Linking Road, Bandra, Mumbai",
        "phone": "022-9876-5432",
        "cuisine": "American",
        "rating": 4.7,
        "menu": [
            ("Classic Smash Burger",   "Double smash patty, cheddar, caramelised onions, house sauce",   289),
            ("Crispy Chicken Burger",  "Buttermilk-fried chicken, slaw, pickles, mayo",                  269),
            ("Veggie Burger",          "Grilled paneer-quinoa patty, lettuce, tomato, smoky aioli",      229),
            ("Loaded Fries",           "Fries topped with cheese sauce, jalapeños, and bacon bits",      189),
            ("Chocolate Milkshake",    "Thick chocolate shake with whipped cream",                       149),
        ],
    },
    {
        "name": "Noodle Bar Tokyo",
        "address": "Indiranagar, Bengaluru",
        "phone": "080-5544-3322",
        "cuisine": "Japanese",
        "rating": 4.6,
        "menu": [
            ("Spicy Ramen Bowl",     "Rich tonkotsu broth, chashu pork, soft egg, nori, bamboo shoots",  379),
            ("Chicken Teriyaki Don", "Glazed chicken over steamed rice with sesame and scallions",       349),
            ("Veg Pad Thai Noodles", "Stir-fried rice noodles with tofu, peanuts, lime",                 299),
            ("Gyoza Dumplings",      "Pan-fried pork dumplings with soy-vinegar dip (6 pcs)",            259),
            ("Miso Soup",            "Traditional dashi broth with tofu and seaweed",                     99),
        ],
    },
    {
        "name": "Biryani House",
        "address": "Banjara Hills, Hyderabad",
        "phone": "040-1122-3344",
        "cuisine": "Indian",
        "rating": 4.8,
        "menu": [
            ("Hyderabadi Chicken Biryani", "Slow-cooked basmati, marinated chicken, saffron, fried onions, raita", 349),
            ("Mutton Biryani",             "Tender mutton dum-cooked with aromatic spices and basmati",  429),
            ("Veg Biryani",                "Mixed vegetables, paneer, basmati, herbs, fried onions",     249),
            ("Butter Chicken",             "Creamy tomato gravy with tandoori chicken",                  329),
            ("Garlic Naan",                "Soft naan brushed with garlic butter",                        69),
        ],
    },
    {
        "name": "Wrap Station",
        "address": "Park Street, Kolkata",
        "phone": "033-4455-6677",
        "cuisine": "Mexican",
        "rating": 4.4,
        "menu": [
            ("Chicken Shawarma Wrap", "Grilled chicken, garlic sauce, pickles, fries, fresh veggies",    199),
            ("Paneer Tikka Wrap",     "Smoky paneer, mint chutney, onions, lettuce in soft tortilla",    179),
            ("Beef Burrito",          "Slow-cooked beef, rice, beans, salsa, sour cream, cheese",        319),
            ("Veggie Quesadilla",     "Mixed peppers, beans, melted cheese in a toasted tortilla",       229),
            ("Loaded Nachos",         "Tortilla chips with cheese sauce, jalapeños, salsa, guacamole",   249),
        ],
    },
    {
        "name": "Sweet Spot",
        "address": "Brigade Road, Bengaluru",
        "phone": "080-9988-7766",
        "cuisine": "Desserts",
        "rating": 4.9,
        "menu": [
            ("Molten Lava Cake",     "Warm chocolate cake with flowing centre, vanilla bean ice cream", 149),
            ("Tiramisu",             "Coffee-soaked ladyfingers layered with mascarpone cream",         189),
            ("Cheesecake Slice",     "New York style baked cheesecake with strawberry compote",         169),
            ("Gulab Jamun (3 pcs)",  "Soft milk dumplings soaked in rose-cardamom syrup",                89),
            ("Mango Lassi",          "Sweet creamy yoghurt drink with fresh mango",                      99),
        ],
    },
]

CUSTOMERS = [
    {"name": "Rahul Sharma",  "email": "rahul@example.com",  "phone": "9876543210", "address": "Flat 12, Connaught Place, New Delhi"},
    {"name": "Ananya Mehta",  "email": "ananya@example.com", "phone": "9123456780", "address": "B-204, Bandra West, Mumbai"},
    {"name": "Arjun Singh",   "email": "arjun@example.com",  "phone": "9988776655", "address": "MG Road, Bengaluru"},
    {"name": "Priya Iyer",    "email": "priya@example.com",  "phone": "9765432109", "address": "Indiranagar, Bengaluru"},
    {"name": "Karan Patel",   "email": "karan@example.com",  "phone": "9887766554", "address": "Satellite, Ahmedabad"},
]

DELIVERY_PARTNERS = [
    {"name": "Ravi Kumar",   "phone": "9000011111", "vehicle_type": "Bike",    "status": "available"},
    {"name": "Priya Verma",  "phone": "9000022222", "vehicle_type": "Scooter", "status": "busy"},
    {"name": "Mohit Patel",  "phone": "9000033333", "vehicle_type": "Cycle",   "status": "available"},
    {"name": "Sneha Roy",    "phone": "9000044444", "vehicle_type": "Bike",    "status": "available"},
]


def seed():
    """Insert sample data. Idempotent — does nothing if data already exists."""
    if Restaurant.query.count() > 0:
        print(f"  ↳ Database already has {Restaurant.query.count()} restaurants — skipping seed.")
        return

    print("  ↳ Seeding restaurants and menu items…")
    rest_objs = []
    for r in RESTAURANTS:
        rest = Restaurant(
            name=r["name"], address=r["address"], phone=r["phone"],
            cuisine=r["cuisine"], rating=r["rating"],
        )
        db.session.add(rest)
        db.session.flush()  # get rest.id
        rest_objs.append(rest)
        for name, desc, price in r["menu"]:
            db.session.add(MenuItem(
                restaurant_id=rest.id,
                name=name, description=desc, price=price, available=True,
            ))

    print("  ↳ Seeding customers…")
    cust_objs = []
    for c in CUSTOMERS:
        cust = Customer(name=c["name"], email=c["email"], phone=c["phone"], address=c["address"])
        db.session.add(cust)
        cust_objs.append(cust)

    print("  ↳ Seeding delivery partners…")
    dp_objs = []
    for d in DELIVERY_PARTNERS:
        dp = DeliveryPartner(name=d["name"], phone=d["phone"],
                             vehicle_type=d["vehicle_type"], status=d["status"])
        db.session.add(dp)
        dp_objs.append(dp)

    db.session.flush()

    # A few example orders so the tracker has something to look up.
    print("  ↳ Seeding sample orders…")

    def make_order(customer, restaurant, partner, status, items):
        order = Order(customer_id=customer.id, restaurant_id=restaurant.id,
                      delivery_partner_id=partner.id if partner else None, status=status)
        db.session.add(order)
        db.session.flush()
        total = 0
        for menu_item, qty in items:
            db.session.add(OrderItem(
                order_id=order.id, menu_item_id=menu_item.id,
                quantity=qty, price=menu_item.price,
            ))
            total += float(menu_item.price) * qty
        order.total_amount = total
        return order, total

    # Order 1: delivered, paid via UPI
    pizza_items = [m for m in rest_objs[0].menu_items]
    o1, t1 = make_order(cust_objs[0], rest_objs[0], dp_objs[0], "delivered",
                        [(pizza_items[0], 1), (pizza_items[4], 2)])
    db.session.add(Payment(order_id=o1.id, amount=t1, method="upi",
                           status="success", paid_at=datetime.utcnow()))

    # Order 2: out for delivery, paid via card
    burger_items = [m for m in rest_objs[1].menu_items]
    o2, t2 = make_order(cust_objs[1], rest_objs[1], dp_objs[1], "dispatched",
                        [(burger_items[0], 2), (burger_items[3], 1)])
    db.session.add(Payment(order_id=o2.id, amount=t2, method="card",
                           status="success", paid_at=datetime.utcnow()))

    # Order 3: preparing
    biryani_items = [m for m in rest_objs[3].menu_items]
    o3, t3 = make_order(cust_objs[2], rest_objs[3], dp_objs[3], "preparing",
                        [(biryani_items[0], 1), (biryani_items[4], 2)])
    db.session.add(Payment(order_id=o3.id, amount=t3, method="upi",
                           status="success", paid_at=datetime.utcnow()))

    db.session.commit()

    print("  ✓ Seed complete.")
    print(f"    {Restaurant.query.count()} restaurants")
    print(f"    {MenuItem.query.count()} menu items")
    print(f"    {Customer.query.count()} customers")
    print(f"    {Order.query.count()} sample orders")


def init_db(reset: bool = False):
    app = create_app()
    with app.app_context():
        print(f"Using DB: {app.config['SQLALCHEMY_DATABASE_URI']}")
        if reset:
            print("Dropping all existing tables…")
            db.drop_all()
        print("Creating database tables…")
        db.create_all()
        seed()
        print("\nDone! Run `python run.py` and open http://127.0.0.1:5000")


if __name__ == "__main__":
    init_db(reset="--reset" in sys.argv)
