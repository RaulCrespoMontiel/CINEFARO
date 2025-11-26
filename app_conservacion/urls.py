# app_conservacion/urls.py
from django.urls import path
from . import views

app_name = 'app_conservacion' 

urlpatterns = [
    
    # 🌟 RUTA CRUCIAL: Detalle de Película Huérfana 🌟
    # El <int:pk> captura el ID de la película
    path('<int:pk>/', views.detalle_huerfana, name='detalle_huerfana'),

    # 🌟 AÑADIR ESTA RUTA PARA SOLUCIONAR EL ERROR 🌟
    # Esta ruta maneja la lógica para que los usuarios sugieran información.
    path('<int:pk>/sugerir-metadato/', views.sugerir_metadato, name='sugerir_metadato'),
    # 🌟 RUTA NUEVA: Listado de TODAS las Películas Huérfanas 🌟
    path('listado/', views.listado_huerfanas, name='listado_huerfanas'),
]