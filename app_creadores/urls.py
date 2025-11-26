# app_creadores/urls.py
from django.urls import path
from . import views
from .models import ObraIndependiente

app_name = 'app_creadores' 

urlpatterns = [
    # 🌟 NUEVA RUTA: Para mostrar el formulario y procesar la subida de una obra
    # La URL será algo como: /creadores/subir-obra/
    path('subir-obra/', views.subir_obra, name='subir_obra'),
    
    # Ruta para ver el detalle de una obra (ej: /creadores/1/)
    path('<int:obra_id>/', views.detalle_obra, name='detalle_obra'),
    
    # Ruta para procesar la propina (ej: /creadores/1/propina/)
    path('<int:obra_id>/propina/', views.dar_propina, name='dar_propina'),

    path('', views.lista_obras, name='lista_obras'),

    # 🌟 NUEVA RUTA: Para listar obras filtradas por una categoría específica 🌟
    path('categoria/<int:pk>/', views.obras_por_categoria, name='obras_por_categoria'),

    # 🌟 RUTA NUEVA: Listado de TODAS las Obras Independientes 🌟
    path('listado/', views.listado_independientes, name='listado_independientes'),
]