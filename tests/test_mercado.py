import requests
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def buscar_mercado_livre(produto, offset=0, limit=50):
    url = f'https://api.mercadolibre.com/sites/MLB/search?q={produto}&offset={offset}&limit={limit}'
    response = requests.get(url)

    if response.status_code == 200:
        resultados = response.json()["results"]
        
        return resultados
    else:
        print(f"Erro ao buscar dados: {response.status_code} - {response.text}")
        return []


buscar_mercado_livre("notebook")