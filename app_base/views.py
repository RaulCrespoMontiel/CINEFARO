from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# NO NECESITAMOS ContentType si usamos ForeignKeys directos.
# from django.contrib.contenttypes.models import ContentType 
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, Http404

# Asegúrate de que estos modelos y formularios existan y estén bien definidos
from .forms import RegistroForm # Necesaria para registro_usuario
#from app_creadores.forms import ComentarioForm # Asumiendo que el formulario está en app_creadores
from .forms import ComentarioForm
from app_creadores.models import ObraIndependiente 
from app_conservacion.models import PeliculaHuerfana
from app_base.models import Categoria # 👈 Modelo Categoria de la BD
from app_base.models import Comentario # Asumiendo que el modelo Comentario está aquí
from django.db.models import Count, Q, F


"""
def home(request):
    slogan_del_dia = "El cine que importa, de los que importan."
    
    # --- 1. CONSULTA DE CONTENIDO PRINCIPAL ---
    
    # Tendencias: Las 6 obras independientes más recientes (la lógica de filtro por GET es innecesaria aquí)
    tendencias = ObraIndependiente.objects.all().order_by('-fecha_publicacion')[:6]
    
    # Últimas de Conservación (Huérfanas)
    ultimas_conservacion = PeliculaHuerfana.objects.all().order_by('-fecha_ingreso')[:6]

    # --- 2. DATOS PARA LA BARRA LATERAL (SIDEBAR) ---
    
    # Géneros: Obtenemos todas las categorías (para el listado Géneros (Ficción Independiente))
    categorias_sidebar = Categoria.objects.all().order_by('nombre') 
    
    # Directores Destacados: Obtenemos los usuarios que han publicado obras
    autores_con_obras = User.objects.filter(obras_creadas__isnull=False).distinct()
    
    # --- 3. CONTEXTO ---
    context = {
        'slogan': slogan_del_dia,
        'tendencias': tendencias,
        'ultimas_conservacion': ultimas_conservacion,
        
        # DATOS DE BARRA LATERAL
        'categorias_sidebar': categorias_sidebar,
        'autores_con_obras': autores_con_obras,
        'titulo_categorias': 'Géneros (Ficción Independiente)', # Título para el Sidebar
    }
    
    return render(request, 'home.html', context)
"""

def home(request):
    slogan_del_dia = "El cine que importa, de los que importan."
    
    # --- 1. CONSULTA DE CONTENIDO PRINCIPAL ---
    
    # Tendencias: Las 6 obras independientes más recientes
    tendencias = ObraIndependiente.objects.all().order_by('-fecha_publicacion')[:6]
    
    # Últimas de Conservación (Huérfanas)
    ultimas_conservacion = PeliculaHuerfana.objects.all().order_by('-fecha_ingreso')[:6]

    # --- 2. DATOS PARA LA BARRA LATERAL (SIDEBAR) ---
    
    # 🌟 MODIFICACIÓN PARA UNIFICAR GÉNEROS Y OBTENER CONTEO 🌟
    # --------------------------------------------------------
    
    # 1. Anotar el conteo de obras independientes (related_name: obras_independientes)
    # 2. Anotar el conteo de películas huérfanas (related_name: peliculahuerfana_set, si no se especificó)
    # 3. Sumar ambos conteos (total_obras)
    # 4. Filtrar para solo mostrar categorías con total_obras > 0
    
    categorias_unificadas = Categoria.objects.annotate(
        num_independientes=Count('obras_independientes', distinct=True),
        
        # ❌ CAMBIAR: 'peliculahuerfana_set'
        # ✅ A: 'peliculas_huerfanas'
        num_huerfanas=Count('peliculas_huerfanas', distinct=True), 
        
        total_obras=F('num_independientes') + F('num_huerfanas')
    ).filter(
        total_obras__gt=0
    ).order_by('nombre')
    
    # --------------------------------------------------------
    
    # Directores Destacados: Obtenemos los usuarios que han publicado obras
    autores_con_obras = User.objects.filter(obras_creadas__isnull=False).distinct()
    
    # --- 3. CONTEXTO ---
    context = {
        'slogan': slogan_del_dia,
        'tendencias': tendencias,
        'ultimas_conservacion': ultimas_conservacion,
        
        # DATOS DE BARRA LATERAL
        'categorias_sidebar': categorias_unificadas, # 👈 Usamos el QuerySet unificado
        'autores_con_obras': autores_con_obras,
        'titulo_categorias': 'Géneros (Ficción y Conservación)', # 👈 Título actualizado
    }
    
    return render(request, 'home.html', context)

# La función registro_usuario no necesita cambios, solo asegúrate que RegistroForm está importado.
def registro_usuario(request):
    # ... (código existente) ...
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = RegistroForm()
        
    context = {'form': form}
    return render(request, 'registro.html', context)


