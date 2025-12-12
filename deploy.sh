#!/bin/bash
# deploy.sh - Script de deploy para desarrollo/producción

echo "🚀 Iniciando despliegue del Sistema de Gestión de Obras..."

# Variables
PROJECT_DIR="/media/familiataboada/MARIO_LUMA/Mario_Trabajo/LUMAPROJECTDJANGO"
VENV_DIR="$PROJECT_DIR/venv"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para log
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Verificar si existe el directorio del proyecto
if [ ! -d "$PROJECT_DIR" ]; then
    error "Directorio del proyecto no encontrado: $PROJECT_DIR"
    exit 1
fi

cd $PROJECT_DIR

# Verificar si Python está disponible
if ! command -v python &> /dev/null; then
    error "Python no está instalado o no está en el PATH"
    exit 1
fi

# Verificar entorno virtual
if [ ! -d "$VENV_DIR" ]; then
    log "Creando entorno virtual..."
    python -m venv $VENV_DIR
fi

# Activar entorno virtual
log "Activando entorno virtual..."
source $VENV_DIR/bin/activate

# Instalar/actualizar dependencias
log "Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Aplicar migraciones
log "Aplicando migraciones..."
python manage.py makemigrations
python manage.py migrate

# Colectar archivos estáticos
log "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

# Crear superusuario si no existe
log "Verificando superusuario..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Superusuario creado: admin / admin123')
else:
    print('✅ Superusuario ya existe')
"

# Verificar si hay errores
log "Verificando el sistema..."
python manage.py check --deploy

# Cargar datos iniciales (opcional)
log "Cargando datos iniciales..."
python manage.py shell -c "
from gestion.models import *
# Datos iniciales aquí si es necesario
print('✅ Sistema verificado correctamente')
"

log "✅ Despliegue completado exitosamente!"
log "📝 Para ejecutar el servidor: python manage.py runserver"
log "🌐 Accede en: http://127.0.0.1:8000"
log "👤 Usuario: admin | Contraseña: admin123"