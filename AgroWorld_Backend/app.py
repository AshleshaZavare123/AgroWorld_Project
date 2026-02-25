from flask import Flask, render_template, request, redirect, url_for
from db import get_connection

app = Flask(__name__)

# ---------------- DEFAULT ROUTE ----------------
@app.route("/")
def default():
    return redirect("/login")


# ---------------- LOGIN PAGE ----------------
@app.route("/login")
def login():
    return render_template("login.html")


# ---------------- SIGNUP ----------------
@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
        (name, email, password)
    )
    conn.commit()
    conn.close()

    return redirect("/login")


# ---------------- LOGIN POST ----------------
@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE email=%s AND password=%s",
        (email, password)
    )
    user = cur.fetchone()
    conn.close()

    if user:
        return redirect("/home")
    else:
        return "Invalid Login"


# ---------------- HOME ----------------
@app.route("/home")
def home():
    return render_template("home.html")


# ---------------- PRODUCTS ----------------
@app.route("/products")
def products():
    return render_template("products.html")


# ---------------- ORDERVIEW PAGE ----------------
@app.route("/orderview")
def orderview():
    return render_template("orderview.html")


# ---------------- ADMIN ----------------
@app.route("/admin")
def admin():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()

    return render_template("admin.html", products=products)


# ---------------- ADD PRODUCT ----------------
@app.route("/add_product", methods=["POST"])
def add_product():
    name = request.form["name"]
    category = request.form["category"]
    price = request.form["price"]
    description = request.form["description"]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, category, price, description) VALUES (%s,%s,%s,%s)",
        (name, category, price, description)
    )
    conn.commit()
    conn.close()

    return redirect("/admin")


# ---------------- DELETE PRODUCT ----------------
@app.route("/delete_product/<int:id>")
def delete_product(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=%s", (id,))
    conn.commit()
    conn.close()

    return redirect("/admin")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)