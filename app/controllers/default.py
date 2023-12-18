from flask import render_template

from app import app

from ..models.forms import EditProductForm
from ..models.tables import Product

# from app.models.forms import LoginForm


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/restock", methods=["GET", "POST"])
def restock():
    return render_template("restock.html")


@app.route("/products", methods=["GET", "POST"])
def products():
    products = Product.query.order_by(Product.id).all()
    return render_template("products_list.html", products=products)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    return render_template("restock.html")


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
        return render_template("products_list.html", products=products)
    return render_template("edit_product.html", product=product, form=form)
