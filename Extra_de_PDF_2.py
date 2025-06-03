# Nombre del scritp: Extra_de_PDF_2.py
# Descripción: Este script extrae texto de archivos PDF en una carpeta específica
# y guarda las líneas que contienen ciertas palabras clave en un archivo Excel.
# Autor: Alfredo
# Fecha: 2023-10-20
# Modificaciones: 02-06-2025
# Importar las bibliotecas necesarias

# Principales cambios:
# 1. Se creo un archivo de configuración `config.py` para manejar la carpeta de los PDFs.
# 2. Se agrego la palabra clave "01400205034020511968" para extraer líneas específicas de transferencias.
# en el file config.py. 
# 3. Se modificó la lógica de extracción para tomar la línea anterior a la encontrada.
# 


import os
import pdfplumber
import pandas as pd
import re
import config # Asegúrate de que config.py contenga las configuraciones necesarias


# Carpeta que contiene los archivos PDF
#pdf_folder = 'C:\\Users\\Alfredo\\Desktop\\Alfredo\\Afip\\IIGG\\2023\\Bancos'
# Se lee la carpeta desde el archivo de configuración.
print (pdf_folder := config.pdf_folder)  # Usando el operador walrus para asignar y mostrar



# Condiciones de búsqueda
#keywords = 
#       ["LEY 25413 GRAL.", "IMPUESTO PAIS", "PERCEPCION RG 4815/2020"]
#       [ texto para capturar pago de expensas]

keywords = config.keywords_imp_cheq # para tomar la lineas de la transferencia o imp al cheq.

# Lista para almacenar los datos extraídos
extracted_data = []

# Función para extraer texto línea por línea basado en las palabras clave
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                # lo que sigue es para el caso de las expensas de Gandhi, sino se usa se comenta
                # y se cambia line_ant por line en la funcon actract_data abajo
                line_ant=""   # esto es para tomar la linear anterior a la encontrada
                for line in lines:
                    for keyword in keywords:
                        if keyword in line:
                            extracted_data.append({'pdf_file': os.path.basename(pdf_path), 
                                                   'text': line_ant})
                    line_ant=line 


# Función para extraer solo las filas que tienen 2 importes y separarlas correctamente
def procesar_fila(texto):
    # Busca todos los importes: números con coma como decimal y puntos como miles
    numeros = re.findall(r'-?\d{1,3}(?:\.\d{3})*,\d{2}-?', texto)
    
    # Si hay al menos dos importes...
    if len(numeros) >= 2:
        # Encontrar posición del primer número
        pos = texto.find(numeros[0])
        descripcion = texto[:pos].strip()
        debito = numeros[0]
        saldo = numeros[1]
        return pd.Series(['esta OK', descripcion, debito, saldo])
    else:
        return pd.Series([None, None, None, None])    
    
    

# Recorrer todos los archivos PDF en la carpeta
lista_de_files = os.listdir(pdf_folder)
contar_pf = 0
for pdf_file in lista_de_files:
    if pdf_file.endswith('.pdf'):
        extract_text_from_pdf(os.path.join(pdf_folder, pdf_file))
        contar_pf += 1


print (f"Se han procesado {contar_pf} archivos PDF.")

# Convertir los datos extraídos en un DataFrame de Pandas
df = pd.DataFrame(extracted_data)


# Formatear el dataframe para que tenga las columnas adecuadas
df.columns = ['Archivo PDF', 'Texto Extraído']
# Eliminar filas duplicadas
df.drop_duplicates(inplace=True)
# Reemplazar los valores NaN con una cadena vacía
df.fillna('', inplace=True)
# Formatear la columna "Texto Extradio" para sepeara en mas columnas el texto inicial 
# y los dos numeros finales"


# Asumiendo que ya tenés cargado tu DataFrame como `df` con columnas: ['Archivo PDF', 'Texto Extraído']
# Creamos nuevas columnas aplicando la función a cada fila
df[['Column que debe quedar', 'Descrp', 'Debito', 'Saldo']] = df['Texto Extraído'].apply(procesar_fila)


# Opcional: ver solo las filas procesadas correctamente
df_ok = df[df['Column que debe quedar'] == 'esta OK']


# Mostramos el resultado final limpio
print(df_ok[['Archivo PDF', 'Descrp', 'Debito', 'Saldo']])

print(df_ok.shape)

# Guardar el DataFrame en un archivo Excel
df_ok.to_excel(os.path.join(pdf_folder, "registros_extraidos.xlsx"), index=False)


