from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    FieldList,
    FormField,
    HiddenField,
    IntegerField,
    PasswordField,
    StringField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, Email

from .tables import Product


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
    product_id = IntegerField("Product ID", validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])


class OrderForm(FlaskForm):
    """A form for one or more item"""

    total_items = HiddenField("Total Items")
    order_items = FieldList(FormField(OrderItemForm), min_entries=1)
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    pass


class CreateAccountForm(FlaskForm):
    pass
