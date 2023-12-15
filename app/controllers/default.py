from flask import render_template

from app import app


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/restock")
def restock():
    return render_template("add_inventory.html")


@app.route("/dashboard")
def dashboard():
    return render_template("add_inventory.html")


@app.route("/logout")
def logout():
    return render_template("add_inventory.html")
