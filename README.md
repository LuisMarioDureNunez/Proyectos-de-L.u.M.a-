# 🏪 Mi Tienda Premium - Sistema de Gestión Empresarial

Sistema completo de gestión empresarial desarrollado con Django, especializado en construcción y comercio con funcionalidades avanzadas.

## 🚀 Características Principales

### ✨ Funcionalidades Core
- **Sistema de Autenticación Avanzado**: Roles personalizados (Admin, Vendedor, Cliente)
- **Gestión de Productos**: CRUD completo con imágenes, categorías y stock
- **Sistema de Pedidos**: Carrito de compras, checkout y seguimiento
- **Dashboard Interactivo**: Estadísticas en tiempo real y gráficos
- **Reportes Avanzados**: Exportación PDF/Excel con gráficos
- **Sistema de Notificaciones**: Email automático y notificaciones push

### 🛡️ Seguridad y Middleware
- **Middleware de Permisos**: Control granular de acceso por roles
- **Auditoría Completa**: Logging de todas las acciones importantes
- **Seguridad Avanzada**: Protección XSS, CSRF, rate limiting
- **Autenticación Robusta**: Sesiones seguras y validación de usuarios

### 🌐 Características Empresariales
- **Multi-idioma**: Soporte para español e inglés
- **Formato Paraguayo**: Moneda guaraníes, formato de números
- **Sistema de Construcción**: Gestión de obras, presupuestos, materiales
- **API REST**: Endpoints para integración con otras aplicaciones
- **PWA Ready**: Configuración para aplicación web progresiva

## 📋 Requisitos del Sistema

### Requisitos Mínimos
- Python 3.8+
- Django 4.2+
- SQLite (desarrollo) / PostgreSQL (producción)
- 2GB RAM mínimo
- 1GB espacio en disco

### Dependencias Principales
```
Django==4.2.7
Pillow==10.0.1
reportlab==4.4.4
django-crispy-forms==2.4
djangorestframework==3.16.1
```

## 🛠️ Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone <tu-repositorio>
cd LUMAPROJECTDJANGO
```

### 2. Crear Entorno Virtual
```bash
# Windows
python -m venv lumaproject_venv
lumaproject_venv\Scripts\activate

# Linux/Mac
python3 -m venv lumaproject_venv
source lumaproject_venv/bin/activate
```

### 3. Instalar Dependencias
```bash
# Para desarrollo
pip install -r requirements.txt

# Para producción
pip install -r requirements_production.txt
```

### 4. Configurar Variables de Entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones
# Generar SECRET_KEY segura:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Configurar Base de Datos
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear Superusuario
```bash
# Método manual
python manage.py createsuperuser

# Método automático (desarrollo)
python manage_production.py superuser
```

### 7. Recolectar Archivos Estáticos
```bash
python manage.py collectstatic
```

### 8. Ejecutar Servidor de Desarrollo
```bash
python manage.py runserver
```

## 🔧 Configuración Avanzada

### Configuración de Producción
```bash
# Usar configuración de producción
export DJANGO_SETTINGS_MODULE=mi_tienda.production_settings

