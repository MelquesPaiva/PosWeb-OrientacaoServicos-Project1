from datetime import datetime
import mysql.connector
import os

DB="payment_processor_db"
DB_PASS=os.environ["DB_PAYMENT_PROCESSOR_PASS"]
DB_USER=os.environ["DB_PAYMENT_PROCESSOR_USER"]
DB_NAME="payment_processor"

def mysql_conn():
    return mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB, database=DB_NAME)    

def create_payment(payment_data):
    if "customer_name" not in payment_data:
        payment_data["customer_name"] = "Not informed"

    create_payment_sql = ("INSERT INTO payments"
                          "(status, amount, customer_email, customer_name, created_at, confirmed_at, cancelled_at) "
                          "VALUES (%(status)s, %(amount)s, %(customer_email)s, %(customer_name)s, %(created_at)s, %(confirmed_at)s, %(cancelled_at)s)")
    conn = mysql_conn()
    cursor = conn.cursor(dictionary=True)
    payment_data["created_at"] = datetime.today()
    payment_data["confirmed_at"] = None
    payment_data["cancelled_at"] = None

    if payment_data["status"] == "co":
        payment_data["confirmed_at"] = payment_data["created_at"]
    elif payment_data["status"] == "ca":
        payment_data["cancelled_at"] = payment_data["created_at"]

    cursor.execute(create_payment_sql, payment_data)

    conn.commit()
    cursor.close()
    conn.close()
