from flask_wtf import FlaskForm, Form
from wtforms import (
    BooleanField,
    FieldList,
    FormField,
    HiddenField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .tables import Product, User


class LoginForm(FlaskForm):
    email = StringField(label="E-mail", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit_button = SubmitField(label="Log in")

    def validate_login(self, email):
        user = User.query.filter_by(email=email.data).first()

        if not user:
            raise ValidationError("E-mail not registered, please create an account.")


class CreateAccountForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    email = StringField(label="E-mail", validators=[DataRequired(), Email()])
    password = PasswordField(
        label="Password", validators=[DataRequired(), Length(6, 28)]
    )
    password_confirmation = PasswordField(
        label="Password",
        validators=[
            DataRequired(),
            Length(6, 28),
            EqualTo("password", message="passwords must match"),
        ],
    )
    submit_button = SubmitField(label="Create an account")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError("E-mail already registered, Log in to proceed")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError("Username already taken, please choose another")


class EditProductForm(FlaskForm):
    name = StringField(label="Product Name", validators=[DataRequired()])
    price = IntegerField(label="Product Price", validators=[DataRequired()])
    quantity_available = IntegerField(
        label="Quantity available", validators=[DataRequired()]
    )
    submit_button = SubmitField(label="Update")

    def validate_quantity_available(self, quantity_available):
        product = Product.query.filter_by(name=self.name.data).first()
        if quantity_available.data < product.quantity_available:
            raise ValidationError("Stock can only be reduced registering sales")


"""    def validate_name(self, name):
        product_names_list = [product.name for product in Product.query.all()]
        if name in product_names_list:
            raise ValidationError("Another product with the same name already exists")"""


class OrderItemForm(FlaskForm):
    customer_id = SelectField("Customer", coerce=int, validators=[DataRequired()])
    product_id = SelectField("Product ID", coerce=int, validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    submit = SubmitField("Submit Item")

    def validate_quantity(self, quantity):
        product = Product.query.get(self.product_id.data)
        stock_quantity = product.quantity_available
        if quantity.data > stock_quantity:
            raise ValidationError(
                f"Not enough stock for this item. Quantity available: {stock_quantity}"
            )


class AddOrderItemForm(FlaskForm):
    product_id = SelectField("Product ID", coerce=int, validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    customer_id = HiddenField("customer_id")

    def validate_quantity(self, quantity):
        product = Product.query.get(self.product_id.data)
        """if not product:
            raise ValidationError("Invalid product selected")"""

        stock_quantity = product.quantity_available
        if quantity.data > stock_quantity:
            raise ValidationError(
                f"Not enough stock for this item. Quantity available: {stock_quantity}"
            )

    submit = SubmitField("Submit Item")


class OrderForm(FlaskForm):
    """A form for one or more item"""

    total_items = HiddenField("Total Items")
    order_items = FieldList(FormField(OrderItemForm), max_entries=1)
    submit = SubmitField("Submit")
