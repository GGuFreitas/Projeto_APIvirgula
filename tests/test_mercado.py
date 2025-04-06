import requests

access_token = "APP_USR-3323411277855821-040521-001ec100578fea8c8b5c9fbeb3f13b3d-2123436478"
produto = "placa de vídeo"
url = f"https://api.mercadolibre.com/sites/MLB/search?q={produto}"

headers = {
    "Authorization": f"Bearer {access_token}"
}

response = requests.get(url, headers=headers)

print(f"Status: {response.status_code}")
print(response.json())