# O usar script de gestión
python manage_production.py setup
```

### Configuración de Email (Gmail)
1. Habilitar autenticación de 2 factores en Gmail
2. Generar contraseña de aplicación
3. Configurar en .env:
```env
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_password_de_aplicacion
```

### Configuración AWS S3 (Opcional)
```env
USE_S3=True
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_STORAGE_BUCKET_NAME=mi-tienda-bucket
```

## 📊 Uso del Sistema

### Acceso por Roles

#### Administrador
- **URL**: `/admin/` o `/dashboard/`
- **Permisos**: Acceso completo al sistema
- **Funciones**: Gestión de usuarios, productos, reportes

#### Vendedor
- **URL**: `/dashboard/`
- **Permisos**: Gestión de productos y ventas
- **Funciones**: CRUD productos, ver reportes básicos

#### Cliente
- **URL**: `/dashboard/`
- **Permisos**: Compras y perfil personal
- **Funciones**: Realizar pedidos, ver historial

### Funcionalidades Principales

#### Gestión de Productos
```
/productos/                 # Lista de productos
/productos/crear/          # Crear producto
/productos/editar/<id>/    # Editar producto
/productos/eliminar/<id>/  # Eliminar producto
```

#### Sistema de Pedidos
```
/carrito/                  # Ver carrito
/pedidos/checkout/         # Proceso de compra
/pedidos/                  # Historial de pedidos
```

#### Reportes y Exportación
```
/reportes/                 # Dashboard de reportes
/exportar/productos/       # Exportar productos
/reportes/ventas/          # Reportes de ventas
```

## 🚀 Despliegue en Producción

### Heroku
```bash
# Instalar Heroku CLI
# Crear aplicación
heroku create mi-tienda-app

# Configurar variables de entorno
heroku config:set SECRET_KEY=tu_secret_key
heroku config:set DEBUG=False

# Desplegar
git push heroku main
```

### Railway
```bash
# Conectar con Railway
railway login
railway init
railway up
```

### Vercel
```bash
# Instalar Vercel CLI
npm i -g vercel

# Desplegar
vercel --prod
```

## 🛠️ Scripts de Gestión

### Script de Producción
```bash
# Configuración completa
python manage_production.py setup

# Crear backup
python manage_production.py backup

# Verificar sistema
python manage_production.py check

# Restaurar backup
python manage_production.py restore backup_file.json
```

### Comandos Útiles
```bash
# Verificar configuración
python manage.py check --deploy

# Crear datos de ejemplo
python crear_datos_ejemplo.py

# Convertir precios a guaraníes
python convertir_precios_guaranies.py
```

## 📁 Estructura del Proyecto

```
LUMAPROJECTDJANGO/
├── mi_tienda/              # Configuración principal
│   ├── settings.py         # Configuración base
│   ├── production_settings.py  # Configuración producción
│   ├── env_settings.py     # Configuración con variables de entorno
│   └── urls.py            # URLs principales
├── gestion/               # Aplicación principal
│   ├── models.py          # Modelos de datos
│   ├── views.py           # Vistas principales
│   ├── middleware_mejorado.py  # Middleware personalizado
│   └── context_processors.py  # Procesadores de contexto
├── templates/             # Plantillas HTML
├── static/               # Archivos estáticos
├── media/                # Archivos multimedia
├── requirements.txt      # Dependencias base
├── requirements_production.txt  # Dependencias producción
├── manage_production.py  # Script de gestión
└── .env.example         # Ejemplo de variables de entorno
```

## 🔍 Troubleshooting

### Problemas Comunes

#### Error de Migraciones
```bash
python manage.py makemigrations --empty gestion
python manage.py migrate --fake-initial
```

#### Error de Archivos Estáticos
```bash
python manage.py collectstatic --clear
python manage.py collectstatic --noinput
```

#### Error de Permisos
```bash
# Verificar middleware habilitado en settings.py
# Verificar roles de usuario en admin
```

#### Error de Base de Datos
```bash
# Resetear base de datos (CUIDADO: borra datos)
python manage.py flush
python manage.py migrate
```

## 📞 Soporte y Contacto

- **Email**: soporte@mitienda.com
- **Documentación**: Ver archivos .md en el proyecto
- **Issues**: Crear issue en el repositorio

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo LICENSE para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📈 Roadmap

### Próximas Funcionalidades
- [ ] Integración con WhatsApp Business
- [ ] Sistema de chat en tiempo real
- [ ] Aplicación móvil React Native
- [ ] Integración con sistemas de pago locales
- [ ] Dashboard de analytics avanzado
- [ ] Sistema de inventario automático

---

**Desarrollado con ❤️ por Luma Construction & Tech**

*Versión 2.0.0 - Diciembre 2024*