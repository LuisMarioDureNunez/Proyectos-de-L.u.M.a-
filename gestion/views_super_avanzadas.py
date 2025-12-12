# views_super_avanzadas.py - FUNCIONALIDADES SUPER AVANZADAS PARA PARAGUAY
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Sum, Count, Avg
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta, date
from decimal import Decimal

from .models import *
from .forms import *
from .views import es_administrador, puede_gestionar_obras

# =============================================
# GESTIÓN DE CONTRATISTAS SUPER AVANZADA
# =============================================

@login_required
@user_passes_test(es_administrador)
def lista_contratistas(request):
    """Lista de contratistas con filtros avanzados"""
    contratistas = Contratista.objects.all().order_by('-calificacion_promedio', '-total_trabajos_completados')
    
    # Filtros avanzados
    especialidad_filter = request.GET.get('especialidad')
    departamento_filter = request.GET.get('departamento')
    estado_filter = request.GET.get('estado')
    calificacion_min = request.GET.get('calificacion_min')
    query = request.GET.get('q')
    
    if especialidad_filter:
        contratistas = contratistas.filter(especialidad=especialidad_filter)
    
    if departamento_filter:
        contratistas = contratistas.filter(departamento=departamento_filter)
    
    if estado_filter:
        contratistas = contratistas.filter(estado=estado_filter)
    
    if calificacion_min:
        contratistas = contratistas.filter(calificacion_promedio__gte=calificacion_min)
    
    if query:
        contratistas = contratistas.filter(
            Q(usuario__first_name__icontains=query) |
            Q(usuario__last_name__icontains=query) |
            Q(nombre_empresa__icontains=query) |
            Q(ciudad__icontains=query)
        )
    
    # Paginación
    paginator = Paginator(contratistas, 12)
    page_number = request.GET.get('page')
    contratistas_page = paginator.get_page(page_number)
    
    # Estadísticas
    stats = {
        'total_contratistas': contratistas.count(),
        'disponibles': contratistas.filter(estado='disponible').count(),
        'ocupados': contratistas.filter(estado='ocupado').count(),
        'calificacion_promedio': contratistas.aggregate(avg=Avg('calificacion_promedio'))['avg'] or 0,
        'especialidades': Contratista.objects.values('especialidad').annotate(count=Count('id')).order_by('-count')[:5]
    }
    
    context = {
        'contratistas': contratistas_page,
        'stats': stats,
        'especialidades': Contratista.ESPECIALIDADES,
        'departamentos': Contratista.DEPARTAMENTOS_PARAGUAY,
        'estados': Contratista.ESTADOS,
        'especialidad_filter': especialidad_filter or '',
        'departamento_filter': departamento_filter or '',
        'estado_filter': estado_filter or '',
        'calificacion_min': calificacion_min or '',
        'query': query or '',
    }
    
    return render(request, 'gestion/contratistas/lista.html', context)

@login_required
@user_passes_test(es_administrador)
def nuevo_contratista(request):
    """Crear nuevo contratista"""
    if request.method == 'POST':
        form = ContratistaForm(request.POST, request.FILES)
        if form.is_valid():
            contratista = form.save(commit=False)
            # Crear usuario si no existe
            if not hasattr(request.user, 'perfil_contratista'):
                contratista.usuario = request.user
            contratista.save()
            messages.success(request, f'✅ Contratista {contratista.nombre_empresa or contratista.usuario.get_full_name()} creado exitosamente')
            return redirect('lista_contratistas')
    else:
        form = ContratistaForm()
    
    return render(request, 'gestion/contratistas/form.html', {
        'form': form,
        'titulo': 'Nuevo Contratista',
        'accion': 'Crear'
    })

