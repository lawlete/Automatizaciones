import pdfplumber
import os
import pandas as pd

# Definir las palabras clave que estamos buscando
keywords = ["LEY 25413 GRAL.", "IMPUESTO PAIS", "PERCEPCION RG 4815/2020"]

# Función para extraer registros de un PDF que contienen las palabras clave
def extract_records_from_pdf(pdf_path):
    records = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                for keyword in keywords:
                    if keyword in text:
                        records.append((pdf_path, keyword, text))
                        break
    return records

# Ruta a la carpeta que contiene los archivos PDF
folder_path = "C:\\Users\\Alfredo\\Desktop\\Alfredo\\Afip\\IIGG\\2023\\Bancos"

# Lista para almacenar todos los registros extraídos
all_records = []

# Recorrer todos los archivos en la carpeta
for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(folder_path, filename)
        records = extract_records_from_pdf(pdf_path)
        all_records.extend(records)

# Convertir los registros a un DataFrame de pandas
df = pd.DataFrame(all_records, columns=["Archivo", "Palabra Clave", "Contenido"])

# Guardar los registros en un archivo Excel
df.to_excel("registros_extraidos.xlsx", index=False)
