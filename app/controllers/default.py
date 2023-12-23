from flask import redirect, render_template, url_for

from app import app, db

from ..models.forms import AddOrderItemForm, EditProductForm, OrderForm, OrderItemForm
from ..models.tables import Customer, Order, OrderItem, Product


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


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
        order = Order(customer_id=form.customer_id.data)
        order_item = OrderItem(
            item_id=form.product_id.data, quantity=form.quantity.data, total_price=1
        )
        db.session.add(order_item)

        order.order_items.append(order_item)
        db.session.add(order)
        db.session.commit()
        print("ORDERRR = ", order)
        return redirect(url_for("order", id=order.id))
    return render_template("create_order.html", form=form, products=products)


@app.route("/order/<int:id>", methods=["GET", "POST"])
def order(id):
    form = AddOrderItemForm()
    products = Product.query.all()
    form.product_id.choices = [(product.id, product.name) for product in products]

    order_items = OrderItem.query.filter_by(order_id=id).all()
    product_names = [Product.query.get(item.item_id).name for item in order_items]
    print(type(id))
    print("ORDER ITEMSSSSS: ", order_items)

    if form.validate_on_submit():
        print("CHECKPOINT")
        print("ID: ", id)
        order = Order.query.get(id)
        print("TENTANDO ACESSAR ORDER ", order)
        new_order_item = OrderItem(
            order_id=order.id,
            item_id=form.product_id.data,
            quantity=form.quantity.data,
            total_price=2,
        )
        db.session.add(new_order_item)
        db.session.commit()
        order.order_items.append(new_order_item)
        db.session.commit()
        return redirect(url_for("order", id=order.id))

    return render_template(
        "order.html",
        order=id,
        order_items=order_items,
        product_names=product_names,
        zip=zip,
        form=form,
    )


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
