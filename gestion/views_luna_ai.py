# views_luna_ai.py - VISTAS PARA L.u.N.a AI SUPER AVANZADA
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.db.models import Sum, Count, Avg
import json
from decimal import Decimal

from .models import *

@csrf_exempt
def luna_ai_chat(request):
    """Endpoint principal para el chat con L.u.N.a AI"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '').lower()
            user_id = data.get('user_id')
            
            # Obtener conocimiento actualizado del sistema
            knowledge = get_luna_knowledge(request.user if request.user.is_authenticated else None)
            
            # Generar respuesta inteligente
            response = generate_luna_response(question, knowledge, request.user if request.user.is_authenticated else None)
            
            return JsonResponse({
                'success': True,
                'response': response,
                'timestamp': timezone.now().isoformat()
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt
def luna_ai_login(request):
    """Login específico para L.u.N.a AI"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'user': {
                        'username': user.username,
                        'full_name': user.get_full_name() or user.username,
                        'role': user.get_rol_display(),
                        'avatar': user.get_avatar_url(),
                        'is_admin': user.es_administrador()
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Credenciales inválidas'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

def get_luna_knowledge(user=None):
    """Obtiene el conocimiento completo y actualizado del sistema"""
    try:
        # Estadísticas generales
        stats = {
            'total_obras': Obra.objects.count(),
            'total_presupuestos': Presupuesto.objects.count(),
            'total_materiales': Material.objects.count(),
            'total_contratistas': Contratista.objects.count() if 'Contratista' in globals() else 0,
            'total_empleados': Empleado.objects.count() if 'Empleado' in globals() else 0,
            'total_proveedores': Proveedor.objects.count() if 'Proveedor' in globals() else 0,
            'total_usuarios': UsuarioPersonalizado.objects.count(),
        }
        
        # Materiales con precios actualizados
        materiales = {}
        for material in Material.objects.filter(activo=True)[:20]:
            materiales[material.nombre.lower()] = {
                'precio': float(material.precio),
                'stock': material.stock,
                'unidad': material.unidad_medida,
                'id': material.id
            }
        
        # Maquinarias disponibles
        maquinarias = {}
        for maquinaria in Maquinaria.objects.all()[:15]:
            maquinarias[maquinaria.nombre.lower()] = {
                'costo': float(maquinaria.costo_alquiler_dia),
                'estado': maquinaria.get_estado_display(),
                'disponible': maquinaria.estado == 'disponible',
                'id': maquinaria.id
            }
        
        # Obras del usuario (si está logueado)
        obras_usuario = []
        if user and user.is_authenticated:
            if user.es_administrador():
                obras = Obra.objects.all()[:10]
            else:
                obras = Obra.objects.filter(cliente=user)[:10]
            
            for obra in obras:
                obras_usuario.append({
                    'nombre': obra.nombre,
                    'estado': obra.get_estado_display(),
                    'presupuesto': float(obra.presupuesto_asignado),
                    'ubicacion': obra.ubicacion,
                    'progreso': obra.progreso_porcentaje()
                })
        
        # Contratistas disponibles
        contratistas = []
        if 'Contratista' in globals():
            for contratista in Contratista.objects.filter(activo=True, estado='disponible')[:10]:
                contratistas.append({
                    'nombre': contratista.nombre_empresa or contratista.usuario.get_full_name(),
                    'especialidad': contratista.get_especialidad_display(),
                    'calificacion': float(contratista.calificacion_promedio),
                    'tarifa_dia': float(contratista.tarifa_por_dia),
                    'departamento': contratista.get_departamento_display(),
                    'telefono': contratista.telefono_principal
                })
        
        # Proveedores recomendados
        proveedores = []
        if 'Proveedor' in globals():
            for proveedor in Proveedor.objects.filter(activo=True)[:8]:
                proveedores.append({
                    'nombre': proveedor.nombre_empresa,
                    'tipo': proveedor.get_tipo_proveedor_display(),
                    'calificacion': float(proveedor.get_calificacion_promedio()),
                    'telefono': proveedor.telefono_principal,
                    'departamento': proveedor.get_departamento_display()
                })
        
        return {
            'stats': stats,
            'materiales': materiales,
            'maquinarias': maquinarias,
            'obras_usuario': obras_usuario,
            'contratistas': contratistas,
            'proveedores': proveedores,
            'user_info': {
                'is_authenticated': user.is_authenticated if user else False,
                'username': user.username if user and user.is_authenticated else None,
                'role': user.get_rol_display() if user and user.is_authenticated else None,
                'is_admin': user.es_administrador() if user and user.is_authenticated else False
            }
        }
        
    except Exception as e:
        print(f"Error obteniendo conocimiento de Luna: {e}")
        return {
            'stats': {'total_obras': 0, 'total_presupuestos': 0, 'total_materiales': 0},
            'materiales': {},
            'maquinarias': {},
            'obras_usuario': [],
            'contratistas': [],
            'proveedores': [],
            'user_info': {'is_authenticated': False}
        }

