# views_repositorios.py - Vistas para gestión de repositorios GitHub
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Count, Avg, Sum
from django.core.paginator import Paginator
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import models
import requests
import json
from datetime import timedelta

from .models import RepositorioGitHub, TagRepositorio, ComentarioRepositorio, EstadisticaRepositorio
from .forms_repositorios import (
    RepositorioGitHubForm, FiltroRepositoriosForm, TagRepositorioForm,
    ComentarioRepositorioForm, SincronizarGitHubForm, ImportarGitHubForm
)

# =============================================
# VISTAS PRINCIPALES DE REPOSITORIOS
# =============================================

@login_required
def lista_repositorios(request):
    """Vista principal con todos los repositorios en formato increíble"""
    
    # Obtener todos los repositorios activos
    repositorios = RepositorioGitHub.objects.filter(activo=True).select_related('desarrollador')
    
    # Aplicar filtros
    form_filtros = FiltroRepositoriosForm(request.GET)
    if form_filtros.is_valid():
        data = form_filtros.cleaned_data
        
        # Filtro de búsqueda
        if data.get('busqueda'):
            repositorios = repositorios.filter(
                Q(nombre__icontains=data['busqueda']) |
                Q(descripcion__icontains=data['busqueda']) |
                Q(tecnologia_principal__icontains=data['busqueda']) |
                Q(cliente_proyecto__icontains=data['busqueda'])
            )
        
        # Filtros específicos
        if data.get('tipo_proyecto'):
            repositorios = repositorios.filter(tipo_proyecto=data['tipo_proyecto'])
        
        if data.get('tecnologia'):
            repositorios = repositorios.filter(
                Q(tecnologia_principal=data['tecnologia']) |
                Q(tecnologias_adicionales__contains=[data['tecnologia']])
            )
        
        if data.get('estado'):
            repositorios = repositorios.filter(estado=data['estado'])
        
        if data.get('solo_destacados'):
            repositorios = repositorios.filter(es_destacado=True)
        
        if data.get('solo_comerciales'):
            repositorios = repositorios.filter(es_comercial=True)
        
        # Ordenamiento
        if data.get('ordenar_por'):
            repositorios = repositorios.order_by(data['ordenar_por'])
    
    # Ordenamiento por defecto
    if not form_filtros.is_valid() or not form_filtros.cleaned_data.get('ordenar_por'):
        repositorios = repositorios.order_by('-es_destacado', '-fecha_ultimo_commit', '-estrellas')
    
    # Paginación
    paginator = Paginator(repositorios, 12)  # 12 repositorios por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estadísticas generales
    stats = {
        'total_repositorios': RepositorioGitHub.objects.filter(activo=True).count(),
        'repositorios_destacados': RepositorioGitHub.objects.filter(activo=True, es_destacado=True).count(),
        'repositorios_comerciales': RepositorioGitHub.objects.filter(activo=True, es_comercial=True).count(),
        'total_estrellas': RepositorioGitHub.objects.filter(activo=True).aggregate(
            total=models.Sum('estrellas')
        )['total'] or 0,
        'tecnologias_populares': RepositorioGitHub.objects.filter(activo=True).values(
            'tecnologia_principal'
        ).annotate(count=Count('id')).order_by('-count')[:5],
        'tipos_proyecto_populares': RepositorioGitHub.objects.filter(activo=True).values(
            'tipo_proyecto'
        ).annotate(count=Count('id')).order_by('-count')[:5],
    }
    
    # Tags más populares
    tags_populares = TagRepositorio.objects.filter(activo=True).annotate(
        repo_count=Count('repositorios', filter=Q(repositorios__activo=True))
    ).order_by('-repo_count')[:10]
    
    context = {
        'repositorios': page_obj,
        'form_filtros': form_filtros,
        'stats': stats,
        'tags_populares': tags_populares,
        'titulo': '🚀 Repositorios GitHub - L.u.M.a',
        'puede_crear': True,  # Todos los usuarios pueden crear repositorios
    }
    
    return render(request, 'gestion/repositorios/lista_increible.html', context)

