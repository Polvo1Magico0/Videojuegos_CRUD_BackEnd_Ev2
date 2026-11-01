from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.listar_juegos, name='listar_juegos'),
    path('crear/', views.crear_juego, name='crear_juego'),
    path('editar/<int:id>/', views.editar_juego, name='editar_juego'),
    path('vista/<int:id>/', views.ver_juego, name='ver_juego'),
    path('eliminar/<int:id>/', views.eliminar_juego, name='eliminar_juego'),
    
    # API REST - Videojuegos

    path('api/videojuegos/',views.VideojuegoApiView.as_view(),name='api_videojuegos'),
    path('api/videojuegos/<int:id>/',views.VideojuegoDetalleApiView.as_view(),name='api_videojuego_detalle'),
    path('api/token/', obtain_auth_token, name='api_token'),
]