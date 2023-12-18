from datetime import datetime

from app import db


class Customer(db.Model):
    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    postcode = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)

    orders = db.relationship("Order", backref="customer")

    def __repr__(self):
        return "<Customer: %r>" % self.first_name + self.last_name


class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    shipped_date = db.Column(db.DateTime)
    delivered_date = db.Column(db.DateTime)
    coupon_code = db.Column(db.String(50))
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)

    order_items = db.relationship("OrderItem", backref="order")

    def __repr__(self):
        return "<Order ID: %r>" % self.id


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    quantity_available = db.Column(db.Integer)

    def __repr__(self):
        return "<Product: %r>" % self.name


class OrderItem(db.Model):
    __tablename__ = "order_item"

    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("product.id"), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
