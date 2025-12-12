# ⏱️ Sistema de Producción en Tiempo Real - L.u.M.a

## Gestión Completa de Obras por Períodos Temporales

Este sistema permite monitorear y gestionar la producción de obras civiles en tiempo real con vistas por **Hora**, **Día**, **Semana**, **Quincena**, **Mes** y **Año**.

## 🎯 Funcionalidades Principales

### ⏰ **Vistas Temporales**

1. **Por Hora**: Monitoreo en tiempo real de la producción actual
2. **Por Día**: Seguimiento diario de avances y costos
3. **Por Semana**: Análisis semanal de productividad
4. **Por Quincena**: Evaluación quincenal de proyectos
5. **Por Mes**: Reportes mensuales completos
6. **Por Año**: Análisis anual y tendencias

### 📊 **Métricas en Tiempo Real**

- **Producción Actual**: Porcentaje de avance en el período seleccionado
- **Empleados Activos**: Número de trabajadores en tiempo real
- **Obras en Proceso**: Cantidad de proyectos activos
- **Costos Totales**: Gastos acumulados por período
- **Eficiencia**: Porcentaje de eficiencia operativa

### 🏗️ **Control de Obras**

- Estado en tiempo real de cada obra
- Progreso visual con barras animadas
- Empleados asignados por proyecto
- Días restantes estimados
- Porcentaje de presupuesto utilizado

### 👷 **Gestión de Personal**

- **Empleados Activos**: Lista en tiempo real
- **Especialidades**: Maestros, electricistas, plomeros, etc.
- **Horas Trabajadas**: Control de jornadas laborales
- **Asignación por Obra**: Distribución de personal

### 🏢 **Contratistas**

- **Empresas Activas**: Constructoras trabajando
- **Obras Asignadas**: Proyectos por contratista
- **Eficiencia**: Rendimiento de cada empresa
- **Empleados Totales**: Personal por contratista

## 🚀 Archivos del Sistema

### Templates Principales
```
templates/gestion/produccion/
├── dashboard_tiempo_real.html     # Dashboard principal
├── dashboard_produccion.html      # Vista básica
└── reporte_completo.html         # Reportes por períodos
```

### Vistas (Backend)
```python
# views_produccion.py
- dashboard_tiempo_real()          # Vista principal
- api_datos_tiempo_real()         # API AJAX
- reporte_produccion_completo()   # Reportes
```

### URLs
```python
path('produccion/tiempo-real/', dashboard_tiempo_real)
path('produccion/api/tiempo-real/', api_datos_tiempo_real)
path('produccion/reporte-completo/', reporte_produccion_completo)
```

## 📱 Características Técnicas

### 🎨 **Interfaz Visual**

- **Diseño Responsivo**: Adaptable a móviles y tablets
- **Animaciones Suaves**: Transiciones profesionales
- **Gráficos Interactivos**: Chart.js para visualización
- **Colores Temáticos**: Gradientes profesionales
- **Iconografía**: Font Awesome icons

### ⚡ **Tiempo Real**

- **Actualización Automática**: Cada 30 segundos
- **WebSocket Ready**: Preparado para conexiones en vivo
- **API REST**: Endpoints para datos dinámicos
- **Notificaciones**: Alertas de cambios importantes

### 📊 **Gráficos y Visualización**

```javascript
// Gráfico de Producción
Chart.js con:
- Líneas de tendencia
- Barras comparativas
- Animaciones fluidas
- Colores dinámicos
```

### 🔄 **Actualización Automática**

```javascript
// Intervalos de actualización
- Métricas: cada 30 segundos
- Gráficos: cada 2 minutos  
- Listas: cada 1 minuto
- Reloj: cada 1 segundo
```

## 🎯 Cómo Usar el Sistema

### 1. **Acceso al Dashboard**
```
Menú Lateral → TIEMPO REAL
URL: /produccion/tiempo-real/
```

### 2. **Cambiar Período**
- Clic en botones: Hora, Día, Semana, Quincena, Mes, Año
- Los datos se actualizan automáticamente
- Gráficos se regeneran con nueva información

### 3. **Monitoreo en Vivo**
- **Badge "LIVE"**: Indica actualización en tiempo real
- **Reloj Digital**: Hora y fecha actuales
- **Métricas Animadas**: Contadores con efectos

### 4. **Análisis de Datos**
- **Gráfico Principal**: Tendencias de producción
- **Gráfico de Costos**: Distribución por categorías
- **Listas Dinámicas**: Obras, empleados, contratistas

