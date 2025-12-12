# production_settings.py - Configuración específica para producción
import os
from .settings import *

# =============================================
# ⭐ CONFIGURACIÓN DE PRODUCCIÓN
# =============================================

# Seguridad
DEBUG = False
ALLOWED_HOSTS = [
    'tu-dominio.com',
    'www.tu-dominio.com',
    'mitienda.herokuapp.com',
    'mitienda.railway.app',
    'mitienda.vercel.app',
]

# Base de datos para producción (PostgreSQL recomendado)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'mi_tienda_prod'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Configuración de archivos estáticos para producción
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Configuración de archivos multimedia (usar AWS S3 en producción real)
if os.environ.get('USE_S3') == 'True':
    # Configuración AWS S3
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    
    # Configuración de archivos estáticos y multimedia
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# Configuración de email para producción
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = f'Mi Tienda Premium <{EMAIL_HOST_USER}>'

# Configuración de seguridad HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Configuración de cache para producción (Redis recomendado)
if os.environ.get('REDIS_URL'):
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': os.environ.get('REDIS_URL'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }

# Configuración de logging para producción
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/django.log',
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'mail_admins'],
            'level': 'WARNING',
            'propagate': True,
        },
        'gestion': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Variables de entorno requeridas
REQUIRED_ENV_VARS = [
    'SECRET_KEY',
    'DB_PASSWORD',
    'EMAIL_HOST_USER',
    'EMAIL_HOST_PASSWORD',
]

# Verificar variables de entorno
missing_vars = [var for var in REQUIRED_ENV_VARS if not os.environ.get(var)]
if missing_vars:
    raise Exception(f"Variables de entorno faltantes: {', '.join(missing_vars)}")

# Configuración específica para diferentes plataformas de despliegue
if 'DYNO' in os.environ:
    # Configuración para Heroku
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(conn_max_age=600)
    
elif 'RAILWAY_ENVIRONMENT' in os.environ:
    # Configuración para Railway
    ALLOWED_HOSTS.append(f"{os.environ.get('RAILWAY_STATIC_URL', '')}")
    
elif 'VERCEL' in os.environ:
    # Configuración para Vercel
    ALLOWED_HOSTS.append('.vercel.app')

print("🚀 Configuración de producción cargada correctamente")