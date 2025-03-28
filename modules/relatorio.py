import pandas as pd
from fpdf import FPDF

def gerar_relatorio_excel(produto, resultados):
    df = pd.DataFrame(resultados)
    df.to_excel(f"{produto}_relatorio.xlsx", index=False)

def gerar_relatorio_pdf(produto, resultados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Relatório de {produto}", ln=True, align='C')
    
    for item in resultados:
        pdf.cell(200, 10, txt=f"{item['title']} - R$ {item['price']}", ln=True)
    
    pdf.output(f"{produto}_relatorio.pdf")