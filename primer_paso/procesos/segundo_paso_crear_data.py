import pymongo
import sqlite3
import mysql.connector
import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

# Función para generar datos ficticios
def generate_fake_data(table_name, num_records):
    if table_name == "usuarios":
        return [
            {
                "nombre_usuario": fake.user_name(),
                "correo": fake.email(),
                "fecha_registro": fake.date_this_decade(),
                "amigos": random.sample(range(1, num_records + 1), min(random.randint(1, 10), num_records))
            }
            for _ in range(num_records)
        ]
    elif table_name == "empleados":
        return [
            {
                "nombre": fake.first_name(),
                "apellido": fake.last_name(),
                "edad": random.randint(22, 65),
                "puesto": fake.job(),
                "salario": round(random.uniform(30000, 100000), 2)
            }
            for _ in range(num_records)
        ]
    elif table_name == "clientes":
        return [
            {
                "nombre": fake.name(),
                "direccion": fake.address(),
                "correo": fake.email(),
                "telefono": fake.phone_number()
            }
            for _ in range(num_records)
        ]
    elif table_name == "productos":
        return [
            {
                "nombre_producto": fake.word(),
                "precio": round(random.uniform(5, 100), 2),
                "stock": random.randint(10, 100)
            }
            for _ in range(num_records)
        ]
    elif table_name == "proyectos":
        return [
            {
                "nombre_proyecto": fake.word(),
                "fecha_inicio": fake.date_this_decade(),
                "fecha_fin": fake.date_this_decade(),
                "estado": random.choice(["En curso", "Terminado", "Cancelado"])
            }
            for _ in range(num_records)
        ]

# Conexión a SQLite
with sqlite3.connect("sqlite_redes_sociales.db") as sqlite_conn:
    sqlite_cursor = sqlite_conn.cursor()

    # Generar datos ficticios y insertar en la tabla de usuarios
    usuarios_data = generate_fake_data("usuarios", 10)
    sqlite_cursor.executemany("INSERT INTO usuarios (nombre_usuario, correo, fecha_registro) VALUES (?, ?, ?)",
                              [(user["nombre_usuario"], user["correo"], user["fecha_registro"]) for user in usuarios_data])

# Conexión a MySQL (Recursos Humanos)
with mysql.connector.connect(
    host="tu_host_mysql",
    user="tu_usuario_mysql",
    password="tu_contraseña_mysql",
    database="recursos_humanos"
) as mysql_conn_recursos_humanos:
    mysql_cursor_recursos_humanos = mysql_conn_recursos_humanos.cursor()

    # Generar datos ficticios y insertar en la tabla de empleados
    empleados_data = generate_fake_data("empleados", 10)
    mysql_cursor_recursos_humanos.executemany("INSERT INTO empleados (nombre, apellido, edad, puesto, salario) VALUES (%s, %s, %s, %s, %s)",
                                              [(emp["nombre"], emp["apellido"], emp["edad"], emp["puesto"], emp["salario"]) for emp in empleados_data])

# Conexión a MySQL (Ventas)
with mysql.connector.connect(
    host="tu_host_mysql",
    user="tu_usuario_mysql",
    password="tu_contraseña_mysql",
    database="ventas"
) as mysql_conn_ventas:
    mysql_cursor_ventas = mysql_conn_ventas.cursor()

    # Generar datos ficticios y insertar en la tabla de clientes
    clientes_data = generate_fake_data("clientes", 10)
    mysql_cursor_ventas.executemany("INSERT INTO clientes (nombre, direccion, correo, telefono) VALUES (%s, %s, %s, %s)",
                                     [(cli["nombre"], cli["direccion"], cli["correo"], cli["telefono"]) for cli in clientes_data])

# Conexión a MySQL (Inventario)
with mysql.connector.connect(
    host="tu_host_mysql",
    user="tu_usuario_mysql",
    password="tu_contraseña_mysql",
    database="inventario"
) as mysql_conn_inventario:
    mysql_cursor_inventario = mysql_conn_inventario.cursor()

    # Generar datos ficticios y insertar en la tabla de productos
    productos_data = generate_fake_data("productos", 10)
    mysql_cursor_inventario.executemany("INSERT INTO productos (nombre_producto, precio, stock) VALUES (%s, %s, %s)",
                                         [(prod["nombre_producto"], prod["precio"], prod["stock"]) for prod in productos_data])

# Conexión a PostgreSQL
with psycopg2.connect(
    host="tu_host_postgres",
    user="tu_usuario_postgres",
    password="tu_contraseña_postgres",
    database="nombre_db_postgres"
) as postgres_conn:
    postgres_cursor = postgres_conn.cursor()

    # Proceso ETL para SQLite (Redes Sociales)
    sqlite_cursor.execute("SELECT * FROM usuarios")
    sqlite_data_usuarios = sqlite_cursor.fetchall()

    for row in sqlite_data_usuarios:
        postgres_cursor.execute(
            "INSERT INTO usuarios (nombre_usuario, correo, fecha_registro, amigos) VALUES (%s, %s, %s, %s)",
            (row[1], row[3], row[4], [])  # Ajusta los índices según tu esquema
        )

    # Proceso ETL para MySQL (Recursos Humanos)
    mysql_cursor_recursos_humanos.execute("SELECT * FROM empleados")
    mysql_data_empleados = mysql_cursor_recursos_humanos.fetchall()

    for row in mysql_data_empleados:
        postgres_cursor.execute(
            "INSERT INTO empleados (nombre, apellido, edad, puesto, salario) VALUES (%s, %s, %s, %s, %s)",
            (row[1], row[2], row[3], row[4], row[5])
        )

    # Proceso ETL para MySQL (Ventas)
    mysql_cursor_ventas.execute("SELECT * FROM clientes")
    mysql_data_clientes_ventas = mysql_cursor_ventas.fetchall()

    for row in mysql_data_clientes_ventas:
        postgres_cursor.execute(
            "INSERT INTO clientes (nombre, direccion, correo, telefono) VALUES (%s, %s, %s, %s)",
            (row[1], row[2], row[3], row[4])
        )

    # Proceso ETL para MySQL (Inventario)
    mysql_cursor_inventario.execute("SELECT * FROM productos")
    mysql_data_productos_inventario = mysql_cursor_inventario.fetchall()

    for row in mysql_data_productos_inventario:
        postgres_cursor.execute(
            "INSERT INTO productos (nombre_producto, precio, stock) VALUES (%s, %s, %s)",
            (row[1], row[2], row[3])
        )

# Confirmar la transacción y cerrar las conexiones
postgres_conn.commit()
postgres_conn.close()
sqlite_conn.close()
mysql_conn_recursos_humanos.close()
mysql_conn_ventas.close()
mysql_conn_inventario.close()
