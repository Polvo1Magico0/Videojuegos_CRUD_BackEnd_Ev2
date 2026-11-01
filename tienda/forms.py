from django import forms
from .models import Videojuego


class VideojuegoForm(forms.ModelForm):
    precio = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'min': 0})
    )

    stock = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'min': 0})
    )

    class Meta:
        model = Videojuego
        fields = '__all__'