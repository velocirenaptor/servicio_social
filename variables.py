import csv

with open("data/datosGPS1.csv") as f:

    reader = csv.DictReader(f)

    print("Columnas GPS:")
    print(reader.fieldnames)