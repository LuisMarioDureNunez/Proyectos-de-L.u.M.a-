"""
URL configuration for mi_tienda project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # API (comentado hasta instalar rest_framework)
    # path('api/v1/', include('gestion.api.urls')),
    
    # WebSocket para notificaciones (comentado hasta instalar channels)
    # path('ws/', include('gestion.routing')),
    
    path('admin/', admin.site.urls),
    path('', include('gestion.urls')),  # Incluir URLs de la app gestión
    path('accounts/', include('django.contrib.auth.urls')),  # URLs de autenticación
    
    # PWA URLs deshabilitadas hasta instalar django-pwa
    # path('', include('pwa.urls')),  # Manifest, Service Worker, etc.
]

# Servir archivos multimedia en desarrollo
if settings.DEBUG:
 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)