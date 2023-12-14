import os
import django
from faker import Faker

# Configurar la configuración de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "view.settings")
django.setup()

# Importa el modelo de DimensionUsuarios
from view.models import DimensionUsuarios

# Crear una instancia de Faker
faker = Faker()

# Crear y guardar 20 usuarios aleatorios
usuarios = []
for _ in range(20):
    nombre_usuario = faker.first_name()
    correo = faker.email()
    usuario = DimensionUsuarios(nombre_usuario=nombre_usuario, correo=correo)
    usuarios.append(usuario)

# Guardar los usuarios en la base de datos
DimensionUsuarios.objects.bulk_create(usuarios)

print("20 usuarios aleatorios insertados exitosamente.")
