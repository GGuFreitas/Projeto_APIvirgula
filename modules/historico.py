import json
import os
import time

HISTORICO_ARQUIVO = "historico_buscas.json"

def salvar_historico(produto, resultados):
    historico = carregar_historico()

    # Extrair dados essenciais de cada item
    resultados_essenciais = []
    for item in resultados:
        dados_essenciais = {
        "Nome": item["title"],
        "Vendedor": item["seller"]["nickname"],
        "Data": item.get("date", "N/A"),
        "Quantidade": item.get("available_quantity", "N/A"),
        "Endereço": item.get("address", {}).get("state_name", "N/A"),
        "Preço": item["price"],
        "Link": item["permalink"],
        "Domain ID": item.get("domain_id", "N/A"),
        "Imagem": item.get("thumbnail", "N/A")
    } 
        resultados_essenciais.append(dados_essenciais)
    
    # Adicionar ao histórico
    historico.append({"produto": produto, "data": time.strftime("%Y-%m-%d %H:%M:%S"), "resultados": resultados_essenciais})

    # Salvar o histórico atualizado no arquivo
    with open(HISTORICO_ARQUIVO, "w") as f:
        json.dump(historico, f, indent=4)

def carregar_historico():
    if os.path.exists(HISTORICO_ARQUIVO):
        with open(HISTORICO_ARQUIVO, "r") as f:
            return json.load(f)
    return []

def limpar_historico():
    """Remove todo o histórico de buscas do arquivo JSON."""
    if os.path.exists(HISTORICO_ARQUIVO):
        with open(HISTORICO_ARQUIVO, "w") as f:
            json.dump([], f, indent=4)  # Substitui o conteúdo por uma lista vazia
        return True
    return False