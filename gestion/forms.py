# forms.py - VERSIÓN MÍNIMA FUNCIONAL
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UsuarioPersonalizado, Material, Maquinaria, Herramienta, Obra, Presupuesto, ItemPresupuesto, Producto, Pedido, Contratista, Propietario, Propiedad, Empleado, Proveedor, ProductoProveedor, EvaluacionProveedor, ContratoContratista
# Formularios existentes
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'stock', 'imagen']

class FormularioRegistro(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = UsuarioPersonalizado
        fields = ['username', 'email', 'password1', 'password2']

# Formularios para gestión de obras
class FormularioMaterial(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'unidad_medida']

class FormularioMaquinaria(forms.ModelForm):
    class Meta:
        model = Maquinaria
        fields = ['nombre', 'descripcion', 'estado', 'costo_alquiler_dia']

class FormularioHerramienta(forms.ModelForm):
    class Meta:
        model = Herramienta
        fields = ['nombre', 'descripcion', 'estado', 'cantidad_total']

class FormularioObra(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['nombre', 'descripcion', 'ubicacion', 'cliente', 'fecha_inicio', 'fecha_fin_estimada', 'presupuesto_asignado']

class FormularioPresupuesto(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['obra', 'descripcion_servicios', 'total']

class ItemPresupuestoForm(forms.ModelForm):
    """Formulario para items de presupuesto con cálculos en tiempo real"""
    
    class Meta:
        model = ItemPresupuesto
        fields = ['tipo', 'descripcion', 'cantidad', 'unidad_medida', 'precio_unitario', 'material', 'maquinaria', 'herramienta']
        widgets = {
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del item...'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control calculable',
                'step': '0.01',
                'min': '0.01'
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'form-control calculable',
                'step': '0.01',
                'min': '0.01'
            }),
            'unidad_medida': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'material': forms.Select(attrs={'class': 'form-control select-material'}),
            'maquinaria': forms.Select(attrs={'class': 'form-control'}),
            'herramienta': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        cantidad = cleaned_data.get('cantidad')
        precio_unitario = cleaned_data.get('precio_unitario')
        
        if cantidad and precio_unitario:
            # Validar que el total no sea cero
            total = cantidad * precio_unitario
            if total <= 0:
                raise forms.ValidationError("El total del item debe ser mayor a cero.")
        
        return cleaned_data

class PresupuestoForm(forms.ModelForm):
    """Formulario principal de presupuesto"""
    
    class Meta:
        model = Presupuesto
        fields = ['obra', 'constructor', 'descripcion_servicios', 'iva_porcentaje', 'dias_validez']
        widgets = {
            'obra': forms.Select(attrs={
                'class': 'form-control select-obra',
                'data-live-search': 'true'
            }),
            'constructor': forms.Select(attrs={
                'class': 'form-control',
                'data-live-search': 'true'
            }),
            'descripcion_servicios': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción detallada de los servicios a realizar...'
            }),
            'iva_porcentaje': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'max': '100'
            }),
            'dias_validez': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '365'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filtrar obras según el usuario
        if user and not user.es_administrador:
            if user.es_cliente:
                self.fields['obra'].queryset = Obra.objects.filter(cliente=user)
            elif user.es_constructor:
                self.fields['obra'].queryset = Obra.objects.filter(constructor=user)
        
        # Filtrar constructores
        self.fields['constructor'].queryset = self.fields['constructor'].queryset.filter(rol='constructor')

class PresupuestoWizardForm(forms.Form):
    """Formulario wizard para creación paso a paso de presupuestos"""
    
    # Paso 1: Información básica
    obra = forms.ModelChoiceField(
        queryset=Obra.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select-obra'})
    )
    descripcion_servicios = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Descripción general del trabajo...'
        })
    )
    
    # Paso 2: Configuración
    iva_porcentaje = forms.DecimalField(
        initial=10,
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'min': '0',
            'max': '100'
        })
    )
    dias_validez = forms.IntegerField(
        initial=30,
        min_value=1,
        max_value=365,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '365'
        })
    )

# =============================================
# FORMULARIOS SUPER AVANZADOS PARA PARAGUAY
# =============================================

