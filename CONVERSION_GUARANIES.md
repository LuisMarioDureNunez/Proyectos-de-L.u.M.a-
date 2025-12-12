# 🇵🇾 Conversión a Guaraníes Paraguayos

## Resumen
Este documento describe el proceso completo para convertir todos los precios de la aplicación L.u.M.a de dólares estadounidenses (USD) a guaraníes paraguayos (PYG).

## 📋 ¿Qué se ha convertido?

### Base de Datos
- ✅ **Materiales**: Todos los precios de materiales de construcción
- ✅ **Productos**: Todos los precios de productos en el inventario
- ✅ **Maquinaria**: Costos de alquiler por día
- ✅ **Items de Presupuesto**: Precios unitarios en presupuestos
- ✅ **Presupuestos**: Totales recalculados automáticamente
- ✅ **Contratos**: Montos totales y anticipos

### Templates (Interfaz de Usuario)
- ✅ **Carrito de Compras**: Precios y totales
- ✅ **Checkout**: Resumen de pago y totales
- ✅ **Confirmación de Pedido**: Detalles de pago
- ✅ **Lista de Pedidos**: Totales de pedidos
- ✅ **Dashboard**: Estadísticas y precios promedio
- ✅ **Emails**: Notificaciones de productos y precios

## 💱 Tasa de Cambio Utilizada
- **1 USD = 7,300 PYG** (Guaraníes paraguayos)
- Esta tasa puede actualizarse modificando la variable `TASA_CAMBIO` en los scripts

## 🚀 Cómo Ejecutar la Conversión

### Opción 1: Script Completo (Recomendado)
```bash
cd c:\L.u.M.a-app\LUMAPROJECTDJANGO
python ejecutar_conversion_completa.py
```

### Opción 2: Script Simple (Solo Materiales y Productos)
```bash
python convertir_precios_simple.py
```

### Opción 3: Comando de Django
```bash
python manage.py convertir_a_guaranies --confirmar
```

### Opción 4: Con Tasa de Cambio Personalizada
```bash
python manage.py convertir_a_guaranies --tasa-cambio 7500 --confirmar
```

## 📁 Archivos Creados/Modificados

### Scripts de Conversión
- `ejecutar_conversion_completa.py` - Script principal completo
- `convertir_precios_simple.py` - Script básico
- `convertir_precios_guaranies.py` - Script detallado con interacción
- `gestion/management/commands/convertir_a_guaranies.py` - Comando Django

### Templates Actualizados
- `templates/carrito/ver_carrito.html`
- `templates/pedidos/checkout.html`
- `templates/pedidos/confirmacion.html`
- `templates/pedidos/lista_pedidos.html`
- `templates/dashboard/dashboard.html`
- `templates/emails/producto_actualizado.html`
- `templates/emails/producto_creado.html`
- `templates/emails/stock_bajo.html`

## 🎨 Formato de Visualización

### Antes (USD)
```
$8,500.00
$25,000.00
$150,000.00
```

### Después (PYG)
```
62.050.000 Gs.
182.500.000 Gs.
1.095.000.000 Gs.
```

## 🔧 Filtros de Template Disponibles

La aplicación incluye filtros personalizados para formatear guaraníes:

```django
{% load paraguay_filters %}

{{ precio|guaranies }}  <!-- Formato: Gs. 1.500.000 -->
{{ precio|floatformat:0 }} Gs.  <!-- Formato: 1500000 Gs. -->
```

## ⚠️ Consideraciones Importantes

### Antes de Ejecutar
1. **Hacer backup de la base de datos**
2. **Verificar que no hay usuarios activos**
3. **Confirmar la tasa de cambio actual**

### Después de Ejecutar
1. **Reiniciar el servidor Django**
2. **Verificar todos los precios en la interfaz**
3. **Probar el flujo completo de compra**
4. **Actualizar documentación de usuario**

## 🧪 Verificación Post-Conversión

### Checklist de Verificación
- [ ] Los precios se muestran en guaraníes en el catálogo
- [ ] El carrito calcula correctamente los totales
- [ ] El checkout muestra los montos correctos
- [ ] Los presupuestos se generan con precios en guaraníes
- [ ] Los emails muestran precios en guaraníes
- [ ] El dashboard muestra estadísticas correctas

### Páginas a Verificar
1. **Lista de Productos** - `/productos/`
2. **Carrito** - `/carrito/`
3. **Checkout** - `/checkout/`
4. **Dashboard** - `/dashboard/`
5. **Presupuestos** - `/gestion/presupuestos/`

## 🔄 Reversión (Si es necesario)

Si necesitas revertir los cambios:

1. **Restaurar backup de la base de datos**
2. **Revertir cambios en templates** (usar Git si está disponible)
3. **Actualizar la tasa de cambio a 1/7300 para convertir de PYG a USD**

## 📞 Soporte

Si encuentras algún problema durante la conversión:

1. **Verificar logs de error** en la consola
2. **Revisar la integridad de la base de datos**
3. **Contactar al equipo de desarrollo**

## 📊 Estadísticas de Conversión

Después de ejecutar la conversión, verás un resumen como:

```
🎉 CONVERSIÓN COMPLETADA EXITOSAMENTE
====================================
📦 Materiales convertidos: 10
🛍️ Productos convertidos: 15
🚜 Maquinarias convertidas: 5
📋 Items de presupuesto convertidos: 25
📊 Presupuestos recalculados: 8
📄 Contratos convertidos: 3
====================================
✅ Todos los precios han sido convertidos a Guaraníes (PYG)
```

## 🌟 Beneficios de la Conversión

1. **Localización Completa**: Precios en moneda local paraguaya
2. **Mejor UX**: Los usuarios ven precios en su moneda familiar
3. **Precisión**: Eliminación de conversiones manuales
4. **Profesionalismo**: Aplicación completamente localizada

---

**Fecha de Conversión**: $(date)
**Versión**: 1.0
**Tasa de Cambio**: 1 USD = 7,300 PYG