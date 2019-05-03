from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from resellcalculator import calculate
from passlib.hash import sha256_crypt
from functools import wraps


app = Flask(__name__)
# Config MySQL
app.config['MYSQL_HOST'] = 'stockx.crtkis7w0hsc.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'stockx'
app.config['MYSQL_PASSWORD'] = 'stockx123'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)


class queryForm(Form):
    stockxLink = StringField('Stockx Link', [validators.Length(min=1, max=300)])


@app.route('/')
def index():
    return render_template('interactive.html')

@app.route('/background_process')
def background_process():
    stockxLink = request.args.get('proglang')
    tax = request.args.get('tax')
    print stockxLink
    notification_list = calculate(stockxLink, tax)
    return jsonify(result=notification_list)


#@app.route('/', methods=['GET','POST'])
#def index():
#    form = queryForm(request.form)
#    if request.method == 'POST' and form.validate():
#        stockxLink = form.stockxLink.data
#        stockxLinkList = stockxLink.split(" ")
#        trimmedStockxLink = stockxLinkList[-1]
#        print trimmedStockxLink
#        notification_list = calculate(trimmedStockxLink)
#        return '\n'.join(notification_list)
#    return render_template('index.html', form=form)

# About
@app.route('/about')
def about():
    return render_template('about.html')


# Contact
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Register Form Class
#class RegisterForm(Form):
#    name = StringField('Name', [validators.Length(min=1, max=50)])
#    username = StringField('Username', [validators.Length(min=4, max=25)])
#    email = StringField('Email', [validators.Length(min=6, max=50)])
#    password = PasswordField('Password', [
#        validators.DataRequired(),
#        validators.EqualTo('confirm', message='Passwords do not match')
#    ])
#    confirm = PasswordField('Confirm Password')
#
#
## User Register
#@app.route('/register', methods=['GET', 'POST'])
#def register():
#    form = RegisterForm(request.form)
#    if request.method == 'POST' and form.validate():
#        name = form.name.data
#        email = form.email.data
#        username = form.username.data
#        password = sha256_crypt.encrypt(str(form.password.data))
#
#        # Create cursor
#        cur = mysql.connection.cursor()
#
#        # Execute query
#        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
#
#        # Commit to DB
#        mysql.connection.commit()
#
#        # Close connection
#        cur.close()
#
#        flash('You are now registered and can log in', 'success')
#
#        return redirect(url_for('login'))
#    return render_template('register.html', form=form)
#
#
## User login
#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    if request.method == 'POST':
#        # Get Form Fields
#        username = request.form['username']
#        password_candidate = request.form['password']
#
#        # Create cursor
#        cur = mysql.connection.cursor()
#
#        # Get user by username
#        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
#
#        if result > 0:
#            # Get stored hash
#            data = cur.fetchone()
#            password = data['password']
#            name = data['name']
#
#            # Compare Passwords
#            if sha256_crypt.verify(password_candidate, password):
#                # Passed
#                session['logged_in'] = True
#                session['username'] = username
#                session['name'] = name
#
#                flash('You are now logged in', 'success')
#                return redirect(url_for('dashboard'))
#            else:
#                error = 'Invalid login'
#                return render_template('login.html', error=error)
#            # Close connection
#            cur.close()
#        else:
#            error = 'Username not found'
#            return render_template('login.html', error=error)
#
#    return render_template('login.html')
#
## Check if user logged in
#def is_logged_in(f):
#    @wraps(f)
#    def wrap(*args, **kwargs):
#        if 'logged_in' in session:
#            return f(*args, **kwargs)
#        else:
#            flash('Unauthorized, Please login', 'danger')
#            return redirect(url_for('login'))
#    return wrap
#
## Logout
#@app.route('/logout')
#@is_logged_in
#def logout():
#    session.clear()
#    flash('You are now logged out', 'success')
#    return redirect(url_for('login'))
#
## Dashboard
#@app.route('/dashboard')
#@is_logged_in
#def dashboard():
#    return render_template('dashboard.html')


if __name__ == '__main__':
    app.secret_key = 'mia20170117abc'
    app.run(host="0.0.0.0", port=80, debug=True)
    #app.run()
