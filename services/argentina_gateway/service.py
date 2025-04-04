from flask import Flask, Response, request
import os
import mysql.connector

ALIVE="Yes"
DB="argentina_gateway_db"
DB_PASS=os.environ["DB_ARGENTINA_GATEWAY_PASS"]
DB_USER=os.environ["DB_ARGENTINA_GATEWAY_USER"]
DB_NAME="gateway"

service = Flask("argentina_gateway")

@service.get("/alive")
def isAlive():
    return Response(ALIVE, status=200, mimetype="text/plain")

@service.get("/ping_db")
def pingDb():
    cnx = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB, database=DB_NAME)
    cnx.close()

    return Response("Success", status=200, mimetype="text/plain")

if __name__ == "__main__":
    service.run(host="0.0.0.0", debug=True)