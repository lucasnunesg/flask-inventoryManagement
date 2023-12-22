from flask import redirect, render_template, url_for

from app import app, db

from ..models.forms import EditProductForm, OrderForm
from ..models.tables import Order, OrderItem, Product


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/create-order", methods=["GET", "POST"])
def create_order():
    form = OrderForm()
    products = Product.query.all()
    form.order_items[0].product_id.choices = [
        (product.id, product.name) for product in products
    ]
    if form.validate_on_submit():
        print("Validação OK")
    else:
        print("Validação NOK")
    return render_template("create_order.html", form=form, products=products)


@app.route("/products", methods=["GET", "POST"])
def products():
    products = Product.query.order_by(Product.id).all()
    return render_template("products_list.html", products=products)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    return render_template("index.html")


@app.route("/product/<id>", methods=["GET", "POST"])
def product(id):
    product = Product.query.get(id)
    return render_template("product.html", product=product)


@app.route("/product/<id>/update", methods=["GET", "POST"])
def update_product(id):
    product = Product.query.get(id)
    products = Product.query.order_by(Product.id).all()
    form = EditProductForm(obj=product)

    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.quantity_available = form.quantity_available.data
        db.session.commit()
        return redirect(url_for("products", products=products))
    return render_template("edit_product.html", product=product, form=form)