@login_required
def detalle_repositorio(request, id):
    """Vista detallada de un repositorio específico"""
    repositorio = get_object_or_404(RepositorioGitHub, id=id, activo=True)
    
    # Incrementar contador de vistas
    repositorio.incrementar_vistas()
    
    # Obtener comentarios
    comentarios = repositorio.comentarios.filter(activo=True).select_related('usuario').order_by('-fecha_comentario')
    
    # Formulario para nuevo comentario
    comentario_form = ComentarioRepositorioForm()
    
    # Repositorios relacionados (misma tecnología o tipo)
    repositorios_relacionados = RepositorioGitHub.objects.filter(
        Q(tecnologia_principal=repositorio.tecnologia_principal) |
        Q(tipo_proyecto=repositorio.tipo_proyecto),
        activo=True
    ).exclude(id=repositorio.id)[:6]
    
    # Estadísticas del repositorio
    estadisticas_recientes = repositorio.estadisticas.order_by('-fecha')[:30]
    
    # Verificar si el usuario puede editar
    puede_editar = (
        request.user == repositorio.desarrollador or
        request.user.es_administrador() or
        request.user in repositorio.colaboradores.all()
    )
    
    context = {
        'repositorio': repositorio,
        'comentarios': comentarios,
        'comentario_form': comentario_form,
        'repositorios_relacionados': repositorios_relacionados,
        'estadisticas_recientes': estadisticas_recientes,
        'puede_editar': puede_editar,
    }
    
    return render(request, 'gestion/repositorios/detalle_increible.html', context)

@login_required
def crear_repositorio(request):
    """Crear nuevo repositorio"""
    if request.method == 'POST':
        form = RepositorioGitHubForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            repositorio = form.save()
            messages.success(
                request, 
                f'🎉 Repositorio "{repositorio.nombre}" creado exitosamente!'
            )
            return redirect('detalle_repositorio', id=repositorio.id)
    else:
        form = RepositorioGitHubForm(user=request.user)
    
    # Tags disponibles
    tags_disponibles = TagRepositorio.objects.filter(activo=True).order_by('nombre')
    
    context = {
        'form': form,
        'tags_disponibles': tags_disponibles,
        'titulo': '➕ Agregar Nuevo Repositorio',
        'accion': 'Crear',
    }
    
    return render(request, 'gestion/repositorios/form_increible.html', context)

@login_required
def editar_repositorio(request, id):
    """Editar repositorio existente"""
    repositorio = get_object_or_404(RepositorioGitHub, id=id)
    
    # Verificar permisos
    if not (request.user == repositorio.desarrollador or 
            request.user.es_administrador() or
            request.user in repositorio.colaboradores.all()):
        messages.error(request, '❌ No tienes permisos para editar este repositorio')
        return redirect('detalle_repositorio', id=repositorio.id)
    
    if request.method == 'POST':
        form = RepositorioGitHubForm(request.POST, request.FILES, instance=repositorio, user=request.user)
        if form.is_valid():
            repositorio = form.save()
            messages.success(
                request, 
                f'✅ Repositorio "{repositorio.nombre}" actualizado exitosamente!'
            )
            return redirect('detalle_repositorio', id=repositorio.id)
    else:
        form = RepositorioGitHubForm(instance=repositorio, user=request.user)
    
    # Tags disponibles
    tags_disponibles = TagRepositorio.objects.filter(activo=True).order_by('nombre')
    
    context = {
        'form': form,
        'repositorio': repositorio,
        'tags_disponibles': tags_disponibles,
        'titulo': f'✏️ Editar {repositorio.nombre}',
        'accion': 'Actualizar',
    }
    
    return render(request, 'gestion/repositorios/form_increible.html', context)

@login_required
def eliminar_repositorio(request, id):
    """Eliminar repositorio (soft delete)"""
    repositorio = get_object_or_404(RepositorioGitHub, id=id)
    
    # Verificar permisos
    if not (request.user == repositorio.desarrollador or request.user.es_administrador()):
        messages.error(request, '❌ No tienes permisos para eliminar este repositorio')
        return redirect('detalle_repositorio', id=repositorio.id)
    
    if request.method == 'POST':
        nombre_repositorio = repositorio.nombre
        repositorio.activo = False
        repositorio.save()
        
        messages.success(request, f'🗑️ Repositorio "{nombre_repositorio}" eliminado exitosamente')
        return redirect('lista_repositorios')
    
    context = {
        'repositorio': repositorio,
    }
    
    return render(request, 'gestion/repositorios/eliminar.html', context)

# =============================================
# VISTAS DE COMENTARIOS
# =============================================

