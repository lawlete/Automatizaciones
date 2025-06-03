import pandas as pd
import os
import config

folder = config.pdf_ARBA
ruta_excel = os.path.join(folder, "datos_deudas.xlsx")

df = pd.read_excel(ruta_excel, header=None)

print(f"Total de filas en el DataFrame: {len(df)}")
print(f"Primeras 20 filas del DataFrame:\n{df.head(20)}")

def convertir_importe(importe_texto):
    if pd.isna(importe_texto):
        return None
    
    texto = str(importe_texto).replace('$', '').replace(' ', '').strip()
    
    last_dot = texto.rfind('.')
    if last_dot != -1:
        antes_punto = texto[:last_dot]
        despues_punto = texto[last_dot:]
        antes_punto = antes_punto.replace(',', '')
        texto = antes_punto + despues_punto
    else:
        texto = texto.replace(',', '')
    
    print(f"Importe original texto bruto: '{importe_texto}' -> texto limpio: '{texto}'")
    
    try:
        valor = float(texto)
        # Dividir por 100 porque los últimos 2 dígitos son centavos pegados
        return valor / 100
    except ValueError:
        print(f"Error al convertir a float: '{texto}'")
        return None


# Paso 1: Encontrar índices de filas que son encabezados
indices_encabezados = []
for i, row in df.iterrows():
    if row.isin(["Débito/Crédito"]).any() and row.isin(["Importe original"]).any():
        indices_encabezados.append(i)

if not indices_encabezados:
    print("No se encontraron filas con encabezados.")
    exit()

importes = []

# Paso 2: Iterar cada bloque de datos entre encabezados
for idx_enc in range(len(indices_encabezados)):
    inicio = indices_encabezados[idx_enc] + 1
    if idx_enc + 1 < len(indices_encabezados):
        fin = indices_encabezados[idx_enc + 1]
    else:
        fin = len(df)

    fila_encabezado = df.iloc[indices_encabezados[idx_enc]]
    columnas = list(fila_encabezado.values)

    # Encontrar índice de las columnas importantes
    try:
        idx_dc = columnas.index("Débito/Crédito")
        idx_importe = columnas.index("Importe original")
    except ValueError:
        print(f"Encabezado inválido en fila {indices_encabezados[idx_enc]}")
        continue

    # Paso 3: Procesar filas del bloque
    for i in range(inicio, fin):
        fila = df.iloc[i]
        # Saltar filas con menos columnas o vacías en las posiciones clave
        if len(fila) <= max(idx_dc, idx_importe):
            continue

        valor_dc = fila.iloc[idx_dc]
        if isinstance(valor_dc, str) and valor_dc.startswith("D+"):
            importe_raw = fila.iloc[idx_importe]
            importe = convertir_importe(importe_raw)
            if importe is not None:
                importes.append(importe)

print(f"Importes encontrados (solo filas D+): {importes}")
print(f"Cantidad: {len(importes)}")

total = sum(importes)
print(f"Suma total de 'Importe original' (solo D+): ${total:,.2f}")
