import re
from flask import Flask, render_template, redirect, flash, request, session
import jinja2 

import melons, customers
from forms import LoginForm

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route('/')
def homepage():
    return render_template("base.html")

@app.route('/melons')
def melonsPage():
    melon_list = melons.get_all()
    return render_template("melons.html", melon_list = melon_list)

@app.route('/melon/<melon_id>')
def individualMelons(melon_id):
    melon = melons.get_by_id(melon_id)
    return render_template("individualMelon.html", melon = melon)

@app.route('/cart')
def cartPage():
    order_total=0
    cart_melons = []
    cart = session.get("cart", {})
    for melon_id, quantity in cart.items():
        melon = melons.get_by_id(melon_id)
        
        total_cost = quantity * melon.price
        order_total += total_cost
        
        melon.quantity = quantity
        melon.total_cost = total_cost
        
        cart_melons.append(melon)

    return render_template("cart.html", cart_melons=cart_melons, order_total = order_total)

@app.route('/add_to_cart/<melon_id>')
def add_to_cart(melon_id):
    if 'cart' not in session:
        session['cart']={}
    cart = session['cart']
    cart[melon_id] = cart.get(melon_id, 0) + 1
    session.modified = True
    flash(f"Melon {melon_id} successfully added to cart.")
    print(cart)

    return redirect("/cart")

@app.route("/empty-cart")
def empty_cart():
    session["cart"] = {}

    return redirect("/cart")

@app.route("/login", methods = ['GET','POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = customers.get_by_username(username)
        
        if not user or user['password'] != password:
            flash('Invalid username of password')
            return redirect("/login")
        
        session["username"] = user["username"]
        flash("Logged in.")
        return redirect("/melons")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    del session['username']
    flash("logged out")
    return redirect("/login")

if __name__ == "__main__":
    app.env = "development"
    app.run(debug = True, port = 8000, host = "localhost")