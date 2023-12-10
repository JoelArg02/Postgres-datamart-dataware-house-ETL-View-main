from pymongo import MongoClient
from faker import Faker
from bson import ObjectId
import random
from datetime import datetime, timedelta
import time

time.sleep(30)


# Conéctate a MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["redes"]  # Crea la base de datos "redes"
fake = Faker()

mi_numero = 20

# Colección de Usuarios
for _ in range(mi_numero):
    usuario = {
        "nombre_usuario": fake.user_name(),
        "correo": fake.email(),
        "amigos": []
    }
    db.usuarios.insert_one(usuario)

# Colección de Publicaciones
usuarios_ids = [user["_id"] for user in db.usuarios.find({}, {"_id": 1})]
for _ in range(mi_numero):
    publicacion = {
        "id_usuario": random.choice(usuarios_ids),
        "contenido": fake.text(),
        "fecha_publicacion": datetime.utcnow(),
        "likes": []
    }
    db.publicaciones.insert_one(publicacion)

# Colección de Comentarios
publicaciones_ids = [publicacion["_id"] for publicacion in db.publicaciones.find({}, {"_id": 1})]
for _ in range(mi_numero):
    comentario = {
        "id_publicacion": random.choice(publicaciones_ids),
        "id_usuario": random.choice(usuarios_ids),
        "texto": fake.text(),
        "fecha_comentario": datetime.utcnow()
    }
    db.comentarios.insert_one(comentario)

# Cierra la conexión a MongoDB
client.close()
