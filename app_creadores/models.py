# app_creadores/models.py
from django.db import models
from django.db import models
# Importamos el User de Django para identificar al espectador que paga
from django.contrib.auth.models import User 
from app_base.models import Categoria
from django.urls import reverse

# =========================================================
# 1. Clase principal de las Obras Independientes
# =========================================================
class ObraIndependiente(models.Model):
    
    titulo = models.CharField(max_length=200)
    
    # Nombre público del autor o director (Para seudónimo)
    nombre_autor = models.CharField(
        max_length=100, 
        default='Anónimo', 
        verbose_name='Nombre público del Autor/Director'
    )
    # ❌ CAMBIO CRUCIAL: De ForeignKey a ManyToManyField ❌
    categoria = models.ManyToManyField(
        Categoria, 
        # No se necesita on_delete ya que ManyToMany no elimina la categoría
        related_name='obras_independientes',
        verbose_name='Categoría/Género Principal'
    )
    
    # ✅ CREADOR: Se elimina null=True para hacerlo obligatorio.
    creador = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='obras_creadas'
        # Se asume que el campo es obligatorio (null=False por defecto)
    )
    
    descripcion = models.TextField()
    url_video = models.URLField(max_length=500)
    imagen_portada = models.ImageField(upload_to='portadas/independiente/', default='portadas/default.jpg')
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    
    rating_promedio = models.DecimalField(max_digits=3, decimal_places=1, default=8.5)

    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('detalle_obra', args=[str(self.id)])
    
    class Meta:
        ordering = ['-fecha_publicacion']



# Nuevo modelo para registrar las propinas
class Propina(models.Model):
    # Espectador que dio la propina (asumiendo que es un User de Django)
    espectador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) 
    # A qué obra se destinó la propina
    obra = models.ForeignKey(ObraIndependiente, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"${self.monto} a {self.obra.titulo}"
    


##############
