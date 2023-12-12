from pymongo import MongoClient
import psycopg2
from bson import ObjectId
from datetime import datetime
import random
import time
import json

# Conexión a MongoDB (colección "redes")
mongo_client_redes = MongoClient("mongodb://localhost:27017")
db_redes = mongo_client_redes["redes"]

# Conexión a MongoDB (colección "iot")
mongo_client_iot = MongoClient("mongodb://localhost:27018")
db_iot = mongo_client_iot["iot"]

# Conexión a PostgreSQL
postgres_conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="password",
    database="etlb"
)
postgres_cursor = postgres_conn.cursor()

try:
    # Proceso ETL para la colección "iot"
    dispositivos_data_iot = db_iot.dispositivos.find()
    lecturas_data_iot = db_iot.lecturas_sensores.find()
    alertas_data_iot = db_iot.alertas.find()

    for dispositivo, lectura, alerta in zip(dispositivos_data_iot, lecturas_data_iot, alertas_data_iot):
        id_dispositivo = str(dispositivo.get("_id", ""))
        nombre_dispositivo = dispositivo.get("nombre_dispositivo", "")
        tipo_dispositivo = dispositivo.get("tipo", "")
        ubicacion_dispositivo = dispositivo.get("ubicacion", "")

        tipo_sensor = lectura.get("tipo_sensor", "")
        valor_sensor = lectura.get("valor", 0.0)
        fecha_lectura = lectura.get("fecha_lectura", datetime.utcnow())

        tipo_alerta = alerta.get("tipo_alerta", "")
        fecha_alerta = alerta.get("fecha_alerta", datetime.utcnow())
        estado_alerta = alerta.get("estado", "")

        # Insertar datos en PostgreSQL
        postgres_cursor.execute(
            """
            INSERT INTO lectura_sensores (
                id_dispositivo, nombre_dispositivo, tipo_dispositivo, ubicacion_dispositivo,
                tipo_sensor, valor_sensor, fecha_lectura,
                tipo_alerta, fecha_alerta, estado_alerta
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (
                id_dispositivo, nombre_dispositivo, tipo_dispositivo, ubicacion_dispositivo,
                tipo_sensor, valor_sensor, fecha_lectura,
                tipo_alerta, fecha_alerta, estado_alerta
            )
        )

        # Proceso ETL para la colección "redes"
        # Proceso ETL para la colección "redes"
    usuarios_data_redes = db_redes.usuarios.find()
    publicaciones_data_redes = db_redes.publicaciones.find()
    comentarios_data_redes = db_redes.comentarios.find()

    for usuario, publicacion, comentario in zip(usuarios_data_redes, publicaciones_data_redes, comentarios_data_redes):
        id_usuario = str(usuario.get("_id", ""))
        nombre_usuario = usuario.get("nombre_usuario", "")
        correo_usuario = usuario.get("correo", "")
        amigos_usuario = json.dumps(usuario.get("amigos", []))

        id_publicacion = str(publicacion.get("_id", ""))
        id_usuario_publicacion = str(publicacion.get("id_usuario", ""))
        contenido_publicacion = publicacion.get("contenido", "")
        fecha_publicacion = publicacion.get("fecha_publicacion", datetime.utcnow())
        likes_publicacion = json.dumps(publicacion.get("likes", []))

        id_comentario = str(comentario.get("_id", ""))
        id_publicacion_comentario = str(comentario.get("id_publicacion", ""))
        id_usuario_comentario = str(comentario.get("id_usuario", ""))
        texto_comentario = comentario.get("texto", "")
        fecha_comentario = comentario.get("fecha_comentario", datetime.utcnow())

        # Insertar datos en PostgreSQL
        postgres_cursor.execute(
            """


            DEBE SER UN WHERE O UN SELECT DE UN VIEW DE MONGO
            INSERT INTO redes_data (
                id_usuario, nombre_usuario, correo_usuario, amigos_usuario,
                id_publicacion, id_usuario_publicacion, contenido_publicacion, fecha_publicacion, likes_publicacion,
                id_comentario, id_publicacion_comentario, id_usuario_comentario, texto_comentario, fecha_comentario
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (
                id_usuario, nombre_usuario, correo_usuario, amigos_usuario,
                id_publicacion, id_usuario_publicacion, contenido_publicacion, fecha_publicacion, likes_publicacion,
                id_comentario, id_publicacion_comentario, id_usuario_comentario, texto_comentario, fecha_comentario
            )
        )
        
except Exception as e:
    print(f"Error: {e}")

finally:
    postgres_conn.commit()
    postgres_conn.close()
    mongo_client_iot.close()
    mongo_client_redes.close()