@login_required
def agregar_comentario(request, content_type_str, object_id):
    
    if request.method == 'POST':
        
        # 1. Identificar el modelo y el nombre del argumento de la URL
        if content_type_str == 'obra':
            model_class = ObraIndependiente
            fk_field_name = 'obra_independiente' 
            # 🌟 NOMBRE DE LA URL CON NAMESPACE CORREGIDO 🌟
            redirect_name = 'app_creadores:detalle_obra' 
            redirect_arg_name = 'obra_id'
            
        elif content_type_str == 'huerfana':
            model_class = PeliculaHuerfana
            fk_field_name = 'pelicula_huerfana'
            redirect_name = 'app_conservacion:detalle_huerfana' 
            redirect_arg_name = 'pk'
        else:
            return redirect('home')
            
        # 2. Obtener el objeto padre
        parent_object = get_object_or_404(model_class, pk=object_id)
        
        # 3. Procesar el formulario
        form = ComentarioForm(request.POST) # Asegúrate de que ComentarioForm esté importado
        
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user 
            
            # 4. Asignar el objeto padre
            setattr(comentario, fk_field_name, parent_object)
            comentario.save()
            
            # 5. Redireccionar al detalle de la obra/película con el argumento correcto
            # Creamos el diccionario de argumentos para la redirección: {'obra_id': object_id} o {'pk': object_id}
            redirect_kwargs = {redirect_arg_name: object_id}
            
            return redirect(redirect_name, **redirect_kwargs) # Redirección exitosa
        
    # Si no es POST o el formulario es inválido, regresamos al detalle
    if content_type_str == 'obra':
        return redirect('app_creadores:detalle_obra', obra_id=object_id)
    elif content_type_str == 'huerfana':
        return redirect('app_conservacion:detalle_huerfana', pk=object_id)
    else:
        return redirect('home')

# Nueva vista para listar todas las categorías
def lista_categorias(request):
    # Obtiene todas las categorías ordenadas por nombre
    categorias = Categoria.objects.all().order_by('nombre')
    
    # Prepara el contexto para enviarlo a la plantilla
    context = {
        'categorias': categorias,
        'titulo': 'Explorar Categorías',
    }
    
    # Renderiza la plantilla (que crearemos en el paso 3)
    return render(request, 'lista_categorias.html', context)



def busqueda_global(request):
    query = request.GET.get('q') 
    
    obras_independientes = ObraIndependiente.objects.none() # Inicialización limpia
    peliculas_huerfanas = PeliculaHuerfana.objects.none()    # Inicialización limpia
    
    filtro_activo = "Búsqueda"

    if query:
        # 1. CONSULTA PARA OBRAS INDEPENDIENTES
        consulta_obras = (
            Q(titulo__icontains=query) |
            Q(nombre_autor__icontains=query) | 
            Q(categoria__nombre__icontains=query) |
            Q(creador__username__icontains=query) 
        )
        
        # Intentamos añadir el filtro por año (ObraIndependiente usa 'anio_produccion')
        try:
            if query.isdigit() and len(query) == 4:
                consulta_obras = consulta_obras | Q(anio_produccion=int(query))
        except:
            pass 

        # Ejecutamos la consulta para Obras Independientes
        obras_independientes = ObraIndependiente.objects.filter(consulta_obras).distinct()
        
        # ----------------------------------------------------
        
        # 2. CONSULTA PARA PELÍCULAS HUÉRFANAS (¡NUEVO!)
        consulta_huerfanas = (
            Q(titulo__icontains=query) |
            
            # ❌ CAMBIAR autor_director_conocido por nombre_autor ❌
            Q(nombre_autor__icontains=query) | 
            
            Q(categorias__nombre__icontains=query) |
            Q(descripcion__icontains=query)
        )
        
        # Intentamos añadir el filtro por año (PeliculaHuerfana usa 'anio_estimado')
        try:
            if query.isdigit() and len(query) == 4:
                consulta_huerfanas = consulta_huerfanas | Q(anio_estimado=int(query))
        except:
            pass

        # Ejecutamos la consulta para Películas Huérfanas
        peliculas_huerfanas = PeliculaHuerfana.objects.filter(consulta_huerfanas).distinct()

        # ----------------------------------------------------

        filtro_activo = f"Resultados para: \"{query}\""

    context = {
        # Renombramos 'obras' para ser más claro
        'obras_independientes': obras_independientes, 
        'peliculas_huerfanas': peliculas_huerfanas, # 👈 Nuevo
        'filtro_activo': filtro_activo,
        'query': query,
    }
    
    # 3. CAMBIAR LA PLANTILLA A UNA GENÉRICA DE BÚSQUEDA
    # Usa una plantilla nueva (busqueda_global.html) que muestre ambas secciones
    return render(request, 'busqueda_global.html', context)