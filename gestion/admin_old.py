from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioPersonalizado, Tienda, Categoria, Producto, Material, Maquinaria, Herramienta, Obra, Presupuesto

# Personalizar la visualización del usuario en el admin
class UsuarioPersonalizadoAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('rol', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Personalizada', {
            'fields': ('rol', 'telefono', 'direccion', 'avatar', 'tienda', 'es_activo')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Personalizada', {
            'fields': ('rol', 'telefono', 'email', 'es_activo')
        }),
    )

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'fecha_creacion']
    search_fields = ['nombre']
    list_filter = ['fecha_creacion']

class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'categoria', 'stock', 'fecha_creacion']
    list_filter = ['categoria', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock']

class MaterialAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'stock', 'unidad_medida', 'creado_por', 'fecha_creacion']
    list_filter = ['unidad_medida', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']

class MaquinariaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'modelo', 'marca', 'estado', 'costo_alquiler_dia', 'creado_por']
    list_filter = ['estado', 'marca']
    search_fields = ['nombre', 'modelo', 'descripcion']

class HerramientaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'estado', 'cantidad_disponible', 'cantidad_total', 'creado_por']
    list_filter = ['estado']
    search_fields = ['nombre', 'descripcion']

class ObraAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cliente', 'constructor', 'estado', 'fecha_inicio', 'presupuesto_asignado']
    list_filter = ['estado', 'fecha_inicio']
    search_fields = ['nombre', 'ubicacion', 'descripcion']

class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ['id', 'obra', 'cliente', 'total', 'estado', 'fecha_creacion']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['obra__nombre', 'cliente__username']

# Registrar todos los modelos
admin.site.register(UsuarioPersonalizado, UsuarioPersonalizadoAdmin)
admin.site.register(Tienda)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Maquinaria, MaquinariaAdmin)
admin.site.register(Herramienta, HerramientaAdmin)
admin.site.register(Obra, ObraAdmin)
admin.site.register(Presupuesto, PresupuestoAdmin)