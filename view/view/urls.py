from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
        path('mostrar-usuarios/', views.mostrar_usuarios, name='mostrar_usuarios'),

]