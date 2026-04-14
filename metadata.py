import os
import csv
from PIL import Image
from PIL.ExifTags import TAGS

CARPETA_BASE = "../imagenes"
SALIDA = "data/fotos.csv"


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

    writer.writerow([
        "categoria",
        "nombre",
        "ruta",
        "fecha_exif"
    ])

    # recorrer carpetas
    for categoria in os.listdir(CARPETA_BASE):

        ruta_categoria = os.path.join(
            CARPETA_BASE,
            categoria
        )

        if os.path.isdir(ruta_categoria):

            for archivo in os.listdir(ruta_categoria):

                if archivo.lower().endswith(
                    (".jpg", ".jpeg", ".png")
                ):

                    ruta_imagen = os.path.join(
                        ruta_categoria,
                        archivo
                    )

                    fecha_exif = obtener_fecha_exif(
                        ruta_imagen
                    )

                    writer.writerow([
                        categoria,
                        archivo,
                        ruta_imagen,
                        fecha_exif
                    ])

print("CSV generado:", SALIDA)