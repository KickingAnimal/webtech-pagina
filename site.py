from flask import Flask, render_template, redirect, request, session
from flask_bcrypt import Bcrypt
from database import *

bcrypt = Bcrypt()
app = Flask(__name__)

# Set the secret key (needed for session)
# Normally this would generate a random key like this:
# >>> import os
# >>> os.urandom(24)
# But I'm using a fixed key for this example

app.secret_key = "secret"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/app/login', methods=['POST'])
def login_user():
    # Get the form data
    username = request.form['username']
    password = request.form['password']

    # Check if the username exists
    user_id = do_database(f"SELECT COUNT(id) FROM users WHERE username = '{username}'")
    if user_id[0][0] == 0:
        return render_template('login.html')#, message="Username does not exist")
    
    # Check if the password is correct
    user_password = do_database(f"SELECT password FROM users WHERE username = '{username}'")
    if not bcrypt.check_password_hash(user_password[0][0], password):
        return render_template('login.html') #, message="Password is incorrect")

    # If the username and password are correct, log the user in and set the session
    session['username'] = username

    # Return user to home page
    return redirect('/')

app.route('/logout')
def logout():
    # Check if the user is logged in
    if 'username' in session:
        # Remove the username from the session
        session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)