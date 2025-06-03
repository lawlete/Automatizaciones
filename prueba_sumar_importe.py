import pandas as pd
import os
import config

folder = config.pdf_ARBA
ruta_excel = os.path.join(folder, "datos_deudas.xlsx")

df = pd.read_excel(ruta_excel, header=None)
df_sub = df.iloc[:, 1:].copy()  # quitamos la columna vacía

def convertir_importe(importe_texto):
    if pd.isna(importe_texto):
        return None
    texto = str(importe_texto).replace('$', '').replace(' ', '').strip()
    texto = texto.replace('.', '').replace(',', '.')
    print(f"Importe original texto bruto: '{importe_texto}' -> texto limpio: '{texto}'")
    try:
        return float(texto)
    except ValueError:
        return None

total_importe = 0.0
i = 0
while i < len(df_sub):
    fila = df_sub.iloc[i]
    if "Débito/Crédito" in fila.values and "Importe original" in fila.values:
        encabezado = list(fila.values)
        idx_dc = encabezado.index("Débito/Crédito")
        idx_importe = encabezado.index("Importe original")
        print(f"Encabezado encontrado en fila {i}: {encabezado}")
        print(f"Índice 'Débito/Crédito': {idx_dc}")
        print(f"Índice 'Importe original': {idx_importe}")
        i += 1
        while i < len(df_sub):
            fila_datos = df_sub.iloc[i]
            if "Débito/Crédito" in fila_datos.values and "Importe original" in fila_datos.values:
                break

            valor_dc = fila_datos.iloc[idx_dc]
            print(f"Fila {i} valores columna Débito/Crédito: '{valor_dc}'")
            if isinstance(valor_dc, str) and valor_dc.startswith("D+"):
                importe = convertir_importe(fila_datos.iloc[idx_importe])
                print(f"Fila {i} - valor_dc: '{valor_dc}', importe convertido: {importe}")
                if importe is not None:
                    total_importe += importe
            i += 1
    else:
        i += 1

print(f"Suma total de 'Importe original' (solo D+): ${total_importe:,.2f}")
