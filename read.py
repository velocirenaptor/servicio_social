import xml.etree.ElementTree as ET
import psycopg2
from datetime import datetime

# Leer XML
tree = ET.parse('fotos_relacionadas.xml')
root = tree.getroot()

# Conexión a PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="museopalmillas",
    user="ren0kun",
    password="r0579"
)

cursor = conn.cursor()

for registro in root.findall('registro'):
    nombre = registro.find('nombre').text
    fecha_str = registro.find('fecha').text
    id_rel = registro.find('id_relacionado').text
    lat = registro.find('lat').text
    lon = registro.find('lon').text
    diff = registro.find('diferencia_segundos').text
    confianza = registro.find('confianza').text

    # Convertir fecha (IMPORTANTE)
    fecha = datetime.strptime(fecha_str, "%Y:%m:%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO registros 
        (nombre, fecha, id_relacionado, lat, lon, diferencia_segundos, confianza)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (nombre, fecha, id_rel, lat, lon, diff, confianza))

conn.commit()
cursor.close()
conn.close()

print("Insercion completada")