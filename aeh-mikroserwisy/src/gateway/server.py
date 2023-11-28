import os, json, requests
from flask import Flask, request, send_file
from auth import validate
from auth_svc import access

server = Flask(__name__)


@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err

@server.route("/", methods=["GET"])
def home():
    access, err = validate.token(request)

    if err:
        return err

    access = json.loads(access)

    response = requests.get(
        f"http://{os.environ.get('PRODUCTS_ADDRESS')}/products"
    )

    return response.content

@server.route("/crud/products", methods=["POST"])
def crud_products():
    access, err = validate.token(request)

    if err:
        return err

    access = json.loads(access)

    if access["admin"]:
        arg=request.args.to_dict()
        if arg['action']=='create':
            response = requests.post(
                f"http://{os.environ.get('PRODUCTS_ADDRESS')}/products/create?name={arg['name']}&price={arg['price']}&description={arg['description']}"
            )

            return response.status_code
        elif arg['action']=='delete':
            response = requests.post(
                f"http://{os.environ.get('PRODUCTS_ADDRESS')}/products/delete/{arg['id']}"
            )

            return response.status_code
        elif arg['action']=='update':
            response = requests.post(
                f"http://{os.environ.get('PRODUCTS_ADDRESS')}/products/update/{arg['id']}?name={arg['name']}&price={arg['price']}&description={arg['description']}"
            )

            return response.status_code

    else:
        return "not authorized", 401

@server.route("/crud/users", methods=["POST","GET"])
def crud_users():
    access, err = validate.token(request)

    if err:
        return err

    access = json.loads(access)
    if access["admin"]:
        if request.method == 'GET':
            response = requests.get(
                f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/users"
            )
            return response.content
        arg=request.args.to_dict()
        if arg['action']=='create':
            response = requests.post(
                f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/users/create?email={arg['email']}&password={arg['password']}"
            )

            return response.status_code
        elif arg['action']=='delete':
            response = requests.post(
                f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/users/delete/{arg['id']}"
            )

            return response.status_code
        elif arg['action']=='update':
            response = requests.post(
                f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/users/update/{arg['id']}?email={arg['email']}&password={arg['password']}"
            )

            return response.status_code


    else:
        return "not authorized", 401

@server.route("/signup", methods=["POST"])
def signup():
    arg = request.args.to_dict()
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/users/create?email={arg['email']}&password={arg['password']}"
    )

    return response.status_code

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
