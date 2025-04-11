from flask import Flask, Response, request
from datetime import datetime
import os
import mysql.connector
import json

ALIVE="Yes"
DB="brazillian_gateway_db"
DB_PASS=os.environ["DB_BRAZILLIAN_GATEWAY_PASS"]
DB_USER=os.environ["DB_BRAZILLIAN_GATEWAY_USER"]
DB_NAME="gateway"

service = Flask("brazillian_gateway")

@service.get("/alive")
def is_alive():
    return Response(ALIVE, status=200, mimetype="text/plain")

def mysql_conn():
    return mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB, database=DB_NAME)    

@service.get("/ping_db")
def ping_db():
    cnx = mysql_conn()
    cnx.close()

    return Response("Success", status=200, mimetype="text/plain")

@service.post("/charge")
def charge():
    response, status_code = {
        "status": "SUCCESS",
        "message": "Payment charged successfully",
        "payment": {},
    }, 200

    payment_data = request.get_json()
    if payment_data["amount"] is None or payment_data["amount"] == "" or payment_data["amount"] == 0:
        response["status"] = "ERROR"
        response["message"] = "Amount is required"
        return Response(json.dumps(response), status=400, mimetype="application/json")
    
    if payment_data["customer_email"] is None or payment_data["customer_email"] == "" or payment_data["customer_email"] == 0:
        response["status"] = "ERROR"
        response["message"] = "Customer email is required"
        return Response(json.dumps(response), status=400, mimetype="application/json")
    
    if "customer_name" not in payment_data:
        payment_data["customer_name"] = "Not informed"

    create_payment_sql = ("INSERT INTO payments"
                          "(status, amount, customer_email, customer_name, created_at, confirmed_at, cancelled_at) "
                          "VALUES (%(status)s, %(amount)s, %(customer_email)s, %(customer_name)s, %(created_at)s, %(confirmed_at)s, %(cancelled_at)s)")
    conn = mysql_conn()
    cursor = conn.cursor()
    payment_data["created_at"] = datetime.today()
    payment_data["confirmed_at"] = None
    payment_data["cancelled_at"] = None

    try:
        payment_data["status"] = "pending"
        if payment_data["auto_capture"] == True:
            payment_data["status"] = "confirmed"
            payment_data["confirmed_at"] = payment_data["created_at"]
    except mysql.connector.Error as err:
        return Response(status=500, mimetype="application/json")
    except Exception as e:
        response.status = "ERROR"
        response.message = "Unexpected error"
        status_code = 500
        payment_data["status"] = "cancelled"
        payment_data["cancelled_at"] = payment_data["created_at"]

    cursor.execute(create_payment_sql, payment_data)

    response["payment"] = {
        "status": payment_data["status"]
    }

    conn.commit()
    cursor.close()
    conn.close()
    return Response(json.dumps(response), status=status_code, mimetype="application/json")

@service.get("/query")
def query():
    response = {
        "status": "SUCCESS",
        "message": "Payment recovered successfully",
    }
    id = request.args.get('id')
    if id == None or id == 0:
        response["status"] = "ERROR"
        response["message"] = "Inform the payment id"
        return Response(json.dumps(response), status=400, mimetype="application/json")

    conn = mysql_conn()
    cursor = conn.cursor(dictionary=True)
    query_sql = "SELECT id, amount, customer_name, created_at, confirmed_at, cancelled_at FROM payments WHERE id = %s"
    result = {}
    try:
        cursor.execute(query_sql, (id,))
        result = cursor.fetchone()
    except mysql.connector.Error as err:
        return Response(status=500, mimetype="application/json")
    finally:
        cursor.close()
        conn.close()

    if result is None:
        response["status"] = "NOT_FOUND"
        response["message"] = "Payment not found"
        return Response(json.dumps(response), status=200, mimetype="application/json")

    final_result = {
        "id": result["id"],
        "amount": result["amount"],
        "customer_email": result["customer_email"],
        "customer_name": result["customer_name"] if result["customer_name"] is not None else "Not informed",
        "created_at": result["created_at"].strftime('%Y-%m-%d %H:%I:%S'),
        "confirmed_at": result["confirmed_at"].strftime('%Y-%m-%d %H:%I:%S') if result["confirmed_at"] is not None else "",
        "cancelled_at": result["cancelled_at"].strftime('%Y-%m-%d %H:%I:%S') if result["cancelled_at"] is not None else "",
    }

    response["payment"] = final_result

    return Response(json.dumps(response), status=200, mimetype="application/json")

if __name__ == "__main__":
    service.run(host="0.0.0.0", debug=True)
