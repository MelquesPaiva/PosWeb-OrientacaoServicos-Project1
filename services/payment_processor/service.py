from flask import Flask, Response, request
from datetime import datetime
from brazil import charge_payment as brazil_charge_payment
from argentina import charge_payment as argentina_charge_payment
from validate_request import validate_request
import json
from db.db import create_payment

ALIVE="Yes"

service = Flask("payment_processor")

@service.get("/alive")
def is_alive():
    return Response(ALIVE, status=200, mimetype="text/plain")

@service.post("/charge")
def charge():
    response, status_code = {
        "status": "SUCCESS",
        "message": "Payment was charged successfully",
        "payment_status": ""
    }, 200

    payment_data = request.get_json()

    valid, message = validate_request(payment_data=payment_data)
    if valid is False:
        response["status"] = "ERROR"
        response["message"] = message
        return Response(json.dumps(response), status=400, mimetype="application/json")
        
    if payment_data["country"] == "ar":
        status, message, payment_status = argentina_charge_payment(payment_data=payment_data)
        payment_data["status"] = payment_status
        response["status"] = status
        response["message"] = message
        response["payment_status"] = payment_status

        create_payment(payment_data=payment_data)

        return response
    
    if payment_data["country"] == "br":
        status, message, payment_status = brazil_charge_payment(payment_data=payment_data)
        payment_data["status"] = payment_status
        response["status"] = status
        response["message"] = message
        response["payment_status"] = payment_status

        create_payment(payment_data=payment_data)

        return response

    response["status"] = "ERROR"
    response["message"] = "Invalid country"
    return Response(json.dumps(response), status=400, mimetype="application/json")

if __name__ == "__main__":
    service.run(host="0.0.0.0", debug=True)