@login_required
@require_http_methods(["POST"])
def agregar_comentario(request, repositorio_id):
    """Agregar comentario a un repositorio"""
    repositorio = get_object_or_404(RepositorioGitHub, id=repositorio_id, activo=True)
    
    # Verificar si ya comentó
    comentario_existente = ComentarioRepositorio.objects.filter(
        repositorio=repositorio,
        usuario=request.user
    ).first()
    
    if comentario_existente:
        messages.warning(request, '⚠️ Ya has comentado en este repositorio')
        return redirect('detalle_repositorio', id=repositorio_id)
    
    form = ComentarioRepositorioForm(request.POST)
    if form.is_valid():
        comentario = form.save(commit=False)
        comentario.repositorio = repositorio
        comentario.usuario = request.user
        comentario.save()
        
        messages.success(request, '💬 Comentario agregado exitosamente')
    else:
        messages.error(request, '❌ Error al agregar el comentario')
    
    return redirect('detalle_repositorio', id=repositorio_id)

# =============================================
# VISTAS DE SINCRONIZACIÓN CON GITHUB
# =============================================

@login_required
def sincronizar_repositorio(request, id):
    """Sincronizar un repositorio específico con GitHub"""
    repositorio = get_object_or_404(RepositorioGitHub, id=id)
    
    # Verificar permisos
    if not (request.user == repositorio.desarrollador or request.user.es_administrador()):
        return JsonResponse({'success': False, 'error': 'Sin permisos'})
    
    try:
        api_url = repositorio.get_url_github_api()
        if not api_url:
            return JsonResponse({'success': False, 'error': 'URL de GitHub inválida'})
        
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            # Actualizar datos
            repositorio.estrellas = data.get('stargazers_count', 0)
            repositorio.forks = data.get('forks_count', 0)
            repositorio.watchers = data.get('watchers_count', 0)
            repositorio.issues_abiertas = data.get('open_issues_count', 0)
            repositorio.lenguaje_principal = data.get('language')
            repositorio.tamaño_kb = data.get('size', 0)
            
            # Fechas
            from django.utils.dateparse import parse_datetime
            if data.get('updated_at'):
                repositorio.fecha_ultimo_commit = parse_datetime(data['updated_at'])
            
            repositorio.sincronizado_github = True
            repositorio.ultima_sincronizacion = timezone.now()
            repositorio.save()
            
            # Guardar estadísticas históricas
            EstadisticaRepositorio.objects.update_or_create(
                repositorio=repositorio,
                fecha=timezone.now().date(),
                defaults={
                    'estrellas': repositorio.estrellas,
                    'forks': repositorio.forks,
                    'watchers': repositorio.watchers,
                    'issues_abiertas': repositorio.issues_abiertas,
                }
            )
            
            return JsonResponse({
                'success': True,
                'data': {
                    'estrellas': repositorio.estrellas,
                    'forks': repositorio.forks,
                    'watchers': repositorio.watchers,
                    'issues_abiertas': repositorio.issues_abiertas,
                    'ultima_sincronizacion': repositorio.ultima_sincronizacion.strftime('%d/%m/%Y %H:%M')
                }
            })
        else:
            return JsonResponse({'success': False, 'error': 'Repositorio no encontrado en GitHub'})
            
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def sincronizar_todos_repositorios(request):
    """Sincronizar todos los repositorios del usuario con GitHub"""
    if request.method == 'POST':
        form = SincronizarGitHubForm(request.POST, user=request.user)
        if form.is_valid():
            repositorios_a_sincronizar = []
            
            if form.cleaned_data.get('sincronizar_todos'):
                repositorios_a_sincronizar = RepositorioGitHub.objects.filter(
                    desarrollador=request.user,
                    activo=True
                )
            else:
                repositorios_a_sincronizar = form.cleaned_data.get('repositorios', [])
            
            sincronizados = 0
            errores = 0
            
            for repositorio in repositorios_a_sincronizar:
                try:
                    # Lógica de sincronización (similar a sincronizar_repositorio)
                    api_url = repositorio.get_url_github_api()
                    if api_url:
                        response = requests.get(api_url, timeout=10)
                        if response.status_code == 200:
                            data = response.json()
                            
                            repositorio.estrellas = data.get('stargazers_count', 0)
                            repositorio.forks = data.get('forks_count', 0)
                            repositorio.watchers = data.get('watchers_count', 0)
                            repositorio.issues_abiertas = data.get('open_issues_count', 0)
                            repositorio.ultima_sincronizacion = timezone.now()
                            repositorio.save()
                            
                            sincronizados += 1
                        else:
                            errores += 1
                    else:
                        errores += 1
                except:
                    errores += 1
            
            if sincronizados > 0:
                messages.success(
                    request, 
                    f'✅ {sincronizados} repositorios sincronizados exitosamente'
                )
            if errores > 0:
                messages.warning(
                    request, 
                    f'⚠️ {errores} repositorios no pudieron sincronizarse'
                )
            
            return redirect('lista_repositorios')
    else:
        form = SincronizarGitHubForm(user=request.user)
    
    context = {
        'form': form,
        'titulo': '🔄 Sincronizar Repositorios con GitHub',
    }
    
    return render(request, 'gestion/repositorios/sincronizar.html', context)

