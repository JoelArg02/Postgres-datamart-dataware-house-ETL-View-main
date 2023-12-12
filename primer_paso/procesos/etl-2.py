import psycopg2
from pymongo import MongoClient
from datetime import datetime
import json

# Conexión a MongoDB
mongo_client = MongoClient("mongodb://localhost:27017")
db = mongo_client["redes"]

# Conexión a PostgreSQL
postgres_conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="password",
    database="etlb"
)
postgres_cursor = postgres_conn.cursor()

try:
    # Transferir datos de Usuarios
    for usuario in db.usuarios.find():
        postgres_cursor.execute(
            "INSERT INTO usuarios (id_usuario, nombre_usuario, correo) VALUES (%s, %s, %s)",
            (usuario["id_usuario"], usuario["nombre_usuario"], usuario["correo"])
        )

    # Transferir datos de Publicaciones
    for publicacion in db.publicaciones.find():
        postgres_cursor.execute(
            "INSERT INTO publicaciones (id_publicacion, id_usuario, contenido, fecha_publicacion) VALUES (%s, %s, %s, %s)",
            (publicacion["id_publicacion"], publicacion["id_usuario"], publicacion["contenido"], publicacion["fecha_publicacion"])
        )

        # Transferir datos de Likes de Publicaciones
        for like in publicacion["likes"]:
            postgres_cursor.execute(
                "INSERT INTO publicacion_likes (id_publicacion, id_usuario) VALUES (%s, %s)",
                (publicacion["id_publicacion"], like)
            )

    # Transferir datos de Comentarios
    for comentario in db.comentarios.find():
        postgres_cursor.execute(
            "INSERT INTO comentarios (id_publicacion, texto, fecha_comentario) VALUES (%s, %s, %s)",
            (comentario["id_publicacion"], comentario["texto"], comentario["fecha_comentario"])
        )

except Exception as e:
    print(f"Error: {e}")
    postgres_conn.rollback()
else:
    postgres_conn.commit()
finally:
    postgres_conn.close()
    mongo_client.close()