@login_required
@user_passes_test(es_administrador)
def editar_contratista(request, id):
    """Editar contratista existente"""
    contratista = get_object_or_404(Contratista, id=id)
    
    if request.method == 'POST':
        form = ContratistaForm(request.POST, request.FILES, instance=contratista)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ Contratista {contratista.nombre_empresa or contratista.usuario.get_full_name()} actualizado exitosamente')
            return redirect('lista_contratistas')
    else:
        form = ContratistaForm(instance=contratista)
    
    return render(request, 'gestion/contratistas/form.html', {
        'form': form,
        'titulo': 'Editar Contratista',
        'accion': 'Actualizar',
        'contratista': contratista
    })

@login_required
def detalle_contratista(request, id):
    """Detalle completo de un contratista"""
    contratista = get_object_or_404(Contratista, id=id)
    
    # Contratos del contratista
    contratos = contratista.contratos.all().order_by('-fecha_creacion')[:10]
    
    # Estadísticas del contratista
    stats = {
        'contratos_activos': contratos.filter(estado='en_ejecucion').count(),
        'contratos_completados': contratos.filter(estado='completado').count(),
        'monto_total_contratos': contratos.aggregate(total=Sum('monto_total'))['total'] or 0,
    }
    
    context = {
        'contratista': contratista,
        'contratos': contratos,
        'stats': stats,
    }
    
    return render(request, 'gestion/contratistas/detalle.html', context)

# =============================================
# GESTIÓN DE PROPIETARIOS SUPER AVANZADA
# =============================================

@login_required
@user_passes_test(es_administrador)
def lista_propietarios(request):
    """Lista de propietarios con filtros avanzados"""
    propietarios = Propietario.objects.all().order_by('-fecha_registro')
    
    # Filtros
    tipo_filter = request.GET.get('tipo')
    departamento_filter = request.GET.get('departamento')
    verificado_filter = request.GET.get('verificado')
    query = request.GET.get('q')
    
    if tipo_filter:
        propietarios = propietarios.filter(tipo_propietario=tipo_filter)
    
    if departamento_filter:
        propietarios = propietarios.filter(departamento=departamento_filter)
    
    if verificado_filter:
        propietarios = propietarios.filter(verificado=verificado_filter == 'true')
    
    if query:
        propietarios = propietarios.filter(
            Q(nombre_completo__icontains=query) |
            Q(cedula_ruc__icontains=query) |
            Q(ciudad__icontains=query)
        )
    
    # Paginación
    paginator = Paginator(propietarios, 15)
    page_number = request.GET.get('page')
    propietarios_page = paginator.get_page(page_number)
    
    # Estadísticas
    stats = {
        'total_propietarios': propietarios.count(),
        'verificados': propietarios.filter(verificado=True).count(),
        'con_propiedades': propietarios.filter(propiedades__isnull=False).distinct().count(),
        'tipos': Propietario.objects.values('tipo_propietario').annotate(count=Count('id')).order_by('-count')
    }
    
    context = {
        'propietarios': propietarios_page,
        'stats': stats,
        'tipos': Propietario.TIPOS_PROPIETARIO,
        'departamentos': Contratista.DEPARTAMENTOS_PARAGUAY,
        'tipo_filter': tipo_filter or '',
        'departamento_filter': departamento_filter or '',
        'verificado_filter': verificado_filter or '',
        'query': query or '',
    }
    
    return render(request, 'gestion/propietarios/lista.html', context)

@login_required
@user_passes_test(es_administrador)
def nuevo_propietario(request):
    """Crear nuevo propietario"""
    if request.method == 'POST':
        form = PropietarioForm(request.POST, request.FILES)
        if form.is_valid():
            propietario = form.save(commit=False)
            propietario.usuario = request.user
            propietario.save()
            messages.success(request, f'✅ Propietario {propietario.nombre_completo} creado exitosamente')
            return redirect('lista_propietarios')
    else:
        form = PropietarioForm()
    
    return render(request, 'gestion/propietarios/form.html', {
        'form': form,
        'titulo': 'Nuevo Propietario',
        'accion': 'Crear'
    })

