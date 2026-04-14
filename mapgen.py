from pyproj import Transformer
import csv

# Zona UTM probable en Veracruz
transformer = Transformer.from_crs(
    "EPSG:32614",
    "EPSG:4326",
    always_xy=True
)

with open("resultado_latlon.csv", "w", newline="") as out:

    writer = csv.writer(out)

    writer.writerow([
        "nombre",
        "lat",
        "lon"
    ])

    with open("resultado.csv") as f:

        reader = csv.DictReader(f)

        for fila in reader:

            # 🔹 verificar que tenga coordenadas
            if not fila["E_UTM"] or not fila["N_UTM"]:
                continue   # saltar fila vacía

            try:
                e = float(fila["E_UTM"])
                n = float(fila["N_UTM"])

                lon, lat = transformer.transform(e, n)

                writer.writerow([
                    fila["nombre"],
                    lat,
                    lon
                ])

            except ValueError:
                continue  # si falla conversión, saltar

print("Archivo resultado_latlon.csv generado")
