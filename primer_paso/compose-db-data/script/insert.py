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

mi_numero = 100

client = MongoClient("mongodb://localhost:27017")
db = client["redes"]

usuarios = []
ids_usuario = []

for _ in range(mi_numero):
    id_usuario = random.randint(1, 9999)
    ids_usuario.append(id_usuario)

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

ids_publicacion = [] 

for _ in range(mi_numero):
    id_pub = random.randint(1, 1000) 
    ids_publicacion.append(id_pub) 

    publicacion = {
        "id_publicacion": id_pub, 
        "id_usuario": random.choice(ids_usuario),
        "contenido": fake.text(),
        "fecha_publicacion": datetime.utcnow(),
        "likes": random.sample(ids_usuario, random.randint(0, len(ids_usuario)))
    }
    db.publicaciones.insert_one(publicacion)

for _ in range(mi_numero):
    comentario = {
        "id_publicacion": random.choice(ids_publicacion),
        "texto": fake.text(),
        "fecha_comentario": datetime.utcnow()
    }
    db.comentarios.insert_one(comentario)



client.close()

client_iot = MongoClient("mongodb://localhost:27018")
db_iot = client_iot["iot"]

tipos_sensores = ["Sensor de Temperatura", "Sensor de Humedad", "Sensor de Luz", "Sensor de Presión", "Sensor de Sonido"]


dispositivos_data = [
    {
        "nombre_dispositivo": fake.word() + " device",
        "tipo": fake.word(),
        "ubicacion": fake.city()
    }
    for _ in range(mi_numero)
]

dispositivos_ids = db_iot.dispositivos.insert_many(dispositivos_data).inserted_ids

sensor_data = [
    {
        "tipo_sensor": random.choice(tipos_sensores),
        "id_dispositivo": random.choice(dispositivos_ids)
    }
    for _ in range(mi_numero)
]

db_iot.sensores_informacion.insert_many(sensor_data)

lecturas_data = [
    {
        "valor": fake.random.uniform(0, 100),
        "fecha_lectura": fake.date_time_this_decade(),
        "id_dispositivo": random.choice(dispositivos_ids)
    }
    for _ in range(mi_numero)
]

db_iot.lecturas_sensores.insert_many(lecturas_data)

alertas_data = [
    {
        "tipo_alerta": fake.word() + " alert",
        "fecha_alerta": fake.date_time_this_decade(),
        "estado": random.choice(["Activa", "Inactiva"]),
        "id_dispositivo": random.choice(dispositivos_ids)
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
    'port': 3307 
}

db_config_sales = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root_password',
    'database': 'ventas',
    'port': 3308 
}

db_config_billing = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root_password',
    'database': 'gestion_facturacion',
    'port': 3309 
}

db_config_projects = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root_password',
    'database': 'gestion_proyectos',
    'port': 3310 
}

def insert_fake_data(connection, table, data):
    cursor = connection.cursor()
    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, tuple(data.values()))
    connection.commit()

fake = Faker()

id_proveedor = []
id_producto = []
with pymysql.connect(**db_config_inventario) as connection:
  
    for _ in range(mi_numero): 
        provider_data = {
            'nombre_proveedor': fake.company(),
            'direccion': fake.address(),
            'contacto': fake.name()
        }
        insert_fake_data(connection, 'proveedores', provider_data)
        cursor = connection.cursor()
        cursor.execute("SELECT LAST_INSERT_ID();")
        proveedor_id = cursor.fetchone()[0]
        cursor.close()
        id_proveedor.append(proveedor_id)

    for _ in range(mi_numero):
        product_data = {
            'nombre_producto': fake.word(),
            'categoria': fake.word(),
            'stock_actual': fake.random_int(min=1, max=100),
            'stock_minimo': fake.random_int(min=1, max=50),
            'id_proveedor': fake.random_element(elements=id_proveedor)
        }
        insert_fake_data(connection, 'productos', product_data)
        cursor = connection.cursor()
        cursor.execute("SELECT LAST_INSERT_ID();")
        producto_id = cursor.fetchone()[0]
        cursor.close()
        id_producto.append(producto_id)
    
    for _ in range(mi_numero):
        pedido_data = {
            'id_producto': fake.random_element(elements=id_producto),
            'id_proveedor': fake.random_element(elements=id_proveedor),
            'cantidad': fake.random_int(min=1, max=20),
            'fecha_pedido': fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d')
        }
        insert_fake_data(connection, 'pedidos', pedido_data)

client_ids = []
factur_ids = []

