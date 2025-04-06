import requests
from modules.auth import obter_token_valido
from modules.historico import salvar_historico
from modules.auth import carregar_token

def buscar_mercado_livre(produto, offset=0, limit=50, usar_token=True):
    headers = {}
    ACCESS_TOKEN = None

    if usar_token:
        ACCESS_TOKEN = obter_token_valido()
        if not ACCESS_TOKEN:
            print("Não foi possível obter um token válido.")
            return []
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        print(f"Token usado na requisição: {ACCESS_TOKEN}")  # <- só imprime se for usar

    url = f'https://api.mercadolibre.com/sites/MLB/search?q={produto}&offset={offset}&limit={limit}'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        resultados = response.json()["results"]
        #salvar_historico(produto, resultados)
        return resultados
    else:
        print(f"Erro ao buscar dados: {response.status_code} - {response.text}")
        return []

