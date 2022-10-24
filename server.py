from flask import Flask, render_template, redirect, flash, request
import jinja2

app = Flask(__name__)
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route('/')
def homepage():
    return render_template("base.html")
@app.route('/melons')
def melonsPage():
    return render_template("melons.html")
@app.route('/melon/<melon_id>')
def individualPage(melon_id):
    return render_template("individualMelon.html")
@app.route('/cart')
def cartPage():
    return render_template("cart.html")
@app.route('/add_to_cart/<melon_id>')
def add_to_cart(melon_id):
    return f"{melon_id} added to cart"












if __name__ == "__Main__":
    app.env = "development"
    app.run(debug = True, port = 8000, host = "localhost")