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
    product_id = SelectField("Product ID", coerce=int, validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])

    """def validate_quantity(self, quantity):
        product = Product.query.get(self.product_id)
        stock_quantity = product.quantity_available
        if quantity > stock_quantity:
            raise ValidationError(
                "Not enough stock for this item. Quantity available" + stock_quantity
            )"""


class OrderForm(FlaskForm):
    """A form for one or more item"""

    total_items = HiddenField("Total Items")
    order_items = FieldList(FormField(OrderItemForm), min_entries=1)
    submit = SubmitField("Submit")

    def validate_order_items(self, order_items):
        print("Order Items:", self.order_items.data)
        print("Total Items:", self.total_items.data)
        for item in order_items:
            product_id = item.product_id.data
            quantity = item.quantity.data

            print("Product id: ", product_id, "Qty: ", quantity)
            product = Product.query.get(product_id)
            print("Product: ", product)
            stock_quantity = product.quantity_available
            if quantity > stock_quantity:
                raise ValidationError(
                    "Not enough stock for this item. Quantity available"
                )


class LoginForm(FlaskForm):
    pass


class CreateAccountForm(FlaskForm):
    pass
