# URLs para el sistema de idiomas multilenguaje
from django.urls import path
from . import views_idiomas

urlpatterns = [
    # APIs del sistema de idiomas
    path('api/languages/', views_idiomas.get_supported_languages, name='api_supported_languages'),
    path('api/language/change/', views_idiomas.change_language, name='api_change_language'),
    path('api/language/translations/', views_idiomas.get_language_translations, name='api_language_translations'),
    path('api/language/preference/', views_idiomas.get_user_language_preference, name='api_user_language_preference'),
    path('api/language/save-preference/', views_idiomas.save_user_language_preference, name='api_save_language_preference'),
    path('api/language/statistics/', views_idiomas.language_statistics, name='api_language_statistics'),
]