## 💰 Gestión de Costos

### Por Categorías
- **Materiales**: 40% del costo total
- **Mano de Obra**: 35% del costo total
- **Maquinaria**: 15% del costo total
- **Transporte**: 7% del costo total
- **Otros**: 3% del costo total

### Por Empleado (Tiempo Real)
```python
COSTOS_EMPLEADOS = {
    'peón': {'hora': 12000, 'dia': 96000, 'mes': 2500000},
    'oficial': {'hora': 18000, 'dia': 144000, 'mes': 3800000},
    'maestro': {'hora': 25000, 'dia': 200000, 'mes': 5200000},
    'electricista': {'hora': 22000, 'dia': 176000, 'mes': 4600000},
    'plomero': {'hora': 20000, 'dia': 160000, 'mes': 4200000}
}
```

## 📈 Datos de Ejemplo por Período

### Hora Actual
- Producción: 85%
- Empleados: 24 activos
- Obras: 5 en proceso
- Costo: 850.000 Gs.

### Día Completo
- Producción: 78%
- Empleados: 32 activos
- Obras: 7 en proceso
- Costo: 8.500.000 Gs.

### Semana
- Producción: 82%
- Empleados: 45 promedio
- Obras: 12 activas
- Costo: 65.000.000 Gs.

### Mes
- Producción: 88%
- Empleados: 52 promedio
- Obras: 18 completadas
- Costo: 280.000.000 Gs.

### Año
- Producción: 85%
- Empleados: 48 promedio
- Obras: 156 completadas
- Costo: 3.200.000.000 Gs.

## 🔧 Configuración Técnica

### JavaScript Principal
```javascript
class ProduccionTiempoReal {
    constructor() {
        this.periodoActual = 'hora';
        this.charts = {};
        this.intervalos = {};
    }
    
    // Métodos principales
    cambiarPeriodo(periodo)
    cargarDatos()
    crearGraficos()
    iniciarActualizacionAutomatica()
}
```

### API Endpoints
```python
# Datos en tiempo real
GET /produccion/api/tiempo-real/?periodo=hora

# Respuesta JSON
{
    "produccion_actual": 85,
    "empleados_activos": 24,
    "obras_activas": 5,
    "costo_total": 850000,
    "timestamp": "2024-01-15T14:30:00"
}
```

### Integración con IoT (Futuro)
```python
# Sensores en obras
- Contadores de personal (RFID)
- Medidores de progreso (Drones)
- Sensores de maquinaria (GPS)
- Cámaras de seguridad (IA)
```

## 📊 Reportes y Exportación

### Formatos Disponibles
- **PDF**: Reporte completo imprimible
- **Excel**: Datos para análisis
- **JSON**: API para integraciones

### Contenido de Reportes
- Métricas por todos los períodos
- Gráficos comparativos
- Tablas de datos
- Análisis de tendencias

## 🌟 Características Avanzadas

### Animaciones CSS
```css
@keyframes pulse-badge {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}
```

### Efectos Visuales
- **Partículas Flotantes**: Elementos decorativos
- **Gradientes Dinámicos**: Colores profesionales
- **Sombras Suaves**: Profundidad visual
- **Transiciones**: Cambios suaves

### Responsive Design
```css
@media (max-width: 768px) {
    .metric-realtime { padding: 15px; }
    .vista-btn { padding: 8px 15px; }
    .chart-container { padding: 15px; }
}
```

## 🚀 Futuras Mejoras

1. **Integración IoT**: Sensores reales en obras
2. **Machine Learning**: Predicciones de producción
3. **Realidad Aumentada**: Visualización 3D de obras
4. **Blockchain**: Trazabilidad de materiales
5. **Inteligencia Artificial**: Optimización automática

## 📞 Soporte y Mantenimiento

### Monitoreo del Sistema
- Logs de errores automáticos
- Alertas de rendimiento
- Backup de datos en tiempo real
- Métricas de uso del sistema

### Troubleshooting
```javascript
// Debug en consola
console.log('🎯 Sistema de Producción cargado');
console.log('📊 Gráficos inicializados');
console.log('⏱️ Actualización automática activa');
```

---

**Desarrollado por L.u.M.a System** 🇵🇾  
*Sistema de Gestión de Obras Civiles - Paraguay*

**Versión**: 2.0  
**Última actualización**: Enero 2024