# app_conservacion/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import PeliculaHuerfana, SugerenciaMetadato
from .forms import SugerenciaForm
from app_base.forms import ComentarioForm # ¡IMPORTAR COMENTARIO FORM!
from django.contrib import messages
 
    
def detalle_huerfana(request, pk): # 👈 Argumento cambiado a 'pk'
    
    pelicula = get_object_or_404(PeliculaHuerfana, pk=pk)
    
    # --- Lógica para procesar el formulario de sugerencia (POST) ---
    if request.method == 'POST':
        # Instanciamos SugerenciaForm con los datos del POST
        sugerencia_form = SugerenciaForm(request.POST) 
        
        if sugerencia_form.is_valid():
            sugerencia = sugerencia_form.save(commit=False)
            sugerencia.pelicula = pelicula
            sugerencia.usuario = request.user # Asumimos que el usuario está autenticado
            sugerencia.save()
            
            messages.success(request, '¡Tu sugerencia de metadato ha sido enviada para revisión!')
            # Redirigimos de vuelta a la misma página de detalle
            return redirect('app_conservacion:detalle_huerfana', pk=pelicula.pk)
        else:
            # Si el formulario falla, se pasa al contexto para mostrar errores
            pass # Continúa al render, usando el formulario con errores

    # --- Lógica GET (o si el POST falló) ---
    else:
        sugerencia_form = SugerenciaForm()
    
    # Filtrar solo las sugerencias pendientes para mostrar el conteo
    sugerencias_pendientes = SugerenciaMetadato.objects.filter(pelicula=pelicula, estado='Pendiente')
    
    # Instanciar el formulario de comentarios
    comentario_form = ComentarioForm() 

    context = {
        'pelicula': pelicula,
        'form': sugerencia_form, # Usado para la sugerencia de metadatos
        'form_comentario': comentario_form, # Usado para comentarios
        'sugerencias_pendientes': sugerencias_pendientes,
    }
    
    return render(request, 'detalle_huerfana.html', context)

 

def sugerir_metadato(request, pk):
    
    pelicula = get_object_or_404(PeliculaHuerfana, pk=pk)

    if request.method == 'POST':
        # 1. Aquí iría la lógica para procesar y guardar los metadatos sugeridos
        
        # 2. Mensaje de feedback
        messages.success(request, '¡Gracias! Tu sugerencia de metadato ha sido enviada para revisión.')
        
        # 3. Redirección SEGURA de vuelta al detalle
        return redirect('app_conservacion:detalle_huerfana', pk=pelicula.pk)
    
    # Si alguien intenta acceder por GET, redirigimos también
    return redirect('app_conservacion:detalle_huerfana', pk=pelicula.pk)

def listado_huerfanas(request):
    # Obtener todas las películas huérfanas
    peliculas = PeliculaHuerfana.objects.all().order_by('-fecha_ingreso')
    
    context = {
        'obras_independientes': [], # Enviamos una lista vacía
        'peliculas_huerfanas': peliculas, # Usamos el QuerySet de huérfanas
        'filtro_activo': 'Todas las Películas de Conservación (Huérfanas)',
    }
    # Reutilizamos la plantilla que ya modificaste
    return render(request, 'lista_obras.html', context)