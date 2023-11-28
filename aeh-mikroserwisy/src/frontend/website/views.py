from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user
from . import  app
import jwt
from .auth import require_api_token
from .functions import decodeFlaskCookie
import requests,json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
@require_api_token
def home():
    try:
        flask_cookie = request.cookies['session']
        cookie=decodeFlaskCookie(secret_key=app.secret_key,cookieValue=flask_cookie)
        bearer='Bearer '+cookie
        print(bearer)
        response = requests.get(
            f"http://aehmikroserwisy.com/", headers={'Authorization': bearer}
        )
    except:
        return redirect(url_for('auth.login'))
    if response.status_code!=200:
        return redirect(url_for('auth.login'))
    encoded_json=response.content
    my_json = encoded_json.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    final_data = json.dumps(data, indent=4, sort_keys=True)
    dict_json=json.loads(final_data)
    print(dict_json)
    return render_template("home.html", products=dict_json, session=session['api_session_token'])

@views.route('/crud/products', methods=['GET','POST'])
@require_api_token
def crud_products():
    if request.method == 'GET':
        try:
            flask_cookie = request.cookies['session']
            cookie=decodeFlaskCookie(secret_key=app.secret_key,cookieValue=flask_cookie)
            bearer='Bearer '+cookie
            print(bearer)
            response = requests.get(
                f"http://aehmikroserwisy.com/", headers={'Authorization': bearer}
            )
        except:
            return redirect(url_for('views.home'))
        if response.status_code!=200:
            return redirect(url_for('views.home'))
        encoded_json=response.content
        my_json = encoded_json.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        final_data = json.dumps(data, indent=4, sort_keys=True)
        dict_json=json.loads(final_data)
        print(dict_json)
        return render_template("crud_products.html", products=dict_json, session=session['api_session_token'])
    else:
        try:
            flask_cookie = request.cookies['session']
            cookie=decodeFlaskCookie(secret_key=app.secret_key,cookieValue=flask_cookie)
            bearer='Bearer '+cookie
            if request.form.get('delete'):
                id_to_delete=request.form.get('delete')
                response = requests.post(
                    f"http://aehmikroserwisy.com/crud/products?action=delete&id={id_to_delete}", headers={'Authorization': bearer}
                )
            elif request.form.get('update_id'):
                id_to_update=request.form.get('update_id')
                name_to_update = request.form.get('update_name')
                price_to_update = request.form.get('update_price')
                description_to_update = request.form.get('update_description')
                response = requests.post(
                    f"http://aehmikroserwisy.com/crud/products?action=update&name={name_to_update}&id={id_to_update}&price={price_to_update}&description={description_to_update}", headers={'Authorization': bearer}
                )
            else:
                name_to_create = request.form.get('name')
                price_to_create = request.form.get('price')
                description_to_create = request.form.get('description')
                response = requests.post(
                    f"http://aehmikroserwisy.com/crud/products?action=create&name={name_to_create}&price={price_to_create}&description={description_to_create}",
                    headers={'Authorization': bearer}
                )
            return redirect(url_for('views.crud_products'))
        except:
            return redirect(url_for('views.home'))
        if response.status_code!=200:
            return redirect(url_for('views.home'))
        encoded_json=response.content
        my_json = encoded_json.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        final_data = json.dumps(data, indent=4, sort_keys=True)
        dict_json=json.loads(final_data)
        print(dict_json)
        return render_template("crud_products.html", products=dict_json, session=session['api_session_token'])

@views.route('/crud/users', methods=['GET','POST'])
@require_api_token
def crud_users():
    if request.method == 'GET':
        try:
            flask_cookie = request.cookies['session']
            cookie=decodeFlaskCookie(secret_key=app.secret_key,cookieValue=flask_cookie)
            bearer='Bearer '+cookie
            print(bearer)
            response = requests.get(
                f"http://aehmikroserwisy.com/crud/users", headers={'Authorization': bearer}
            )
        except:
            return redirect(url_for('views.home'))
        if response.status_code!=200:
            return redirect(url_for('views.home'))
        encoded_json=response.content
        print(encoded_json)
        my_json = encoded_json.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        final_data = json.dumps(data, indent=4, sort_keys=True)
        dict_json=json.loads(final_data)
        print(dict_json)
        return render_template("crud_users.html", users=dict_json, session=session['api_session_token'])
    else:
        try:
            flask_cookie = request.cookies['session']
            cookie=decodeFlaskCookie(secret_key=app.secret_key,cookieValue=flask_cookie)
            bearer='Bearer '+cookie
            if request.form.get('delete'):
                id_to_delete=request.form.get('delete')
                response = requests.post(
                    f"http://aehmikroserwisy.com/crud/users?action=delete&id={id_to_delete}", headers={'Authorization': bearer}
                )
            elif request.form.get('update_id'):
                id_to_update=request.form.get('update_id')
                email_to_update = request.form.get('update_email')
                password_to_update = request.form.get('update_password')
                response = requests.post(
                    f"http://aehmikroserwisy.com/crud/users?action=update&email={email_to_update}&id={id_to_update}&password={password_to_update}", headers={'Authorization': bearer}
                )
            else:
                email_to_create = request.form.get('email')
                password_to_create = request.form.get('password')
                response = requests.post(
                    f"http://aehmikroserwisy.com/crud/users?action=create&email={email_to_create}&password={password_to_create}",
                    headers={'Authorization': bearer}
                )
            return redirect(url_for('views.crud_users'))
        except:
            return redirect(url_for('views.home'))
        if response.status_code!=200:
            return redirect(url_for('views.home'))
        encoded_json=response.content
        my_json = encoded_json.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        final_data = json.dumps(data, indent=4, sort_keys=True)
        dict_json=json.loads(final_data)
        print(dict_json)
        return render_template("crud_users.html", products=dict_json, session=session['api_session_token'])

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')