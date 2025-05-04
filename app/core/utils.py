import os
import shutil


def ensure_clean_dir(path):
    """Elimina el directorio si existe y lo vuelve a crear."""
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def delete_file(path):
    """Elimina un archivo si existe."""
    if os.path.isfile(path):
        os.remove(path)


def delete_files_in_dir(dir_path):
    """Elimina todos los archivos dentro de un directorio dado."""
    if os.path.isdir(dir_path):
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)


def delete_dirs(*dirs):
    """Elimina múltiples carpetas si existen."""
    for d in dirs:
        if os.path.exists(d):
            shutil.rmtree(d)