with pymysql.connect(**db_config_billing) as connection:
    for _ in range(mi_numero):
        client_data = {
            'nombre_cliente': fake.name(),
            'direccion': fake.address(),
            'correo': fake.email(),
            'telefono': fake.phone_number()[:9]
        }
        insert_fake_data(connection, 'clientes', client_data)
        cursor = connection.cursor()
        cursor.execute("SELECT LAST_INSERT_ID();")
        client_id = cursor.fetchone()[0]
        cursor.close()
        client_ids.append(client_id)

    for _ in range(mi_numero):
        factura_data = {
            'id_cliente': fake.random_element(elements=client_ids),
            'fecha_factura': fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d'),
            'total_factura': fake.random_int(min=100, max=1000) + fake.random_number(digits=2) / 100
        }
        insert_fake_data(connection, 'facturas', factura_data)
        cursor = connection.cursor()
        cursor.execute("SELECT LAST_INSERT_ID();")
        factura_id = cursor.fetchone()[0]
        cursor.close()
        factur_ids.append(factura_id)

    for _ in range(mi_numero):
        detalle_data = {
            'id_factura': fake.random_element(elements=factur_ids),
            'id_producto': fake.random_element(elements=id_producto),
            'cantidad': fake.random_int(min=1, max=20),
            'precio_unitario': fake.random_int(min=10, max=100) + fake.random_number(digits=2) / 100
        }
        insert_fake_data(connection, 'detalles_factura', detalle_data)


id_proyect = []

id_empleado = []
id_departamento = []
with pymysql.connect(**db_config_hr) as connection:
    for _ in range(mi_numero):
        departamento_data = {
            'nombre_departamento': fake.word()
        }
        insert_fake_data(connection, 'departamentos', departamento_data)
        cursor = connection.cursor()
        cursor.execute("SELECT LAST_INSERT_ID();")
        departamento_id = cursor.fetchone()[0]
        cursor.close()
        id_departamento.append(departamento_id)

    for _ in range(mi_numero):
        empleado_data = {
            'nombre': fake.first_name(),
            'apellido': fake.last_name(),
            'edad': fake.random_int(min=20, max=60),
            'puesto': fake.job(),
            'salario': fake.random_int(min=30000, max=80000) + fake.random_number(digits=2) / 100,
            'id_departamento': fake.random_element(elements=id_departamento)
        }
        insert_fake_data(connection, 'empleados', empleado_data)
        cursor = connection.cursor()
        cursor.execute("SELECT LAST_INSERT_ID();")
        empleado_id = cursor.fetchone()[0]
        cursor.close()
        id_empleado.append(empleado_id)

    for _ in range(mi_numero):
        historial_data = {
            'id_empleado': fake.random_element(elements=id_empleado),
            'salario_anterior': fake.random_int(min=30000, max=80000) + fake.random_number(digits=2) / 100,
            'salario_nuevo': fake.random_int(min=30000, max=80000) + fake.random_number(digits=2) / 100,
            'fecha_modificacion': fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d')
        }
        insert_fake_data(connection, 'historial_salarios', historial_data)

with pymysql.connect(**db_config_projects) as connection:
    for _ in range(mi_numero):
        project_data = {
            'nombre_proyecto': fake.catch_phrase(),
            'fecha_inicio': fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d'),
            'fecha_fin': fake.date_between(start_date='today', end_date='+30d').strftime('%Y-%m-%d'),
            'estado': fake.word()
        }
        insert_fake_data(connection, 'proyectos', project_data)
        cursor = connection.cursor()
        cursor.execute("SELECT LAST_INSERT_ID();")
        proyect_id = cursor.fetchone()[0]
        cursor.close()
        id_proyect.append(proyect_id)

    for _ in range(mi_numero):
        tarea_data = {
            'id_proyecto': fake.random_element(elements=id_proyect),
            'descripcion': fake.text(),
            'fecha_limite': fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d'),
            'estado_tarea': fake.word()
        }
        insert_fake_data(connection, 'tareas', tarea_data)


    for _ in range(mi_numero):
        miembro_data = {
            'id_proyecto': fake.random_element(elements=id_proyect),
            'id_empleado': fake.random_element(elements=id_empleado),
            'rol': fake.word()
        }
        insert_fake_data(connection, 'miembros_equipo', miembro_data)

with pymysql.connect(**db_config_sales) as connection:
    for _ in range(mi_numero):
        client_data = {
            'nombre': fake.name(),
            'direccion': fake.address(),
            'correo': fake.email(),
            'telefono': fake.phone_number()[:9],
            'facturado': bool(fake.random_int(min=0, max=1))
        }
        insert_fake_data(connection, 'clientes', client_data)

    for _ in range(mi_numero):
        venta_data = {
            'id_producto': fake.random_element(elements=id_producto),
            'id_cliente': fake.random_element(elements=client_ids),
            'fecha_venta': fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d'),
            'total_venta': fake.random_int(min=100, max=1000) + fake.random_number(digits=2) / 100
        }
        insert_fake_data(connection, 'ventas', venta_data)
