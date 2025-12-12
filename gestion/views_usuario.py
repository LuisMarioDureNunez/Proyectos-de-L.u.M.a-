from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings
import os
import json

@login_required
def perfil_usuario(request):
    """Vista del perfil de usuario con foto y logo de empresa"""
    
    user = request.user
    
    # Estadísticas del usuario
    estadisticas = {
        'productos_creados': getattr(user, 'productos_creados', []),
        'obras_realizadas': getattr(user, 'obras_constructor', []) if hasattr(user, 'obras_constructor') else [],
        'pedidos_realizados': getattr(user, 'pedidos', []) if hasattr(user, 'pedidos') else [],
        'notificaciones': getattr(user, 'notificaciones', []) if hasattr(user, 'notificaciones') else [],
    }
    
    context = {
        'user': user,
        'estadisticas': estadisticas,
    }
    
    return render(request, 'usuarios/perfil_usuario.html', context)

@login_required
@csrf_exempt
def actualizar_avatar(request):
    """Actualizar foto de perfil del usuario"""
    
    if request.method == 'POST' and request.FILES.get('avatar'):
        try:
            avatar_file = request.FILES['avatar']
            
            # Validar tipo de archivo
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if avatar_file.content_type not in allowed_types:
                return JsonResponse({
                    'success': False,
                    'error': 'Tipo de archivo no permitido. Use JPG, PNG o GIF.'
                })
            
            # Validar tamaño (máximo 5MB)
            if avatar_file.size > 5 * 1024 * 1024:
                return JsonResponse({
                    'success': False,
                    'error': 'El archivo es demasiado grande. Máximo 5MB.'
                })
            
            # Eliminar avatar anterior si existe
            if request.user.avatar:
                if default_storage.exists(request.user.avatar.name):
                    default_storage.delete(request.user.avatar.name)
            
            # Guardar nuevo avatar
            request.user.avatar = avatar_file
            request.user.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Avatar actualizado correctamente',
                'avatar_url': request.user.avatar.url
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error al actualizar avatar: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'No se recibió ningún archivo'
    })

@login_required
@csrf_exempt
def actualizar_logo(request):
    """Actualizar logo de la empresa del usuario"""
    
    if request.method == 'POST' and request.FILES.get('logo'):
        try:
            logo_file = request.FILES['logo']
            
            # Verificar que el usuario tenga una tienda
            if not hasattr(request.user, 'tienda') or not request.user.tienda:
                return JsonResponse({
                    'success': False,
                    'error': 'Primero debe crear una empresa'
                })
            
            # Validar tipo de archivo
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if logo_file.content_type not in allowed_types:
                return JsonResponse({
                    'success': False,
                    'error': 'Tipo de archivo no permitido. Use JPG, PNG o GIF.'
                })
            
            # Validar tamaño (máximo 3MB)
            if logo_file.size > 3 * 1024 * 1024:
                return JsonResponse({
                    'success': False,
                    'error': 'El archivo es demasiado grande. Máximo 3MB.'
                })
            
            # Eliminar logo anterior si existe
            if request.user.tienda.logo:
                if default_storage.exists(request.user.tienda.logo.name):
                    default_storage.delete(request.user.tienda.logo.name)
            
            # Guardar nuevo logo
            request.user.tienda.logo = logo_file
            request.user.tienda.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Logo actualizado correctamente',
                'logo_url': request.user.tienda.logo.url
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error al actualizar logo: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'No se recibió ningún archivo'
    })

@login_required
@csrf_exempt
def actualizar_perfil(request):
    """Actualizar información del perfil del usuario"""
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            full_name = request.POST.get('full_name', '').strip()
            email = request.POST.get('email', '').strip()
            telefono = request.POST.get('telefono', '').strip()
            direccion = request.POST.get('direccion', '').strip()
            
            # Validar email
            if email and email != request.user.email:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                    return JsonResponse({
                        'success': False,
                        'error': 'Este email ya está en uso por otro usuario'
                    })
            
            # Actualizar campos
            if full_name:
                names = full_name.split(' ', 1)
                request.user.first_name = names[0]
                request.user.last_name = names[1] if len(names) > 1 else ''
            
            if email:
                request.user.email = email
            
            if hasattr(request.user, 'telefono'):
                request.user.telefono = telefono
            
            if hasattr(request.user, 'direccion'):
                request.user.direccion = direccion
            
            request.user.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Perfil actualizado correctamente'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error al actualizar perfil: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Método no permitido'
    })