def generate_luna_response(question, knowledge, user=None):
    """Genera respuestas inteligentes basadas en el conocimiento del sistema"""
    q = question.lower()
    
    # Respuestas sobre precios y materiales
    if any(word in q for word in ['precio', 'costo', 'cuanto', 'material', 'vale']):
        if knowledge['materiales']:
            response = '💰 <strong>Precios Actualizados de Materiales (Guaraníes):</strong><br><br>'
            for nombre, data in list(knowledge['materiales'].items())[:10]:
                response += f"🔹 <strong>{nombre.title()}:</strong> ₲ {data['precio']:,.0f} por {data['unidad']}<br>"
                response += f"   📦 Stock disponible: {data['stock']}<br><br>"
            response += '<em>💡 Precios actualizados en tiempo real desde la base de datos</em>'
            return response
        else:
            return "No hay materiales registrados en el sistema actualmente."
    
    # Respuestas sobre contratistas
    if any(word in q for word in ['contratista', 'constructor', 'especialista', 'trabajador']):
        if knowledge['contratistas']:
            response = '👷 <strong>Contratistas Disponibles:</strong><br><br>'
            for contratista in knowledge['contratistas'][:8]:
                response += f"🔹 <strong>{contratista['nombre']}</strong><br>"
                response += f"   🛠️ {contratista['especialidad']} | ⭐ {contratista['calificacion']:.1f}/5<br>"
                response += f"   💰 ₱ {contratista['tarifa_dia']:,.0f}/día | 📍 {contratista['departamento']}<br>"
                response += f"   📞 {contratista['telefono']}<br><br>"
            return response
        else:
            return "No hay contratistas disponibles en este momento."
    
    # Respuestas sobre proveedores
    if any(word in q for word in ['proveedor', 'suministro', 'comprar', 'empresa']):
        if knowledge['proveedores']:
            response = '🚚 <strong>Proveedores Recomendados:</strong><br><br>'
            for proveedor in knowledge['proveedores'][:6]:
                response += f"🔹 <strong>{proveedor['nombre']}</strong><br>"
                response += f"   🏷️ {proveedor['tipo']} | ⭐ {proveedor['calificacion']:.1f}/5<br>"
                response += f"   📞 {proveedor['telefono']} | 📍 {proveedor['departamento']}<br><br>"
            return response
        else:
            return "No hay proveedores registrados actualmente."
    
    # Respuestas sobre obras (personalizadas si está logueado)
    if any(word in q for word in ['obra', 'proyecto', 'construccion', 'mis obras']):
        if user and user.is_authenticated and knowledge['obras_usuario']:
            response = f'🏗️ <strong>Tus Obras, {user.get_full_name() or user.username}:</strong><br><br>'
            for obra in knowledge['obras_usuario'][:5]:
                response += f"🔹 <strong>{obra['nombre']}</strong><br>"
                response += f"   📊 Estado: {obra['estado']} | 📈 Progreso: {obra['progreso']}%<br>"
                response += f"   💰 Presupuesto: ₱ {obra['presupuesto']:,.0f}<br>"
                response += f"   📍 Ubicación: {obra['ubicacion']}<br><br>"
            return response
        else:
            stats = knowledge['stats']
            return f"🏗️ <strong>Información General de Obras:</strong><br><br>El sistema tiene registradas <strong>{stats['total_obras']} obras</strong> en total.<br><br>Para ver información específica de tus obras, inicia sesión en L.u.N.a AI."
    
    # Respuestas sobre estadísticas
    if any(word in q for word in ['estadistica', 'numero', 'total', 'cuantos', 'datos']):
        stats = knowledge['stats']
        response = '📊 <strong>Estadísticas Completas del Sistema L.u.M.a:</strong><br><br>'
        response += f"🏗️ <strong>Obras:</strong> {stats['total_obras']}<br>"
        response += f"📋 <strong>Presupuestos:</strong> {stats['total_presupuestos']}<br>"
        response += f"📦 <strong>Materiales:</strong> {stats['total_materiales']}<br>"
        response += f"👷 <strong>Contratistas:</strong> {stats['total_contratistas']}<br>"
        response += f"👥 <strong>Empleados:</strong> {stats['total_empleados']}<br>"
        response += f"🚚 <strong>Proveedores:</strong> {stats['total_proveedores']}<br>"
        response += f"👤 <strong>Usuarios:</strong> {stats['total_usuarios']}<br><br>"
        response += '<em>📈 Datos actualizados en tiempo real</em>'
        return response
    
    # Respuestas sobre maquinarias
    if any(word in q for word in ['maquinaria', 'alquiler', 'equipo', 'herramienta']):
        if knowledge['maquinarias']:
            response = '🚜 <strong>Maquinarias Disponibles:</strong><br><br>'
            for nombre, data in list(knowledge['maquinarias'].items())[:8]:
                estado_icon = '✅' if data['disponible'] else '❌'
                response += f"🔹 <strong>{nombre.title()}:</strong> ₱ {data['costo']:,.0f}/día<br>"
                response += f"   {estado_icon} {data['estado']}<br><br>"
            return response
        else:
            return "No hay maquinarias registradas en el sistema."
    
    # Respuestas sobre presupuestos
    if any(word in q for word in ['presupuesto', 'cotizar', 'calcular', 'precio total']):
        return """📋 <strong>Gestión Inteligente de Presupuestos:</strong><br><br>
        Para crear un presupuesto profesional:<br><br>
        1️⃣ <strong>Selecciona la obra</strong> desde el menú OBRAS<br>
        2️⃣ <strong>Agrega materiales</strong> con precios actualizados automáticamente<br>
        3️⃣ <strong>Incluye contratistas</strong> según especialidad requerida<br>
        4️⃣ <strong>Calcula IVA</strong> (10%) automáticamente<br>
        5️⃣ <strong>Genera PDF</strong> profesional con logo<br><br>
        💡 <strong>Tip:</strong> Todos los precios se actualizan en tiempo real desde la base de datos."""
    
    # Respuestas sobre ayuda
    if any(word in q for word in ['ayuda', 'como', 'usar', 'tutorial', 'help']):
        user_name = user.get_full_name() or user.username if user and user.is_authenticated else "Usuario"
        return f"""❓ <strong>Ayuda Completa - L.u.N.a AI, {user_name}:</strong><br><br>
        🎯 <strong>Puedo ayudarte con información actualizada sobre:</strong><br><br>
        💰 Precios de materiales en tiempo real<br>
        👷 Contratistas disponibles por especialidad<br>
        🚚 Proveedores recomendados con calificaciones<br>
        🏗️ Estado de obras y proyectos<br>
        📋 Creación de presupuestos detallados<br>
        🚜 Disponibilidad de maquinarias<br>
        📊 Estadísticas completas del sistema<br>
        👥 Información de empleados y personal<br><br>
        <strong>¡Pregúntame cualquier cosa específica sobre el sistema L.u.M.a!</strong> 🤖✨"""
    
    # Respuestas sobre la IA
    if any(word in q for word in ['quien eres', 'que eres', 'luna', 'ia', 'inteligencia']):
        return """🤖 <strong>Soy L.u.N.a AI - Inteligencia Artificial Súper Avanzada</strong><br><br>
        Una IA de última generación especializada en:<br><br>
        🧠 <strong>Conocimiento completo</strong> del Sistema L.u.M.a<br>
        💾 <strong>Datos en tiempo real</strong> desde la base de datos<br>
        🇵🇾 <strong>Especializada en Paraguay</strong> y moneda Guaraníes<br>
        👤 <strong>Personalización por usuario</strong> con login<br>
        📊 <strong>Análisis inteligente</strong> de información<br>
        🔄 <strong>Respuestas contextuales</strong> avanzadas<br>
        🎯 <strong>Asistencia específica</strong> por rol de usuario<br><br>
        Creada para ser tu asistente personal inteligente en la gestión de obras civiles. ¡Estoy aquí para hacer tu trabajo más eficiente! ✨"""
    
    # Respuesta por defecto inteligente
    return f"""Entiendo tu consulta: "<em>{question}</em>" 🤔<br><br>
    <strong>Puedo ayudarte mejor con consultas específicas como:</strong><br><br>
    💰 "¿Cuáles son los precios actuales de materiales?"<br>
    👷 "¿Qué contratistas están disponibles?"<br>
    📊 "Muéstrame las estadísticas del sistema"<br>
    🏗️ "¿Cuáles son mis obras activas?"<br>
    🚚 "¿Qué proveedores recomiendan?"<br>
    📋 "¿Cómo crear un presupuesto detallado?"<br>
    🚜 "¿Qué maquinarias están disponibles?"<br><br>
    <strong>¡Hazme una pregunta específica sobre el sistema L.u.M.a!</strong> 🚀"""

@login_required
def luna_ai_dashboard(request):
    """Dashboard específico para L.u.N.a AI con datos personalizados"""
    knowledge = get_luna_knowledge(request.user)
    
    context = {
        'knowledge': knowledge,
        'user_stats': {
            'obras_count': len(knowledge['obras_usuario']),
            'materiales_count': len(knowledge['materiales']),
            'contratistas_count': len(knowledge['contratistas']),
            'proveedores_count': len(knowledge['proveedores'])
        }
    }
    
    return render(request, 'gestion/luna_ai/dashboard.html', context)

def luna_ai_knowledge_api(request):
    """API para obtener el conocimiento actualizado de L.u.N.a"""
    knowledge = get_luna_knowledge(request.user if request.user.is_authenticated else None)
    return JsonResponse(knowledge)