class ContratistaForm(forms.ModelForm):
    """Formulario para gestión de contratistas"""
    
    class Meta:
        model = Contratista
        fields = [
            'nombre_empresa', 'ruc', 'especialidad', 'departamento', 'ciudad',
            'direccion_completa', 'telefono_principal', 'telefono_secundario',
            'email_empresa', 'sitio_web', 'años_experiencia', 'licencia_profesional',
            'tarifa_por_hora', 'tarifa_por_dia', 'tarifa_por_proyecto',
            'disponible_lunes_viernes', 'disponible_sabados', 'disponible_domingos'
        ]
        widgets = {
            'nombre_empresa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la empresa...'
            }),
            'ruc': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'RUC del contratista...'
            }),
            'especialidad': forms.Select(attrs={'class': 'form-control'}),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad...'
            }),
            'direccion_completa': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa...'
            }),
            'telefono_principal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+595 XXX XXXXXX'
            }),
            'telefono_secundario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+595 XXX XXXXXX'
            }),
            'email_empresa': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@empresa.com'
            }),
            'sitio_web': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.empresa.com'
            }),
            'años_experiencia': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'licencia_profesional': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de licencia...'
            }),
            'tarifa_por_hora': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1000',
                'min': '0'
            }),
            'tarifa_por_dia': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '10000',
                'min': '0'
            }),
            'tarifa_por_proyecto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '100000',
                'min': '0'
            }),
        }

class PropietarioForm(forms.ModelForm):
    """Formulario para gestión de propietarios"""
    
    class Meta:
        model = Propietario
        fields = [
            'tipo_propietario', 'nombre_completo', 'cedula_ruc', 'fecha_nacimiento',
            'telefono_principal', 'telefono_alternativo', 'email_alternativo',
            'departamento', 'ciudad', 'barrio', 'direccion_completa',
            'presupuesto_maximo', 'tipo_construccion_preferida'
        ]
        widgets = {
            'tipo_propietario': forms.Select(attrs={'class': 'form-control'}),
            'nombre_completo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo...'
            }),
            'cedula_ruc': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cédula o RUC...'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'telefono_principal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+595 XXX XXXXXX'
            }),
            'telefono_alternativo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+595 XXX XXXXXX'
            }),
            'email_alternativo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@alternativo.com'
            }),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad...'
            }),
            'barrio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Barrio...'
            }),
            'direccion_completa': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa...'
            }),
            'presupuesto_maximo': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1000000',
                'min': '0'
            }),
            'tipo_construccion_preferida': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tipo de construcción preferida...'
            }),
        }

class PropiedadForm(forms.ModelForm):
    """Formulario para gestión de propiedades"""
    
    class Meta:
        model = Propiedad
        fields = [
            'tipo_propiedad', 'nombre_propiedad', 'departamento', 'ciudad',
            'barrio', 'direccion_completa', 'superficie_total', 'superficie_construida',
            'habitaciones', 'baños', 'cocheras', 'estado_propiedad',
            'valor_fiscal', 'valor_comercial', 'tiene_agua_corriente',
            'tiene_energia_electrica', 'tiene_cloacas', 'tiene_gas', 'tiene_internet'
        ]
        widgets = {
            'tipo_propiedad': forms.Select(attrs={'class': 'form-control'}),
            'nombre_propiedad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la propiedad...'
            }),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad...'
            }),
            'barrio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Barrio...'
            }),
            'direccion_completa': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa...'
            }),
            'superficie_total': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'superficie_construida': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'habitaciones': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'baños': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'cocheras': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'estado_propiedad': forms.Select(attrs={'class': 'form-control'}),
            'valor_fiscal': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1000000',
                'min': '0'
            }),
            'valor_comercial': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1000000',
                'min': '0'
            }),
        }

class EmpleadoForm(forms.ModelForm):
    """Formulario para gestión de empleados"""
    
    class Meta:
        model = Empleado
        fields = [
            'codigo_empleado', 'cargo', 'cedula_identidad', 'fecha_nacimiento',
            'lugar_nacimiento', 'estado_civil', 'telefono_principal',
            'telefono_emergencia', 'contacto_emergencia', 'departamento',
            'ciudad', 'direccion_completa', 'fecha_ingreso', 'turno',
            'salario_base', 'bonificaciones', 'nivel_educacion',
            'certificaciones', 'años_experiencia'
        ]
        widgets = {
            'codigo_empleado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'EMP-001'
            }),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
            'cedula_identidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de cédula...'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'lugar_nacimiento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lugar de nacimiento...'
            }),
            'estado_civil': forms.Select(attrs={'class': 'form-control'}),
            'telefono_principal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+595 XXX XXXXXX'
            }),
            'telefono_emergencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+595 XXX XXXXXX'
            }),
            'contacto_emergencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del contacto de emergencia...'
            }),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad...'
            }),
            'direccion_completa': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa...'
            }),
            'fecha_ingreso': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'turno': forms.Select(attrs={'class': 'form-control'}),
            'salario_base': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '100000',
                'min': '0'
            }),
            'bonificaciones': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '50000',
                'min': '0'
            }),
            'nivel_educacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nivel de educación...'
            }),
            'certificaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Certificaciones y cursos...'
            }),
            'años_experiencia': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
        }

