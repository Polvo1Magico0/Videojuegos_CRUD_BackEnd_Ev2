from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_juegos, name='listar_juegos'),
    path('crear/', views.crear_juego, name='crear_juego'),
    
    # Agrega aqui las rutas para 'editar_juego' y 'eliminar_juego'
]