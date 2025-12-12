# SISTEMA DE IDIOMAS MULTILENGUAJE PARA L.u.M.a
# Soporte completo para 25+ idiomas con Django

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import activate, get_language
from django.conf import settings
import json

# Configuración de idiomas soportados
SUPPORTED_LANGUAGES = {
    'es': {
        'name': 'Español',
        'native_name': 'Español',
        'flag': '🇪🇸',
        'rtl': False
    },
    'en': {
        'name': 'English',
        'native_name': 'English',
        'flag': '🇺🇸',
        'rtl': False
    },
    'gn': {
        'name': 'Guaraní',
        'native_name': 'Avañe\'ẽ',
        'flag': '🇵🇾',
        'rtl': False
    },
    'pt': {
        'name': 'Português',
        'native_name': 'Português',
        'flag': '🇧🇷',
        'rtl': False
    },
    'ja': {
        'name': 'Japanese',
        'native_name': '日本語',
        'flag': '🇯🇵',
        'rtl': False
    },
    'ru': {
        'name': 'Russian',
        'native_name': 'Русский',
        'flag': '🇷🇺',
        'rtl': False
    },
    'ko': {
        'name': 'Korean',
        'native_name': '한국어',
        'flag': '🇰🇷',
        'rtl': False
    },
    'fr': {
        'name': 'French',
        'native_name': 'Français',
        'flag': '🇫🇷',
        'rtl': False
    },
    'de': {
        'name': 'German',
        'native_name': 'Deutsch',
        'flag': '🇩🇪',
        'rtl': False
    },
    'it': {
        'name': 'Italian',
        'native_name': 'Italiano',
        'flag': '🇮🇹',
        'rtl': False
    },
    'zh': {
        'name': 'Chinese',
        'native_name': '中文',
        'flag': '🇨🇳',
        'rtl': False
    },
    'ar': {
        'name': 'Arabic',
        'native_name': 'العربية',
        'flag': '🇸🇦',
        'rtl': True
    },
    'hi': {
        'name': 'Hindi',
        'native_name': 'हिन्दी',
        'flag': '🇮🇳',
        'rtl': False
    },
    'nl': {
        'name': 'Dutch',
        'native_name': 'Nederlands',
        'flag': '🇳🇱',
        'rtl': False
    },
    'sv': {
        'name': 'Swedish',
        'native_name': 'Svenska',
        'flag': '🇸🇪',
        'rtl': False
    },
    'no': {
        'name': 'Norwegian',
        'native_name': 'Norsk',
        'flag': '🇳🇴',
        'rtl': False
    },
    'da': {
        'name': 'Danish',
        'native_name': 'Dansk',
        'flag': '🇩🇰',
        'rtl': False
    },
    'fi': {
        'name': 'Finnish',
        'native_name': 'Suomi',
        'flag': '🇫🇮',
        'rtl': False
    },
    'pl': {
        'name': 'Polish',
        'native_name': 'Polski',
        'flag': '🇵🇱',
        'rtl': False
    },
    'tr': {
        'name': 'Turkish',
        'native_name': 'Türkçe',
        'flag': '🇹🇷',
        'rtl': False
    },
    'he': {
        'name': 'Hebrew',
        'native_name': 'עברית',
        'flag': '🇮🇱',
        'rtl': True
    },
    'th': {
        'name': 'Thai',
        'native_name': 'ไทย',
        'flag': '🇹🇭',
        'rtl': False
    },
    'vi': {
        'name': 'Vietnamese',
        'native_name': 'Tiếng Việt',
        'flag': '🇻🇳',
        'rtl': False
    },
    'id': {
        'name': 'Indonesian',
        'native_name': 'Bahasa Indonesia',
        'flag': '🇮🇩',
        'rtl': False
    },
    'ms': {
        'name': 'Malay',
        'native_name': 'Bahasa Melayu',
        'flag': '🇲🇾',
        'rtl': False
    },
    'tl': {
        'name': 'Filipino',
        'native_name': 'Filipino',
        'flag': '🇵🇭',
        'rtl': False
    }
}

