import time
import requests
import random


services = [
    "http://api:5000/",
    "http://api:5000/users",
    "http://api:5000/erro",

    "http://cliente-service:5001/clientes",
    "http://pedido-service:5002/pedidos"
]


while True:

    url = random.choice(services)

    try:
        response = requests.get(url)

        print(
            f"{url} -> {response.status_code}",
            flush=True
        )

    except Exception as e:

        print(
            f"Erro chamando {url}: {e}",
            flush=True
        )


    time.sleep(2)