class ProveedorForm(forms.ModelForm):
    """Formulario para gestión de proveedores"""
    
    class Meta:
        model = Proveedor
        fields = [
            'nombre_empresa', 'ruc', 'tipo_proveedor', 'persona_contacto',
            'cargo_contacto', 'telefono_principal', 'telefono_secundario',
            'email_principal', 'email_secundario', 'sitio_web',
            'departamento', 'ciudad', 'direccion_completa', 'años_mercado',
            'capacidad_suministro', 'tiempo_entrega_promedio',
            'forma_pago_preferida', 'descuento_volumen', 'credito_maximo'
        ]
        widgets = {
            'nombre_empresa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la empresa...'
            }),
            'ruc': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'RUC de la empresa...'
            }),
            'tipo_proveedor': forms.Select(attrs={'class': 'form-control'}),
            'persona_contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del contacto...'
            }),
            'cargo_contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cargo del contacto...'
            }),
            'telefono_principal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+595 XXX XXXXXX'
            }),
            'telefono_secundario': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+595 XXX XXXXXX'
            }),
            'email_principal': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@empresa.com'
            }),
            'email_secundario': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email2@empresa.com'
            }),
            'sitio_web': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.empresa.com'
            }),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad...'
            }),
            'direccion_completa': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa...'
            }),
            'años_mercado': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'capacidad_suministro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción de capacidad...'
            }),
            'tiempo_entrega_promedio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'forma_pago_preferida': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Forma de pago preferida...'
            }),
            'descuento_volumen': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'max': '100'
            }),
            'credito_maximo': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1000000',
                'min': '0'
            }),
        }

class ProductoProveedorForm(forms.ModelForm):
    """Formulario para productos de proveedores"""
    
    class Meta:
        model = ProductoProveedor
        fields = [
            'nombre_producto', 'descripcion', 'codigo_producto', 'marca',
            'modelo', 'precio_unitario', 'precio_mayorista', 'stock_disponible',
            'stock_minimo', 'unidad_medida', 'peso', 'dimensiones', 'material'
        ]
        widgets = {
            'nombre_producto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto...'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del producto...'
            }),
            'codigo_producto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código del producto...'
            }),
            'marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Marca...'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Modelo...'
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1000',
                'min': '0'
            }),
            'precio_mayorista': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1000',
                'min': '0'
            }),
            'stock_disponible': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'stock_minimo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'unidad_medida': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Unidad de medida...'
            }),
            'peso': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'dimensiones': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dimensiones...'
            }),
            'material': forms.Select(attrs={'class': 'form-control'}),
        }

class EvaluacionProveedorForm(forms.ModelForm):
    """Formulario para evaluar proveedores"""
    
    class Meta:
        model = EvaluacionProveedor
        fields = [
            'calidad_productos', 'puntualidad_entrega', 'precio_competitivo',
            'atencion_cliente', 'comentarios', 'recomendaria'
        ]
        widgets = {
            'calidad_productos': forms.Select(attrs={'class': 'form-control'}),
            'puntualidad_entrega': forms.Select(attrs={'class': 'form-control'}),
            'precio_competitivo': forms.Select(attrs={'class': 'form-control'}),
            'atencion_cliente': forms.Select(attrs={'class': 'form-control'}),
            'comentarios': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Comentarios sobre el proveedor...'
            }),
        }

class ContratoContratistaForm(forms.ModelForm):
    """Formulario para contratos con contratistas"""
    
    class Meta:
        model = ContratoContratista
        fields = [
            'obra', 'contratista', 'fecha_inicio_prevista', 'fecha_fin_prevista',
            'monto_total', 'anticipo_porcentaje', 'descripcion_trabajo',
            'materiales_incluidos', 'mano_obra_incluida', 'garantia_meses',
            'penalizacion_retraso', 'bonificacion_adelanto'
        ]
        widgets = {
            'obra': forms.Select(attrs={'class': 'form-control'}),
            'contratista': forms.Select(attrs={'class': 'form-control'}),
            'fecha_inicio_prevista': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fin_prevista': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'monto_total': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '100000',
                'min': '0'
            }),
            'anticipo_porcentaje': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'max': '100'
            }),
            'descripcion_trabajo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción detallada del trabajo...'
            }),
            'garantia_meses': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'penalizacion_retraso': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '10000',
                'min': '0'
            }),
            'bonificacion_adelanto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '10000',
                'min': '0'
            }),
        }