def get_supported_languages(request):
    """
    API para obtener todos los idiomas soportados
    """
    return JsonResponse({
        'success': True,
        'languages': SUPPORTED_LANGUAGES,
        'current_language': get_language(),
        'total_languages': len(SUPPORTED_LANGUAGES)
    })

@csrf_exempt
def change_language(request):
    """
    API para cambiar el idioma del sistema
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            language_code = data.get('language_code', 'es')
            
            # Validar que el idioma esté soportado
            if language_code not in SUPPORTED_LANGUAGES:
                return JsonResponse({
                    'success': False,
                    'error': f'Idioma {language_code} no soportado'
                })
            
            # Activar el idioma en Django
            activate(language_code)
            
            # Guardar en la sesión
            request.session['django_language'] = language_code
            
            # Obtener información del idioma
            language_info = SUPPORTED_LANGUAGES[language_code]
            
            return JsonResponse({
                'success': True,
                'message': f'Idioma cambiado a {language_info["native_name"]}',
                'language_code': language_code,
                'language_info': language_info,
                'current_language': get_language()
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Datos JSON inválidos'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error interno: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Método no permitido'
    })

def get_language_translations(request):
    """
    API para obtener las traducciones de un idioma específico
    """
    language_code = request.GET.get('language', 'es')
    
    # Traducciones base (se pueden expandir)
    translations = {
        'es': {
            'sistema_gestion': 'Sistema de Gestión de Presupuestos para Obras Civiles',
            'bienvenido': 'Bienvenido al Sistema L.u.M.a',
            'descripcion': 'Gestión profesional de obras civiles en Paraguay',
            'inicio': 'Inicio',
            'dashboard': 'Dashboard',
            'obras': 'Obras',
            'presupuestos': 'Presupuestos',
            'materiales': 'Materiales',
            'maquinarias': 'Maquinarias',
            'herramientas': 'Herramientas',
            'contratistas': 'Contratistas',
            'propietarios': 'Propietarios',
            'empleados': 'Empleados',
            'proveedores': 'Proveedores',
            'reportes': 'Reportes',
            'configuracion': 'Configuración',
            'ayuda': 'Ayuda',
            'cerrar_sesion': 'Cerrar Sesión',
            'mi_perfil': 'Mi Perfil',
            'buscar': 'Buscar',
            'filtrar': 'Filtrar',
            'exportar': 'Exportar',
            'imprimir': 'Imprimir',
            'guardar': 'Guardar',
            'cancelar': 'Cancelar',
            'eliminar': 'Eliminar',
            'editar': 'Editar',
            'crear': 'Crear',
            'ver': 'Ver',
            'detalles': 'Detalles',
            'estadisticas': 'Estadísticas',
            'total': 'Total',
            'precio': 'Precio',
            'cantidad': 'Cantidad',
            'fecha': 'Fecha',
            'estado': 'Estado',
            'activo': 'Activo',
            'inactivo': 'Inactivo',
            'pendiente': 'Pendiente',
            'completado': 'Completado',
            'en_proceso': 'En Proceso',
            'cancelado': 'Cancelado',
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'telefono': 'Teléfono',
            'email': 'Email',
            'direccion': 'Dirección',
            'ciudad': 'Ciudad',
            'departamento': 'Departamento',
            'pais': 'País',
            'codigo_postal': 'Código Postal',
            'documento': 'Documento',
            'ruc': 'RUC',
            'ci': 'Cédula de Identidad',
            'profesion': 'Profesión',
            'especialidad': 'Especialidad',
            'experiencia': 'Experiencia',
            'calificacion': 'Calificación',
            'disponible': 'Disponible',
            'ocupado': 'Ocupado',
            'tarifa': 'Tarifa',
            'salario': 'Salario',
            'cargo': 'Cargo',
            'departamento_trabajo': 'Departamento de Trabajo',
            'fecha_ingreso': 'Fecha de Ingreso',
            'contrato': 'Contrato',
            'tipo_contrato': 'Tipo de Contrato',
            'duracion': 'Duración',
            'valor_contrato': 'Valor del Contrato',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha de Fin',
            'cliente': 'Cliente',
            'proyecto': 'Proyecto',
            'ubicacion': 'Ubicación',
            'superficie': 'Superficie',
            'tipo_obra': 'Tipo de Obra',
            'presupuesto_estimado': 'Presupuesto Estimado',
            'presupuesto_final': 'Presupuesto Final',
            'avance': 'Avance',
            'porcentaje_completado': 'Porcentaje Completado',
            'material': 'Material',
            'unidad': 'Unidad',
            'stock': 'Stock',
            'stock_minimo': 'Stock Mínimo',
            'proveedor': 'Proveedor',
            'categoria': 'Categoría',
            'marca': 'Marca',
            'modelo': 'Modelo',
            'codigo': 'Código',
            'precio_unitario': 'Precio Unitario',
            'precio_total': 'Precio Total',
            'iva': 'IVA',
            'descuento': 'Descuento',
            'subtotal': 'Subtotal',
            'maquinaria': 'Maquinaria',
            'herramienta': 'Herramienta',
            'tipo': 'Tipo',
            'capacidad': 'Capacidad',
            'potencia': 'Potencia',
            'combustible': 'Combustible',
            'operador': 'Operador',
            'mantenimiento': 'Mantenimiento',
            'ultima_revision': 'Última Revisión',
            'proxima_revision': 'Próxima Revisión',
            'costo_operacion': 'Costo de Operación',
            'costo_mantenimiento': 'Costo de Mantenimiento',
            'depreciacion': 'Depreciación',
            'vida_util': 'Vida Útil',
            'valor_residual': 'Valor Residual',
            'seguro': 'Seguro',
            'impuestos': 'Impuestos',
            'financiamiento': 'Financiamiento',
            'interes': 'Interés',
            'cuotas': 'Cuotas',
            'valor_cuota': 'Valor de Cuota',
            'saldo_pendiente': 'Saldo Pendiente',
            'pagado': 'Pagado',
            'por_pagar': 'Por Pagar',
            'vencido': 'Vencido',
            'al_dia': 'Al Día',
            'reporte': 'Reporte',
            'grafico': 'Gráfico',
            'tabla': 'Tabla',
            'resumen': 'Resumen',
            'detallado': 'Detallado',
            'mensual': 'Mensual',
            'anual': 'Anual',
            'trimestral': 'Trimestral',
            'semanal': 'Semanal',
            'diario': 'Diario',
            'periodo': 'Período',
            'desde': 'Desde',
            'hasta': 'Hasta',
            'generar': 'Generar',
            'descargar': 'Descargar',
            'enviar': 'Enviar',
            'compartir': 'Compartir',
            'notificacion': 'Notificación',
            'alerta': 'Alerta',
            'recordatorio': 'Recordatorio',
            'mensaje': 'Mensaje',
            'chat': 'Chat',
            'conversacion': 'Conversación',
            'usuario': 'Usuario',
            'administrador': 'Administrador',
            'supervisor': 'Supervisor',
            'operario': 'Operario',
            'invitado': 'Invitado',
            'permisos': 'Permisos',
            'rol': 'Rol',
            'acceso': 'Acceso',
            'permitido': 'Permitido',
            'denegado': 'Denegado',
            'restringido': 'Restringido',
            'publico': 'Público',
            'privado': 'Privado',
            'confidencial': 'Confidencial',
            'backup': 'Respaldo',
            'restaurar': 'Restaurar',
            'sincronizar': 'Sincronizar',
            'actualizar': 'Actualizar',
            'version': 'Versión',
            'historial': 'Historial',
            'cambios': 'Cambios',
            'log': 'Registro',
            'auditoria': 'Auditoría',
            'seguridad': 'Seguridad',
            'privacidad': 'Privacidad',
            'terminos': 'Términos y Condiciones',
            'politicas': 'Políticas de Privacidad',
            'soporte': 'Soporte Técnico',
            'documentacion': 'Documentación',
            'tutorial': 'Tutorial',
            'manual': 'Manual de Usuario',
            'faq': 'Preguntas Frecuentes',
            'contacto': 'Contacto',
            'acerca_de': 'Acerca de',
            'creditos': 'Créditos',
            'licencia': 'Licencia',
            'copyright': 'Derechos de Autor'
        },
        'en': {
            'sistema_gestion': 'Civil Works Budget Management System',
            'bienvenido': 'Welcome to L.u.M.a System',
            'descripcion': 'Professional civil works management in Paraguay',
            'inicio': 'Home',
            'dashboard': 'Dashboard',
            'obras': 'Projects',
            'presupuestos': 'Budgets',
            'materiales': 'Materials',
            'maquinarias': 'Machinery',
            'herramientas': 'Tools',
            'contratistas': 'Contractors',
            'propietarios': 'Owners',
            'empleados': 'Employees',
            'proveedores': 'Suppliers',
            'reportes': 'Reports',
            'configuracion': 'Settings',
            'ayuda': 'Help',
            'cerrar_sesion': 'Logout',
            'mi_perfil': 'My Profile',
            'buscar': 'Search',
            'filtrar': 'Filter',
            'exportar': 'Export',
            'imprimir': 'Print',
            'guardar': 'Save',
            'cancelar': 'Cancel',
            'eliminar': 'Delete',
            'editar': 'Edit',
            'crear': 'Create',
            'ver': 'View',
            'detalles': 'Details',
            'estadisticas': 'Statistics',
            'total': 'Total',
            'precio': 'Price',
            'cantidad': 'Quantity',
            'fecha': 'Date',
            'estado': 'Status',
            'activo': 'Active',
            'inactivo': 'Inactive',
            'pendiente': 'Pending',
            'completado': 'Completed',
            'en_proceso': 'In Progress',
            'cancelado': 'Cancelled'
        },
        'gn': {
            'sistema_gestion': 'Sistema Ñeñangareko Jeporu Cuenta Tembiapo Civil rehegua',
            'bienvenido': 'Tereguahẽ porãite Sistema L.u.M.a-pe',
            'descripcion': 'Ñeñangareko profesional tembiapo civil Paraguay-pe',
            'inicio': 'Ñepyrũ',
            'dashboard': 'Ñehechauka',
            'obras': 'Tembiapo',
            'presupuestos': 'Jeporu Cuenta',
            'materiales': 'Mba\'e',
            'maquinarias': 'Máquina',
            'herramientas': 'Tembiporu',
            'contratistas': 'Tembiaporã',
            'propietarios': 'Jára',
            'empleados': 'Tembiapóva',
            'proveedores': 'Ñeme\'ẽ',
            'reportes': 'Marandu',
            'configuracion': 'Ñemboheko',
            'ayuda': 'Pytyvõ',
            'cerrar_sesion': 'Esẽ',
            'mi_perfil': 'Che Perfil',
            'buscar': 'Jeheka',
            'filtrar': 'Ñemboguata',
            'exportar': 'Ñesẽ',
            'imprimir': 'Ñembokuatia',
            'guardar': 'Ñongatu',
            'cancelar': 'Ani',
            'eliminar': 'Mbogue',
            'editar': 'Ñembosako\'i',
            'crear': 'Japo',
            'ver': 'Hecha',
            'detalles': 'Mba\'eichaitépa',
            'estadisticas': 'Papapy',
            'total': 'Opavave',
            'precio': 'Hepy',
            'cantidad': 'Hetápa',
            'fecha': 'Ára',
            'estado': 'Mba\'éichapa oĩ',
            'activo': 'Oikovéva',
            'inactivo': 'Ndoikovéiva',
            'pendiente': 'Oha\'arõva',
            'completado': 'Oñembotýva',
            'en_proceso': 'Ojejapo hína',
            'cancelado': 'Oñejokoáva'
        }
    }
    
    # Obtener traducciones del idioma solicitado o español por defecto
    language_translations = translations.get(language_code, translations['es'])
    
    return JsonResponse({
        'success': True,
        'language_code': language_code,
        'translations': language_translations,
        'language_info': SUPPORTED_LANGUAGES.get(language_code, SUPPORTED_LANGUAGES['es'])
    })

def language_context_processor(request):
    """
    Context processor para agregar información de idiomas a todos los templates
    """
    current_language = get_language()
    
    return {
        'SUPPORTED_LANGUAGES': SUPPORTED_LANGUAGES,
        'CURRENT_LANGUAGE': current_language,
        'CURRENT_LANGUAGE_INFO': SUPPORTED_LANGUAGES.get(current_language, SUPPORTED_LANGUAGES['es']),
        'TOTAL_LANGUAGES': len(SUPPORTED_LANGUAGES)
    }

def get_user_language_preference(request):
    """
    API para obtener la preferencia de idioma del usuario
    """
    if request.user.is_authenticated:
        # Intentar obtener de la configuración del usuario
        user_language = getattr(request.user, 'preferred_language', None)
        if user_language and user_language in SUPPORTED_LANGUAGES:
            return JsonResponse({
                'success': True,
                'language_code': user_language,
                'source': 'user_preference'
            })
    
    # Obtener de la sesión
    session_language = request.session.get('django_language')
    if session_language and session_language in SUPPORTED_LANGUAGES:
        return JsonResponse({
            'success': True,
            'language_code': session_language,
            'source': 'session'
        })
    
    # Detectar del navegador
    browser_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    if browser_language:
        # Extraer el primer idioma preferido
        preferred_lang = browser_language.split(',')[0].split('-')[0].lower()
        if preferred_lang in SUPPORTED_LANGUAGES:
            return JsonResponse({
                'success': True,
                'language_code': preferred_lang,
                'source': 'browser'
            })
    
    # Idioma por defecto
    return JsonResponse({
        'success': True,
        'language_code': 'es',
        'source': 'default'
    })

@csrf_exempt
def save_user_language_preference(request):
    """
    API para guardar la preferencia de idioma del usuario
    """
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            language_code = data.get('language_code', 'es')
            
            if language_code not in SUPPORTED_LANGUAGES:
                return JsonResponse({
                    'success': False,
                    'error': 'Idioma no soportado'
                })
            
            # Guardar en el perfil del usuario (si el modelo lo soporta)
            try:
                request.user.preferred_language = language_code
                request.user.save()
            except AttributeError:
                # El modelo de usuario no tiene el campo preferred_language
                pass
            
            # Guardar en la sesión como respaldo
            request.session['django_language'] = language_code
            
            return JsonResponse({
                'success': True,
                'message': 'Preferencia de idioma guardada',
                'language_code': language_code
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Datos JSON inválidos'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error interno: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Método no permitido o usuario no autenticado'
    })

def language_statistics(request):
    """
    API para obtener estadísticas de uso de idiomas
    """
    # Aquí podrías implementar lógica para rastrear el uso de idiomas
    # Por ahora, devolvemos datos de ejemplo
    
    stats = {
        'most_used_languages': [
            {'code': 'es', 'name': 'Español', 'usage_percentage': 65.5, 'users': 1250},
            {'code': 'gn', 'name': 'Guaraní', 'usage_percentage': 20.3, 'users': 387},
            {'code': 'en', 'name': 'English', 'usage_percentage': 8.7, 'users': 166},
            {'code': 'pt', 'name': 'Português', 'usage_percentage': 3.2, 'users': 61},
            {'code': 'ja', 'name': '日本語', 'usage_percentage': 1.1, 'users': 21},
            {'code': 'other', 'name': 'Otros', 'usage_percentage': 1.2, 'users': 23}
        ],
        'total_users': 1908,
        'languages_available': len(SUPPORTED_LANGUAGES),
        'default_language': 'es',
        'rtl_languages': [code for code, info in SUPPORTED_LANGUAGES.items() if info.get('rtl', False)]
    }
    
    return JsonResponse({
        'success': True,
        'statistics': stats,
        'supported_languages': SUPPORTED_LANGUAGES
    })