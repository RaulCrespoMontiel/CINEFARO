from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Comentario # Importamos el modelo Comentario

# Formulario de Registro (asumo que ya lo tienes)
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo Electrónico')

    class Meta:
        model = User
        fields = ("username", "email", )
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

# 🌟 NUEVO/CORREGIDO: Formulario para crear un comentario 🌟
class ComentarioForm(forms.ModelForm):
    # Solo necesitamos el campo de contenido para que el usuario escriba
    contenido = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe tu comentario aquí...'}), 
                                label='') # No queremos etiqueta para el campo
    
    class Meta:
        model = Comentario
        # Solo necesitamos el contenido, el usuario y la obra/pelicula se asignan en la vista
        fields = ('contenido',)