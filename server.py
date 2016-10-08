from flask import Flask, render_template, request, redirect, flash
# mysqlconnector
from mysqlconnection import MySQLConnector
#regex
import re
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
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

# connect and store the connection in "mysql" note that you pass the database name to the function
mysql = MySQLConnector(app, 'friendships')
# an example of running a query
print mysql.query_db("SELECT * FROM users")
app.run(debug=True)
