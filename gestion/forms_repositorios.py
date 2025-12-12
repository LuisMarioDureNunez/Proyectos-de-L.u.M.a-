# forms_repositorios.py - Formularios para gestión de repositorios GitHub
from django import forms
from django.core.validators import URLValidator
from .models import RepositorioGitHub, TagRepositorio, ComentarioRepositorio
import requests
import json

class RepositorioGitHubForm(forms.ModelForm):
    """Formulario para crear/editar repositorios GitHub"""
    
    # Campos adicionales para mejor UX
    sincronizar_github = forms.BooleanField(
        required=False,
        initial=True,
        help_text="Sincronizar automáticamente datos desde GitHub API"
    )
    
    class Meta:
        model = RepositorioGitHub
        fields = [
            'nombre', 'descripcion', 'url_repositorio', 'url_demo', 'url_documentacion',
            'tipo_proyecto', 'tecnologia_principal', 'tecnologias_adicionales',
            'estado', 'progreso_porcentaje', 'dificultad', 'calidad_codigo',
            'es_destacado', 'es_comercial', 'es_open_source',
            'cliente_proyecto', 'costo_desarrollo', 'tiempo_desarrollo_horas',
            'imagen_preview', 'video_demo', 'tags'
        ]
        
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del repositorio'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción detallada del proyecto...'
            }),
            'url_repositorio': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/usuario/repositorio'
            }),
            'url_demo': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://demo.ejemplo.com'
            }),
            'url_documentacion': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://docs.ejemplo.com'
            }),
            'tipo_proyecto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tecnologia_principal': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tecnologias_adicionales': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'multiple': True,
                'size': 5
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'progreso_porcentaje': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'step': 5
            }),
            'dificultad': forms.Select(attrs={
                'class': 'form-select'
            }),
            'calidad_codigo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'cliente_proyecto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del cliente (opcional)'
            }),
            'costo_desarrollo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Costo en Guaraníes'
            }),
            'tiempo_desarrollo_horas': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Horas de desarrollo'
            }),
            'imagen_preview': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'video_demo': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://youtube.com/watch?v=...'
            }),
            'tags': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
        }
        
        labels = {
            'nombre': '📁 Nombre del Repositorio',
            'descripcion': '📝 Descripción',
            'url_repositorio': '🔗 URL del Repositorio',
            'url_demo': '🌐 URL de Demo',
            'url_documentacion': '📚 Documentación',
            'tipo_proyecto': '🏷️ Tipo de Proyecto',
            'tecnologia_principal': '⚙️ Tecnología Principal',
            'tecnologias_adicionales': '🛠️ Tecnologías Adicionales',
            'estado': '📊 Estado del Proyecto',
            'progreso_porcentaje': '📈 Progreso (%)',
            'dificultad': '⭐ Nivel de Dificultad',
            'calidad_codigo': '💎 Calidad del Código',
            'es_destacado': '🌟 Proyecto Destacado',
            'es_comercial': '💼 Proyecto Comercial',
            'es_open_source': '🔓 Código Abierto',
            'cliente_proyecto': '👤 Cliente',
            'costo_desarrollo': '💰 Costo de Desarrollo',
            'tiempo_desarrollo_horas': '⏱️ Tiempo de Desarrollo (horas)',
            'imagen_preview': '🖼️ Imagen de Vista Previa',
            'video_demo': '🎥 Video Demo',
            'tags': '🏷️ Etiquetas',
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Configurar tecnologías adicionales como choices
        self.fields['tecnologias_adicionales'].widget = forms.CheckboxSelectMultiple(
            choices=RepositorioGitHub.TECNOLOGIAS_PRINCIPALES
        )
        
        # Si es edición, pre-seleccionar tecnologías adicionales
        if self.instance.pk and self.instance.tecnologias_adicionales:
            self.fields['tecnologias_adicionales'].initial = self.instance.tecnologias_adicionales
    
    def clean_url_repositorio(self):
        """Validar que la URL sea de GitHub"""
        url = self.cleaned_data.get('url_repositorio')
        if url and 'github.com' not in url:
            raise forms.ValidationError('La URL debe ser de un repositorio de GitHub')
        return url
    
    def clean_progreso_porcentaje(self):
        """Validar que el progreso esté entre 0 y 100"""
        progreso = self.cleaned_data.get('progreso_porcentaje')
        if progreso is not None and (progreso < 0 or progreso > 100):
            raise forms.ValidationError('El progreso debe estar entre 0 y 100')
        return progreso
    
    def save(self, commit=True):
        """Guardar el repositorio y sincronizar con GitHub si es necesario"""
        repositorio = super().save(commit=False)
        
        if self.user:
            repositorio.desarrollador = self.user
        
        # Procesar tecnologías adicionales
        tecnologias_adicionales = self.cleaned_data.get('tecnologias_adicionales', [])
        if isinstance(tecnologias_adicionales, list):
            repositorio.tecnologias_adicionales = tecnologias_adicionales
        
        if commit:
            repositorio.save()
            
            # Guardar tags many-to-many
            if 'tags' in self.cleaned_data:
                repositorio.tags.set(self.cleaned_data['tags'])
            
            # Sincronizar con GitHub si está habilitado
            if self.cleaned_data.get('sincronizar_github', False):
                self.sincronizar_con_github(repositorio)
        
        return repositorio
    
    def sincronizar_con_github(self, repositorio):
        """Sincronizar datos con la API de GitHub"""
        try:
            api_url = repositorio.get_url_github_api()
            if not api_url:
                return
            
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                # Actualizar datos del repositorio
                repositorio.github_id = data.get('id')
                repositorio.estrellas = data.get('stargazers_count', 0)
                repositorio.forks = data.get('forks_count', 0)
                repositorio.watchers = data.get('watchers_count', 0)
                repositorio.issues_abiertas = data.get('open_issues_count', 0)
                repositorio.lenguaje_principal = data.get('language')
                repositorio.tamaño_kb = data.get('size', 0)
                repositorio.es_privado = data.get('private', False)
                repositorio.es_fork = data.get('fork', False)
                repositorio.tiene_wiki = data.get('has_wiki', False)
                repositorio.tiene_pages = data.get('has_pages', False)
                repositorio.licencia = data.get('license', {}).get('name') if data.get('license') else None
                
                # Fechas
                from django.utils.dateparse import parse_datetime
                if data.get('created_at'):
                    repositorio.fecha_creacion_github = parse_datetime(data['created_at'])
                if data.get('updated_at'):
                    repositorio.fecha_ultimo_commit = parse_datetime(data['updated_at'])
                
                repositorio.sincronizado_github = True
                repositorio.ultima_sincronizacion = timezone.now()
                repositorio.save()
                
        except Exception as e:
            print(f"Error sincronizando con GitHub: {e}")

class FiltroRepositoriosForm(forms.Form):
    """Formulario para filtrar repositorios"""
    
    busqueda = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '🔍 Buscar repositorios...'
        })
    )
    
    tipo_proyecto = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos los tipos')] + RepositorioGitHub.TIPOS_PROYECTO,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    tecnologia = forms.ChoiceField(
        required=False,
        choices=[('', 'Todas las tecnologías')] + RepositorioGitHub.TECNOLOGIAS_PRINCIPALES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    estado = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos los estados')] + RepositorioGitHub.ESTADOS_PROYECTO,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    solo_destacados = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    solo_comerciales = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    ordenar_por = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Orden por defecto'),
            ('-fecha_ultimo_commit', 'Más recientes'),
            ('-estrellas', 'Más estrellas'),
            ('-vistas', 'Más vistas'),
            ('nombre', 'Nombre A-Z'),
            ('-nombre', 'Nombre Z-A'),
            ('-progreso_porcentaje', 'Mayor progreso'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class TagRepositorioForm(forms.ModelForm):
    """Formulario para crear/editar tags de repositorios"""
    
    class Meta:
        model = TagRepositorio
        fields = ['nombre', 'descripcion', 'color', 'icono']
        
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del tag'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del tag...'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color'
            }),
            'icono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-code'
            }),
        }

