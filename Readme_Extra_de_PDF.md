# Extraer línea anterior a "TOTAL MENSUAL RETENCION IMPUESTO LEY 25.413" desde PDFs

Este script en Python abre archivos PDF dentro de una carpeta, busca líneas que contienen la palabra clave `"TOTAL MENSUAL RETENCION IMPUESTO LEY 25.413"` (o variantes definidas en configuración), y extrae la línea anterior a esas. Además, separa texto descriptivo y número, formatea el número para que sea compatible con Excel, y guarda todo en un archivo Excel.

---

## Requisitos

- Python 3.x
- pdfplumber (`pip install pdfplumber`)
- pandas (`pip install pandas`)

---

## Archivos del proyecto

- `Extra_de_PDF_4.py`: script principal para procesar los PDFs.
- `config.py`: archivo de configuración donde se definen la carpeta de PDFs y las palabras clave a buscar.

---

## Configuración (`config.py`)

Debes crear un archivo `config.py` en la misma carpeta que el script con las siguientes variables:

```python
# config.py

# Carpeta donde están los archivos PDF a procesar
pdf_folder = r"C:\ruta\a\tu\carpeta\de\pdfs"

# Lista de palabras clave para buscar (pueden incluir variantes)
keywords_Ley_25413 = [
    "TOTAL MENSUAL RETENCION IMPUESTO LEY 25.413",
    # Puedes agregar más variantes si las hay
]
