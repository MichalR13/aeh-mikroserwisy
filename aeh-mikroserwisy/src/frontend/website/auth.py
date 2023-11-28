from flask import Blueprint, render_template, request, flash, redirect, url_for, session, wrappers
from flask_login import login_user, login_required, logout_user
import requests
from functools import wraps


auth = Blueprint('auth', __name__)

def require_api_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        # Check to see if it's in their session
        if 'api_session_token' not in session:
            # If it isn't return our access denied message (you can also return a redirect or render_template)
            return "Access denied"

        # Otherwise just send them where they wanted to go
        return func(*args, **kwargs)

    return check_token

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(email)
        response = requests.post(
            f"http://aehmikroserwisy.com/login", auth=(email, password)
        )
        jwttoken=response.text
        print(jwttoken)
        session['api_session_token'] = jwttoken
        return redirect(url_for('views.home'))
    session['api_session_token'] = ""
    return render_template("login.html", session=session['api_session_token'])

@auth.route('/logout')
def logout():
    session['api_session_token']=''
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1!=password2:
            return render_template("sign_up.html")
        response = requests.post(
            f"http://aehmikroserwisy.com/signup?email={email}&password={password1}"
        )
        return redirect(url_for('auth.login'))


    return render_template("sign_up.html", session=session['api_session_token'])