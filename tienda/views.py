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
def editar_juego(request, id):
    juego = Videojuego.objects.get(id=id)

    if request.method == 'POST':
        juego.titulo = request.POST['titulo']
        juego.plataforma = request.POST['plataforma']
        juego.precio = request.POST['precio']
        juego.stock = request.POST['stock']

        if request.FILES.get('portada'):
            juego.portada = request.FILES['portada']

        juego.save()

        return redirect('listar_juegos')

    return render(request, 'tienda/editar.html', {
        'juego': juego
    })
    
def ver_juego(request,id):
    juego = Videojuego.objects.get(id=id)
    
    return render(request, 'tienda/vista.html', {
        'juego': juego
    })
    
def eliminar_juego(request,id):
    juego = Videojuego.objects.get(id=id)
    
    if request.method == 'POST':
        
        juego.delete()
        return redirect('listar_juegos')
    
    return render(request, 'tienda/eliminar.html', {
            'juego': juego
        })