from django.shortcuts import render
# app_creadores/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from .models import ObraIndependiente, Propina, Categoria
from django.contrib.auth.models import User
from .forms import PropinaForm, ObraForm
from app_base.forms import ComentarioForm
from django.contrib import messages
from app_conservacion.models import PeliculaHuerfana # 👈 ¡AÑADIR ESTA LÍNEA!

def detalle_obra(request, obra_id):
    
    obra = get_object_or_404(ObraIndependiente, pk=obra_id)
    propina_form = PropinaForm()
    
    # 🌟 NUEVO: Instanciar y pasar el formulario de comentarios
    comentario_form = ComentarioForm() 

    context = {
        'obra': obra,
        'propina_form': propina_form,
        'form_comentario': comentario_form, # Usado en detalle_obra.html
    }
    return render(request, 'detalle_obra.html', context)

 

@login_required 
def dar_propina(request, obra_id): # 👈 Argumento cambiado a 'obra_id'
    
    # Usamos obra_id para buscar la obra
    obra = get_object_or_404(ObraIndependiente, pk=obra_id)

    if request.method == 'POST':
        # --- SIMULACIÓN DE PASARELA DE PAGO MINIMALISTA ---
        
        # 1. (Simulación de la lógica de propina)
        
        # 2. Mostramos un mensaje de éxito/gracias
        # Ya comprobamos que 'messages' está importado
        messages.success(request, f'¡Gracias {request.user.username}! Tu propina ha sido registrada para el creador. (Simulación exitosa)')
        
        # 3. Redirigimos al detalle de la obra usando el namespace y obra_id
        # Redirigimos usando el argumento que espera la vista 'detalle_obra'
        return redirect('app_creadores:detalle_obra', obra_id=obra.pk) 
        
    # Si alguien intenta acceder a la URL por GET
    return HttpResponseForbidden("Solo se permite el método POST para esta acción.")

 
# 🌟 VISTA PARA SUBIR UNA OBRA 🌟
@login_required # ¡IMPORTANTE! Solo permite a usuarios registrados acceder
def subir_obra(request):
    if request.method == 'POST':
        # Instancia el formulario con los datos POST y los archivos (request.FILES es crucial para la imagen)
        form = ObraForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. No guardamos inmediatamente para poder asignar el creador (commit=False)
            obra = form.save(commit=False)
            
            # 2. Asignamos el usuario logueado como creador
            obra.creador = request.user 
            
            # 3. Guardamos la obra en la base de datos, incluyendo la imagen y el usuario
            obra.save()
            
            # 🌟 PASO AGREGADO: Guarda las relaciones Muchos a Muchos (Categorías) 🌟
            # Esto debe ir DESPUÉS de obra.save()
            form.save_m2m()

            # 4. Redireccionamos a la página de detalle de la obra recién creada
            return redirect('app_creadores:detalle_obra', obra_id=obra.id) 
            
    else:
        # Si es una petición GET, mostramos el formulario vacío
        form = ObraForm()
        
    # Usamos la plantilla que creaste: templates/subir_obra.html
    return render(request, 'subir_obra.html', {'form': form})

#

def lista_obras(request):
    obras = ObraIndependiente.objects.all()
    filtro_activo = None
    
    todas_las_categorias = Categoria.objects.all().values_list('pk', 'nombre') # Ejemplo de cómo obtener el key/value
    
    # 2. Manejar el filtro por categoría
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        obras = obras.filter(categoria_id=categoria_id) # Filtrar por el ID
        try:
            filtro_activo = Categoria.objects.get(pk=categoria_id).nombre
        except Categoria.DoesNotExist:
            pass
            
    # 3. Lógica de Filtrado por Autor (Creador)
    autor_id = request.GET.get('autor')
    if autor_id:
        # Buscamos el objeto User
        autor = get_object_or_404(User, pk=autor_id)
        obras = obras.filter(creador=autor)
        filtro_activo = f"Autor: {autor.username}"

    context = {
        'obras': obras,
        'filtro_activo': filtro_activo,
        'todas_las_categorias': todas_las_categorias, # Se envía el listado a la plantilla
        # ... otros contextos ...
    }
    return render(request, 'lista_obras.html', context)



def obras_por_categoria(request, pk):
    # 1. Obtener la categoría por ID
    categoria = get_object_or_404(Categoria, pk=pk)

    # 2. Obtener Obras Independientes que tienen esta categoría
    # La sintaxis del filtro es el nombre del campo en ObraIndependiente que apunta a Categoria (asumo 'categoria')
    obras_independientes = ObraIndependiente.objects.filter(categoria=categoria).order_by('-fecha_publicacion')

    # 3. Obtener Películas Huérfanas que tienen esta categoría
    # La sintaxis del filtro es el nombre del campo en PeliculaHuerfana que apunta a Categoria (asumo 'categorias')
    peliculas_huerfanas = PeliculaHuerfana.objects.filter(categorias=categoria).order_by('-fecha_ingreso')
    
    # El título del filtro
    filtro_activo = f"Resultados para Obras de género: {categoria.nombre}"
    
    context = {
        'categoria': categoria,
        'obras_independientes': obras_independientes,      # 👈 Obras Indie
        'peliculas_huerfanas': peliculas_huerfanas,          # 👈 Películas Huérfanas
        'filtro_activo': filtro_activo,
    }
    
    # Asumo que la plantilla es 'lista_obras.html' o similar, pero debe mostrar AMBOS QuerySets
    return render(request, 'lista_obras.html', context)

def listado_independientes(request):
    # Obtener todas las obras independientes
    obras = ObraIndependiente.objects.all().order_by('-fecha_publicacion')
    
    context = {
        # Usamos los mismos nombres de contexto que en lista_obras.html
        'obras_independientes': obras,
        'peliculas_huerfanas': [], # Enviamos una lista vacía para no romper la plantilla
        'filtro_activo': 'Todas las Películas Independientes',
    }
    # Reutilizamos la plantilla que ya modificaste
    return render(request, 'lista_obras.html', context)