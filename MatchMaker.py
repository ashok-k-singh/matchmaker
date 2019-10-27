import os
import pandas as pd
from sqlalchemy.ext.automap import automap_base
#from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask, render_template, request, redirect, session

from config import pguser, pgpassword, pghost, pgport, pgdatabase, secret_key

engine = create_engine(
    f"postgresql+psycopg2://{pguser}:{pgpassword}" + \
    f"@{pghost}:{pgport}/{pgdatabase}"
)

#############################
#       SET UP DATABASE     #
#############################
df = pd.read_sql('matchdata',
                 engine)

users = pd.read_sql('Users',
                    engine)

Base = automap_base()

# reflect the tables
Base.prepare(engine,
             reflect=True)


#############################
#     HELPFUL FUNCTIONS     #
#############################

def emailExists(email):
    u = users.loc[users['email'] == email]

    return bool(u.shape[0])

def nextIID():
    iids = users['iid'].to_list()
    iids = [int(iid) for iid in iids]
    return str(max(iids) + 1)


app = Flask(__name__)

app.secret_key = secret_key

# Homepage
@app.route("/")
def homepage():
    """Return the homepage."""

    # Format the data to send as json
    return render_template("index.html")

# Query the database and send the jsonified results
@app.route("/login", methods=["GET", "POST"])
def login():
    """Return the login page."""
    if request.method == "POST":
        email    = request.form["userEmail"]
        password = request.form["userPassword"]
        session['email'] = email

        if emailExists(email):
            iid = users.loc[users['email'] == f'{email}']
            return render_template("matches.html",
                                   iid=iid)
        else:
            return render_template("register.html")

    return render_template("login.html")

# Register
# TODO: Set this up so that you can either pass the details or start new
@app.route("/register", methods=["GET", "POST"])
def register():
    """Return the registration page."""
    if request.method == "POST":
        return render_template('register.html')

    # Format the data to send as json
    return render_template("register.html")


if __name__ == "__main__":
    app.run()
