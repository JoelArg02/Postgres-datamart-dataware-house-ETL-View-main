from pymongo import MongoClient
from faker import Faker
from bson import ObjectId
from datetime import datetime, timedelta
import random

mi_numero = 20

fake = Faker('es_ES')

def dispositivo_nombre():
    return fake.word() + " Device"

def tipo_sensor():
    return fake.word() + " Sensor"

def tipo_alerta():
    return fake.word() + " Alert"

client = MongoClient("mongodb://localhost:27018")
db = client["iot"]  
fake = Faker()

dispositivos_data = [
    {
        "nombre_dispositivo": dispositivo_nombre(),
        "tipo": fake.word(),
        "ubicacion": fake.city()
    }
    for _ in range(mi_numero)  # Puedes ajustar la cantidad de dispositivos
]

db.dispositivos.insert_many(dispositivos_data)

# Colección de Lecturas de Sensores
lecturas_data = [
    {
        "id_dispositivo": ObjectId(),
        "tipo_sensor": tipo_sensor(),
        "valor": fake.random.uniform(0, 100),
        "fecha_lectura": fake.date_time_this_decade()
    }
    for _ in range(mi_numero)  # Puedes ajustar la cantidad de lecturas
]

db.lecturas_sensores.insert_many(lecturas_data)

# Colección de Alertas
alertas_data = [
    {
        "id_dispositivo": ObjectId(),
        "tipo_alerta": tipo_alerta(),
        "fecha_alerta": fake.date_time_this_decade(),
        "estado": random.choice(["Activa", "Inactiva"])
    }
    for _ in range(mi_numero)  # Puedes ajustar la cantidad de alertas
]

db.alertas.insert_many(alertas_data)

# Cierra la conexión a MongoDB
client.close()
