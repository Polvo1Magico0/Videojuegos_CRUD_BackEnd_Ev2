from django.shortcuts import render, redirect
from .models import Videojuego
from .forms import VideojuegoForm
#Necesitas importar get_object_or_404 aqui arriba para el Update y Delete

def listar_juegos(request):
    juegos = Videojuego.objects.all()
    return render(request, 'tienda/listar.html', {'juegos': juegos})

def crear_juego(request):
    if request.method == 'POST':
        form = VideojuegoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_juegos')
    else:
        form = VideojuegoForm()
    return render(request, 'tienda/formulario.html', {'form': form})
 
# Crea aqui abajo las funciones def editar_juego(request, id): y def eliminar_juego(request, id):