@login_required
def importar_desde_github(request):
    """Importar repositorios desde GitHub automáticamente"""
    if request.method == 'POST':
        form = ImportarGitHubForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username_github']
            incluir_forks = form.cleaned_data['incluir_forks']
            solo_publicos = form.cleaned_data['solo_publicos']
            limite = form.cleaned_data['limite_repositorios']
            
            try:
                # Obtener repositorios del usuario
                url = f'https://api.github.com/users/{username}/repos'
                params = {
                    'type': 'public' if solo_publicos else 'all',
                    'sort': 'updated',
                    'per_page': limite
                }
                
                response = requests.get(url, params=params, timeout=15)
                if response.status_code == 200:
                    repos_data = response.json()
                    
                    importados = 0
                    omitidos = 0
                    
                    for repo_data in repos_data:
                        # Verificar si es fork y si se deben incluir
                        if repo_data.get('fork', False) and not incluir_forks:
                            omitidos += 1
                            continue
                        
                        # Verificar si ya existe
                        if RepositorioGitHub.objects.filter(
                            url_repositorio=repo_data['html_url']
                        ).exists():
                            omitidos += 1
                            continue
                        
                        # Crear repositorio
                        repositorio = RepositorioGitHub.objects.create(
                            desarrollador=request.user,
                            nombre=repo_data['name'],
                            descripcion=repo_data.get('description', '') or f"Repositorio {repo_data['name']}",
                            url_repositorio=repo_data['html_url'],
                            github_id=repo_data['id'],
                            estrellas=repo_data.get('stargazers_count', 0),
                            forks=repo_data.get('forks_count', 0),
                            watchers=repo_data.get('watchers_count', 0),
                            issues_abiertas=repo_data.get('open_issues_count', 0),
                            lenguaje_principal=repo_data.get('language'),
                            tamaño_kb=repo_data.get('size', 0),
                            es_privado=repo_data.get('private', False),
                            es_fork=repo_data.get('fork', False),
                            tiene_wiki=repo_data.get('has_wiki', False),
                            tiene_pages=repo_data.get('has_pages', False),
                            licencia=repo_data.get('license', {}).get('name') if repo_data.get('license') else None,
                            sincronizado_github=True,
                            ultima_sincronizacion=timezone.now()
                        )
                        
                        # Fechas
                        from django.utils.dateparse import parse_datetime
                        if repo_data.get('created_at'):
                            repositorio.fecha_creacion_github = parse_datetime(repo_data['created_at'])
                        if repo_data.get('updated_at'):
                            repositorio.fecha_ultimo_commit = parse_datetime(repo_data['updated_at'])
                        
                        repositorio.save()
                        importados += 1
                    
                    messages.success(
                        request,
                        f'🎉 {importados} repositorios importados exitosamente. {omitidos} omitidos.'
                    )
                    return redirect('lista_repositorios')
                else:
                    messages.error(request, '❌ Error al obtener repositorios de GitHub')
            
            except Exception as e:
                messages.error(request, f'❌ Error durante la importación: {str(e)}')
    else:
        form = ImportarGitHubForm()
    
    context = {
        'form': form,
        'titulo': '📥 Importar Repositorios desde GitHub',
    }
    
    return render(request, 'gestion/repositorios/importar.html', context)

# =============================================
# VISTAS DE ESTADÍSTICAS Y DASHBOARD
# =============================================

