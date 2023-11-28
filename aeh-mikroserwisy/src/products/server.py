import datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL
import json
from werkzeug.datastructures import ImmutableMultiDict

server = Flask(__name__)
mysql = MySQL(server)

# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))


@server.route('/products', methods=['GET'])
def products():
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT id,name, price, description FROM products;"
    )
    records = cur.fetchall()
    array=[]
    for record in records:
        entry = {
            "id": record[0],
            "name": record[1],
            "price": record[2],
            "description": record[3]
        }
        array.append(entry)
    print(json.dumps(array,indent=2))
    cur.close()
    return json.dumps(array,indent=2), 200

@server.route('/products/update/<int:id>', methods=['POST'])
def update_products(id):
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT * FROM products WHERE id="+str(id)+";"
    )
    if res==0:
        return "No such entry", 200
    arg=request.args.to_dict()
    sql_query=""
    if "name" in arg:
        sql_query=sql_query+"name="+"\'"+arg['name']+"\'"+","
    if "price" in arg:
        sql_query=sql_query+"price="+arg['price']+","
    if "description" in arg:
        sql_query=sql_query+"description="+"\'"+arg['description']+"\'"+","
    sql_query=sql_query[:-1]
    upd="UPDATE products SET "+sql_query+" WHERE id="+str(id)+";"
    cur = mysql.connection.cursor()
    res = cur.execute(
        upd
    )
    mysql.connection.commit()
    cur.close()
    return "Successfuly updated "+str(id),200

@server.route('/products/delete/<int:id>', methods=['POST'])
def delete_products(id):
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT * FROM products WHERE id="+str(id)+";"
    )
    if res==0:
        return "No such entry", 200
    delete = "DELETE FROM products WHERE id=" + str(id) + ";"
    cur = mysql.connection.cursor()
    res = cur.execute(
        delete
    )
    mysql.connection.commit()
    cur.close()
    return "Successfuly deleted "+str(id),200

@server.route('/products/create', methods=['POST'])
def create_products():
    cur = mysql.connection.cursor()
    arg = request.args.to_dict()
    sql_query = ""
    if "name" not in arg or "price" not in arg or "description" not in arg:
        return "Not enough data", 200
    sql_query = sql_query + "name=" + "\'" + arg['name'] + "\'" + ","
    sql_query = sql_query + "price=" + arg['price'] + ","
    sql_query = sql_query + "description=" + "\'" + arg['description'] + "\'"
    create = "INSERT INTO products (name,price,description) VALUES (" +"\'"+ arg['name']+"\'" + "," + arg['price'] + "," + "\'"+arg[
        'description']+"\'" + ");"
    cur = mysql.connection.cursor()
    res = cur.execute(
        create
    )
    mysql.connection.commit()
    cur.close()
    return "Successfuly created", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5001)
