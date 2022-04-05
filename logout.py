from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)

# Set the secret key (needed for session)
# Normally this would generate a random key like this:
# >>> import os
# >>> os.urandom(24)
# But I'm using a fixed key for this example

app.secret_key = "secret"

app.route('/logout')
def logout():
    # Check if the user is logged in
    if 'username' in session:
        # Remove the username from the session
        session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)