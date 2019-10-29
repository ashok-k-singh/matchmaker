import pandas as pd
import numpy as np
import os

# psycopg2 doesn't like numpy datatypes without the following...
from psycopg2.extensions import register_adapter, AsIs
def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)
register_adapter(np.float64, addapt_numpy_float64)
register_adapter(np.int64, addapt_numpy_int64)

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from sqlalchemy import create_engine

from flask import Flask, flash, render_template
from flask import request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from flask_login import login_required, login_user
from flask_login import logout_user, current_user
from user import User

from config import pghost, pgport, pguser, pgpassword, pgdatabase
from sklearn.ensemble import RandomForestClassifier

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

# Build the machine learning model

# Get the matchmaker database and read into a dataframe
engine = create_engine(f"postgresql+psycopg2://{pguser}:{pgpassword}@{pghost}:{pgport}/{pgdatabase}")
connection = engine.connect()
matchsql = f'SELECT * FROM "matchdata"'
matchDate = pd.read_sql_query(matchsql,connection)
connection.close()

#Build the necessary data for the machine learning model
X_data = matchDate.drop(["couple_id","f_intrace","samerace", "match", "m_intrace"], axis=1)
X_data = X_data.round(decimals=0)
y_data = matchDate["match"]

#Split the data into train and test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, random_state=1, stratify=y_data)

#Using the Random Forest Model, fit and train the data
rfmodel = RandomForestClassifier(n_estimators=200)
rfmodel = rfmodel.fit(X_train, y_train)


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

# Route to Get the MatchData
@app.route('/matchdata')
@login_required
def matchdata():
  
    # Get the current user data
    my_df = pd.DataFrame(curr_user_profile, index=[0])

    #Get the other users data from the database 
    engine = create_engine(f"postgresql+psycopg2://{pguser}:{pgpassword}@{pghost}:{pgport}/{pgdatabase}")
    connection = engine.connect()
    # Get the database
    user_sql = f'SELECT * FROM "Users"'
    df = pd.read_sql_query(user_sql,connection)
    connection.close()
    
    # Get the opposite gender data to find the potential match 
    if (my_df["gender"][0] == 1):
        opp_df = df[df["gender"] == 0] 
        my_df["merge_gender"] = 0 
    else:
        opp_df = df[df["gender"] == 1]  
        my_df["merge_gender"] = 1 
    
    #Merge current user data with opposite gender data from the database  
    merge_df = pd.merge(opp_df, my_df, left_on='gender', right_on='merge_gender', how='left', suffixes=('_partner', '_user'))
    merge_df = merge_df.sort_values(by=['iid_partner'])

    #Prepare the data for running the model 
    X_match = merge_df[["age_partner", "imprace_partner", "attr_partner", "sinc_partner", "intel_partner", 
                "fun_partner", "amb_partner", "race_partner", "age_user", "imprace_user", 
                "attr_user", "sinc_user", "intel_user", "fun_user", "amb_user", "race_user"]]
    X_match = X_match.round(decimals=0)

    # Run the random foreset model to predict the matches 
    matches = rfmodel.predict(X_match)

    # build the iid list of partner matches  
    match_list = []
    for i in range(len(matches)):
        if matches[i] == 1:                    
                match_list.append(merge_df["iid_partner"][i]) 
    
    match_dictionary = getMatches(match_list)
    
    return jsonify(match_dictionary)

# Callback used to reload user object from the user ID stored in the session
@login_manager.user_loader
def load_user(email):
    users_password = curr_user_profile['password']
    if users_password:
        return User(email)

def getMatches(iid_list):
    # first build a list of matches from the list of iids  
    match_list = [session.query(Users).filter_by(iid=iid).one() for iid in iid_list]

    # now build a list of dictionaries for the matches.js function
    matches = []
    for match in match_list:
        matches.append({'screenname': match.screenname,
                        'age': int(match.age),
                        'email': match.email,
                        'photo': match.photo})
    return matches

if __name__ == "__main__":
    app.run(debug=True)
