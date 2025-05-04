# services/normalizer.py
import os
import numpy as np
import rasterio
from sklearn.preprocessing import MinMaxScaler
from app.services.cleaner import eliminar_archivo_si_existe

def normalizar_tif(ruta_tif):
    nombre_archivo = os.path.basename(ruta_tif)
    nombre_salida = f"normalizado_{nombre_archivo}"
    carpeta = "data/normalized"
    os.makedirs(carpeta, exist_ok=True)
    ruta_salida = os.path.join(carpeta, nombre_salida)

    eliminar_archivo_si_existe(ruta_salida)

    with rasterio.open(ruta_tif) as src:
        perfil = src.profile
        data = src.read()
        bandas, alto, ancho = data.shape

        data_norm = np.empty_like(data, dtype=np.float32)
        scaler = MinMaxScaler()

        for i in range(bandas):
            banda = data[i].reshape(-1, 1)
            banda_norm = scaler.fit_transform(banda).reshape(alto, ancho)
            data_norm[i] = banda_norm

        perfil.update(dtype='float32')

        with rasterio.open(ruta_salida, 'w', **perfil) as dst:
            dst.write(data_norm)

    print(f"✅ Imagen normalizada guardada como {ruta_salida}")
    return ruta_salida