@login_required
def dashboard_repositorios(request):
    """Dashboard con estadísticas de repositorios"""
    
    # Estadísticas generales
    stats = {
        'total_repositorios': RepositorioGitHub.objects.filter(activo=True).count(),
        'mis_repositorios': RepositorioGitHub.objects.filter(desarrollador=request.user, activo=True).count(),
        'total_estrellas': RepositorioGitHub.objects.filter(activo=True).aggregate(
            total=models.Sum('estrellas')
        )['total'] or 0,
        'total_forks': RepositorioGitHub.objects.filter(activo=True).aggregate(
            total=models.Sum('forks')
        )['total'] or 0,
        'repositorios_destacados': RepositorioGitHub.objects.filter(activo=True, es_destacado=True).count(),
        'repositorios_comerciales': RepositorioGitHub.objects.filter(activo=True, es_comercial=True).count(),
    }
    
    # Repositorios más populares
    repositorios_populares = RepositorioGitHub.objects.filter(activo=True).order_by('-estrellas', '-forks')[:10]
    
    # Repositorios recientes
    repositorios_recientes = RepositorioGitHub.objects.filter(activo=True).order_by('-fecha_agregado')[:10]
    
    # Tecnologías más usadas
    tecnologias_populares = RepositorioGitHub.objects.filter(activo=True).values(
        'tecnologia_principal'
    ).annotate(count=Count('id')).order_by('-count')[:10]
    
    # Tipos de proyecto más comunes
    tipos_proyecto = RepositorioGitHub.objects.filter(activo=True).values(
        'tipo_proyecto'
    ).annotate(count=Count('id')).order_by('-count')[:10]
    
    # Actividad reciente (últimos 30 días)
    hace_30_dias = timezone.now() - timedelta(days=30)
    actividad_reciente = RepositorioGitHub.objects.filter(
        fecha_agregado__gte=hace_30_dias,
        activo=True
    ).order_by('-fecha_agregado')[:20]
    
    context = {
        'stats': stats,
        'repositorios_populares': repositorios_populares,
        'repositorios_recientes': repositorios_recientes,
        'tecnologias_populares': tecnologias_populares,
        'tipos_proyecto': tipos_proyecto,
        'actividad_reciente': actividad_reciente,
    }
    
    return render(request, 'gestion/repositorios/dashboard.html', context)

# =============================================
# VISTAS AJAX Y API
# =============================================

@login_required
def buscar_repositorios_ajax(request):
    """Búsqueda AJAX de repositorios"""
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse({'repositorios': []})
    
    repositorios = RepositorioGitHub.objects.filter(
        Q(nombre__icontains=query) |
        Q(descripcion__icontains=query),
        activo=True
    )[:10]
    
    resultados = []
    for repo in repositorios:
        resultados.append({
            'id': repo.id,
            'nombre': repo.nombre,
            'descripcion': repo.descripcion[:100],
            'tipo_proyecto': repo.get_tipo_proyecto_display(),
            'tecnologia_principal': repo.get_tecnologia_principal_display(),
            'estrellas': repo.estrellas,
            'url': f'/repositorios/{repo.id}/',
            'icono': repo.get_icono_tipo(),
        })
    
    return JsonResponse({'repositorios': resultados})

@login_required
def estadisticas_repositorio_ajax(request, id):
    """Obtener estadísticas de un repositorio vía AJAX"""
    repositorio = get_object_or_404(RepositorioGitHub, id=id, activo=True)
    
    # Estadísticas de los últimos 30 días
    hace_30_dias = timezone.now().date() - timedelta(days=30)
    estadisticas = repositorio.estadisticas.filter(fecha__gte=hace_30_dias).order_by('fecha')
    
    datos = {
        'fechas': [stat.fecha.strftime('%d/%m') for stat in estadisticas],
        'estrellas': [stat.estrellas for stat in estadisticas],
        'forks': [stat.forks for stat in estadisticas],
        'watchers': [stat.watchers for stat in estadisticas],
        'vistas': [stat.vistas_dia for stat in estadisticas],
    }
    
    return JsonResponse(datos)

# =============================================
# VISTAS DE GESTIÓN DE TAGS
# =============================================

@login_required
def gestionar_tags(request):
    """Gestionar tags de repositorios"""
    tags = TagRepositorio.objects.filter(activo=True).annotate(
        repo_count=Count('repositorios', filter=Q(repositorios__activo=True))
    ).order_by('nombre')
    
    if request.method == 'POST':
        form = TagRepositorioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Tag creado exitosamente')
            return redirect('gestionar_tags')
    else:
        form = TagRepositorioForm()
    
    context = {
        'tags': tags,
        'form': form,
    }
    
    return render(request, 'gestion/repositorios/gestionar_tags.html', context)