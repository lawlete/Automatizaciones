import os
import pdfplumber
import pandas as pd
import re
import config

# Usar las variables desde config.py
pdf_folder = getattr(config, 'pdf_folder', '.')
keywords = getattr(config, 'keywords_Ley_25413', [])

print(f"Carpeta de PDFs: {pdf_folder}")
print(f"Palabras clave para búsqueda: {keywords}")

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
                    if "DEBITO" in keyword.upper():
                        clave = "DEBITO"
                    else:
                        clave = "CREDITO"
                    if keyword in line:
                        extracted_data.append({
                            'Archivo PDF': os.path.basename(pdf_path),
                            'Texto Extraído': prev_line,
                            'Movimiento': clave
                        })
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

print("Procesando líneas para extraer descripción y número...")

for archivo in os.listdir(pdf_folder):
    if archivo.lower().endswith(".pdf"):
        extract_previous_line_with_number(os.path.join(pdf_folder, archivo))

df = pd.DataFrame(extracted_data)

if not df.empty:
    df[['Descripción', 'Importe']] = df['Texto Extraído'].apply(procesar_linea)

print(f"Se encontraron {len(df)} líneas con las palabras clave '{keywords}'.")
print(df)

output_path = os.path.join(pdf_folder, "retenciones_mensuales_25413.xlsx")
df.to_excel(output_path, index=False)

print(f"Se procesaron {len(df)} registros y se guardaron en:")
print(output_path)
print("Proceso completado.")
