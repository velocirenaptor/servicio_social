import csv
from datetime import datetime, timedelta

# tolerancia máxima (ajústala luego)
TOLERANCIA = timedelta(minutes=1000)

# -----------------------------
# Parsear fechas
# -----------------------------

def parse_fecha_foto(fecha_str):

    if not fecha_str:
        return None

    try:
        return datetime.strptime(
            fecha_str.strip(),
            "%Y:%m:%d %H:%M:%S"
        )
    except:
        return None


def parse_fecha_gps(fecha_str):

    if not fecha_str:
        return None

    try:
        fecha = datetime.strptime(
            fecha_str.strip(),
            "%Y-%m-%dT%H:%M:%SZ"
        )

        # Ajustar zona horaria
        return fecha - timedelta(hours=6)

    except:
        return None


# -----------------------------
# Cargar GPS
# -----------------------------

gps_datos = []

with open("datosGPS1.csv") as f:

    reader = csv.DictReader(f)

    # Mostrar columnas reales
    print("Columnas GPS detectadas:")
    print(reader.fieldnames)

    for fila in reader:

        fecha = parse_fecha_gps(
            fila.get("time")
        )

        if not fecha:
            continue

        # detectar columnas posibles
        eutm = (
            fila.get("E_UTM")
            or fila.get("EUTM")
            or fila.get("E UTM")
        )

        nutm = (
            fila.get("N_UTM")
            or fila.get("NUTM")
            or fila.get("N UTM")
        )

        gps_datos.append({
            "id": fila.get("Wpt_ID"),
            "E_UTM": eutm,
            "N_UTM": nutm,
            "fecha": fecha
        })


# Ordenar por fecha (muy importante)
gps_datos.sort(
    key=lambda x: x["fecha"]
)

print("GPS cargados:", len(gps_datos))

# Verificar primer GPS
if gps_datos:
    print("Primer GPS ejemplo:")
    print(gps_datos[0])


# -----------------------------
# Buscar GPS más cercano
# -----------------------------

def buscar_gps_mas_cercano(fecha_foto):

    gps_cercano = None
    menor_diferencia = None

    for gps in gps_datos:

        diferencia = abs(
            gps["fecha"] - fecha_foto
        )

        if menor_diferencia is None:

            menor_diferencia = diferencia
            gps_cercano = gps

        elif diferencia < menor_diferencia:

            menor_diferencia = diferencia
            gps_cercano = gps

    if menor_diferencia <= TOLERANCIA:
        return gps_cercano, menor_diferencia

    return None, None


# -----------------------------
# Generar resultado
# -----------------------------

with open("resultado.csv", "w", newline="") as out:

    writer = csv.writer(out)

    writer.writerow([
        "categoria",
        "nombre",
        "gps_id",
        "E_UTM",
        "N_UTM",
        "fecha_foto",
        "diferencia_minutos"
    ])

    with open("fotos.csv") as f:

        reader = csv.DictReader(f)

        print("\nColumnas fotos detectadas:")
        print(reader.fieldnames)

        asociadas = 0
        sin_gps = 0

        for fila in reader:

            categoria = fila["categoria"]
            nombre = fila["nombre"]

            fecha_foto = parse_fecha_foto(
                fila["fecha_exif"]
            )

            if not fecha_foto:
                continue

            gps, diferencia = buscar_gps_mas_cercano(
                fecha_foto
            )

            if gps:

                minutos = round(
                    diferencia.total_seconds() / 60,
                    2
                )

                writer.writerow([
                    categoria,
                    nombre,
                    gps["id"],
                    gps["E_UTM"],
                    gps["N_UTM"],
                    fecha_foto,
                    minutos
                ])

                asociadas += 1

            else:

                writer.writerow([
                    categoria,
                    nombre,
                    "",
                    "",
                    "",
                    fecha_foto,
                    ""
                ])

                sin_gps += 1


print("\nArchivo resultado.csv generado")

print("Fotos asociadas:", asociadas)
print("Fotos sin GPS:", sin_gps)