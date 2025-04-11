import requests

CHARGE_ENDPOINT = "http://brazillian_gateway:5000/charge"
PAYMENT_CANCELLED_STATUS = "ca"
PAYMENT_PENDING_STATUS = "pe"
PAYMENT_CONFIRMED_STATUS = "co"

def charge_payment(payment_data):
    brazil_request_data = {
        "amount": payment_data["amount"],
        "auto_capture": payment_data["auto_capture"],
        "customer_email": payment_data["customer_email"],
        "customer_name": payment_data["customer_name"] if "customer_name" in payment_data else "",
    }

    result = requests.post(CHARGE_ENDPOINT, json=brazil_request_data)
    if result.status_code != 200:
        return "ERROR", "Unable to process payment", PAYMENT_CANCELLED_STATUS

    response = result.json()

    if response["status"] == "NOT_FOUND":
        return "PAYMENT_DOES_NOT_EXISTS", "Payment does not exists", PAYMENT_CANCELLED_STATUS
    
    payment_status = PAYMENT_CONFIRMED_STATUS
    if response["payment"]["status"] == "pending":
        payment_status = PAYMENT_PENDING_STATUS

    return "SUCCESS", "Payment charged", payment_status

if __name__ == "__main__":
    charge_payment({
        "amount": 100,
        "customer_name": "Melques",
        "customer_email": "melque1703@gmail.com",
        "auto_capture": False
    })