import tkinter as tk
from tkinter import messagebox, ttk
from modules.mercado_livre import buscar_mercado_livre
from modules.relatorio import gerar_relatorio_excel, gerar_relatorio_pdf
from modules.historico import carregar_historico
from gui.componentes import criar_botao

def buscar():
    produto = entrada.get()
    if not produto:
        messagebox.showwarning("Aviso", "Digite um nome de produto para buscar.")
        return
    
    resultados = buscar_mercado_livre(produto)
    if resultados:
        tree.delete(*tree.get_children())
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

root = tk.Tk()
root.title("Analisador de Preços")
root.geometry("800x700")
root.configure(bg="#F8F8F8")

tk.Label(root, text="Comparador de Preços", font=("Arial", 16, "bold"), bg="#F8F8F8").pack(pady=10)

entrada = tk.Entry(root, font=("Arial", 14))
entrada.pack(pady=5, padx=20, fill=tk.X)

criar_botao(root, "Buscar", "#007AFF", buscar).pack(pady=10, padx=20, fill=tk.X)
criar_botao(root, "Gerar Relatório Excel", "#34C759", gerar_relatorio_excel).pack(pady=10, padx=20, fill=tk.X)
criar_botao(root, "Gerar Gráfico de Preços", "#FF9500", gerar_relatorio_pdf).pack(pady=10, padx=20, fill=tk.X)
criar_botao(root, "Ver Histórico de Buscas", "#5856D6", ver_historico).pack(pady=10, padx=20, fill=tk.X)

colunas = ("Nome", "Preço", "Link")
tree = ttk.Treeview(root, columns=colunas, show="headings", height=15)
tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

for col in colunas:
    tree.heading(col, text=col)
    tree.column(col, width=200, anchor="center")

root.mainloop()
