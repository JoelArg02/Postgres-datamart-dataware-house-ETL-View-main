import psycopg2
from pymongo import MongoClient
from faker import Faker
import random

# Conexión a MongoDB
client_mongo = MongoClient("mongodb://localhost:27018")
db_mongo = client_mongo["iot"]

# Conexión a PostgreSQL
conn_pg = psycopg2.connect(
    dbname="etlb", 
    user="postgres", 
    password="password", 
    host="localhost"
)
cur = conn_pg.cursor()

# Crear tablas en PostgreSQL
cur.execute("""
    CREATE TABLE IF NOT EXISTS dispositivos (
        id_dispositivo SERIAL PRIMARY KEY,
        nombre VARCHAR(255),
        tipo VARCHAR(255),
        ubicacion VARCHAR(255)
    );
""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS sensores (
        id_sensor SERIAL PRIMARY KEY,
        tipo_sensor VARCHAR(255),
        id_dispositivo INTEGER REFERENCES dispositivos(id_dispositivo)
    );
""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS lecturas (
        id_lecturas SERIAL PRIMARY KEY,
        valor FLOAT,
        fecha_lectura TIMESTAMP,
        id_dispositivo_lecturas INTEGER REFERENCES dispositivos(id_dispositivo)
    );
""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS alertas (
        id_alerta SERIAL PRIMARY KEY,
        tipo_alerta VARCHAR(255),
        fecha_alerta TIMESTAMP,
        estado VARCHAR(50),
        id_dispositivo_alertas INTEGER REFERENCES dispositivos(id_dispositivo)
    );
""")
conn_pg.commit()

# Función para insertar datos en PostgreSQL
def insert_pg_data(table, data):
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING id_dispositivo;"
    cur.execute(query, list(data.values()))
    return cur.fetchone()[0]

# Insertar datos de dispositivos
for dispositivo in db_mongo.dispositivos.find({}):
    dispositivo_data = {
        "nombre": dispositivo["nombre_dispositivo"],
        "tipo": dispositivo["tipo"],
        "ubicacion": dispositivo["ubicacion"]
    }
    id_dispositivo = insert_pg_data("dispositivos", dispositivo_data)

    for sensor in db_mongo.sensores.find({"id_dispositivo": dispositivo["_id"]}):
        sensor_data = {
            "id_dispositivo": id_dispositivo,
            "tipo_sensor": sensor["tipo_sensor"],
            "valor": sensor["valor"]
        }
        sensor_id = insert_pg_data("sensores", sensor_data)

        # Insertar datos de lecturas y alertas relacionadas
        for lectura in db_mongo.lecturas_sensores.find({"id_dispositivo": dispositivo["_id"]}):
            lectura_data = {
                "id_sensor": sensor_id,
                "valor": lectura["valor"],
                "fecha_lectura": lectura["fecha_lectura"]
            }
            insert_pg_data("lecturas", lectura_data)

        for alerta in db_mongo.alertas.find({"id_dispositivo": dispositivo["_id"]}):
            alerta_data = {
                "id_sensor": sensor_id,
                "tipo_alerta": alerta["tipo_alerta"],
                "fecha_alerta": alerta["fecha_alerta"],
                "estado": alerta["estado"]
            }
            insert_pg_data("alertas", alerta_data)

# Cerrar conexiones
conn_pg.commit()
cur.close()
conn_pg.close()
client_mongo.close()
