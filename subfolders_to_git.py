import os
import sys
import subprocess

def run_command(command, cwd=None):
    try:
        result = subprocess.run(command, cwd=cwd, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando: {' '.join(command)}")
        print(f"   ➤ {e.stderr.strip()}")
        return None

def create_gitignore(path):
    gitignore_path = os.path.join(path, '.gitignore')
    if not os.path.exists(gitignore_path):
        with open(gitignore_path, 'w') as f:
            f.write("""# Ignorar entornos virtuales y archivos comunes
venv/
__pycache__/
*.pyc
.DS_Store
*.log
.env
*.sqlite3
*.db
node_modules/
dist/
build/
""")

def checkout_or_create_branch(branch_name, cwd):
    result = subprocess.run(["git", "rev-parse", "--verify", branch_name],
                            cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        run_command(["git", "checkout", branch_name], cwd=cwd)
    else:
        run_command(["git", "checkout", "-b", branch_name], cwd=cwd)

def main():
    if len(sys.argv) != 3:
        print("Uso: python subfolders_to_git.py <carpeta_raiz> <url_repo_remoto>")
        sys.exit(1)

    root_folder = os.path.abspath(sys.argv[1])
    remote_repo = sys.argv[2]

    print(f"Procesando subcarpetas dentro de: {root_folder}\n")

    for subfolder in os.listdir(root_folder):
        subfolder_path = os.path.join(root_folder, subfolder)

        if os.path.isdir(subfolder_path) and not subfolder.startswith("."):
            print(f"📁 Procesando: {subfolder}")

            # Crear .gitignore si no existe
            create_gitignore(subfolder_path)

            # Si está vacía la carpeta, crear README.md para que git pueda hacer commit
            if not os.listdir(subfolder_path):
                readme_path = os.path.join(subfolder_path, "README.md")
                with open(readme_path, "w") as f:
                    f.write(f"# {subfolder}\n")

            # Inicializar git
            run_command(["git", "init"], cwd=subfolder_path)
            run_command(["git", "add", "."], cwd=subfolder_path)
            run_command(["git", "commit", "-m", f"Initial commit for {subfolder}"], cwd=subfolder_path)

            # Crear o cambiar a la rama con el nombre de la subcarpeta
            branch_name = subfolder
            checkout_or_create_branch(branch_name, cwd=subfolder_path)

            # Conectar al repo remoto (removiendo primero origin si existía)
            run_command(["git", "remote", "remove", "origin"], cwd=subfolder_path)
            run_command(["git", "remote", "add", "origin", remote_repo], cwd=subfolder_path)

            # Hacer push a la rama (descomentá esta línea si querés que haga push automático)
            run_command(["git", "push", "-u", "origin", branch_name], cwd=subfolder_path)

            print(f"✅ Preparado repo en rama '{branch_name}' para {subfolder}\n")

if __name__ == "__main__":
    main()
