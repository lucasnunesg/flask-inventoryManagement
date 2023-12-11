from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object("config")

db = SQLAlchemy(app)

migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run()

from app.controllers import default

from .models.tables import InventoryItem
