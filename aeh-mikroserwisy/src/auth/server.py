import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL
import json

server = Flask(__name__)
mysql = MySQL(server)

# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))


@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401

    # check db for username and password
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username,)
    )

    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "invalid credentials", 401


@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )
    except:
        return "not authorized", 403

    return decoded, 200



@server.route('/users', methods=['GET'])
def read_users():
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT id,email, password FROM user;"
    )
    records = cur.fetchall()
    array=[]
    for record in records:
        entry = {
            "id": record[0],
            "email": record[1],
            "password": record[2]
        }
        array.append(entry)
    print(json.dumps(array,indent=2))
    cur.close()
    return json.dumps(array,indent=2), 200

@server.route('/users/update/<int:id>', methods=['POST'])
def update_users(id):
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT * FROM user WHERE id="+str(id)+";"
    )
    if res==0:
        return "No such entry", 200
    arg=request.args.to_dict()
    sql_query=""
    if "email" in arg:
        sql_query=sql_query+"email="+"\'"+arg['email']+"\'"+","
    if "password" in arg:
        sql_query=sql_query+"password="+"\'"+arg['password']+"\'"+","
    sql_query=sql_query[:-1]
    upd="UPDATE user SET "+sql_query+" WHERE id="+str(id)+";"
    cur = mysql.connection.cursor()
    res = cur.execute(
        upd
    )
    mysql.connection.commit()
    cur.close()
    return "Successfuly updated "+str(id),200

@server.route('/users/delete/<int:id>', methods=['POST'])
def delete_users(id):
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT * FROM user WHERE id="+str(id)+";"
    )
    if res==0:
        return "No such entry", 200
    delete = "DELETE FROM user WHERE id=" + str(id) + ";"
    cur = mysql.connection.cursor()
    res = cur.execute(
        delete
    )
    mysql.connection.commit()
    cur.close()
    return "Successfuly deleted "+str(id),200

@server.route('/users/create', methods=['POST'])
def create_users():
    cur = mysql.connection.cursor()
    arg = request.args.to_dict()
    sql_query = ""
    if "email" not in arg or "password" not in arg:
        return "Not enough data", 200
    sql_query = sql_query + "email=" + "\'" + arg['email'] + "\'" + ","
    sql_query = sql_query + "password=" + arg['password'] + ","
    create = "INSERT INTO user (email,password) VALUES (" +"\'"+ arg['email']+"\'" + "," + "\'" + arg['password'] + "\'" + ");"
    cur = mysql.connection.cursor()
    res = cur.execute(
        create
    )
    mysql.connection.commit()
    cur.close()
    return "Successfuly created", 200

def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz,
        },
        secret,
        algorithm="HS256",
    )

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
