from pydantic import BaseModel
from typing import List

class ImagenRequest(BaseModel):
    fecha_inicio: str 
    fecha_fin: str
    coordenadas: List[List[float]] 
