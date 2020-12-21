import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    if request.method == "GET":
        return render_template("add_cash.html")
    else:
        db.execute("UPDATE users SET cash = cash + :amount WHERE id=:user_id", amount = request.form.get("cash"), user_id=session["user_id"])
        flash("Cash Added")
        return redirect("/")

@app.route("/")
@login_required
def index():
    rows = db.execute("""
        SELECT symbol, SUM(shares) as totalShares
        FROM transactions
        WHERE user_id = :user_id
        GROUP BY symbol
        HAVING totalShares > 0;
    """, user_id=session["user_id"])
    holdings = []
    grand_total = 0
    for row in rows:
        stock = lookup(row["symbol"])
        holdings.append({
            "symbol": stock["symbol"],
            "name": stock["name"],
            "shares": row["totalShares"],
            "price": usd(stock["price"]),
            "total": usd(stock["price"] * row["totalShares"])
        })
        grand_total += stock["price"] * row["totalShares"]
    rows = db.execute("SELECT cash FROM users WHERE id=:user_id", user_id=session["user_id"])
    cash = rows[0]["cash"]
    grand_total += cash

    return render_template("index.html", holdings=holdings, cash=usd(cash), grand_total=usd(grand_total))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    #if GET then send to html input page
    if request.method == "GET":
        return render_template("buy.html")

    #get input and check validity
    else:
        symbol=lookup(request.form.get("symbol"))
        if not symbol:
            return apology("Please provide valid stock symbol", 400)
        elif symbol == None:
            return apology("Please provide valid stock symbol", 400)

        shares=request.form.get("shares")
        if not shares:
            return apology("Please provide number of shares requested", 400)
        try:
            shares = int(shares)
        except:
            return apology("Share number must be a positive integer")
        if shares < 0:
            return apology("Share number must be a positive integer")

        quote = lookup(request.form.get("symbol"))
        price = quote.get("price")
        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        shares = int(request.form.get("shares"))

        #find how much cash buyer has
        row = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
        cash = float(row[0]["cash"])

        updated_cash = cash - shares * stock['price']

        # If the user don't have enough money, apologize - otherwise update purchases and cash amount
        if updated_cash < 0:
            return apology("You don't have enough money to complete this transcation", 400)
        else:
            # update cash total
            db.execute("UPDATE users SET cash= :updated_cash WHERE id=:id",
            updated_cash=updated_cash,
            id=session["user_id"])

            # insert purchase history into new table "transactions"
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price ) VALUES (:user_id, :symbol, :shares, :price)", user_id=session["user_id"], symbol=stock["symbol"], shares=shares, price=stock["price"])

            flash("Stock Purchased")
            return redirect("/")


@app.route("/history")
@login_required
def history():
    transactions = db.execute("SELECT symbol, shares, price, date FROM transactions WHERE user_id=:user_id", user_id=session["user_id"])
    for i in range(len(transactions)):
        transactions[i]["price"] = usd(transactions[i]["price"])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")

    else:
        symbol = request.form.get("symbol")
        stock = lookup(symbol)

        stockname = stock["name"]
        stocksymbol = stock["symbol"]
        stockprice = stock["price"]

        return render_template("quoted.html", name=stockname, price=stockprice, symbol=stocksymbol)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    # User reached route via POST (as by submitting a form via POST)
    #get details and perform checks
    else:
        username=request.form.get("username")
        if not username:
            return apology("must provide username", 400)

        password=request.form.get("password")
        if not password:
            return apology("must provide password", 400)

        confirmation=request.form.get("confirmation")
        if not confirmation:
            return apology("must provide confirmation of password", 400)
        if password != request.form.get("confirmation"):
            return apology("Passwords do not match", 400)

        hash=generate_password_hash(password)

        #put in to db and check username available
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash);", username=username, hash=hash)
        if not result:
            return apology("Username already exists")

        # Redirect user to home page
        return redirect("/login")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    #if GET then send to html input page
    if request.method == "GET":
        rows=db.execute("""
            SELECT symbol
            FROM transactions
            WHERE user_id=:user_id
            GROUP BY symbol
            HAVING SUM(shares) > 0;
        """, user_id=session["user_id"])
        return render_template("sell.html", symbols=[row["symbol"] for row in rows])
    else:
        symbol=lookup(request.form.get("symbol"))

        if not symbol:
            return apology("Please provide valid stock symbol", 400)
        elif symbol == None:
            return apology("Please provide stock symbol", 400)

        shares=int(request.form.get("shares"))
        if not shares:
            return apology("Please provide number of shares", 400)
        elif shares < 0:
            return apology("Please provide valid number of shares", 400)

        quote = lookup(request.form.get("symbol"))
        price = quote.get("price")
        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        shares = int(request.form.get("shares"))

        rows=db.execute("SELECT symbol, SUM(shares) as totalShares FROM transactions WHERE user_id=:user_id GROUP BY symbol HAVING totalShares > 0;", user_id=session["user_id"])
        for row in rows:
            if row["symbol"] == symbol:
                if shares > row["totalShares"]:
                    return apology("You do not have that many shares")

        row = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
        cash = (row[0]["cash"])

        updated_cash = cash + shares * stock['price']

        # update cash total
        db.execute("UPDATE users SET cash=:updated_cash WHERE id=:id",
            updated_cash=updated_cash,
            id=session["user_id"])

        # insert into "transactions"
        db.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price)
            VALUES (:user_id, :symbol, :shares, :price)
            """,
            user_id=session["user_id"],
            symbol=stock["symbol"],
            shares= -1*shares,
            price=stock["price"]
        )

        flash("Stock Sold")
        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
