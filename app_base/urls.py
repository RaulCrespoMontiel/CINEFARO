from django.urls import path
from . import views

urlpatterns = [
    # Mapea la raíz de la app ('') a la función 'home' en views.py
    path('', views.home, name='home'),
    path('registro/', views.registro_usuario, name='registro'),
    # 🌟 RUTA CRUCIAL: Para agregar comentarios a cualquier objeto (Obra o Pelicula)
    path('comentario/<str:content_type_str>/<int:object_id>/agregar/', 
         views.agregar_comentario, name='agregar_comentario'),
    # 🌟 NUEVO ENDPOINT: Ruta para ver todas las categorías
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    # 🌟 NUEVA RUTA: Búsqueda Global 🌟
    path('buscar/', views.busqueda_global, name='busqueda_global'),

     
   
]
 
 