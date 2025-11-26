#app_base/models.py
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Modelo que usamos para la llave foránea de ObraIndependiente
# Si moviste Categoria aquí, asegúrate de que esté bien definido
class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
        
    class Meta:
        verbose_name_plural = "Categorías"

# --- Modelo de Comentario ---
class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # usamos 'app_creadores.ObraIndependiente'
    obra_independiente = models.ForeignKey(
        'app_creadores.ObraIndependiente', 
        on_delete=models.CASCADE, 
        related_name='comentarios', 
        null=True, 
        blank=True
    )

    # usamos 'app_conservacion.PeliculaHuerfana'
    pelicula_huerfana = models.ForeignKey(
        'app_conservacion.PeliculaHuerfana', 
        on_delete=models.CASCADE, 
        related_name='comentarios_huerfanas', # Usar nombre distinto
        null=True, 
        blank=True
    )

    def __str__(self):
        return f'Comentario de {self.usuario.username} en {self.fecha_creacion.strftime("%Y-%m-%d")}'