@login_required
def detalle_propietario(request, id):
    """Detalle completo de un propietario"""
    propietario = get_object_or_404(Propietario, id=id)
    
    # Propiedades del propietario
    propiedades = propietario.propiedades.all().order_by('-fecha_registro')
    
    # Obras del propietario
    obras = Obra.objects.filter(cliente=propietario.usuario).order_by('-fecha_creacion')[:5]
    
    context = {
        'propietario': propietario,
        'propiedades': propiedades,
        'obras': obras,
    }
    
    return render(request, 'gestion/propietarios/detalle.html', context)

# =============================================
# GESTIÓN DE PROPIEDADES
# =============================================

@login_required
def lista_propiedades(request):
    """Lista de propiedades"""
    if request.user.es_administrador():
        propiedades = Propiedad.objects.all().order_by('-fecha_registro')
    else:
        # Solo propiedades del usuario si es propietario
        try:
            propietario = request.user.perfil_propietario
            propiedades = propietario.propiedades.all().order_by('-fecha_registro')
        except:
            propiedades = Propiedad.objects.none()
    
    # Filtros
    tipo_filter = request.GET.get('tipo')
    departamento_filter = request.GET.get('departamento')
    estado_filter = request.GET.get('estado')
    
    if tipo_filter:
        propiedades = propiedades.filter(tipo_propiedad=tipo_filter)
    
    if departamento_filter:
        propiedades = propiedades.filter(departamento=departamento_filter)
    
    if estado_filter:
        propiedades = propiedades.filter(estado_propiedad=estado_filter)
    
    context = {
        'propiedades': propiedades,
        'tipos': Propiedad.TIPOS_PROPIEDAD,
        'departamentos': Contratista.DEPARTAMENTOS_PARAGUAY,
        'estados': Propiedad.ESTADOS_PROPIEDAD,
        'tipo_filter': tipo_filter or '',
        'departamento_filter': departamento_filter or '',
        'estado_filter': estado_filter or '',
    }
    
    return render(request, 'gestion/propiedades/lista.html', context)

@login_required
def nueva_propiedad(request):
    """Crear nueva propiedad"""
    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES)
        if form.is_valid():
            propiedad = form.save(commit=False)
            # Asignar al propietario actual o crear uno
            try:
                propiedad.propietario = request.user.perfil_propietario
            except:
                messages.error(request, '❌ Debe ser un propietario registrado para crear propiedades')
                return redirect('lista_propiedades')
            
            propiedad.save()
            messages.success(request, f'✅ Propiedad {propiedad.nombre_propiedad} creada exitosamente')
            return redirect('lista_propiedades')
    else:
        form = PropiedadForm()
    
    return render(request, 'gestion/propiedades/form.html', {
        'form': form,
        'titulo': 'Nueva Propiedad',
        'accion': 'Crear'
    })

# =============================================
# GESTIÓN DE EMPLEADOS SUPER AVANZADA
# =============================================

