import os
import sys
import subprocess

def run_command(command, cwd=None):
    try:
        result = subprocess.run(command, cwd=cwd, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando: {' '.join(command)}\n{e.stderr}")
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

            # Crear .gitignore
            create_gitignore(subfolder_path)

            # Inicializar git
            run_command(["git", "init"], cwd=subfolder_path)
            run_command(["git", "add", "."], cwd=subfolder_path)
            run_command(["git", "commit", "-m", f"Initial commit for {subfolder}"], cwd=subfolder_path)

            # Crear rama con el nombre de la subcarpeta
            #run_command(["git", "checkout", "-b", subfolder], cwd=subfolder_path)
            branch_name = subfolder  # nombre de la subcarpeta, usado como nombre de la rama
            checkout_or_create_branch(branch_name, cwd=subfolder_path)


            # Conectar al repo remoto (con nombre 'origin')
            run_command(["git", "remote", "remove", "origin"], cwd=subfolder_path)  # Por si ya existía
            run_command(["git", "remote", "add", "origin", remote_repo], cwd=subfolder_path)

            # Push a la nueva rama
            # run_command(["git", "push", "-u", "origin", subfolder], cwd=subfolder_path)

            print(f"✅ Subido a rama '{subfolder}' en {remote_repo}\n")

if __name__ == "__main__":
    main()
