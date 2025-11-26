from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Necesario para media/static
from django.conf.urls.static import static # Necesario para media/static
from app_base import views as base_views # Importamos la vista 'home' y 'agregar_comentario'



urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URL de inicio para la aplicación base (home)
    path('', base_views.home, name='home'),
    
    # Conexión de las URLs de las aplicaciones
    path('creadores/', include('app_creadores.urls')),
    path('conservacion/', include('app_conservacion.urls', namespace='app_conservacion')), # 🌟 AÑADIR NAMESPACE 🌟
    
    # 🌟 URL DE COMENTARIOS (Vive en app_base/views.py) 🌟
    # Captura el tipo ('obra' o 'huerfana') y el ID del objeto
    path('comentar/<str:content_type_str>/<int:object_id>/', 
         base_views.agregar_comentario, name='agregar_comentario'),

    # La inclusión de app_base.urls ya no es necesaria si home, registro y comentar están aquí.
    #path('', include('app_base.urls')), 

    # URL de registro separada
    path('registro/', base_views.registro_usuario, name='registro'), 

    # Conexión de las vistas de autenticación de Django: login, logout, etc.
    path('', include('django.contrib.auth.urls')), 

    # 🌟 ¡SOLUCIÓN! INCLUYE TODAS las URLs de app_base en la raíz ('') 🌟
    path('', include('app_base.urls')), 
    # -----------------------------------------------------------------
]


# 🌟 Configuración de archivos MEDIA (para portadas)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)