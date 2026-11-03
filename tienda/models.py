from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q

class Videojuego(models.Model):
    titulo = models.CharField(max_length=100)
    plataforma = models.CharField(max_length=50)
    precio = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1000000)
        ]
    )
    stock = models.IntegerField(default=0)
    portada = models.ImageField(upload_to='portadas/', null=True, blank=True)

    def __str__(self):
        return self.titulo
    
       
    @property
    def precio_mostrar(self):
        if self.precio == 0:
            return "Gratis"

        return self.precio


    @property
    def stock_mostrar(self):
        if self.stock > 100:
            return "+99"

        return self.stock

    
class Meta:
    constraints = [
        models.CheckConstraint(
            check=Q(precio__gte=0) & Q(precio__lte=1000000),
            name='precio_dentro_de_limites'
        )
    ]