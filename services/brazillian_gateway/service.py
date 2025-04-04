from flask import Flask, Response, request
import os

ALIVE="Yes"
DB="brazillian_gateway_db"
DB_PASS=os.environ["DB_BRAZILLIAN_GATEWAY_PASS"]
DB_USER=os.environ["DB_BRAZILLIAN_GATEWAY_USER"]
DB_NAME="gateway"

service = Flask("brazillian_gateway")

@service.get("/alive")
def isAlive():
    return Response(ALIVE, status=200, mimetype="text/plain")

if __name__ == "__main__":
    service.run(host="0.0.0.0", debug=True)
