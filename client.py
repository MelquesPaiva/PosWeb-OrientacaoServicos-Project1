import urllib.request as request
from faker import Faker
from time import sleep
import requests
import random

HOST="http://localhost:5002"
CHARGE_URL=f"{HOST}/charge"
ALIVE_URL=f"{HOST}/alive"
COUNTRY_OPTIONS=["br", "ar"]
COUNTRY_CURRENCY={
    "ar": "ARS",
    "br": "BRL",
}

def create_payment_data():
    fake = Faker()

    country = random.choice(COUNTRY_OPTIONS)
    auto_capture = False
    if random.randint(1, 2) == 1:
        auto_capture = True

    return {
        "customer_name": fake.name(),
        "customer_email": fake.email(),
        "amount": random.randint(100, 250),
        "country": country,
        "currency": COUNTRY_CURRENCY[country],
        "auto_capture": auto_capture
    }

def service_is_alive():
    content = None
    try:
        response = request.urlopen(ALIVE_URL)
        if response.code == 200:
            content = response.read().decode("utf-8")
    except Exception as e:
        print(f"ocorreu um erro acessando a url {ALIVE_URL}")

    return content == "Yes"


def send_payment_request(payment_data):
    result = requests.post(CHARGE_URL, json=payment_data)
    response = result.json()
    if result.status_code != 200:
        message = response["message"] if message in response else "Ocorreu um erro ao gerar o pagamento"
        print(message)
    elif response["status"] == "ERROR":
        print (response["message"])
    elif response["status"] == "SUCCESS":
        print (f"{response['message']}. Status do pagamento: {response['payment_status']} - País: {payment_data['country']}")
    else:
        print ("Ocorreu um erro inesperado")

if __name__ == "__main__":
    while True:
        if service_is_alive() == False:
            print("Serviço para processar pagamentos não está vivo")
        else:
            send_payment_request(payment_data=create_payment_data())

        sleep(10)
