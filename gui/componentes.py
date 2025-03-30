import tkinter as tk
from tkinter import messagebox, ttk
from modules.mercado_livre import buscar_mercado_livre
from modules.relatorio import gerar_relatorio_excel, gerar_relatorio_pdf
from modules.historico import carregar_historico
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from io import BytesIO
from fpdf import FPDF
import pandas as pd
import numpy as np
import pyperclip
from modules.utils import abrir_link
import requests

def criar_botao(parent, texto, cor, comando):
    return tk.Button(parent, text=texto, font=("Arial", 12), bg=cor, fg="white", relief=tk.FLAT, command=comando)

