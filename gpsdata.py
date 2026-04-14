import csv
from datetime import datetime, timedelta


def parse_fecha_gps(fecha_str):
    try:
        fecha = datetime.strptime(
            fecha_str,
            "%Y-%m-%dT%H:%M:%SZ"
        )

        # ajustar horario si es UTC
        return fecha - timedelta(hours=6)

    except:
        return None


gps_datos = []

with open("datosGPS1.csv") as f:

    reader = csv.DictReader(f)

    for fila in reader:

        fecha = parse_fecha_gps(
            fila.get("time")
            or fila.get("CreationTime")
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


# verificar
for g in gps_datos[:5]:
    print(g)