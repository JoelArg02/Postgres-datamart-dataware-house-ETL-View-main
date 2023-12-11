from pymongo import MongoClient
from faker import Faker
from bson import ObjectId
from datetime import datetime, timedelta
import random

mi_numero = 20

fake = Faker('es_ES')

tipos_dispositivos_iot = [
    "Sensor de temperatura",
    "Sensor de humedad",
    "Sensor de luz",
    "Actuador de puerta",
    "Cámara de seguridad IoT",
    "Dispositivo de rastreo GPS",
    "Interruptor inteligente",
    "Dispositivo de medición de calidad del aire",
    "Sensor de movimiento",
    "Medidor de consumo de energía",
]

def dispositivo_nombre():
    return fake.word() + " device"

def tipo_sensor():
    return random.choice(tipos_dispositivos_iot)

def tipo_alerta(tipo_sensor):
    # Asocia tipos específicos de alertas con tipos de sensores
    if "temperatura" in tipo_sensor.lower():
        return "Alerta de temperatura"
    elif "humedad" in tipo_sensor.lower():
        return "Alerta de humedad"
    elif "luz" in tipo_sensor.lower():
        return "Alerta de luz"
    elif "puerta" in tipo_sensor.lower():
        return "Alerta de estado de la puerta"
    elif "gps" in tipo_sensor.lower():
        return "Alerta de posición GPS"
    elif "interruptor" in tipo_sensor.lower():
        return "Alerta de estado del interruptor"
    elif "calidad del aire" in tipo_sensor.lower():
        return "Alerta de calidad del aire"
    elif "movimiento" in tipo_sensor.lower():
        return "Alerta de movimiento"
    elif "consumo de energía" in tipo_sensor.lower():
        return "Alerta de consumo de energía"
    # Agrega más casos según sea necesario
    else:
        return "Alerta general"


client = MongoClient("mongodb://localhost:27018")
db = client["iot"]  
fake = Faker()

# Colección de Dispositivos
dispositivos_data = [
    {
        "nombre_dispositivo": dispositivo_nombre(),
        "tipo": random.choice(tipos_dispositivos_iot),
        "ubicacion": fake.city()
    }
    for _ in range(mi_numero)
]

dispositivos_ids = db.dispositivos.insert_many(dispositivos_data).inserted_ids

# Colección de Sensores
sensores_data = [
    {
        "id_dispositivo": dispositivo_id,
        "tipo_sensor": tipo_sensor(),
        "valor_actual": fake.random.uniform(0, 100)
    }
    for dispositivo_id in dispositivos_ids
]

sensores_ids = db.sensores.insert_many(sensores_data).inserted_ids

# Colección de Lecturas de Sensores
lecturas_data = [
    {
        "id_sensor": sensor_id,
        "valor": fake.random.uniform(0, 100),
        "fecha_lectura": fake.date_time_this_decade()
    }
    for sensor_id in sensores_ids
    for _ in range(mi_numero)
]

db.lecturas_sensores.insert_many(lecturas_data)

# Colección de Alertas
alertas_data = [
    {
        "id_sensor": sensor_id,
        "tipo_alerta": tipo_alerta(db.sensores.find_one({"_id": sensor_id})["tipo_sensor"]),
        "fecha_alerta": fake.date_time_this_decade(),
        "estado": random.choice(["Activa", "Inactiva"])
    }
    for sensor_id in sensores_ids
    for _ in range(mi_numero)
]

db.alertas.insert_many(alertas_data)

# Cierra la conexión a MongoDB
client.close()