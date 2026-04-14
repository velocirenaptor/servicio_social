import csv
from datetime import datetime, timedelta

def parse_fecha_foto(fecha_str):

    if not fecha_str:
        return None

    try:
        return datetime.strptime(
            fecha_str,
            "%Y:%m:%d %H:%M:%S"
        ).date()

    except:
        return None

def parse_fecha(fecha_str):

    if not fecha_str:
        return None

    try:
        return datetime.strptime(
            fecha_str,
            "%Y:%m:%d %H:%M:%S"
        )

    except:
        try:
            fecha = datetime.strptime(
                fecha_str,
                "%Y-%m-%dT%H:%M:%SZ"
            )

            return fecha - timedelta(hours=6)

        except:
            return None
        
gps_datos = []

with open("datosGPS1.csv") as f:

    reader = csv.DictReader(f)

    for fila in reader:

        fecha = parse_fecha(
            fila.get("time")
        )

        if fecha:

            gps_datos.append({
                "id": fila.get("Wpt_ID"),
                "lat": fila.get("Latitude"),
                "lon": fila.get("Longitude"),
                "E_UTM": fila.get("E_UTM"),
                "N_UTM": fila.get("N_UTM"),
                "fecha": fecha.date()
            })


print("GPS cargados:", len(gps_datos))


gps_por_fecha = {}

for gps in gps_datos:

    fecha = gps["fecha"]

    if fecha not in gps_por_fecha:
        gps_por_fecha[fecha] = []

    gps_por_fecha[fecha].append(gps)

print("Fechas únicas GPS:", len(gps_por_fecha))

# 🔹 Crear archivo resultado
with open("resultado.csv", "w", newline="") as out:

    writer = csv.writer(out)

    # encabezados
    writer.writerow([
        "nombre",
        "id",
        "E_UTM",
        "N_UTM",
        "fecha"
    ])

    # 🔹 leer fotos
    with open("fotos.csv") as f:

        reader = csv.DictReader(f)

        for fila in reader:

            nombre = fila["nombre"]

            fecha_foto = parse_fecha_foto(
                fila["fecha_exif"]
            )

            if not fecha_foto:
                continue

            # 🔎 buscar GPS del mismo día
            if fecha_foto in gps_por_fecha:

                gps_del_dia = gps_por_fecha[fecha_foto]

                for gps in gps_del_dia:

                    writer.writerow([
                        nombre,
                        gps["id"],
                        gps["E_UTM"],
                        gps["N_UTM"],
                        fecha_foto
                    ])

            else:

                writer.writerow([
                    nombre,
                    "",
                    "",
                    "",
                    fecha_foto
                ])

print("Archivo resultado.csv generado")