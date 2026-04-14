import csv
import os

# carpeta donde están las imágenes
CARPETA_IMAGENES = "imagenes/artefactos"

with open("mapa.kml", "w") as kml:

    kml.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
""")

    with open("resultado_latlon.csv") as f:

        reader = csv.DictReader(f)

        for fila in reader:

            nombre = fila["nombre"]
            lat = fila["lat"]
            lon = fila["lon"]

            # ruta relativa a la imagen
            ruta_imagen = os.path.join(
                CARPETA_IMAGENES,
                nombre
            )

            kml.write(f"""
<Placemark>

    <name>{nombre}</name>

    <description>
        <![CDATA[
        <img src="{ruta_imagen}" width="400"/>
        ]]>
    </description>

    <Point>
        <coordinates>
            {lon},{lat},0
        </coordinates>
    </Point>

</Placemark>
""")

    kml.write("""
</Document>
</kml>
""")

print("Archivo mapa.kml generado")