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
usuarios = []
for _ in range(mi_numero):
    usuario = {
        "id_usuario": random.randint(1, 100),
        "nombre_usuario": fake.user_name(),
        "correo": fake.email(),
        "amigos": []
    }
    usuarios.append(usuario)
    result = db.usuarios.insert_one(usuario)
    if result.inserted_id:
        print(f"Inserción de usuario exitosa. ID: {result.inserted_id}")
    else:
        print("Error en la inserción de usuario")

# Agrega amigos a algunos usuarios
for usuario in usuarios:
    amigos_potenciales = [u for u in usuarios if u != usuario and random.choice([True, False])]
    usuario["amigos"] = [amigo["id_usuario"] for amigo in amigos_potenciales]

    # Actualiza el documento en la base de datos con la lista de amigos
    result = db.usuarios.update_one({"_id": usuario["_id"]}, {"$set": {"amigos": usuario["amigos"]}})
    if result.modified_count > 0:
        print(f"Actualización de amigos para usuario {usuario['id_usuario']} exitosa.")
    else:
        print(f"Error en la actualización de amigos para usuario {usuario['id_usuario']}")

# Colección de Publicaciones
usuarios_ids = [user["_id"] for user in db.usuarios.find({}, {"_id": 1})]
for _ in range(mi_numero):
    publicacion = {
        "id_usuario": random.choice(usuarios_ids),
        "contenido": fake.text(),
        "fecha_publicacion": datetime.utcnow(),
        "likes": []
    }
    result = db.publicaciones.insert_one(publicacion)
    if result.inserted_id:
        print(f"Inserción de publicación exitosa. ID: {result.inserted_id}")
    else:
        print("Error en la inserción de publicación")

# Colección de Comentarios
publicaciones_ids = [publicacion["_id"] for publicacion in db.publicaciones.find({}, {"_id": 1})]
for _ in range(mi_numero):
    comentario = {
        "id_publicacion": random.choice(publicaciones_ids),
        "id_usuario": random.choice(usuarios_ids),
        "texto": fake.text(),
        "fecha_comentario": datetime.utcnow()
    }
    result = db.comentarios.insert_one(comentario)
    if result.inserted_id:
        print(f"Inserción de comentario exitosa. ID: {result.inserted_id}")
    else:
        print("Error en la inserción de comentario")

# Cierra la conexión a MongoDB
client.close()
