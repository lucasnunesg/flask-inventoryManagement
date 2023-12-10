from datetime import datetime

from app import db


class InventoryItem(db.Model):
    __tablename__ = "inventory"

    sku = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    unit_cost = db.Column(db.Float, nullable=False)
    amount_in_stock = db.Column(db.Integer, nullable=False)
    amount_sold = db.Column(db.Integer, nullable=False)
    revenue = db.Column(db.Float, nullable=False)
    latest_sale = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "<Inventory item: %r>" % self.name


""" 
UPCOMING MODELS (WILL BE IMPLEMENTED LATER)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    role = db.relationship("Role", backref="user", lazy=True)

    def __repr__(self):
        return "<User %r>" % self.username
    
class Role(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    usernames = db.relationship("User", foreign_keys=user_id)

    def __repr__(self):
        return "<Role %r>" % self.name
    
"""
