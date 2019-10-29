from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct

from flask import Flask, flash, render_template
from flask import request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from flask_login import login_required, login_user
from flask_login import logout_user, current_user
from user import User

from config import pghost, pgport, pguser, pgpassword, pgdatabase

app = Flask(__name__)

# needed by flask_login
app.secret_key = 'tPXJY3X37Qybz4QykV+hOyUxVQeEXf1Ao2C8upz+fGQXKsM'
login_manager = LoginManager(app)

# to avoid browser to cache static assets served by Flask
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# database setup - step 1
db_uri = f'postgresql://{pguser}:{pgpassword}@{pghost}:{pgport}/{pgdatabase}'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db = SQLAlchemy(app)

# database setup - step 2
# reflect an existing database into a new model
Base = automap_base()

session = Session(db.engine)


# reflect the tables
# database setup - step 3
Base.prepare(db.engine, reflect=True)
# This fails because there is no user table
Users = Base.classes.Users

# this dictionary holds the current user profile
curr_user_profile = {'iid': -1,
                     'firstname': '',
                     'lastname': '',
                     'email': '',
                     'password': '',
                     'photo': '',
                     'gender': '',
                     'age': -1,
                     'race': -1,
                     'imprace': -1,
                     'attr': -1,
                     'sinc': -1,
                     'fun': -1,
                     'intel': -1,
                     'amb': -1  }

# function to initialize current user profile
def init_curr_user_profile():
    curr_user_profile = {'iid': -1,
                         'firstname': '',
                         'lastname': '',
                         'email': '',
                         'password': '',
                         'photo': '',
                         'gender': '',
                         'age': -1,
                         'race': -1,
                         'imprace': -1,
                         'attr': -1,
                         'sinc': -1,
                         'fun': -1,
                         'intel': -1,
                         'amb': -1  }


#################################################
# Routes definition
#################################################

# Route to Homepage
@app.route('/')
def home():
    """Go to the homepage"""
    return render_template("index.html")

# Route to Login
@app.route('/login', methods=["POST", "GET"])
def login():
    """For GET requests, display the login form.
    For POSTS, login the current user by processing the form.
    """
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        session = Session(db.engine)

        users_passwords = session.query(Users.password).filter(Users.email==email).first()
        if users_passwords: users_password=users_passwords[0]
        else: users_password=None

        if users_password and users_password == password:
            user = User(email)
            login_user(user, remember=True)

            # load user data from database into current user profile dictionary
            row = session.query(Users).filter(Users.email==current_user.email).first()
            for column in row.__table__.columns:
                curr_user_profile[column.name] = getattr(row, column.name)

            return redirect(url_for('matches'))
        else:
            flash(u'Invalid username or password', 'danger')
            return render_template("login.html")

# Route to Logout
@app.route('/logout')
def logout():
    logout_user()
    init_curr_user_profile
    return redirect(url_for("home"))

# Route to Update
@app.route('/update', methods=["POST", "GET"])
@login_required
def update():
    """For GET requests, display the signup form.
    For POSTS, login the current user by processing the form.
    """
    if request.method == 'GET':
        return render_template("update.html",
                               user_profile = curr_user_profile)

    elif request.method == 'POST':
        # load newly input form data into current user profile dictionary
        for key in curr_user_profile:
            if(key == 'iid'): continue  # omitting 'iid' field
            curr_user_profile[key] = request.form.get(key)

    return redirect(url_for('matches'))

# Route to Signup
@app.route('/signup', methods=["POST", "GET"])
def signup():
    """For GET requests, display the signup form.
    For POSTS, login the current user by processing the form.
    """
    if request.method == 'GET':
        return render_template("signup.html")
    elif request.method == 'POST':
        # load newly input form data into current user profile dictionary
        for key in curr_user_profile:
            if(key == 'iid'): continue  # omitting 'iid' field
            curr_user_profile[key] = request.form.get(key)

    # login new user
    user = User(curr_user_profile['email'])
    login_user(user, remember=True)

    return redirect(url_for('matches'))

# Route to Matches
@app.route('/matches')
@login_required
def matches():
    return render_template("matches.html", user_profile = curr_user_profile)

# Callback used to reload user object from the user ID stored in the session
@login_manager.user_loader
def load_user(email):
    users_password = curr_user_profile['password']
    if users_password:
        return User(email)


if __name__ == "__main__":
    app.run(debug=True)
