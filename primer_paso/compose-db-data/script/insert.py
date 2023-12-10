from pymongo import MongoClient
from bson import ObjectId
import random
from datetime import datetime, timedelta
import time
import pymysql
import pymysql.cursors
import mysql.connector
from faker import Faker

fake = Faker('es_ES')

mi_numero = 20

client_redes = MongoClient("mongodb://localhost:27017")
db_redes = client_redes["redes"]

mi_numero = 20

# Colección de Usuarios en "redes"
for _ in range(mi_numero):
    usuario_redes = {
        "nombre_usuario": fake.user_name(),
        "correo": fake.email(),
        "amigos": []
    }
    db_redes.usuarios.insert_one(usuario_redes)

# Colección de Publicaciones en "redes"
usuarios_ids_redes = [user["_id"] for user in db_redes.usuarios.find({}, {"_id": 1})]
for _ in range(mi_numero):
    publicacion_redes = {
        "id_usuario": random.choice(usuarios_ids_redes),
        "contenido": fake.text(),
        "fecha_publicacion": datetime.utcnow(),
        "likes": []
    }
    db_redes.publicaciones.insert_one(publicacion_redes)

# Colección de Comentarios en "redes"
publicaciones_ids_redes = [publicacion["_id"] for publicacion in db_redes.publicaciones.find({}, {"_id": 1})]
for _ in range(mi_numero):
    comentario_redes = {
        "id_publicacion": random.choice(publicaciones_ids_redes),
        "id_usuario": random.choice(usuarios_ids_redes),
        "texto": fake.text(),
        "fecha_comentario": datetime.utcnow()
    }
    db_redes.comentarios.insert_one(comentario_redes)


client_redes.close()

client_iot = MongoClient("mongodb://localhost:27018")
db_iot = client_iot["iot"]

fake = Faker()

dispositivos_data = [
    {
        "nombre_dispositivo": fake.word() + " Device",
        "tipo": fake.word(),
        "ubicacion": fake.city()
    }
    for _ in range(mi_numero)
]

db_iot.dispositivos.insert_many(dispositivos_data)

lecturas_data = [
    {
        "id_dispositivo": ObjectId(),
        "tipo_sensor": fake.word() + " Sensor",
        "valor": fake.random.uniform(0, 100),
        "fecha_lectura": fake.date_time_this_decade()
    }
    for _ in range(mi_numero)
]

db_iot.lecturas_sensores.insert_many(lecturas_data)

alertas_data = [
    {
        "id_dispositivo": ObjectId(),
        "tipo_alerta": fake.word() + " Alert",
        "fecha_alerta": fake.date_time_this_decade(),
        "estado": random.choice(["Activa", "Inactiva"])
    }
    for _ in range(mi_numero)
]

db_iot.alertas.insert_many(alertas_data)

client_iot.close()

db_config_inventario = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root_password',
    'database': 'inventario',
    'port': 3306 
}

db_config_hr = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root_password',
    'database': 'recursos_humanos',
    'port': 3307  # Puerto de MySQL diferente al predeterminado
}

db_config_sales = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root_password',
    'database': 'ventas',
    'port': 3308  # Puerto de MySQL diferente al predeterminado
}

db_config_billing = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root_password',
    'database': 'gestion_facturacion',
    'port': 3309  # Puerto de MySQL diferente al predeterminado
}

db_config_projects = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root_password',
    'database': 'gestion_proyectos',
    'port': 3310  # Puerto de MySQL diferente al predeterminado
}

# Función para insertar datos ficticios en la base de datos
def insert_fake_data(connection, table, data):
    cursor = connection.cursor()
    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, tuple(data.values()))
    connection.commit()

# Generar datos ficticios con Faker
fake = Faker()

# Insertar datos ficticios en la base de datos de inventario
with pymysql.connect(**db_config_inventario) as connection:
    for _ in range(mi_numero):  # Insertar 10 productos ficticios
        product_data = {
            'nombre_producto': fake.word(),
            'categoria': fake.word(),
            'stock_actual': fake.random_int(min=1, max=100),
            'stock_minimo': fake.random_int(min=1, max=50)
        }
        insert_fake_data(connection, 'productos', product_data)

    for _ in range(mi_numero):  # Insertar 5 proveedores ficticios
        provider_data = {
            'nombre_proveedor': fake.company(),
            'direccion': fake.address(),
            'contacto': fake.name()
        }
        insert_fake_data(connection, 'proveedores', provider_data)

    for _ in range(mi_numero):  # Insertar 8 pedidos ficticios
        pedido_data = {
            'id_producto': fake.random_int(min=1, max=10),
            'id_proveedor': fake.random_int(min=1, max=5),
            'cantidad': fake.random_int(min=1, max=20),
            'fecha_pedido': fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d')
        }
        insert_fake_data(connection, 'pedidos', pedido_data)