@login_required
@user_passes_test(es_administrador)
def lista_empleados(request):
    """Lista de empleados con filtros avanzados"""
    empleados = Empleado.objects.all().order_by('-fecha_ingreso')
    
    # Filtros
    cargo_filter = request.GET.get('cargo')
    estado_filter = request.GET.get('estado')
    departamento_filter = request.GET.get('departamento')
    turno_filter = request.GET.get('turno')
    query = request.GET.get('q')
    
    if cargo_filter:
        empleados = empleados.filter(cargo=cargo_filter)
    
    if estado_filter:
        empleados = empleados.filter(estado=estado_filter)
    
    if departamento_filter:
        empleados = empleados.filter(departamento=departamento_filter)
    
    if turno_filter:
        empleados = empleados.filter(turno=turno_filter)
    
    if query:
        empleados = empleados.filter(
            Q(usuario__first_name__icontains=query) |
            Q(usuario__last_name__icontains=query) |
            Q(codigo_empleado__icontains=query) |
            Q(cedula_identidad__icontains=query)
        )
    
    # Estadísticas
    stats = {
        'total_empleados': empleados.count(),
        'activos': empleados.filter(estado='activo').count(),
        'en_vacaciones': empleados.filter(estado='vacaciones').count(),
        'salario_promedio': empleados.aggregate(avg=Avg('salario_base'))['avg'] or 0,
        'cargos': Empleado.objects.values('cargo').annotate(count=Count('id')).order_by('-count')[:5]
    }
    
    context = {
        'empleados': empleados,
        'stats': stats,
        'cargos': Empleado.CARGOS,
        'estados': Empleado.ESTADOS_EMPLEADO,
        'departamentos': Contratista.DEPARTAMENTOS_PARAGUAY,
        'turnos': Empleado.TURNOS,
        'cargo_filter': cargo_filter or '',
        'estado_filter': estado_filter or '',
        'departamento_filter': departamento_filter or '',
        'turno_filter': turno_filter or '',
        'query': query or '',
    }
    
    return render(request, 'gestion/empleados/lista.html', context)

@login_required
@user_passes_test(es_administrador)
def nuevo_empleado(request):
    """Crear nuevo empleado"""
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            empleado = form.save(commit=False)
            empleado.usuario = request.user  # Temporal, debería ser el usuario del empleado
            empleado.save()
            messages.success(request, f'✅ Empleado {empleado.usuario.get_full_name()} creado exitosamente')
            return redirect('lista_empleados')
    else:
        form = EmpleadoForm()
    
    return render(request, 'gestion/empleados/form.html', {
        'form': form,
        'titulo': 'Nuevo Empleado',
        'accion': 'Crear'
    })

@login_required
def detalle_empleado(request, id):
    """Detalle completo de un empleado"""
    empleado = get_object_or_404(Empleado, id=id)
    
    # Verificar permisos
    if not request.user.es_administrador() and empleado.usuario != request.user:
        messages.error(request, '❌ No tienes permisos para ver este empleado')
        return redirect('lista_empleados')
    
    context = {
        'empleado': empleado,
    }
    
    return render(request, 'gestion/empleados/detalle.html', context)

# =============================================
# GESTIÓN DE PROVEEDORES SUPER AVANZADA
# =============================================

@login_required
@user_passes_test(es_administrador)
def lista_proveedores(request):
    """Lista de proveedores con filtros avanzados"""
    proveedores = Proveedor.objects.all().order_by('-calificacion_calidad', 'nombre_empresa')
    
    # Filtros
    tipo_filter = request.GET.get('tipo')
    departamento_filter = request.GET.get('departamento')
    estado_filter = request.GET.get('estado')
    calificacion_min = request.GET.get('calificacion_min')
    query = request.GET.get('q')
    
    if tipo_filter:
        proveedores = proveedores.filter(tipo_proveedor=tipo_filter)
    
    if departamento_filter:
        proveedores = proveedores.filter(departamento=departamento_filter)
    
    if estado_filter:
        proveedores = proveedores.filter(estado=estado_filter)
    
    if calificacion_min:
        proveedores = proveedores.filter(calificacion_calidad__gte=calificacion_min)
    
    if query:
        proveedores = proveedores.filter(
            Q(nombre_empresa__icontains=query) |
            Q(persona_contacto__icontains=query) |
            Q(ciudad__icontains=query)
        )
    
    # Estadísticas
    stats = {
        'total_proveedores': proveedores.count(),
        'activos': proveedores.filter(estado='activo').count(),
        'preferidos': proveedores.filter(estado='preferido').count(),
        'calificacion_promedio': proveedores.aggregate(avg=Avg('calificacion_calidad'))['avg'] or 0,
        'tipos': Proveedor.objects.values('tipo_proveedor').annotate(count=Count('id')).order_by('-count')[:5]
    }
    
    context = {
        'proveedores': proveedores,
        'stats': stats,
        'tipos': Proveedor.TIPOS_PROVEEDOR,
        'departamentos': Contratista.DEPARTAMENTOS_PARAGUAY,
        'estados': Proveedor.ESTADOS_PROVEEDOR,
        'tipo_filter': tipo_filter or '',
        'departamento_filter': departamento_filter or '',
        'estado_filter': estado_filter or '',
        'calificacion_min': calificacion_min or '',
        'query': query or '',
    }
    
    return render(request, 'gestion/proveedores/lista.html', context)

