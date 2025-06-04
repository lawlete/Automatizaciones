# subfolders_to_git.py

Este script automatiza la inicialización de repositorios Git en cada subcarpeta dentro de una carpeta raíz dada, crea un `.gitignore` básico, inicializa commits y conecta cada subcarpeta a un repositorio remoto en una rama con el mismo nombre que la subcarpeta. Además, sube los cambios automáticamente.

---

## ¿Qué hace este script?

- Recorre todas las subcarpetas de una carpeta raíz.
- En cada subcarpeta:
  - Crea un archivo `.gitignore` si no existe (ignora archivos comunes y entornos virtuales).
  - Si la carpeta está vacía, crea un `README.md` para permitir hacer commits.
  - Inicializa un repositorio Git (`git init`).
  - Hace un commit inicial con todos los archivos.
  - Crea o cambia a una rama llamada igual que la subcarpeta.
  - Conecta la carpeta a un repositorio remoto Git (removiendo cualquier remoto `origin` previo).
  - Hace push a la rama remota correspondiente.

---

## Uso

```bash
python subfolders_to_git.py <carpeta_raiz> <url_repo_remoto>
