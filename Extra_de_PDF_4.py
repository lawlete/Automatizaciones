# Nombre del script: Extra_de_PDF_4.py
# Descripción: Extrae la línea anterior a "TOTAL MENSUAL RETENCION IMPUESTO LEY 25.413"
# y separa texto de número, formateando el número para Excel.
# Autor: Alfredo
# Fecha: 2025-06-03

import os
import pdfplumber
import pandas as pd
import re
import config

# Carpeta de PDFs
print(pdf_folder := config.pdf_folder)

# Palabra clave
keywords = config.keywords_Ley_25413

# Lista para los resultados
extracted_data = []

def extract_previous_line_with_number(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            lines = text.split('\n')
            prev_line = ""
            for line in lines:
                for keyword in keywords:
                    if "DEBITO" in keyword:
                        clave = "DEBITO"
                    else:
                        clave = "CREDITO" 
                    # Verificamos si la línea contiene la keyword
                    if keyword in line:
                        # Guardamos la línea anterior a la que contiene la keyword
                        extracted_data.append({'Archivo PDF': os.path.basename(pdf_path), 
                                            'Texto Extraído': prev_line,
                                            'Movimiento': clave})
                prev_line = line


def procesar_linea(texto):
    match = re.search(r'(-?\d{1,3}(?:\.\d{3})*,\d{2})', texto)
    if match:
        numero_str = match.group(1)
        texto_limpio = texto.replace(numero_str, '').strip()
        numero = float(numero_str.replace('.', '').replace(',', '.'))
        return pd.Series([texto_limpio, numero])
    else:
        return pd.Series([texto.strip(), None])

# Procesar texto para separar descripción y número
print("Procesando líneas para extraer descripción y número...")
# Recorremos los PDFs
for archivo in os.listdir(pdf_folder):
    if archivo.lower().endswith(".pdf"):
        extract_previous_line_with_number(os.path.join(pdf_folder, archivo))

# Crear DataFrame
df = pd.DataFrame(extracted_data)

# Separar en descripción y número
df[['Descripción', 'Importe']] = df['Texto Extraído'].apply(procesar_linea)

print(f"Se encontraron {len(df)} líneas con las palabras clave '{keywords}'.")
print(df)


# Exportar a Excel
output_path = os.path.join(pdf_folder, "retenciones_mensuales_25413.xlsx")
df.to_excel(output_path, index=False)

print(f"Se procesaron {len(df)} registros y se guardaron en:")
print(output_path)
print("Proceso completado.")
# Fin del script Extra_de_PDF_4.py
