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
        loggedIn=True
        loggedInUser=session['voornaam']
    else:
        loggedIn=False
        loggedInUser="niet ingelogd"
    return render_template('home.html', loggedInUser=loggedInUser, loggedIn=loggedIn)

@app.route('/login')
def login():
    return render_template('login.html', pwLabelKleur="black", uLabelKleur="black")

@app.route('/app/login', methods=['POST'])
def login_user():
    # Get the form data
    voornaam = request.form['voornaam']
    achternaam = request.form['achternaam']
    password = request.form['password']
    begleider = request.form.get('begleider')
    if begleider == None:
        begleider = False
    if begleider == False:
        # Check if the username exists
        user_id = do_database(f"SELECT COUNT(student_ID) FROM student WHERE voornaam = '{voornaam}'")
        if user_id[0][0] == 0:
            return render_template('login.html', uMessage=" does not exist", pwMessage=" is incorrect", uLabelKleur="red", pwLabelKleur="red")

        # Check if the username exists
        user_id = do_database(f"SELECT COUNT(student_ID) FROM student WHERE achternaam = '{achternaam}'")
        if user_id[0][0] == 0:
            return render_template('login.html', uMessage=" does not exist", pwMessage=" is incorrect", uLabelKleur="red", pwLabelKleur="red")

        student_ID = do_database(f"SELECT student_ID FROM student WHERE voornaam = '{voornaam}' AND achternaam = '{achternaam}'")
        # Check if the password is correct
        user_password = do_database(f"SELECT password FROM student WHERE voornaam = '{voornaam}' AND achternaam = '{achternaam}'")
        if not bcrypt.check_password_hash(user_password[0][0], password):
            return render_template('login.html', pwMessage=" is incorrect", pwLabelKleur="red")
        session['student_ID'] = student_ID
    else:
        # Check if the username exists
        user_id = do_database(f"SELECT COUNT(ID) FROM begleider WHERE voornaam = '{voornaam}'")
        if user_id[0][0] == 0:
            return render_template('login.html', uMessage=" does not exist", pwMessage=" is incorrect", uLabelKleur="red", pwLabelKleur="red")

        # Check if the username exists
        user_id = do_database(f"SELECT COUNT(ID) FROM begleider WHERE achternaam = '{achternaam}'")
        if user_id[0][0] == 0:
            return render_template('login.html', uMessage=" does not exist", pwMessage=" is incorrect", uLabelKleur="red", pwLabelKleur="red")

        # Check if the password is correct
        user_password = do_database(f"SELECT password FROM begleider WHERE voornaam = '{voornaam}' AND achternaam = '{achternaam}'")
        if not bcrypt.check_password_hash(user_password[0][0], password):
            return render_template('login.html', pwMessage=" is incorrect", pwLabelKleur="red")

    # If the username and password are correct, log the user in and set the session
    session['voornaam'] = voornaam
    session['achternaam'] = achternaam
    session['begleider'] = begleider
    print(session['voornaam'], session['begleider'])

    # Return user to home page
    return redirect('/')
    
@app.route('/logout')
def logout():
    # Check if the user is logged in
    if 'voornaam' in session:
        # Remove the username from the session
        session.pop('voornaam', None)
    if 'achternaam' in session:
        session.pop('achternaam', None)
    if 'student_ID' in session:
        session.pop('student_ID', None)
    if 'begleider' in session:
        session.pop('begleider', None)
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
    password2 = request.form['password2']

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
    elif password != password2:
        return render_template('register.html', pMessage=" is not the same", pLabelKleur="red")
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Add the user to the database
    do_database(f"INSERT INTO student (student_ID, voornaam, achternaam, password) VALUES ('{student_ID}','{voornaam}','{achternaam}','{hashed_password}')")

    # Log the user in
    session['voornaam'] = voornaam
    session['achternaam'] = achternaam
    session['student_ID'] = student_ID

    # Redirect to the home page
    return redirect('/')

@app.route('/stageGegevens')
def stage_gegevens():
    if 'voornaam' in session:
        loggedIn=True
        loggedInUser=session['voornaam']
    else:
        loggedIn=False
        loggedInUser="niet ingelogd"

    if loggedIn:
        do_database(f"SELECT * FROM stage voornaam = 'session['voornaam']' AND achternaam = 'session['achternaam']'")
        return render_template('stageGegevens.html', loggedInUser=loggedInUser, loggedIn=loggedIn)
    elif loggedIn!=True:
        return render_template('nietIngelogd.html')

@app.route('/stages')
def stages():
    if 'voornaam' in session:
        loggedIn=True
        loggedInUser=session['voornaam']
    else:
        loggedIn=False
        loggedInUser="niet ingelogd"
        
    stageInfo = do_database(f"SELECT si.ID, si.instelling_ID, ins.instellingType, ins.instellingNaam, si.begleider_ID, beg.voornaam, beg.achternaam,  si.omschrijving FROM stageInfo AS si JOIN instelling AS ins ON si.instelling_ID = ins.ID JOIN begleider AS beg ON si.begleider_ID = beg.ID")
    aantalStage = len(stageInfo)
    return render_template('stages.html', loggedInUser=loggedInUser, loggedIn=loggedIn, stageInfo=stageInfo, aantalStage=aantalStage)

@app.route('/stage/edit')
def stage_edit():
    if 'begleider' in session:
        loggedIn=True
        loggedInUser=session['begleider']
    else:
        loggedIn=False
        loggedInUser="Geen begeleider"

    if loggedIn:
        stageInfo = do_database(f"SELECT si.ID, si.instelling_ID, ins.instellingType, ins.instellingNaam, si.begleider_ID, beg.voornaam, beg.achternaam,  si.omschrijving FROM stageInfo AS si JOIN instelling AS ins ON si.instelling_ID = ins.ID JOIN begleider AS beg ON si.begleider_ID = beg.ID")
        aantalStage = len(stageInfo)
        return render_template('edit.html', loggedInUser=loggedInUser, loggedIn=loggedIn, stageInfo=stageInfo, aantalStage=aantalStage)

    elif loggedIn!=True:
        return render_template('nietIngelogd.html')

if __name__ == '__main__':
    app.run(debug=True)