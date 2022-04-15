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
    if 'voornaam' in session:
        return render_template('home.html', loggedInUser=session['voornaam'])
    else:
        return render_template('home.html', loggedInUser="niet ingelogd")

@app.route('/login')
def login():
    return render_template('login.html', pwLabelKleur="black", uLabelKleur="black")

@app.route('/app/login', methods=['POST'])
def login_user():
    # Get the form data
    voornaam = request.form['voornaam']
    achternaam = request.form['achternaam']
    password = request.form['password']

    # Check if the username exists
    user_id = do_database(f"SELECT COUNT(student_ID) FROM student WHERE voornaam = '{voornaam}'")
    if user_id[0][0] == 0:
        return render_template('login.html', uMessage=" does not exist", pwMessage=" is incorrect", uLabelKleur="red", pwLabelKleur="red")
    
    # Check if the username exists
    user_id = do_database(f"SELECT COUNT(student_ID) FROM student WHERE achternaam = '{achternaam}'")
    if user_id[0][0] == 0:
        return render_template('login.html', uMessage=" does not exist", pwMessage=" is incorrect", uLabelKleur="red", pwLabelKleur="red")

    # Check if the password is correct
    user_password = do_database(f"SELECT password FROM student WHERE voornaam = '{voornaam}' AND achternaam = '{achternaam}'")
    if not bcrypt.check_password_hash(user_password[0][0], password):
        return render_template('login.html', pwMessage=" is incorrect", pwLabelKleur="red")

    # If the username and password are correct, log the user in and set the session
    session['voornaam'] = voornaam

    # Return user to home page
    return redirect('/')

@app.route('/logout')
def logout():
    # Check if the user is logged in
    if 'voornaam' in session:
        # Remove the username from the session
        session.pop('voornaam', None)
    return redirect('/')

@app.route('/register')
def register():
    return render_template('register.html', uLabelKleur="black")

@app.route('/app/register', methods=['POST'])
def register_user():
    # Get the form data
    student_ID = request.form['student_ID']
    voornaam = request.form['voornaam']
    achternaam = request.form['achternaam']
    password = request.form['password']

    # Check if the first name already exists
    user_id = do_database(f"SELECT COUNT(student_ID) FROM student WHERE voornaam = '{voornaam}'")
    if user_id[0][0] != 0:
        return render_template('register.html', uMessage=" already exists", uLabelKleur="red")

    # Check if the last name already exists
    user_id = do_database(f"SELECT COUNT(student_ID) FROM student WHERE achternaam = '{achternaam}'")
    if user_id[0][0] != 0:
        return render_template('register.html', uMessage=" already exists", uLabelKleur="red")
    
    student_id = do_database(f"SELECT COUNT(student_ID) FROM student WHERE student_ID = '{student_ID}'")
    if student_id[0][0] != 0:
        return render_template('register.html', uMessage=" already exists", uLabelKleur="red")
    
    # check password not empty and hash the password
    if len(password) == 0:
        return render_template('register.html', pMessage=" must not be empty", pLabelKleur="red")
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    print(student_ID,voornaam,achternaam,hashed_password,password)
    # Add the user to the database
    do_database(f"INSERT INTO student (student_ID, voornaam, achternaam, password) VALUES ('{student_ID}','{voornaam}','{achternaam}','{hashed_password}')")

    # Log the user in
    session['voornaam'] = voornaam

    # Redirect to the home page
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)