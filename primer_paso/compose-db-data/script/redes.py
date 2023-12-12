from pymongo import MongoClient
from faker import Faker
import random
from datetime import datetime
import time

client = MongoClient("mongodb://localhost:27017")
db = client["redes"]
fake = Faker()

mi_numero = 20

usuarios = []
ids_usuario = []  # Lista para guardar los IDs generados

for _ in range(mi_numero):
    id_usuario = random.randint(1, 100)
    ids_usuario.append(id_usuario)  # Guarda el ID generado

    usuario = {
        "id_usuario": id_usuario,
        "nombre_usuario": fake.user_name(),
        "correo": fake.email(),
        "amigos": []
    }
    usuarios.append(usuario)
    db.usuarios.insert_one(usuario)

for usuario in usuarios:
    amigos_potenciales = [u for u in usuarios if u != usuario and random.choice([True, False])]
    usuario["amigos"] = [amigo["id_usuario"] for amigo in amigos_potenciales]
    db.usuarios.update_one({"id_usuario": usuario["id_usuario"]}, {"$set": {"amigos": usuario["amigos"]}})

ids_publicacion = []  # Lista para almacenar los IDs de publicación

for _ in range(mi_numero):
    id_pub = random.randint(1, 1000)  # Genera un ID único para la publicación
    ids_publicacion.append(id_pub)  # Guarda el ID generado

    publicacion = {
        "id_publicacion": id_pub,  # Asigna el ID único a la publicación
        "id_usuario": random.choice(ids_usuario),
        "contenido": fake.text(),
        "fecha_publicacion": datetime.utcnow(),
        "likes": random.sample(ids_usuario, random.randint(0, len(ids_usuario)))
    }
    db.publicaciones.insert_one(publicacion)

for _ in range(mi_numero):
    comentario = {
        "id_publicacion": random.choice(ids_publicacion),  # Usa un ID de la lista de IDs de publicación
        "texto": fake.text(),
        "fecha_comentario": datetime.utcnow()
    }
    db.comentarios.insert_one(comentario)



client.close()
