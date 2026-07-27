import requests
import time


SERVICES = [
    "http://api:5000/health",
    "http://cliente-service:5001/clientes",
    "http://pedido-service:5002/pedidos"
]


while True:

    for url in SERVICES:

        try:
            response = requests.get(url, timeout=5)

            print(
                url,
                response.status_code
            )

        except Exception as e:
            print(
                "Erro:",
                url,
                e
            )

    time.sleep(2)
