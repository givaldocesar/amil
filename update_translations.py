import os
import subprocess
import glob

ts_file = os.path.join("i18n", "amil_pt_BR.ts") 

def main():
    print("Iniciando varredura de arquivos Python...")
    
    ts_files = glob.glob(os.path.join("i18n", "*.ts"))

    if not ts_files:
        print("Erro: Nenhum arquivo .ts encontrado na pasta i18n!")
        return

    print(f"Idiomas encontrados para atualizar: {', '.join(ts_files)}")
    
    py_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py") and file != "update_translations.py":
                path = os.path.join(root, file)
                py_files.append(path)
    
    if not py_files:
        print("Erro: Nenhum arquivo .py encontrado!")
        return

    print(f"Encontrados {len(py_files)} arquivos Python. Extraindo tr()...")
    
    cmd = ["pylupdate5"] + py_files + ["-ts"] + ts_files

    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("\nSucesso! Todos os arquivos de idioma foram atualizados.")
        print("Agora você já pode abrir o Qt Linguist e traduzir as novas palavras!")
    else:
        print("\nErro ao executar o pylupdate5:")
        print(result.stderr)

if __name__ == "__main__":
    main()