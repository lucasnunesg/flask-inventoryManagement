from flask import flash, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from app import app, db

from ..models.forms import AddOrderItemForm, EditProductForm, OrderItemForm
from ..models.tables import Customer, Order, OrderItem, Product


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/products", methods=["GET", "POST"])
def products():
    products = Product.query.order_by(Product.id).all()
    return render_template("products_list.html", products=products)


@app.route("/product/<id>", methods=["GET", "POST"])
def product(id):
    product = Product.query.get(id)
    return render_template("product.html", product=product)


@app.route("/product/<id>/update", methods=["GET", "POST"])
def update_product(id):
    product = Product.query.get(id)
    form = EditProductForm(obj=product)

    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.quantity_available = form.quantity_available.data
        db.session.commit()
        return redirect(url_for("products"))
    return render_template("edit_product.html", product=product, form=form)


@app.route("/product/<id>/delete", methods=["GET", "POST", "DELETE"])
def delete_product(id):
    try:
        product = Product.query.get(id)
        db.session.delete(product)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        error_info = str(e.orig)
        print(error_info)
    return redirect(url_for("products"))


@app.route("/add-product", methods=["GET", "POST"])
def add_product():
    return render_template("add_product.html")


@app.route("/create-order", methods=["GET", "POST"])
def create_order():
    form = OrderItemForm()
    products = Product.query.all()
    customers = Customer.query.all()
    form.product_id.choices = [(product.id, product.name) for product in products]
    form.customer_id.choices = [
        (customer.id, customer.first_name) for customer in customers
    ]

    if form.validate_on_submit():
        customer_id = form.customer_id.data
        order = Order(customer_id=customer_id)
        product = Product.query.get(form.product_id.data)
        quantity = form.quantity.data
        order_item = OrderItem(
            item_id=form.product_id.data,
            quantity=quantity,
            total_price=product.price * quantity,
        )
        db.session.add(order_item)

        order.order_items.append(order_item)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for("order", id=order.id, customer_id=customer_id))
    return render_template("create_order.html", form=form, products=products)


@app.route("/order/<int:id>", methods=["GET", "POST"])
def order(id):
    form = AddOrderItemForm()
    products = Product.query.all()
    form.product_id.choices = [(product.id, product.name) for product in products]

    order_items = OrderItem.query.filter_by(order_id=id).all()
    product_names = [Product.query.get(item.item_id).name for item in order_items]
    print(type(id))
    order = Order.query.get(id)
    customer_id = order.customer_id
    customer = Customer.query.get(customer_id)
    products_for_order = {
        item.item_id: Product.query.get(item.item_id) for item in order_items
    }

    if form.validate_on_submit():
        customer = Customer.query.get(customer_id)
        product = Product.query.get(form.product_id.data)
        quantity = form.quantity.data
        new_order_item = OrderItem(
            order_id=order.id,
            item_id=form.product_id.data,
            quantity=quantity,
            total_price=product.price * quantity,
        )
        try:
            db.session.add(new_order_item)
            db.session.commit()
            order.order_items.append(new_order_item)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            error_info = str(e.orig)
            if "UNIQUE constraint" in error_info:
                flash("Same product ID already in order", "error")
            else:
                flash("Unknown error", "error")
        return redirect(url_for("order", id=order.id, customer_id=customer_id))
    return render_template(
        "order.html",
        order=id,
        order_items=order_items,
        product_names=product_names,
        customer=customer,
        zip=zip,
        form=form,
        products_for_order=products_for_order,
    )


@app.route("/delete-orderitem/<item_id>/<order_id>", methods=["GET", "POST", "DELETE"])
def delete_orderitem(item_id, order_id):
    order_item = (
        OrderItem.query.filter_by(item_id=item_id).filter_by(order_id=order_id).first()
    )
    db.session.delete(order_item)
    db.session.commit()
    return redirect(url_for("order", id=order_id))


@app.route("/close-order/<id>", methods=["GET", "POST"])
def close_order(id):
    order = Order.query.get(id)
    order_items = OrderItem.query.filter_by(order_id=order.id).all()
    for item in order_items:
        product = Product.query.get(item.item_id)
        product.quantity_available -= item.quantity
        db.session.commit()
    return redirect(url_for("products"))


@app.route("/logout", methods=["GET", "POST"])
def logout():
    return render_template("index.html")
