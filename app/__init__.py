from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_pyfile("config.py")

db = SQLAlchemy(app)

migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "index"

from app.controllers import default

from .models.tables import Customer, Order, OrderItem, Product
