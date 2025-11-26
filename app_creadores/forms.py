# app_creadores/forms.py

from django import forms
from .models import Propina, ObraIndependiente

# 1. Formulario de Propina (Usado en detalle_obra)
class PropinaForm(forms.ModelForm):
    # Definimos el campo 'monto' como input de número con un mínimo de 5
    monto = forms.DecimalField(
        min_value=5.00,
        max_digits=10, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'placeholder': '5.00', 'min': '5.00', 'step': '5.00'})
    )

    class Meta:
        model = Propina
        # Solo pedimos el monto, el espectador y la obra se añaden en la vista
        fields = ['monto'] 

# 2. Formulario de Obra (Usado en subir_obra)

class ObraForm(forms.ModelForm):
    class Meta:
        model = ObraIndependiente
        
        # 🌟 CAMPOS ACTUALIZADOS 🌟
        # Ahora incluye 'nombre_autor' y 'categoria'
        # 'creador' sigue excluido porque se asigna automáticamente en la vista.
        fields = [
            'titulo', 
            'nombre_autor', 
            'categoria',
            'descripcion', 
            'url_video', 
            'imagen_portada', 
            'rating_promedio'
        ]
        
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            
            # 🌟 CAMBIO CLAVE: Usar CheckboxSelectMultiple 🌟
            'categoria': forms.CheckboxSelectMultiple(), 
            # Esto renderizará todas las categorías como una lista de casillas.
        }

        