@login_required
@user_passes_test(es_administrador)
def nuevo_proveedor(request):
    """Crear nuevo proveedor"""
    if request.method == 'POST':
        form = ProveedorForm(request.POST, request.FILES)
        if form.is_valid():
            proveedor = form.save()
            messages.success(request, f'✅ Proveedor {proveedor.nombre_empresa} creado exitosamente')
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm()
    
    return render(request, 'gestion/proveedores/form.html', {
        'form': form,
        'titulo': 'Nuevo Proveedor',
        'accion': 'Crear'
    })

@login_required
def detalle_proveedor(request, id):
    """Detalle completo de un proveedor"""
    proveedor = get_object_or_404(Proveedor, id=id)
    
    # Productos del proveedor
    productos = proveedor.productos.all().order_by('nombre_producto')[:10]
    
    # Evaluaciones del proveedor
    evaluaciones = proveedor.evaluaciones.all().order_by('-fecha_evaluacion')[:5]
    
    context = {
        'proveedor': proveedor,
        'productos': productos,
        'evaluaciones': evaluaciones,
    }
    
    return render(request, 'gestion/proveedores/detalle.html', context)

# =============================================
# GESTIÓN DE CONTRATOS CON CONTRATISTAS
# =============================================

@login_required
@user_passes_test(es_administrador)
def lista_contratos(request):
    """Lista de contratos con contratistas"""
    contratos = ContratoContratista.objects.all().order_by('-fecha_creacion')
    
    # Filtros
    estado_filter = request.GET.get('estado')
    obra_filter = request.GET.get('obra')
    contratista_filter = request.GET.get('contratista')
    
    if estado_filter:
        contratos = contratos.filter(estado=estado_filter)
    
    if obra_filter:
        contratos = contratos.filter(obra_id=obra_filter)
    
    if contratista_filter:
        contratos = contratos.filter(contratista_id=contratista_filter)
    
    # Estadísticas
    stats = {
        'total_contratos': contratos.count(),
        'en_ejecucion': contratos.filter(estado='en_ejecucion').count(),
        'completados': contratos.filter(estado='completado').count(),
        'monto_total': contratos.aggregate(total=Sum('monto_total'))['total'] or 0,
    }
    
    context = {
        'contratos': contratos,
        'stats': stats,
        'estados': ContratoContratista.ESTADOS_CONTRATO,
        'obras': Obra.objects.all(),
        'contratistas': Contratista.objects.all(),
        'estado_filter': estado_filter or '',
        'obra_filter': obra_filter or '',
        'contratista_filter': contratista_filter or '',
    }
    
    return render(request, 'gestion/contratos/lista.html', context)

