import requests
import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageTk
from io import BytesIO
import json
import time
from fpdf import FPDF
import os

'''ID do aplicativo 3323411277855821

Chave secreta do app: LQIagbEPicyhxCYy7gTh8VyrGmgWSCBS

obter autorização
https://auth.mercadolivre.com.br/authorization?response_type=code&client_id=3323411277855821&redirect_uri=https://github.com/GGuFreitas


code = TG-67db4fa562dace000153e946-2123436478
'''

CLIENT_ID = "3323411277855821"
CLIENT_SECRET = "LQIagbEPicyhxCYy7gTh8VyrGmgWSCBS"
REFRESH_TOKEN = "TG-67db4fe76911c00001432d9b-2123436478"
HISTORICO_ARQUIVO = "historico_buscas.json"

# Variável global para o campo de entrada
entrada = None

# Função para renovar o token de acesso
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

# Buscar produtos no Mercado Livre com paginação
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

def buscar():
    global entrada  # Acessar a variável global
    produto = entrada.get()
    if not produto:
        messagebox.showwarning("Aviso", "Digite um nome de produto para buscar.")
        return
    
    resultados = buscar_mercado_livre(produto)
    if resultados:
        tree.delete(*tree.get_children())  # Limpar resultados anteriores
        
        for item in resultados:
            tree.insert("", "end", values=(item["title"], f'R$ {item["price"]:.2f}', item["seller"]["nickname"], item["permalink"]))
    else:
        messagebox.showinfo("Resultado", "Nenhum produto encontrado.")

# gerar excel
def gerar_relatorio_excel():
    global entrada  # Acessar a variável global
    pass

# Criar relatório em PDF com gráficos
def gerar_relatorio_pdf():
    pass

# Salvar histórico de buscas
def salvar_historico(produto, resultados):
    historico = carregar_historico()
    historico.append({"produto": produto, "data": time.strftime("%Y-%m-%d %H:%M:%S"), "resultados": resultados})
    with open(HISTORICO_ARQUIVO, "w") as f:
        json.dump(historico, f, indent=4)

# Carregar histórico de buscas
def carregar_historico():
    if os.path.exists(HISTORICO_ARQUIVO):
        with open(HISTORICO_ARQUIVO, "r") as f:
            return json.load(f)
    return []

def ver_historico():
    historico = carregar_historico()
    if not historico:
        messagebox.showinfo("Histórico", "Nenhum histórico de buscas encontrado.")
        return
    
    historico_texto = "\n".join([f"{h['data']} - {h['produto']}" for h in historico])
    messagebox.showinfo("Histórico de Buscas", historico_texto)
    
# Criar interface gráfica
root = tk.Tk()
root.title("Analisador de Preços")
root.geometry("800x700")
root.configure(bg="#F8F8F8")

tk.Label(root, text="Comparador de Preços", font=("Arial", 16, "bold"), bg="#F8F8F8").pack(pady=10)

# Definir a variável global 'entrada'
entrada = tk.Entry(root, font=("Arial", 14))
entrada.pack(pady=5, padx=20, fill=tk.X)

tk.Button(root, text="Buscar", font=("Arial", 14, "bold"), bg="#007AFF", fg="white", relief=tk.FLAT, command=buscar).pack(pady=10, padx=20, ipadx=10, ipady=5, fill=tk.X)

tk.Button(root, text="Gerar Relatório Excel", font=("Arial", 12), bg="#34C759", fg="white", relief=tk.FLAT, command=gerar_relatorio_excel).pack(pady=10, padx=20, ipadx=10, ipady=5, fill=tk.X)

tk.Button(root, text="Gerar Gráfico de Preços", font=("Arial", 12), bg="#FF9500", fg="white", relief=tk.FLAT, command=gerar_relatorio_pdf).pack(pady=10, padx=20, ipadx=10, ipady=5, fill=tk.X)

tk.Button(root, text="Ver Histórico de Buscas", font=("Arial", 12), bg="#5856D6", fg="white", relief=tk.FLAT, command=ver_historico).pack(pady=10, padx=20, ipadx=10, ipady=5, fill=tk.X)

# Criar Treeview para listar os produtos
colunas = ("Nome", "Preço", "Vendedor", "Link")
tree = ttk.Treeview(root, columns=colunas, show="headings", height=15)
tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

for col in colunas:
    tree.heading(col, text=col)
    tree.column(col, width=200, anchor="center")

# Frame para imagens dos produtos
image_frame = tk.Frame(root, bg="#F8F8F8")
image_frame.pack(pady=10)

root.mainloop()