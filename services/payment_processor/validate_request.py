def validate_request(payment_data):
    if "amount" not in payment_data or payment_data["amount"] is None or payment_data["amount"] == "" or payment_data["amount"] == 0:
        return False, "Amount is required"
    
    if "customer_email" not in payment_data or payment_data["customer_email"] is None or payment_data["customer_email"] == "" or payment_data["customer_email"] == 0:
        return False, "Customer email is required"

    if "country" not in payment_data or payment_data["country"] is None or payment_data["country"] == "":
        return False, "Country is required"
    
    if "currency" not in payment_data or payment_data["currency"] is None or payment_data["currency"] == "":
        return False, "Currency is required"

    return True, ""    
