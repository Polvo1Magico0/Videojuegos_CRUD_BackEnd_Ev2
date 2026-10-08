from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_juegos, name='listar_juegos'),
    path('crear/', views.crear_juego, name='crear_juego'),
    path('editar/<int:id>/', views.editar_juego, name='editar_juego'),
    path('vista/<int:id>/',views.ver_juego, name='ver_juego'),
    path('eliminar/<int:id>/',views.eliminar_juego,name='eliminar_juego'),
    

]