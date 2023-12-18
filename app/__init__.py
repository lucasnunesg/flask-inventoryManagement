from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_pyfile("config.py")

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app.controllers import default

from .models.tables import Customer, Order, OrderItem, Product
