import tkinter as tk

def criar_botao(parent, texto, cor, comando):
    return tk.Button(parent, text=texto, font=("Arial", 12), bg=cor, fg="white", relief=tk.FLAT, command=comando)
