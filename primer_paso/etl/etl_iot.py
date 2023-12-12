
import pymongo
import psycopg2

# Conexión a MongoDB
mongo_client = pymongo.MongoClient("mongodb://localhost:27018")
mongo_db = mongo_client["iot"]

# Conexión a PostgreSQL
pg_conn = psycopg2.connect(
    dbname='tu_base_de_datos', 
    user='tu_usuario', 
    password='tu_contraseña', 
    host='localhost'
)
pg_cursor = pg_conn.cursor()

# Función para cargar datos en PostgreSQL
def cargar_en_postgresql(coleccion, tabla_pg):
    documentos = mongo_db[coleccion].find()
    for doc in documentos:
        # Aquí deberías adaptar esta parte para que coincida con tu esquema en PostgreSQL
        columns = doc.keys()
        values = [doc[column] for column in columns]
        insert_query = f"INSERT INTO {tabla_pg} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})"
        pg_cursor.execute(insert_query, values)

# Cargar colecciones en PostgreSQL
# Suponiendo que 'dispositivos_data' es una colección en la base de datos 'iot'
cargar_en_postgresql('dispositivos_data', 'dispositivos_data_pg')

# Confirmar cambios y cerrar conexiones
pg_conn.commit()
pg_cursor.close()
pg_conn.close()
mongo_client.close()
