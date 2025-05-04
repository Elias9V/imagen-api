# services/patcher.py

import os
import shutil
import rasterio
from app.services.cleaner import eliminar_directorio_si_existe

def generar_patches(ruta_tif):
    output_dir = "data/patches/patches"
    eliminar_directorio_si_existe(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    with rasterio.open(ruta_tif) as src:
        data = src.read()
        profile = src.profile
        bandas, alto, ancho = data.shape

    profile.update({
        "height": 128,
        "width": 128,
        "count": bandas,
        "dtype": "float32"
    })

    patch_size = 128
    count = 0

    for y in range(0, alto - patch_size + 1, patch_size):
        for x in range(0, ancho - patch_size + 1, patch_size):
            patch = data[:, y:y + patch_size, x:x + patch_size]
            if patch.shape[1] == patch_size and patch.shape[2] == patch_size:
                nombre_parche = f"patch_{count:04d}.tif"
                ruta_salida = os.path.join(output_dir, nombre_parche)
                with rasterio.open(ruta_salida, 'w', **profile) as dst:
                    dst.write(patch)
                count += 1

    print(f"✅ {count} parches generados en '{output_dir}'")
    return output_dir
