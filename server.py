from flask import Flask, render_template, request, redirect, flash
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

@app.route('/')
def index():
    return render_template('/index.html')
@app.route('/login', methods=['POST'])
def login():
    user_query = "SELECT * FROM users WHERE email = :email"
    user_data = {
        'email': request.form['email']
    }
    user = mysql.query_db(user_query, user_data)[0]
    print(user['pw_hash'])
    if bcrypt.check_password_hash(user['pw_hash'], request.form['pw']):
        flash("Password Correct")
        return render_template('/success.html')
    else:
        flash("Wrong password")
        return redirect('/')

# Handles Registration
@app.route('/register', methods=['POST'])
def registration():
    print(request.form)
    if not name_regex.match(request.form['first_name']) or not name_regex.match(request.form['last_name']):
        flash("Invalid first or last name")
    if not email_regex.match(request.form['email']):
        flash("Invalid Email Address!")
    else:
        flash("New user successfully registered")
        pw_hash = bcrypt.generate_password_hash(request.form['pw'])
        print(pw_hash)
        query = "INSERT INTO users (first_name, last_name, email, pw_hash, created_at, updated_at) VALUES (:first_name, :last_name, :email, :pw_hash, Now(), Now());"
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'pw_hash': pw_hash
        }
        mysql.query_db(query, data)
        return render_template('/success.html')
    return redirect('/')

app.run(debug=True)
