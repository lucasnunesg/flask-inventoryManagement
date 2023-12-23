import random
from sqlite3 import IntegrityError

import faker_commerce
from faker import Faker
from sqlalchemy import exc

from app import db
from app.models.tables import Customer, Order, OrderItem, Product

fake = Faker()


def add_customers():
    for _ in range(100):
        customer = Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            address=fake.street_address(),
            postcode=fake.postcode(),
            email=fake.email(),
        )
        db.session.add(customer)
    db.session.commit()


def add_orders():
    customers = Customer.query.all()

    for _ in range(100):
        customer = random.choice(customers)

        order_date = fake.date_time_this_year()
        shipped_date = None
        shipped_date = random.choices(
            [None, fake.date_time_between(start_date=order_date)],
            weights=[10, 90],
        )[0]

        delivered_date = None
        if shipped_date:
            delivered_date = random.choices(
                [None, fake.date_time_between(start_date=shipped_date)],
                weights=[50, 50],
            )[0]

        coupon_code = random.choices(
            [None, "50OFF", "FREESHIPPING", "2FOR1"],
            weights=[80, 5, 5, 5],
        )[0]

        order = Order(
            customer_id=customer.id,
            order_date=order_date,
            shipped_date=shipped_date,
            delivered_date=delivered_date,
            coupon_code=coupon_code,
        )

        db.session.add(order)

    db.session.commit()


def add_products():
    for _ in range(10):
        # Create fake product names using faker-commerce module
        fake.add_provider(faker_commerce.Provider)
        product = Product(
            name=fake.ecommerce_name(),
            price=random.randint(10, 200),
            quantity_available=random.randint(1, 50),
        )
        db.session.add(product)
    db.session.commit()


# You don't have to add products exactly when you create an order, this operation can be delayed
def add_order_products():
    orders = Order.query.all()
    products = Product.query.all()

    # For every order select a random number of products between 1 and 5
    for order in orders:
        k = random.randint(1, 5)
        purchased_products = random.sample(products, k)

        for product in purchased_products:
            order_item = OrderItem(
                order_id=order.id,
                item_id=product.id,
                quantity=k,
                total_price=k * product.price,
            )
            db.session.add(order_item)

    db.session.commit()


def clear_databases():
    for i in [Customer, Order, Product, OrderItem]:
        try:
            i.query.delete()
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()


def create_random_data(clear_db=True):
    if clear_db:
        clear_databases()
    add_customers()
    add_orders()
    add_products()
    add_order_products()
