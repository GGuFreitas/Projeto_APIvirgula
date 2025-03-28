import requests
import json
import time
from config import CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN


def renovar_token():
    url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN
    }
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        data = response.json()
        with open("token.json", "w") as f:
            json.dump(data, f)
        return data["access_token"]
    else:
        print("Erro ao renovar token:", response.json())
        return None

# Obtém um token válido automaticamente
def obter_token_valido():
    """Carrega o token salvo e renova se necessário"""
    try:
        with open("token.json", "r") as f:
            content = f.read().strip()  # Remove espaços em branco para evitar erro
            if not content:  # Se o arquivo estiver vazio
                return renovar_token()
            tokens = json.loads(content)
        
        if time.time() > tokens.get("expires_in", 0):
            return renovar_token()
        return tokens["access_token"]
    except (FileNotFoundError, json.JSONDecodeError):
        return renovar_token()