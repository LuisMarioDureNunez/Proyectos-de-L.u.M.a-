# gestion/urls.py - VERSIÓN COMPLETA Y MEJORADA
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from django.conf import settings
import os
from . import views
from .views import RegistroUsuario
from .views_auth import LoginMejoradoView, RegistroMejoradoView, logout_mejorado, cambiar_password, verificar_estado_usuario, test_login
from .views_login_simple import login_ultra_simple, test_debug
from gestion import views
from gestion import views_super_avanzadas
from gestion import views_luna_ai
from gestion import views_repositorios
from gestion.views_produccion import dashboard_tiempo_real, api_datos_tiempo_real, reporte_produccion_completo, panel_obras_tiempo_real, panel_empleados_tiempo_real, panel_contratistas_tiempo_real

urlpatterns = [
    # ==================== URLs PÚBLICAS ====================
    path('', views.bienvenida, name='bienvenida'),
    path('home/', views.home, name='home'),
    
    # ==================== AUTENTICACIÓN SIMPLE PARA DEBUG ====================
    path('accounts/login/', login_ultra_simple, name='login'),
    # path('accounts/login/', LoginMejoradoView.as_view(), name='login'),  # Deshabilitado temporalmente
    path('accounts/logout/', logout_mejorado, name='logout'),
    path('registro/', RegistroMejoradoView.as_view(), name='registro'),
    path('cambiar-password/', cambiar_password, name='cambiar_password'),
    path('verificar-usuario/', verificar_estado_usuario, name='verificar_usuario'),
    path('test-login/', test_login, name='test_login'),  # Para pruebas
    path('debug/', test_debug, name='debug'),  # Debug info
    path('emergency-login/', auth_views.LoginView.as_view(template_name='registration/login_emergencia.html'), name='emergency_login'),  # Login de emergencia
    
    # ==================== DASHBOARD ====================
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/super/', views.dashboard_super, name='dashboard_super'),
    path('dashboard/increible/', views.dashboard_increible, name='dashboard_increible'),
    path('dashboard/paraguay/', views.dashboard_paraguay, name='dashboard_paraguay'),
    
    # ==================== GESTIÓN DE MATERIALES ====================
    path('materiales/', views.lista_materiales, name='lista_materiales'),
    path('materiales/nuevo/', views.nuevo_material, name='nuevo_material'),
    path('materiales/editar/<int:id>/', views.editar_material, name='editar_material'),
    path('materiales/eliminar/<int:id>/', views.eliminar_material, name='eliminar_material'),
    
    # ==================== GESTIÓN DE MAQUINARIAS ====================
    path('maquinarias/', views.lista_maquinarias, name='lista_maquinarias'),
    path('maquinarias/nueva/', views.nueva_maquinaria, name='nueva_maquinaria'),
    path('maquinarias/editar/<int:id>/', views.editar_maquinaria, name='editar_maquinaria'),
    path('maquinarias/eliminar/<int:id>/', views.eliminar_maquinaria, name='eliminar_maquinaria'),
    
    # ==================== GESTIÓN DE HERRAMIENTAS ====================
    path('herramientas/', views.lista_herramientas, name='lista_herramientas'),
    path('herramientas/nueva/', views.nueva_herramienta, name='nueva_herramienta'),
    path('herramientas/editar/<int:id>/', views.editar_herramienta, name='editar_herramienta'),
    path('herramientas/eliminar/<int:id>/', views.eliminar_herramienta, name='eliminar_herramienta'),
    
    # ==================== GESTIÓN DE OBRAS ====================
    path('obras/', views.lista_obras, name='lista_obras'),
    path('obras/nueva/', views.nueva_obra, name='nueva_obra'),
    path('obras/editar/<int:id>/', views.editar_obra, name='editar_obra'),
    path('obras/eliminar/<int:id>/', views.eliminar_obra, name='eliminar_obra'),
    path('obras/finalizadas/', views.obras_finalizadas, name='obras_finalizadas'),
    path('obras/<int:id>/', views.detalle_obra, name='detalle_obra'),
    
    # ==================== GESTIÓN DE PRESUPUESTOS ====================
    path('presupuestos/', views.lista_presupuestos, name='lista_presupuestos'),
    path('presupuestos/solicitar/', views.solicitar_presupuesto, name='solicitar_presupuesto'),
    path('presupuestos/nuevo/', views.nuevo_presupuesto, name='nuevo_presupuesto'),
    path('presupuestos/editar/<int:id>/', views.editar_presupuesto, name='editar_presupuesto'),
    path('presupuestos/<int:id>/', views.detalle_presupuesto, name='detalle_presupuesto'),
    path('presupuestos/aceptar/<int:id>/', views.aceptar_presupuesto, name='aceptar_presupuesto'),
    path('presupuestos/rechazar/<int:id>/', views.rechazar_presupuesto, name='rechazar_presupuesto'),
    path('presupuestos/replantear/<int:id>/', views.replantear_presupuesto, name='replantear_presupuesto'),
    path('presupuestos/imprimir/<int:id>/', views.imprimir_presupuesto, name='imprimir_presupuesto'),
    
    # ==================== GESTIÓN DE PERFIL ====================
    path('perfil/', views.gestionar_perfil, name='gestionar_perfil'),
    
    # ==================== ADMINISTRACIÓN DE USUARIOS ====================
    path('gestion/usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('admin/usuarios/editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    
    # ==================== UTILITARIOS Y AJAX ====================
    path('buscar/', views.buscar_ajax, name='buscar_ajax'),
    path('reportes/', views.reportes_avanzados, name='reportes_avanzados'),
    
    # ==================== PRESUPUESTOS AVANZADOS ====================
    path('presupuestos/crear-avanzado/', views.crear_presupuesto_avanzado, name='crear_presupuesto_avanzado'),
    path('presupuestos/calcular-ajax/', views.calcular_presupuesto_ajax, name='calcular_presupuesto_ajax'),
    path('presupuestos/duplicar/<int:presupuesto_id>/', views.duplicar_presupuesto, name='duplicar_presupuesto'),
    path('presupuestos/material/<int:material_id>/', views.obtener_datos_material_ajax, name='obtener_datos_material'),
    path('presupuestos/reporte-pdf/<int:presupuesto_id>/', views.reporte_presupuesto_pdf, name='reporte_presupuesto_pdf'),
    
    # ==================== REPORTES AVANZADOS ====================
    path('reportes/estadisticas/', views.reportes_estadisticas_avanzadas, name='reportes_estadisticas_avanzadas'),
    path('reportes/exportar-excel/', views.exportar_estadisticas_excel, name='exportar_estadisticas_excel'),
    path('reportes/exportar/', views.exportar_reporte_completo, name='exportar_reporte_completo'),
    path('presupuestos/<int:presupuesto_id>/pdf/', views.generar_reporte_presupuesto_pdf, name='generar_reporte_presupuesto_pdf'),
    path('presupuestos/<int:presupuesto_id>/pdf-completo/', views.generar_reporte_completo_pdf, name='generar_reporte_completo_pdf'),
    
    # ==================== FUNCIONALIDADES SUPER AVANZADAS PARA PARAGUAY ====================
    
    # GESTIÓN DE CONTRATISTAS
    path('contratistas/', views_super_avanzadas.lista_contratistas, name='lista_contratistas'),
    path('contratistas/nuevo/', views_super_avanzadas.nuevo_contratista, name='nuevo_contratista'),
    path('contratistas/editar/<int:id>/', views_super_avanzadas.editar_contratista, name='editar_contratista'),
    path('contratistas/<int:id>/', views_super_avanzadas.detalle_contratista, name='detalle_contratista'),
    
    # GESTIÓN DE PROPIETARIOS
    path('propietarios/', views_super_avanzadas.lista_propietarios, name='lista_propietarios'),
    path('propietarios/nuevo/', views_super_avanzadas.nuevo_propietario, name='nuevo_propietario'),
    path('propietarios/<int:id>/', views_super_avanzadas.detalle_propietario, name='detalle_propietario'),
    
    # GESTIÓN DE PROPIEDADES
    path('propiedades/', views_super_avanzadas.lista_propiedades, name='lista_propiedades'),
    path('propiedades/nueva/', views_super_avanzadas.nueva_propiedad, name='nueva_propiedad'),
    
    # GESTIÓN DE EMPLEADOS
    path('empleados/', views_super_avanzadas.lista_empleados, name='lista_empleados'),
    path('empleados/nuevo/', views_super_avanzadas.nuevo_empleado, name='nuevo_empleado'),
    path('empleados/<int:id>/', views_super_avanzadas.detalle_empleado, name='detalle_empleado'),
    
    # GESTIÓN DE PROVEEDORES
    path('proveedores/', views_super_avanzadas.lista_proveedores, name='lista_proveedores'),
    path('proveedores/nuevo/', views_super_avanzadas.nuevo_proveedor, name='nuevo_proveedor'),
    path('proveedores/<int:id>/', views_super_avanzadas.detalle_proveedor, name='detalle_proveedor'),
    
    # GESTIÓN DE CONTRATOS
    path('contratos/', views_super_avanzadas.lista_contratos, name='lista_contratos'),
    path('contratos/nuevo/', views_super_avanzadas.nuevo_contrato, name='nuevo_contrato'),
    
    # DASHBOARD SUPER COMPLETO
    path('dashboard/super-completo/', views_super_avanzadas.dashboard_super_completo, name='dashboard_super_completo'),
    
    # AJAX AVANZADO
    path('ajax/contratistas/', views_super_avanzadas.buscar_contratistas_ajax, name='buscar_contratistas_ajax'),
    path('ajax/proveedores/', views_super_avanzadas.buscar_proveedores_ajax, name='buscar_proveedores_ajax'),
    path('ajax/estadisticas/', views_super_avanzadas.estadisticas_dashboard_ajax, name='estadisticas_dashboard_ajax'),
    
    # L.u.N.a AI SUPER AVANZADA
    path('luna-ai/chat/', views_luna_ai.luna_ai_chat, name='luna_ai_chat'),
    path('luna-ai/login/', views_luna_ai.luna_ai_login, name='luna_ai_login'),
    path('luna-ai/knowledge/', views_luna_ai.luna_ai_knowledge_api, name='luna_ai_knowledge'),
    path('luna-ai/dashboard/', views_luna_ai.luna_ai_dashboard, name='luna_ai_dashboard'),
    
    # CHAT LUMA FLOTANTE
    path('chat/widget/', views.chat_widget, name='chat_widget'),
    
    # PWA OFFLINE PAGE
    path('offline/', views.offline, name='offline'),
    
    # ==================== PRODUCCIÓN DE OBRAS ====================
    path('produccion/', views.dashboard_produccion, name='dashboard_produccion'),
    path('produccion/tiempo-real/', dashboard_tiempo_real, name='dashboard_tiempo_real'),
    path('produccion/panel-obras/', panel_obras_tiempo_real, name='panel_obras_tiempo_real'),
    path('produccion/panel-empleados/', panel_empleados_tiempo_real, name='panel_empleados_tiempo_real'),
    path('produccion/panel-contratistas/', panel_contratistas_tiempo_real, name='panel_contratistas_tiempo_real'),
    path('produccion/datos-tiempo-real/', views.datos_tiempo_real, name='datos_tiempo_real'),
    path('produccion/api/tiempo-real/', api_datos_tiempo_real, name='api_datos_tiempo_real'),
    path('produccion/reporte-completo/', reporte_produccion_completo, name='reporte_produccion_completo'),
    path('obras/<int:obra_id>/produccion/', views.detalle_produccion_obra, name='detalle_produccion_obra'),
    path('obras/<int:obra_id>/registrar-produccion/', views.registrar_produccion, name='registrar_produccion'),
    path('obras/<int:obra_id>/reporte-produccion/', views.reporte_produccion_pdf, name='reporte_produccion_pdf'),
    path('costos-empleados/', views.costos_empleados_api, name='costos_empleados_api'),
    
    # ==================== PERFIL DE USUARIO ====================
    path('usuarios/perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('usuarios/actualizar-avatar/', views.actualizar_avatar, name='actualizar_avatar'),
    path('usuarios/actualizar-logo/', views.actualizar_logo, name='actualizar_logo'),
    path('usuarios/actualizar-perfil/', views.actualizar_perfil, name='actualizar_perfil'),
    path('usuarios/estadisticas/', views.estadisticas_usuario, name='estadisticas_usuario'),
    path('usuarios/configuracion-notificaciones/', views.configuracion_notificaciones, name='configuracion_notificaciones'),
    
    # SISTEMA DE IDIOMAS MULTILENGUAJE
    path('idiomas/', include('gestion.urls_idiomas')),
    
    # ==================== REPOSITORIOS GITHUB ====================
    path('repositorios/', views_repositorios.lista_repositorios, name='lista_repositorios'),
    path('repositorios/crear/', views_repositorios.crear_repositorio, name='crear_repositorio'),
    path('repositorios/<int:id>/', views_repositorios.detalle_repositorio, name='detalle_repositorio'),
    path('repositorios/<int:id>/editar/', views_repositorios.editar_repositorio, name='editar_repositorio'),
    path('repositorios/<int:id>/eliminar/', views_repositorios.eliminar_repositorio, name='eliminar_repositorio'),
    path('repositorios/<int:id>/sincronizar/', views_repositorios.sincronizar_repositorio, name='sincronizar_repositorio'),
    path('repositorios/<int:repositorio_id>/comentar/', views_repositorios.agregar_comentario, name='agregar_comentario'),
    path('repositorios/dashboard/', views_repositorios.dashboard_repositorios, name='dashboard_repositorios'),
    path('repositorios/sincronizar-todos/', views_repositorios.sincronizar_todos_repositorios, name='sincronizar_todos_repositorios'),
    path('repositorios/importar-github/', views_repositorios.importar_desde_github, name='importar_desde_github'),
    path('repositorios/tags/', views_repositorios.gestionar_tags, name='gestionar_tags'),
    
    # AJAX para repositorios
    path('ajax/repositorios/buscar/', views_repositorios.buscar_repositorios_ajax, name='buscar_repositorios_ajax'),
    path('ajax/repositorios/<int:id>/estadisticas/', views_repositorios.estadisticas_repositorio_ajax, name='estadisticas_repositorio_ajax'),
    
    # ==================== MEJORAS INCREÍBLES ====================
    path('mejoras/', include('gestion.urls_mejoras')),
    
    # PWA SERVICE WORKER Y MANIFEST
    path('sw.js', views.service_worker, name='service_worker'),
    path('manifest.json', views.manifest_json, name='manifest'),
    path('instalar/', views.pwa_install, name='pwa_install'),
]

# URLs para desarrollo (solo en DEBUG)
from django.conf import settings
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)