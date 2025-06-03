# 🧾 Extractor de Texto desde PDFs con Python

Este proyecto extrae líneas específicas de texto desde archivos PDF almacenados en una carpeta local, basándose en palabras clave definidas. Es útil para encontrar transferencias bancarias, percepciones impositivas o movimientos específicos en documentos PDF como resúmenes bancarios o facturas.

## 📂 Estructura del Proyecto

```
proyecto/
│
├── venv/                      # Entorno virtual
├── config.py                 # Configuración con ruta a la carpeta de PDFs
├── extractor.py              # Script principal
├── registros_extraidos.xlsx  # Archivo de salida generado
└── README.md                 # Este archivo
```

## ⚙️ Requisitos

* Python 3.8 o superior
* pip

### Instalación de dependencias

Primero, activa el entorno virtual:

```bash
# En Windows
venv\Scripts\activate

# En macOS/Linux
source venv/bin/activate
```

Luego instala las dependencias:

```bash
pip install -r requirements.txt
```

**Nota:** Si no tienes `requirements.txt`, las bibliotecas necesarias son:

```bash
pip install pdfplumber pandas
```

## 🔧 Configuración

Crea un archivo `config.py` con el siguiente contenido (ejemplo):

```python
# config.py
pdf_folder = "C:\\Users\\TuUsuario\\Ruta\\A\\Tus\\PDFs"
```

Este archivo define la carpeta desde donde se leerán los PDFs.

## 🚀 Uso

Ejecuta el script:

```bash
python extractor.py
```

El programa recorrerá todos los archivos `.pdf` en la carpeta especificada y extraerá las líneas que contengan las palabras clave definidas en `keywords`.

### Modificación de palabras clave

En el script `extractor.py`, puedes modificar la lista de palabras clave:

```python
keywords = ["01400205034020511968"]  # Puedes agregar más si es necesario
```

## 📤 Salida

Se genera un archivo `registros_extraidos.xlsx` con las líneas que coinciden, junto con el nombre del archivo PDF de origen.

## 📌 Notas Adicionales

* Se utiliza `line_ant` para capturar la línea anterior a la coincidencia, útil en casos donde la información relevante está en una línea anterior (como en algunas expensas).
* El operador *walrus* (`:=`) se usa para mostrar y asignar la ruta de la carpeta en una línea.