@login_required
def estadisticas_usuario(request):
    """API para obtener estadísticas del usuario"""
    
    user = request.user
    
    # Calcular estadísticas reales
    estadisticas = {
        'productos_creados': 0,
        'obras_realizadas': 0,
        'pedidos_realizados': 0,
        'notificaciones_no_leidas': 0,
        'actividad_reciente': []
    }
    
    # Productos creados
    if hasattr(user, 'productos_creados'):
        estadisticas['productos_creados'] = user.productos_creados.count()
    
    # Obras como constructor
    if hasattr(user, 'obras_constructor'):
        estadisticas['obras_realizadas'] = user.obras_constructor.count()
    
    # Pedidos como cliente
    if hasattr(user, 'pedidos'):
        estadisticas['pedidos_realizados'] = user.pedidos.count()
    
    # Notificaciones no leídas
    if hasattr(user, 'notificaciones'):
        estadisticas['notificaciones_no_leidas'] = user.notificaciones.filter(leida=False).count()
    
    # Actividad reciente (últimas 10 acciones)
    actividades = []
    
    # Agregar productos recientes
    if hasattr(user, 'productos_creados'):
        productos_recientes = user.productos_creados.order_by('-fecha_creacion')[:3]
        for producto in productos_recientes:
            actividades.append({
                'tipo': 'producto_creado',
                'descripcion': f'Producto "{producto.nombre}" creado',
                'fecha': producto.fecha_creacion,
                'icono': 'fas fa-plus-circle',
                'color': 'success'
            })
    
    # Agregar pedidos recientes
    if hasattr(user, 'pedidos'):
        pedidos_recientes = user.pedidos.order_by('-fecha_pedido')[:3]
        for pedido in pedidos_recientes:
            actividades.append({
                'tipo': 'pedido_realizado',
                'descripcion': f'Pedido #{pedido.numero_pedido} realizado',
                'fecha': pedido.fecha_pedido,
                'icono': 'fas fa-shopping-cart',
                'color': 'primary'
            })
    
    # Ordenar por fecha
    actividades.sort(key=lambda x: x['fecha'], reverse=True)
    estadisticas['actividad_reciente'] = actividades[:10]
    
    return JsonResponse(estadisticas)

@login_required
def configuracion_notificaciones(request):
    """Configuración de notificaciones del usuario"""
    
    if request.method == 'POST':
        try:
            # Obtener configuraciones
            email_presupuestos = request.POST.get('email_presupuestos') == 'on'
            email_obras = request.POST.get('email_obras') == 'on'
            email_sistema = request.POST.get('email_sistema') == 'on'
            push_notificaciones = request.POST.get('push_notificaciones') == 'on'
            
            # Obtener o crear configuración
            from .models import ConfiguracionNotificacion
            config, created = ConfiguracionNotificacion.objects.get_or_create(
                usuario=request.user,
                defaults={
                    'email_presupuestos': True,
                    'email_obras': True,
                    'email_sistema': True,
                    'push_presupuestos': True,
                }
            )
            
            # Actualizar configuración
            config.email_presupuestos = email_presupuestos
            config.email_obras = email_obras
            config.email_sistema = email_sistema
            config.push_presupuestos = push_notificaciones
            config.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Configuración de notificaciones actualizada'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    # GET: mostrar configuración actual
    from .models import ConfiguracionNotificacion
    try:
        config = ConfiguracionNotificacion.objects.get(usuario=request.user)
    except ConfiguracionNotificacion.DoesNotExist:
        config = ConfiguracionNotificacion.objects.create(usuario=request.user)
    
    return render(request, 'usuarios/configuracion_notificaciones.html', {'config': config})