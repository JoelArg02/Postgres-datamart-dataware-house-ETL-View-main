from django.shortcuts import render
from .models import DimensionUsuarios

def mostrar_usuarios(request):
    # Obtén todos los usuarios desde la base de datos
    usuarios = DimensionUsuarios.objects.all()
    
    # Renderiza la plantilla con los datos de los usuarios
    return render(request, 'usuarios.html', {'usuarios': usuarios})
