# app_conservacion/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse # ¡Nueva Importación!
from app_base.models import Categoria
"""
# =========================================================
# 1. Clase principal de Películas Huérfanas
# =========================================================
class PeliculaHuerfana(models.Model):
    titulo = models.CharField(max_length=200)
    anio_estimado = models.CharField(max_length=10, blank=True, null=True, default="S.F.") # S.F. = Sin Fecha
    sinopsis_conocida = models.TextField(blank=True, null=True)
    imagen_portada = models.ImageField(upload_to='portadas/huerfanas/', default='portadas/huerfana_default.jpg')
    
    # URL del video (si existe un fragmento de conservación)
    url_video = models.URLField(max_length=500, blank=True, null=True)
    
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    # Método para redirección después de sugerir/comentar
    def get_absolute_url(self):
        # Apunta a la URL 'detalle_huerfana' definida en app_conservacion/urls.py
        return reverse('detalle_huerfana', args=[str(self.id)])
    
    class Meta:
        verbose_name_plural = "Películas Huérfanas"
"""

class PeliculaHuerfana(models.Model):
    # La información es a menudo incompleta o estimada
    titulo = models.CharField(max_length=250)
    
    # Puede ser null y blank ya que el autor puede ser desconocido
    nombre_autor = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        default='Desconocido', 
        verbose_name='Autor/Director conocido'
    )
    
    # Campo para el año de producción (a menudo es una estimación)
    anio_estimado = models.IntegerField(blank=True, null=True, verbose_name='Año Estimado')
    
    # 🌟 CLAVE: Relación de Muchos a Muchos para categorías múltiples 🌟
    categorias = models.ManyToManyField(Categoria, related_name='peliculas_huerfanas')
    
    descripcion = models.TextField(blank=True, null=True) # Sinopsis, a menudo desconocida
    url_video = models.URLField(max_length=500, blank=True, null=True) # Si existe una digitalización
    
    # Si la portada existe, se sube, si no, se usa una por defecto
    imagen_portada = models.ImageField(upload_to='portadas/huerfanas/', default='portadas/default_huerfana.jpg')
    
    # Campos de gestión del archivo
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        # Asumiendo que tendrás una URL 'detalle_huerfana'
        return reverse('detalle_huerfana', args=[str(self.id)])
    
    class Meta:
        ordering = ['-fecha_ingreso']
# =========================================================
# 2. Clase para Sugerencias de Metadatos (Conservación)
# =========================================================
class SugerenciaMetadato(models.Model):
    ESTADO_CHOICES = (
        ('Pendiente', 'Pendiente de Revisión'),
        ('Aceptado', 'Aceptado y Aplicado'),
        ('Rechazado', 'Rechazado'),
    )

    pelicula = models.ForeignKey(PeliculaHuerfana, on_delete=models.CASCADE, related_name='sugerencias')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text="Usuario que realizó la sugerencia")
    
    # Campo que se sugiere modificar (ej: 'director', 'fecha', 'sinopsis')
    campo_sugerido = models.CharField(max_length=100) 
    # El valor propuesto por el usuario
    valor_propuesto = models.TextField()

    fecha_sugerencia = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')

    def __str__(self):
        return f"Sugerencia para {self.pelicula.titulo}: {self.campo_sugerido}"

    class Meta:
        verbose_name_plural = "Sugerencias de Metadatos"