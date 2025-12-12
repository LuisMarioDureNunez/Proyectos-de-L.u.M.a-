"""
Configuración PWA para Mi Tienda Premium
Configuraciones y utilidades para Progressive Web App
"""

# Configuración del manifest
PWA_MANIFEST = {
    "name": "Mi Tienda Premium - Sistema de Gestión",
    "short_name": "Mi Tienda",
    "description": "Sistema completo de gestión empresarial para construcción y comercio",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#667eea",
    "theme_color": "#667eea",
    "orientation": "portrait-primary",
    "scope": "/",
    "lang": "es",
    "categories": ["business", "productivity", "utilities"],
    "icons": [
        {
            "src": "/static/icons/icon-72x72.png",
            "sizes": "72x72",
            "type": "image/png",
            "purpose": "maskable any"
        },
        {
            "src": "/static/icons/icon-96x96.png",
            "sizes": "96x96",
            "type": "image/png",
            "purpose": "maskable any"
        },
        {
            "src": "/static/icons/icon-128x128.png",
            "sizes": "128x128",
            "type": "image/png",
            "purpose": "maskable any"
        },
        {
            "src": "/static/icons/icon-144x144.png",
            "sizes": "144x144",
            "type": "image/png",
            "purpose": "maskable any"
        },
        {
            "src": "/static/icons/icon-152x152.png",
            "sizes": "152x152",
            "type": "image/png",
            "purpose": "maskable any"
        },
        {
            "src": "/static/icons/icon-192x192.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "maskable any"
        },
        {
            "src": "/static/icons/icon-384x384.png",
            "sizes": "384x384",
            "type": "image/png",
            "purpose": "maskable any"
        },
        {
            "src": "/static/icons/icon-512x512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "maskable any"
        }
    ],
    "shortcuts": [
        {
            "name": "Dashboard",
            "short_name": "Dashboard",
            "description": "Ir al dashboard principal",
            "url": "/dashboard/",
            "icons": [{"src": "/static/icons/icon-96x96.png", "sizes": "96x96"}]
        },
        {
            "name": "Obras",
            "short_name": "Obras",
            "description": "Gestionar obras",
            "url": "/obras/",
            "icons": [{"src": "/static/icons/icon-96x96.png", "sizes": "96x96"}]
        },
        {
            "name": "Presupuestos",
            "short_name": "Presupuestos",
            "description": "Ver presupuestos",
            "url": "/presupuestos/",
            "icons": [{"src": "/static/icons/icon-96x96.png", "sizes": "96x96"}]
        }
    ]
}

# Configuración del Service Worker
PWA_SERVICE_WORKER_CONFIG = {
    "cache_name": "mi-tienda-v1.0.0",
    "offline_page": "/offline/",
    "cache_strategies": {
        "static_files": "cache_first",
        "api_calls": "network_first",
        "pages": "stale_while_revalidate"
    },
    "cache_urls": [
        "/",
        "/dashboard/",
        "/obras/",
        "/presupuestos/",
        "/offline/",
        "/static/css/",
        "/static/js/",
        "/static/icons/",
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
    ]
}

# Configuración de notificaciones push
PWA_NOTIFICATIONS_CONFIG = {
    "vapid_public_key": "YOUR_VAPID_PUBLIC_KEY_HERE",
    "vapid_private_key": "YOUR_VAPID_PRIVATE_KEY_HERE",
    "notification_icon": "/static/icons/icon-192x192.png",
    "notification_badge": "/static/icons/icon-72x72.png"
}

# Utilidades PWA
class PWAUtils:
    
    @staticmethod
    def is_pwa_request(request):
        """Detectar si la request viene de una PWA instalada"""
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        return 'wv' in user_agent or request.META.get('HTTP_X_REQUESTED_WITH') == 'com.mitienda.app'
    
    @staticmethod
    def get_install_prompt_data():
        """Obtener datos para el prompt de instalación"""
        return {
            "title": "Instalar Mi Tienda Premium",
            "message": "Instala nuestra app para una mejor experiencia",
            "install_button": "Instalar",
            "cancel_button": "Ahora no"
        }
    
    @staticmethod
    def generate_notification_payload(title, body, icon=None, badge=None, data=None):
        """Generar payload para notificaciones push"""
        return {
            "title": title,
            "body": body,
            "icon": icon or PWA_NOTIFICATIONS_CONFIG["notification_icon"],
            "badge": badge or PWA_NOTIFICATIONS_CONFIG["notification_badge"],
            "data": data or {},
            "requireInteraction": True,
            "actions": [
                {
                    "action": "open",
                    "title": "Abrir",
                    "icon": "/static/icons/icon-96x96.png"
                },
                {
                    "action": "close",
                    "title": "Cerrar"
                }
            ]
        }

# Middleware PWA
class PWAMiddleware:
    """Middleware para funcionalidades PWA"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Agregar headers PWA
        response = self.get_response(request)
        
        # Headers de seguridad para PWA
        if PWAUtils.is_pwa_request(request):
            response['X-Frame-Options'] = 'SAMEORIGIN'
            response['X-Content-Type-Options'] = 'nosniff'
            response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response

# Configuración de caché offline
PWA_OFFLINE_CONFIG = {
    "fallback_pages": {
        "/dashboard/": "/offline/",
        "/obras/": "/offline/",
        "/presupuestos/": "/offline/"
    },
    "cache_duration": 86400,  # 24 horas
    "max_cache_size": 50 * 1024 * 1024,  # 50MB
    "cleanup_interval": 3600  # 1 hora
}