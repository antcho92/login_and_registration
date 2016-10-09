from flask import Flask, render_template, request, redirect, flash, session
# mysqlconnector
from mysqlconnection import MySQLConnector
#regex
import re
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#found a name regex from online
name_regex = re.compile(r'^[A-Z][-a-zA-Z]+$')
#import bcrypt
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "mysecretkey"

# connect and store connection in mysql
mysql = MySQLConnector(app, 'login_and_registration')

# Moving my validations to a function that can be called for login and registration. Not working at the moment
def validate(email, first_name, last_name, password):
    if email and not email_regex.match(request.form['email']):
        flash("Invalid Email Address!")
    if first_name and not name_regex.match(request.form['first_name']):
        flash("Invalid first name")
    if last_name and not name_regex.match(request.form['last_name']):
        flash("Invalid last name")
    if password and len(password) < 8:
        flash("Password must be over 8 characters")

# For keeping user logged in
def logged_in(pw_hash):
    query = "SELECT * FROM users WHERE pw_hash=:pw_hash and email=:email"
    data = {
        'pw_hash': pw_hash,
        'email': request.form['email']
    }
    user = mysql.query_db(query, data)[0]
    session["user"] = user['id']
    print(session['user'])

# Index page with registration and login forms
@app.route('/')
def index():
    return render_template('/index.html')

# Handles login of user
@app.route('/login', methods=['POST'])
def login():
    if request.form['email']:
        user_query = "SELECT * FROM users WHERE email = :email"
        user_data = {
            'email': request.form['email']
        }
        user = mysql.query_db(user_query, user_data)[0]
        print(user['pw_hash'])
        if bcrypt.check_password_hash(user['pw_hash'], request.form['pw']):
            flash("Logged in Successfully")
            return render_template('/success.html')
    flash("Incorrect username or password")
    return redirect('/')

# Handles Registration
@app.route('/register', methods=['POST'])
def registration():
    #validates that there is an email present
    if not request.form['email']:
        flash("Please add an email")
    if not name_regex.match(request.form['first_name']) or not name_regex.match(request.form['last_name']):
        flash("Invalid first or last name")
    if not email_regex.match(request.form['email']):
        flash("Invalid Email Address!")
    if len(request.form['pw']) < 8:
        flash("Password must be greater than 8 characters")
    if request.form['pw'] != request.form['pw_confirmation']:
        flash("Password must match password confirmation")
    # Want to find a way to check if flash has messages in it
    else:
        flash("New user successfully registered")
        pw_hash = bcrypt.generate_password_hash(request.form['pw'])
        query = "INSERT INTO users (first_name, last_name, email, pw_hash, created_at, updated_at) VALUES (:first_name, :last_name, :email, :pw_hash, Now(), Now());"
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'pw_hash': pw_hash
        }
        mysql.query_db(query, data)
        logged_in(pw_hash);
        return render_template('/success.html')
    return redirect('/')

app.run(debug=True)
