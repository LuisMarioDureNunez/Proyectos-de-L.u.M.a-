# 🖼️ Sistema de Modales de Imágenes - L.u.M.a

## Funcionalidad Similar a Facebook

Este sistema implementa una funcionalidad similar a Facebook para mostrar imágenes de perfil y logos de empresa en modales profesionales.

## ✨ Características Principales

### 🎯 Funcionalidades Implementadas

1. **Modal de Imagen de Perfil**
   - Click simple: Muestra la imagen en grande
   - Doble click: Permite cambiar la imagen
   - Información del usuario en el modal
   - Efectos visuales profesionales

2. **Modal de Logo de Empresa**
   - Click simple: Muestra el logo en grande
   - Doble click: Permite cambiar el logo
   - Información de la empresa
   - Diseño corporativo

3. **Efectos Visuales**
   - Partículas animadas en el fondo
   - Efectos de hover con zoom
   - Transiciones suaves
   - Iconos de lupa al hacer hover

## 🚀 Cómo Usar

### En el Perfil de Usuario

```html
<!-- Imagen de perfil clickeable -->
<img src="{{ user.avatar.url }}" 
     class="profile-avatar clickable-image shine-effect" 
     id="profileImage"
     data-tooltip="Clic para ver en grande • Doble clic para cambiar">

<!-- Logo de empresa clickeable -->
<img src="{{ user.tienda.logo.url }}" 
     class="company-logo clickable-image shine-effect" 
     id="companyLogo"
     data-tooltip="Clic para ver en grande • Doble clic para cambiar">
```

### En la Navbar

```html
<!-- Avatar en navbar -->
<img src="{{ user.avatar.url }}" 
     onclick="showProfileModal()"
     style="cursor: pointer;">

<!-- Logo en navbar -->
<img src="{% static 'images/logo.jpeg' %}" 
     onclick="showLogoModal()"
     style="cursor: pointer;">
```

## 🎨 Estilos CSS

### Clases Principales

- `.clickable-image`: Hace que la imagen sea clickeable con efectos
- `.shine-effect`: Agrega efecto de brillo al hacer hover
- `.profile-modal`: Estilo específico para modales de perfil
- `.modal-particles`: Contenedor para partículas animadas

### Efectos Visuales

```css
.clickable-image:hover::before {
    content: '🔍';
    opacity: 1;
    transform: translate(-50%, -50%) scale(1.2);
}
```

## 📱 JavaScript

### Funciones Principales

```javascript
// Mostrar modal de perfil
showProfileModal()

// Mostrar modal de logo
showLogoModal()

// Crear partículas en modal
createModalParticles(modalId)

// Mostrar notificación
showNotification(message, type)
```

### Event Listeners

- **Click simple**: Muestra modal
- **Doble click**: Abre selector de archivos
- **Hover**: Efectos visuales
- **Modal shown**: Crea partículas

## 🔧 Archivos Involucrados

### Templates
- `templates/usuarios/perfil_usuario.html`
- `templates/base.html`

### CSS
- `static/css/image_modals.css`

### JavaScript
- `static/js/image_modals.js`

## 🎯 Funcionalidades Avanzadas

### 1. Partículas Animadas
```javascript
createModalParticles(modalId) {
    // Crea 20 partículas con colores aleatorios
    // Animación flotante de 4-10 segundos
    // Opacidad y tamaño variables
}
```

### 2. Notificaciones
```javascript
showNotification('Imagen actualizada', 'success')
// Aparece en la esquina superior derecha
// Se auto-elimina después de 3 segundos
```

### 3. Efectos de Zoom
- Click en imagen del modal para hacer zoom
- Hover para preview del zoom
- Transiciones suaves

### 4. Tooltips Personalizados
```html
data-tooltip="Clic para ver en grande • Doble clic para cambiar"
```

## 📋 Instrucciones de Uso

### Para el Usuario Final

1. **Ver imagen en grande**:
   - Hacer clic en cualquier imagen de perfil o logo
   - Se abrirá un modal con la imagen ampliada

2. **Cambiar imagen**:
   - Hacer doble clic en la imagen
   - Se abrirá el selector de archivos
   - Seleccionar nueva imagen

3. **Cerrar modal**:
   - Clic en el botón X
   - Clic fuera del modal
   - Tecla Escape

### Para Desarrolladores

1. **Agregar nueva imagen clickeable**:
```html
<img src="ruta/imagen.jpg" 
     class="clickable-image" 
     onclick="showProfileModal()">
```

2. **Personalizar modal**:
```javascript
// Modificar createProfileModal() o createCompanyModal()
// en image_modals.js
```

3. **Agregar nuevos efectos**:
```css
/* En image_modals.css */
.mi-efecto-personalizado {
    /* Estilos personalizados */
}
```

## 🌟 Características Técnicas

### Responsive Design
- Modales adaptativos para móviles
- Imágenes que se ajustan al viewport
- Botones táctiles optimizados

### Performance
- Lazy loading de partículas
- Optimización de animaciones CSS
- Event listeners eficientes

### Accesibilidad
- Soporte para teclado
- ARIA labels apropiados
- Contraste de colores adecuado

## 🎨 Personalización

### Colores del Sistema
```css
:root {
    --primary-color: #002395;
    --secondary-color: #000000;
    --accent-color: #40E0D0;
    --warning-color: #FF6600;
    --gold-color: #ffd700;
}
```

### Animaciones
- Duración: 0.3s - 0.5s
- Easing: ease, ease-in-out
- Transform: scale, translate, rotate

## 🚀 Futuras Mejoras

1. **Galería de imágenes**: Múltiples fotos de perfil
2. **Filtros de imagen**: Efectos en tiempo real
3. **Recorte de imagen**: Editor integrado
4. **Compartir imagen**: Redes sociales
5. **Historial de avatares**: Versiones anteriores

## 📞 Soporte

Para dudas o problemas:
- Revisar la consola del navegador
- Verificar que Bootstrap 5 esté cargado
- Comprobar que jQuery esté disponible
- Validar rutas de archivos CSS/JS

---

**Desarrollado por L.u.M.a System** 🇵🇾
*Sistema de Gestión de Obras Civiles - Paraguay*