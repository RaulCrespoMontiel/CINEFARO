# app_conservacion/forms.py
from django import forms
from .models import SugerenciaMetadato

class SugerenciaForm(forms.ModelForm):
    """
    Formulario para que los usuarios sugieran metadatos faltantes o incorrectos
    para una Película Huérfana.
    """
    class Meta:
        model = SugerenciaMetadato
        # Campos que el usuario puede rellenar:
        fields = ['campo_sugerido', 'valor_propuesto']
        
        # Opcional: Personalizar etiquetas
        labels = {
            'campo_sugerido': 'Campo a Sugerir (Ej: Título, Director, Año)',
            'valor_propuesto': 'Valor Propuesto',
        }