@login_required
@user_passes_test(es_administrador)
def nuevo_contrato(request):
    """Crear nuevo contrato con contratista"""
    if request.method == 'POST':
        form = ContratoContratistaForm(request.POST, request.FILES)
        if form.is_valid():
            contrato = form.save(commit=False)
            contrato.creado_por = request.user
            # Generar número de contrato único
            ultimo_contrato = ContratoContratista.objects.filter(
                numero_contrato__startswith=f'CONT-{timezone.now().year}'
            ).order_by('-numero_contrato').first()
            
            if ultimo_contrato:
                ultimo_numero = int(ultimo_contrato.numero_contrato.split('-')[-1])
                nuevo_numero = ultimo_numero + 1
            else:
                nuevo_numero = 1
            
            contrato.numero_contrato = f'CONT-{timezone.now().year}-{nuevo_numero:04d}'
            contrato.anticipo_monto = (contrato.monto_total * contrato.anticipo_porcentaje) / 100
            contrato.save()
            
            messages.success(request, f'✅ Contrato {contrato.numero_contrato} creado exitosamente')
            return redirect('lista_contratos')
    else:
        form = ContratoContratistaForm()
    
    return render(request, 'gestion/contratos/form.html', {
        'form': form,
        'titulo': 'Nuevo Contrato',
        'accion': 'Crear'
    })

# =============================================
# DASHBOARD SUPER AVANZADO CON NUEVAS FUNCIONALIDADES
# =============================================

@login_required
def dashboard_super_completo(request):
    """Dashboard super completo con todas las nuevas funcionalidades"""
    from decimal import Decimal
    from django.db.models import Sum, Count, Avg
    from django.utils import timezone
    from datetime import timedelta
    
    hoy = timezone.now().date()
    hace_30_dias = hoy - timedelta(days=30)
    
    # Estadísticas principales
    stats = {
        # Estadísticas existentes
        'total_obras': Obra.objects.count(),
        'total_presupuestos': Presupuesto.objects.count(),
        'total_materiales': Material.objects.count(),
        'total_usuarios': UsuarioPersonalizado.objects.count(),
        
        # Nuevas estadísticas
        'total_contratistas': Contratista.objects.count(),
        'contratistas_disponibles': Contratista.objects.filter(estado='disponible').count(),
        'total_propietarios': Propietario.objects.count(),
        'total_propiedades': Propiedad.objects.count(),
        'total_empleados': Empleado.objects.count(),
        'empleados_activos': Empleado.objects.filter(estado='activo').count(),
        'total_proveedores': Proveedor.objects.count(),
        'proveedores_activos': Proveedor.objects.filter(estado='activo').count(),
        'total_contratos': ContratoContratista.objects.count(),
        'contratos_activos': ContratoContratista.objects.filter(estado='en_ejecucion').count(),
    }
    
    # Cálculos financieros
    total_presupuestos_aceptados = Presupuesto.objects.filter(estado='aceptado').aggregate(total=Sum('total'))['total'] or Decimal('0')
    total_contratos_valor = ContratoContratista.objects.filter(estado__in=['firmado', 'en_ejecucion']).aggregate(total=Sum('monto_total'))['total'] or Decimal('0')
    
    stats.update({
        'total_presupuestos_aceptados': total_presupuestos_aceptados,
        'total_contratos_valor': total_contratos_valor,
    })
    
    # Actividad reciente
    actividades_recientes = []
    
    # Contratos recientes
    contratos_nuevos = ContratoContratista.objects.filter(fecha_creacion__gte=hace_30_dias).order_by('-fecha_creacion')[:5]
    for contrato in contratos_nuevos:
        actividades_recientes.append({
            'tipo': 'contrato',
            'accion': 'creado',
            'objeto': f'Contrato {contrato.numero_contrato}',
            'fecha': contrato.fecha_creacion,
            'usuario': contrato.creado_por.username,
            'icono': '📋'
        })
    
    # Contratistas nuevos
    contratistas_nuevos = Contratista.objects.filter(fecha_registro__gte=hace_30_dias).order_by('-fecha_registro')[:5]
    for contratista in contratistas_nuevos:
        actividades_recientes.append({
            'tipo': 'contratista',
            'accion': 'registrado',
            'objeto': contratista.nombre_empresa or contratista.usuario.get_full_name(),
            'fecha': contratista.fecha_registro,
            'usuario': 'Sistema',
            'icono': '👷'
        })
    
    # Ordenar actividades por fecha
    actividades_recientes.sort(key=lambda x: x['fecha'], reverse=True)
    actividades_recientes = actividades_recientes[:10]
    
    # Top contratistas
    top_contratistas = Contratista.objects.filter(
        calificacion_promedio__gt=0
    ).order_by('-calificacion_promedio', '-total_trabajos_completados')[:5]
    
    # Top proveedores
    top_proveedores = Proveedor.objects.filter(
        calificacion_calidad__gt=0
    ).order_by('-calificacion_calidad')[:5]
    
    # Distribución por departamentos
    contratistas_por_departamento = Contratista.objects.values('departamento').annotate(
        total=Count('id')
    ).order_by('-total')[:8]
    
    context = {
        'stats': stats,
        'actividades_recientes': actividades_recientes,
        'top_contratistas': top_contratistas,
        'top_proveedores': top_proveedores,
        'contratistas_por_departamento': list(contratistas_por_departamento),
        'hoy': hoy,
        'user': request.user,
    }
    
    return render(request, 'gestion/dashboard/dashboard_super_completo.html', context)

