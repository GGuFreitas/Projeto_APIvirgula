import requests
from modules.auth import obter_token_valido
from modules.historico import salvar_historico

def buscar_mercado_livre(produto, offset=0, limit=50):
    ACCESS_TOKEN = obter_token_valido()
    if not ACCESS_TOKEN:
        return []

    url = f'https://api.mercadolibre.com/sites/MLB/search?q={produto}&offset={offset}&limit={limit}'
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        resultados = response.json()["results"]
        salvar_historico(produto, resultados)
        return resultados
    else:
        print(f"Erro ao buscar dados: {response.status_code} - {response.text}")
        return []
