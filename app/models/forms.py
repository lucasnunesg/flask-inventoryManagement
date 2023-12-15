from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField


class LoginForm(FlaskForm):
    username = Stringfield()
    password = PasswordField()
    remember_me = BooleanField()

class RegisterSale(FlaskForm):
    sku = 
    