class ComentarioRepositorioForm(forms.ModelForm):
    """Formulario para comentarios de repositorios"""
    
    class Meta:
        model = ComentarioRepositorio
        fields = ['comentario', 'calificacion']
        
        widgets = {
            'comentario': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escribe tu comentario sobre este repositorio...'
            }),
            'calificacion': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        
        labels = {
            'comentario': '💬 Comentario',
            'calificacion': '⭐ Calificación',
        }

class SincronizarGitHubForm(forms.Form):
    """Formulario para sincronizar múltiples repositorios con GitHub"""
    
    repositorios = forms.ModelMultipleChoiceField(
        queryset=RepositorioGitHub.objects.filter(activo=True),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=False
    )
    
    sincronizar_todos = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Sincronizar todos los repositorios'
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['repositorios'].queryset = RepositorioGitHub.objects.filter(
                desarrollador=user,
                activo=True
            )

class ImportarGitHubForm(forms.Form):
    """Formulario para importar repositorios desde GitHub"""
    
    username_github = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuario de GitHub'
        }),
        label='👤 Usuario de GitHub'
    )
    
    incluir_forks = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Incluir repositorios fork'
    )
    
    solo_publicos = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Solo repositorios públicos'
    )
    
    limite_repositorios = forms.IntegerField(
        min_value=1,
        max_value=100,
        initial=20,
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        }),
        label='📊 Límite de repositorios'
    )
    
    def clean_username_github(self):
        """Validar que el usuario de GitHub existe"""
        username = self.cleaned_data.get('username_github')
        if username:
            try:
                response = requests.get(f'https://api.github.com/users/{username}', timeout=10)
                if response.status_code != 200:
                    raise forms.ValidationError('Usuario de GitHub no encontrado')
            except requests.RequestException:
                raise forms.ValidationError('Error al verificar el usuario de GitHub')
        return username