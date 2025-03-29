import tkinter as tk
from tkinter import messagebox, ttk
from modules.mercado_livre import buscar_mercado_livre
from modules.relatorio import gerar_relatorio_excel, gerar_relatorio_pdf
from modules.historico import carregar_historico
from fpdf import FPDF
import pandas as pd
import numpy as np


def buscar():
    produto = entrada.get()
    if not produto:
        messagebox.showwarning("Aviso", "Digite um nome de produto para buscar.")
        return
    
    global resultados
    resultados = buscar_mercado_livre(produto)
    if resultados:
        tree.delete(*tree.get_children())
        precos = [item["price"] for item in resultados]
        
        if precos:
            media_preco.config(text=f"Média: R$ {np.mean(precos):.2f}")
            maior_preco.config(text=f"Maior: R$ {max(precos):.2f}")
            menor_preco.config(text=f"Menor: R$ {min(precos):.2f}")
            variancia.config(text=f"Variância: {np.var(precos):.2f}")
            
        for item in resultados:
            tree.insert("", "end", values=(item["title"], f'R$ {item["price"]:.2f}', item["permalink"]))
    else:
        messagebox.showinfo("Resultado", "Nenhum produto encontrado.")

def ver_historico():
    historico = carregar_historico()
    if not historico:
        messagebox.showinfo("Histórico", "Nenhum histórico de buscas encontrado.")
        return
    historico_texto = "\n".join([f"{h['data']} - {h['produto']}" for h in historico])
    messagebox.showinfo("Histórico de Buscas", historico_texto)


def gerar_relatorio():
    if not resultados:
        messagebox.showwarning("Aviso", "Nenhum dado para gerar relatório.")
        return
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Relatório de Análise de Preços", ln=True, align="C")
    
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.cell(60, 10, "Nome", border=1)
    pdf.cell(40, 10, "Preço", border=1)
    pdf.cell(60, 10, "Loja", border=1)
    pdf.ln()
    
    for item in resultados:
        pdf.cell(60, 10, item["title"][:30], border=1)
        pdf.cell(40, 10, f'R$ {item["price"]:.2f}', border=1)
        pdf.cell(60, 10, item["seller"]["nickname"][:30], border=1)
        pdf.ln()
    
    pdf.output("relatorio.pdf")
    messagebox.showinfo("Sucesso", "Relatório gerado como relatorio.pdf")
    
    
def exportar_excel():
    if not resultados:
        messagebox.showwarning("Aviso", "Nenhum dado para exportar.")
        return
    
    dados_essenciais = [{
        "Nome": item["title"],
        "Vendedor": item["seller"]["nickname"],
        "Data": item.get("date", "N/A"),
        "Quantidade": item.get("available_quantity", "N/A"),
        "Endereço": item.get("address", {}).get("state_name", "N/A"),
        "Preço": item["price"],
        "Link": item["permalink"],
        "Domain ID": item.get("domain_id", "N/A"),
        "Imagem": item.get("thumbnail", "N/A")
    } for item in resultados]
    
    df = pd.DataFrame(dados_essenciais)
    df.to_excel("precos.xlsx", index=False)
    messagebox.showinfo("Sucesso", "Dados essenciais exportados para precos.xlsx")


# Interface gráfica
root = tk.Tk()
root.title("Analisador de Preços")
root.geometry("900x600")
root.configure(bg="#F8F8F8")

frame_esquerdo = tk.Frame(root, bg="#F8F8F8")
frame_esquerdo.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

frame_direito = tk.Frame(root, bg="#F8F8F8")
frame_direito.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

entrada = tk.Entry(frame_esquerdo, font=("Arial", 14))
entrada.pack(pady=5, padx=10, fill=tk.X)

frame_botoes = tk.Frame(frame_esquerdo, bg="#F8F8F8")
frame_botoes.pack(pady=10, padx=10, anchor="w")

botoes = [
    ("Buscar", buscar, "#007AFF"),
    ("Histórico", ver_historico, "#5856D6"),
    ("Exportar Excel", exportar_excel, "#34A853"),
    ("Gerar Relatório PDF", gerar_relatorio, "#FBBC05")
]

for texto, comando, cor in botoes:
    tk.Button(frame_botoes, text=texto, font=("Arial", 12), bg=cor, fg="white", relief=tk.FLAT, command=comando).pack(fill=tk.X, pady=5, ipadx=10, ipady=10)

frame_dados = tk.Frame(frame_direito, bg="#F8F8F8")
frame_dados.pack(fill=tk.X, pady=10)

media_preco = tk.Label(frame_dados, text="Média: -", font=("Arial", 12, "bold"), bg="#F8F8F8")
media_preco.pack(anchor="w")
maior_preco = tk.Label(frame_dados, text="Maior: -", font=("Arial", 12, "bold"), bg="#F8F8F8")
maior_preco.pack(anchor="w")
menor_preco = tk.Label(frame_dados, text="Menor: -", font=("Arial", 12, "bold"), bg="#F8F8F8")
menor_preco.pack(anchor="w")
variancia = tk.Label(frame_dados, text="Variância: -", font=("Arial", 12, "bold"), bg="#F8F8F8")
variancia.pack(anchor="w")

colunas = ("Nome", "Preço", "Vendedor", "Link")
tree = ttk.Treeview(frame_direito, columns=colunas, show="headings", height=8)
tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

for col in colunas:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

root.mainloop()
