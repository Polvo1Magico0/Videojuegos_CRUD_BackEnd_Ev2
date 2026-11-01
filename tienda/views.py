from django.shortcuts import render, redirect, get_object_or_404
from .models import Videojuego
from .forms import VideojuegoForm
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@login_required
def listar_juegos(request):
    juegos = Videojuego.objects.all()
    return render(request, 'tienda/listar.html', {'juegos': juegos})

@login_required
def crear_juego(request):
    if request.method == 'POST':
        form = VideojuegoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_juegos')
    else:
        form = VideojuegoForm()
    return render(request, 'tienda/formulario.html', {'form': form})
 

@login_required
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

@login_required    
def eliminar_juego(request,id):
    juego = Videojuego.objects.get(id=id)
    
    if request.method == 'POST':
        
        juego.delete()
        return redirect('listar_juegos')
    
    return render(request, 'tienda/eliminar.html', {
            'juego': juego
        })
    
#APIS    
    
class VideojuegoApiView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # GET: listar todos los videojuegos
    def get(self, request):

        juegos = Videojuego.objects.all()

        datos = []

        for juego in juegos:
            datos.append({
                'id': juego.id,
                'titulo': juego.titulo,
                'plataforma': juego.plataforma,
                'precio': juego.precio,
                'stock': juego.stock,
                'portada': request.build_absolute_uri(juego.portada.url)
                    if juego.portada else None
            })

        return Response(datos, status=status.HTTP_200_OK)


    # POST: crear un videojuego
    def post(self, request):

        # Recibir los datos
        titulo = request.data.get('titulo')
        plataforma = request.data.get('plataforma')
        precio = request.data.get('precio')
        stock = request.data.get('stock', 0)

        # Validar campos obligatorios
        if not titulo or not plataforma or precio is None:
            return Response({
                'error': 'El titulo, plataforma y precio son obligatorios'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validar texto
        if not isinstance(titulo, str) or not titulo.strip():
            return Response({
                'error': 'El titulo no es valido'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(plataforma, str) or not plataforma.strip():
            return Response({
                'error': 'La plataforma no es valida'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validar longitud de texto
        if len(titulo.strip()) > 100 or len(plataforma.strip()) > 50:
            return Response({
                'error': 'El titulo o la plataforma superan el limite de caracteres'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validar números
        if not isinstance(precio, int) or isinstance(precio, bool) or precio < 0:
            return Response({
                'error': 'El precio debe ser un numero entero mayor o igual a cero'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(stock, int) or isinstance(stock, bool) or stock < 0:
            return Response({
                'error': 'El stock debe ser un numero entero mayor o igual a cero'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Crear y guardar en la BD
        juego = Videojuego.objects.create(
            titulo=titulo.strip(),
            plataforma=plataforma.strip(),
            precio=precio,
            stock=stock
        )

        # Devolver respuesta
        return Response({
            'mensaje': 'Videojuego creado correctamente',
            'videojuego': {
                'id': juego.id,
                'titulo': juego.titulo,
                'plataforma': juego.plataforma,
                'precio': juego.precio,
                'stock': juego.stock,
                'portada': None
            }
        }, status=status.HTTP_201_CREATED)
        
class VideojuegoDetalleApiView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # GET: consultar un videojuego por ID
    def get(self, request, id):

        juego = get_object_or_404(Videojuego, id=id)

        return Response({
            'id': juego.id,
            'titulo': juego.titulo,
            'plataforma': juego.plataforma,
            'precio': juego.precio,
            'stock': juego.stock,
            'portada': request.build_absolute_uri(juego.portada.url)
                if juego.portada else None
        }, status=status.HTTP_200_OK)


    # DELETE: eliminar un videojuego
    def delete(self, request, id):

        juego = get_object_or_404(Videojuego, id=id)

        juego.delete()

        return Response({
            'mensaje' : 'VideoJuego eliminado con exito',
        },status=status.HTTP_200_OK)


    # PUT: actualizar todos los campos del videojuego
    def put(self, request, id):

        juego = get_object_or_404(Videojuego, id=id)

        print("ID recibido:", id)
        print("Datos recibidos:", request.data)
        # Recibir los datos
        titulo = request.data.get('titulo')
        plataforma = request.data.get('plataforma')
        precio = request.data.get('precio')
        stock = request.data.get('stock')

        # Comprobar que se enviaron todos los campos
        if any(campo not in request.data for campo in
               ['titulo', 'plataforma', 'precio', 'stock']):

            return Response({
                'error': 'Debes enviar todos los campos'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validar texto
        if not isinstance(titulo, str) or not titulo.strip():
            return Response({
                'error': 'El titulo no es valido'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(plataforma, str) or not plataforma.strip():
            return Response({
                'error': 'La plataforma no es valida'
            }, status=status.HTTP_400_BAD_REQUEST)

        if len(titulo.strip()) > 100 or len(plataforma.strip()) > 50:
            return Response({
                'error': 'El titulo o la plataforma superan el limite de caracteres'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validar números
        if not isinstance(precio, int) or isinstance(precio, bool) or precio < 0:
            return Response({
                'error': 'El precio debe ser un numero entero mayor o igual a cero'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(stock, int) or isinstance(stock, bool) or stock < 0:
            return Response({
                'error': 'El stock debe ser un numero entero mayor o igual a cero'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Actualizar los datos
        juego.titulo = titulo.strip()
        juego.plataforma = plataforma.strip()
        juego.precio = precio
        juego.stock = stock

        juego.save()
        
        juego.refresh_from_db()

        return Response({
            'mensaje': 'Videojuego actualizado correctamente',
            'id': juego.id,
            'titulo': juego.titulo,
            'plataforma': juego.plataforma,
            'precio': juego.precio,
            'stock': juego.stock
        }, status=status.HTTP_200_OK)