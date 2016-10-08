from flask import Flask, render_template, request, redirect, flash
# mysqlconnector
from mysqlconnection import MySQLConnector
#regex
import re
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex = re.compile(r'')
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

@app.route('/register', methods=['POST'])
def registration():
    print(request.form)
    if len(request.form['first_name']) < 2 or len(request.form['last_name']) < 2:
        flash("Name must be 2 chars or longer")
    elif not email_regex.match(request.form['email']):
        flash("Invalid Email Address!")
    elif
    return redirect('/')

app.run(debug=True)
