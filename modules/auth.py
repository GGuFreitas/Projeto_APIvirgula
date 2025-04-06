import requests
import json
import time
from config import CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN


def renovar_token():
    url = "https://api.mercadolibre.com/oauth/token"

    # Usa o refresh_token do arquivo salvo, se existir
    refresh_token_atual = REFRESH_TOKEN
    try:
        with open("token.json", "r") as f:
            tokens_salvos = json.load(f)
            refresh_token_atual = tokens_salvos.get("refresh_token", REFRESH_TOKEN)
    except:
        pass

    payload = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_token_atual
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        data = response.json()
        data["created_at"] = int(time.time())
        with open("token.json", "w") as f:
            json.dump(data, f)
        return data["access_token"]
    else:
        print("Erro ao renovar token:", response.status_code, response.text)
        return None


def obter_token_valido():
    """Carrega o token salvo e renova se necessário"""
    try:
        with open("token.json", "r") as f:
            content = f.read().strip()
            if not content:
                return renovar_token()
            tokens = json.loads(content)

        created_at = tokens.get("created_at", 0)
        expires_in = tokens.get("expires_in", 0)
        agora = int(time.time())

        # Se o token expirou (6h ou mais), renovar
        if agora > created_at + expires_in:
            return renovar_token()

        return tokens["access_token"]

    except (FileNotFoundError, json.JSONDecodeError):
        return renovar_token()
