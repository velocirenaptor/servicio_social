import os
import csv
from PIL import Image
from PIL.ExifTags import TAGS

CARPETA = "../imagenes/artefactos"
SALIDA = "fotos.csv"

def obtener_fecha_exif(ruta):
    try:
        imagen = Image.open(ruta)
        exif = imagen._getexif()

        if exif:
            for tag, valor in exif.items():
                if TAGS.get(tag) == "DateTimeOriginal":
                    return valor
    except:
        return None

with open(SALIDA, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["nombre", "fecha_exif"])

    for archivo in os.listdir(CARPETA):
        if archivo.lower().endswith((".jpg", ".jpeg", ".png")):
            ruta = os.path.join(CARPETA, archivo)

            fecha_exif = obtener_fecha_exif(ruta)

            writer.writerow([archivo, fecha_exif])

print("CSV generado:", SALIDA)