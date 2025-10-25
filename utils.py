# utils.py
import os

def ensure_folder(folder_path):
    """Garante que a pasta exista. Se não existir, cria."""
    os.makedirs(folder_path, exist_ok=True)

def prepare_subfolders(base_folder, *subfolders):
    """
    Cria uma pasta principal e subpastas dentro dela.
    
    Exemplo:
        folders = prepare_subfolders("img", "tables", "grafico")
        folders["tables"] -> "img/tables"
    """
    ensure_folder(base_folder)
    folder_paths = {}
    for sub in subfolders:
        path = os.path.join(base_folder, sub)
        ensure_folder(path)
        folder_paths[sub] = path
    return folder_paths
