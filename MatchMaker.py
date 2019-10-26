import pandas as pd
from sqlalchemy.ext.automap import automap_base
#from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask, render_template, request

from config import pguser, pgpassword, pghost, pgport, pgdatabase

engine = create_engine(
    f"postgresql+psycopg2://{pguser}:{pgpassword}" + \
    f"@{pghost}:{pgport}/{pgdatabase}"
)

df = pd.read_sql('matchdata',
                 engine)

Base = automap_base()

# reflect the tables
Base.prepare(engine,
             reflect=True)

app = Flask(__name__)

#print users
users = pd.read_sql('Users',
                    engine)
print(users)

# Homepage
@app.route("/")
def homepage():
    """Return the homepage."""

    # Format the data to send as json
    return render_template("index.html")

# Login
@app.route("/login")
def login():
    """Return the login page."""


    # Format the data to send as json
    return render_template("login.html")

# Query the database and send the jsonified results
"""
@app.route("/login_", methods=["GET", "POST"])
def login_():
    if request.method == "POST":
        email = request.form["userEmail"]
        password = request.form["userPassword"]

        db.session.add(pet)
        db.session.commit()
        return redirect("/", code=302)

    if userindata:
        return render_template("matches.html")
    else:
        return render_template("register.html")
    """

# Register
# TODO: Set this up so that you can either pass the details or start new
@app.route("/register")
def register():
    """Return the registration page."""

    # Format the data to send as json
    return render_template("register.html")


if __name__ == "__main__":
    app.run()
