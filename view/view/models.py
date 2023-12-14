from django.db import models

class DimensionUsuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=255)
    correo = models.EmailField(max_length=255)
