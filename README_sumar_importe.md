# Suma Importes Originales desde Excel

Este script en Python procesa un archivo Excel con datos extraídos de PDFs de ARBA, busca las filas que contienen importes de tipo "Débito" (D+), convierte correctamente los valores monetarios y suma el total, mostrando el resultado.

---

## Requisitos

- Python 3.x
- Pandas (`pip install pandas`)
- Archivo Excel exportado desde el PDF (en formato `.xlsx`)

---

## Archivos del proyecto

- `prueba_sumar_importe.py`: script principal que lee el Excel, extrae y suma importes.
- `config.py`: archivo con configuración, donde se define la ruta de la carpeta con los PDFs y/o Excel.

---

## Configuración (`config.py`)

Este archivo debe contener la ruta absoluta o relativa a la carpeta donde se encuentra el archivo Excel que se procesará. Ejemplo:

```python
# config.py
pdf_ARBA = r"C:\Users\Alfredo\Desktop\Alfredo\Trabajo\Automatizaciones\PdfyExcel"
