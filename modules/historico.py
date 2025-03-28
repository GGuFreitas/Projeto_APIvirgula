import json
import os
import time

HISTORICO_ARQUIVO = "historico_buscas.json"

def salvar_historico(produto, resultados):
    historico = carregar_historico()
    historico.append({"produto": produto, "data": time.strftime("%Y-%m-%d %H:%M:%S"), "resultados": resultados})
    with open(HISTORICO_ARQUIVO, "w") as f:
        json.dump(historico, f, indent=4)

def carregar_historico():
    if os.path.exists(HISTORICO_ARQUIVO):
        with open(HISTORICO_ARQUIVO, "r") as f:
            return json.load(f)
    return []