# =============================================
# VISTAS AJAX PARA FUNCIONALIDADES AVANZADAS
# =============================================

@login_required
def buscar_contratistas_ajax(request):
    """Búsqueda AJAX de contratistas"""
    query = request.GET.get('q', '')
    especialidad = request.GET.get('especialidad', '')
    departamento = request.GET.get('departamento', '')
    
    contratistas = Contratista.objects.filter(activo=True, estado='disponible')
    
    if query:
        contratistas = contratistas.filter(
            Q(usuario__first_name__icontains=query) |
            Q(usuario__last_name__icontains=query) |
            Q(nombre_empresa__icontains=query)
        )
    
    if especialidad:
        contratistas = contratistas.filter(especialidad=especialidad)
    
    if departamento:
        contratistas = contratistas.filter(departamento=departamento)
    
    resultados = []
    for contratista in contratistas[:10]:
        resultados.append({
            'id': contratista.id,
            'nombre': contratista.nombre_empresa or contratista.usuario.get_full_name(),
            'especialidad': contratista.get_especialidad_display(),
            'calificacion': float(contratista.calificacion_promedio),
            'tarifa_dia': float(contratista.tarifa_por_dia),
            'departamento': contratista.get_departamento_display(),
        })
    
    return JsonResponse({'resultados': resultados})

@login_required
def buscar_proveedores_ajax(request):
    """Búsqueda AJAX de proveedores"""
    query = request.GET.get('q', '')
    tipo = request.GET.get('tipo', '')
    
    proveedores = Proveedor.objects.filter(activo=True, estado='activo')
    
    if query:
        proveedores = proveedores.filter(nombre_empresa__icontains=query)
    
    if tipo:
        proveedores = proveedores.filter(tipo_proveedor=tipo)
    
    resultados = []
    for proveedor in proveedores[:10]:
        resultados.append({
            'id': proveedor.id,
            'nombre': proveedor.nombre_empresa,
            'tipo': proveedor.get_tipo_proveedor_display(),
            'calificacion': float(proveedor.get_calificacion_promedio()),
            'telefono': proveedor.telefono_principal,
            'email': proveedor.email_principal,
        })
    
    return JsonResponse({'resultados': resultados})

@login_required
def estadisticas_dashboard_ajax(request):
    """Estadísticas en tiempo real para el dashboard"""
    stats = {
        'obras_hoy': Obra.objects.filter(fecha_creacion__date=timezone.now().date()).count(),
        'presupuestos_hoy': Presupuesto.objects.filter(fecha_creacion__date=timezone.now().date()).count(),
        'contratos_hoy': ContratoContratista.objects.filter(fecha_creacion__date=timezone.now().date()).count(),
        'contratistas_disponibles': Contratista.objects.filter(estado='disponible').count(),
        'empleados_activos': Empleado.objects.filter(estado='activo').count(),
    }
    
    return JsonResponse(stats)