# Insertar datos ficticios en la base de datos de gestión de facturación
with pymysql.connect(**db_config_billing) as connection:
    for _ in range(mi_numero):  # Insertar 5 clientes ficticios
        client_data = {
            'nombre_cliente': fake.name(),
            'direccion': fake.address(),
            'correo': fake.email(),
            'telefono': fake.phone_number()[:9]        
        }
        insert_fake_data(connection, 'clientes', client_data)

    for _ in range(mi_numero):  # Insertar 8 facturas ficticias
        factura_data = {
            'id_cliente': fake.random_int(min=1, max=5),
            'fecha_factura': fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d'),
            'total_factura': fake.random_int(min=100, max=1000) + fake.random_number(digits=2) / 100
        }
        insert_fake_data(connection, 'facturas', factura_data)

    for _ in range(mi_numero):  # Insertar 10 detalles de factura ficticios
        detalle_data = {
            'id_factura': fake.random_int(min=1, max=8),
            'id_producto': fake.random_int(min=1, max=10),
            'cantidad': fake.random_int(min=1, max=20),
            'precio_unitario': fake.random_int(min=10, max=100) + fake.random_number(digits=2) / 100
        }
        insert_fake_data(connection, 'detalles_factura', detalle_data)

# Repetir el proceso para otras bases de datos y tablas

# Insertar datos ficticios en la base de datos de gestión de proyectos
with pymysql.connect(**db_config_projects) as connection:
    for _ in range(mi_numero):  # Insertar 5 proyectos ficticios
        project_data = {
            'nombre_proyecto': fake.catch_phrase(),
            'fecha_inicio': fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d'),
            'fecha_fin': fake.date_between(start_date='today', end_date='+30d').strftime('%Y-%m-%d'),
            'estado': fake.word()
        }
        insert_fake_data(connection, 'proyectos', project_data)

    for _ in range(mi_numero):  # Insertar 15 tareas ficticias
        tarea_data = {
            'id_proyecto': fake.random_int(min=1, max=5),
            'descripcion': fake.text(),
            'fecha_limite': fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d'),
            'estado_tarea': fake.word()
        }
        insert_fake_data(connection, 'tareas', tarea_data)

    for _ in range(mi_numero):  # Insertar 10 miembros de equipo ficticios
        miembro_data = {
            'id_proyecto': fake.random_int(min=1, max=5),
            'id_empleado': fake.random_int(min=1, max=50),
            'rol': fake.word()
        }
        insert_fake_data(connection, 'miembros_equipo', miembro_data)

# Insertar datos ficticios en la base de datos de recursos humanos
with pymysql.connect(**db_config_hr) as connection:
    for _ in range(mi_numero):  # Insertar 15 empleados ficticios
        empleado_data = {
            'nombre': fake.first_name(),
            'apellido': fake.last_name(),
            'edad': fake.random_int(min=20, max=60),
            'puesto': fake.job(),
            'salario': fake.random_int(min=30000, max=80000) + fake.random_number(digits=2) / 100
        }
        insert_fake_data(connection, 'empleados', empleado_data)

    for _ in range(mi_numero):  # Insertar 5 departamentos ficticios
        departamento_data = {
            'nombre_departamento': fake.word()
        }
        insert_fake_data(connection, 'departamentos', departamento_data)

    for _ in range(mi_numero):  # Insertar 10 historiales de salarios ficticios
        historial_data = {
            'id_empleado': fake.random_int(min=1, max=15),
            'salario_anterior': fake.random_int(min=30000, max=80000) + fake.random_number(digits=2) / 100,
            'salario_nuevo': fake.random_int(min=30000, max=80000) + fake.random_number(digits=2) / 100,
            'fecha_modificacion': fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d')
        }
        insert_fake_data(connection, 'historial_salarios', historial_data)

# Insertar datos ficticios en la base de datos de ventas
with pymysql.connect(**db_config_sales) as connection:
    for _ in range(mi_numero):  # Insertar 5 clientes ficticios
        client_data = {
            'nombre': fake.name(),
            'direccion': fake.address(),
            'correo': fake.email(),
            'telefono': fake.phone_number()[:9]
        }
        insert_fake_data(connection, 'clientes', client_data)

    for _ in range(mi_numero):  # Insertar 10 productos ficticios
        product_data = {
            'nombre_producto': fake.word(),
            'precio': fake.random_int(min=10, max=100) + fake.random_number(digits=2) / 100,
            'stock': fake.random_int(min=1, max=50)
        }
        insert_fake_data(connection, 'productos', product_data)

    for _ in range(mi_numero):  # Insertar 8 ventas ficticias
        venta_data = {
            'id_cliente': fake.random_int(min=1, max=5),
            'fecha_venta': fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d'),
            'total_venta': fake.random_int(min=100, max=1000) + fake.random_number(digits=2) / 100
        }
        insert_fake_data(connection, 'ventas', venta_data)
