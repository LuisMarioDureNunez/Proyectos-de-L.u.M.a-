# MIDDLEWARE PARA SISTEMA DE IDIOMAS MULTILENGUAJE
# Manejo automático de idiomas en todas las peticiones

from django.utils.translation import activate, get_language
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class LanguageMiddleware(MiddlewareMixin):
    """
    Middleware para manejar automáticamente el idioma del usuario
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def process_request(self, request):
        """
        Procesar la petición para determinar el idioma
        """
        try:
            # Lista de idiomas soportados
            supported_languages = [
                'es', 'en', 'gn', 'pt', 'ja', 'ru', 'ko', 'fr', 'de', 'it',
                'zh', 'ar', 'hi', 'tr', 'nl', 'sv', 'no', 'da', 'fi', 'pl',
                'cs', 'hu', 'ro', 'el', 'he', 'th', 'vi', 'id', 'ms', 'tl'
            ]
            
            language_code = None
            
            # 1. Verificar si hay un idioma en la URL (parámetro GET)
            if 'lang' in request.GET:
                lang_param = request.GET['lang'].lower()
                if lang_param in supported_languages:
                    language_code = lang_param
                    logger.info(f"Idioma detectado desde URL: {language_code}")
            
            # 2. Verificar preferencia del usuario autenticado
            if not language_code and request.user.is_authenticated:
                try:
                    user_lang = getattr(request.user, 'preferred_language', None)
                    if user_lang and user_lang in supported_languages:
                        language_code = user_lang
                        logger.info(f"Idioma del usuario: {language_code}")
                except AttributeError:
                    pass
            
            # 3. Verificar idioma en la sesión
            if not language_code:
                session_lang = request.session.get('django_language')
                if session_lang and session_lang in supported_languages:
                    language_code = session_lang
                    logger.info(f"Idioma de la sesión: {language_code}")
            
            # 4. Verificar cookies
            if not language_code:
                cookie_lang = request.COOKIES.get('django_language')
                if cookie_lang and cookie_lang in supported_languages:
                    language_code = cookie_lang
                    logger.info(f"Idioma de cookie: {language_code}")
            
            # 5. Detectar desde el navegador (Accept-Language header)
            if not language_code:
                accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
                if accept_language:
                    # Parsear el header Accept-Language
                    languages = []
                    for lang_range in accept_language.split(','):
                        lang_range = lang_range.strip()
                        if ';' in lang_range:
                            lang, quality = lang_range.split(';', 1)
                            try:
                                quality = float(quality.split('=')[1])
                            except (ValueError, IndexError):
                                quality = 1.0
                        else:
                            lang, quality = lang_range, 1.0
                        
                        # Extraer código de idioma (ej: 'es-ES' -> 'es')
                        lang_code = lang.split('-')[0].lower()
                        if lang_code in supported_languages:
                            languages.append((lang_code, quality))
                    
                    # Ordenar por calidad (preferencia)
                    languages.sort(key=lambda x: x[1], reverse=True)
                    
                    if languages:
                        language_code = languages[0][0]
                        logger.info(f"Idioma detectado del navegador: {language_code}")
            
            # 6. Idioma por defecto
            if not language_code:
                language_code = getattr(settings, 'LANGUAGE_CODE', 'es')
                logger.info(f"Usando idioma por defecto: {language_code}")
            
            # Activar el idioma
            if language_code:
                activate(language_code)
                request.LANGUAGE_CODE = language_code
                
                # Guardar en la sesión para futuras peticiones
                request.session['django_language'] = language_code
                
                logger.debug(f"Idioma activado: {language_code}")
            
        except Exception as e:
            logger.error(f"Error en LanguageMiddleware: {str(e)}")
            # En caso de error, usar idioma por defecto
            activate('es')
            request.LANGUAGE_CODE = 'es'
    
    def process_response(self, request, response):
        """
        Procesar la respuesta para agregar headers de idioma
        """
        try:
            current_language = getattr(request, 'LANGUAGE_CODE', get_language())
            
            # Agregar header de idioma actual
            response['Content-Language'] = current_language
            
            # Agregar cookie de idioma (si no existe o es diferente)
            if request.COOKIES.get('django_language') != current_language:
                response.set_cookie(
                    'django_language',
                    current_language,
                    max_age=365 * 24 * 60 * 60,  # 1 año
                    httponly=False,  # Permitir acceso desde JavaScript
                    samesite='Lax'
                )
            
            # Agregar headers para SEO multiidioma
            response['Vary'] = 'Accept-Language'
            
        except Exception as e:
            logger.error(f"Error procesando respuesta en LanguageMiddleware: {str(e)}")
        
        return response


class RTLLanguageMiddleware(MiddlewareMixin):
    """
    Middleware para manejar idiomas RTL (Right-to-Left)
    """
    
    RTL_LANGUAGES = ['ar', 'he', 'fa', 'ur']  # Árabe, Hebreo, Persa, Urdu
    
    def process_request(self, request):
        """
        Detectar si el idioma actual es RTL
        """
        try:
            current_language = getattr(request, 'LANGUAGE_CODE', get_language())
            request.IS_RTL = current_language in self.RTL_LANGUAGES
            
            if request.IS_RTL:
                logger.info(f"Idioma RTL detectado: {current_language}")
                
        except Exception as e:
            logger.error(f"Error en RTLLanguageMiddleware: {str(e)}")
            request.IS_RTL = False
    
    def process_response(self, request, response):
        """
        Agregar información RTL a la respuesta
        """
        try:
            if hasattr(request, 'IS_RTL') and request.IS_RTL:
                # Agregar header personalizado para RTL
                response['X-Text-Direction'] = 'rtl'
            else:
                response['X-Text-Direction'] = 'ltr'
                
        except Exception as e:
            logger.error(f"Error procesando respuesta RTL: {str(e)}")
        
        return response


class LanguageRedirectMiddleware(MiddlewareMixin):
    """
    Middleware para redireccionar a URLs con prefijo de idioma
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def process_request(self, request):
        """
        Procesar redirecciones de idioma si es necesario
        """
        try:
            # Solo procesar si está habilitado en settings
            if not getattr(settings, 'USE_I18N_URLS', False):
                return None
            
            path = request.path_info
            
            # Verificar si la URL ya tiene prefijo de idioma
            path_parts = path.strip('/').split('/')
            if path_parts and len(path_parts[0]) == 2:
                # Podría ser un código de idioma
                potential_lang = path_parts[0].lower()
                supported_languages = [
                    'es', 'en', 'gn', 'pt', 'ja', 'ru', 'ko', 'fr', 'de', 'it',
                    'zh', 'ar', 'hi', 'tr', 'nl', 'sv', 'no', 'da', 'fi', 'pl'
                ]
                
                if potential_lang in supported_languages:
                    # La URL ya tiene prefijo de idioma
                    activate(potential_lang)
                    request.LANGUAGE_CODE = potential_lang
                    return None
            
            # Si llegamos aquí, la URL no tiene prefijo de idioma
            # Podríamos redirigir, pero por ahora solo activamos el idioma detectado
            
        except Exception as e:
            logger.error(f"Error en LanguageRedirectMiddleware: {str(e)}")
        
        return None


class LanguageStatsMiddleware(MiddlewareMixin):
    """
    Middleware para recopilar estadísticas de uso de idiomas
    """
    
    def process_request(self, request):
        """
        Registrar estadísticas de uso de idiomas
        """
        try:
            current_language = getattr(request, 'LANGUAGE_CODE', get_language())
            
            # Incrementar contador en caché (si está disponible)
            from django.core.cache import cache
            
            cache_key = f'language_stats_{current_language}'
            current_count = cache.get(cache_key, 0)
            cache.set(cache_key, current_count + 1, timeout=86400)  # 24 horas
            
            # Registrar en logs para análisis posterior
            logger.info(f"Idioma utilizado: {current_language} - IP: {request.META.get('REMOTE_ADDR', 'unknown')}")
            
        except Exception as e:
            logger.error(f"Error en LanguageStatsMiddleware: {str(e)}")


# Context processor para agregar información de idioma a todos los templates
def language_context_processor(request):
    """
    Context processor para agregar información de idioma a todos los templates
    """
    try:
        current_language = getattr(request, 'LANGUAGE_CODE', get_language())
        is_rtl = getattr(request, 'IS_RTL', False)
        
        # Información del idioma actual
        language_info = {
            'es': {'name': 'Español', 'native_name': 'Español', 'flag': '🇪🇸'},
            'en': {'name': 'English', 'native_name': 'English', 'flag': '🇺🇸'},
            'gn': {'name': 'Guaraní', 'native_name': 'Avañe\'ẽ', 'flag': '🇵🇾'},
            'pt': {'name': 'Português', 'native_name': 'Português', 'flag': '🇧🇷'},
            'ja': {'name': 'Japanese', 'native_name': '日本語', 'flag': '🇯🇵'},
            'ru': {'name': 'Russian', 'native_name': 'Русский', 'flag': '🇷🇺'},
            'ko': {'name': 'Korean', 'native_name': '한국어', 'flag': '🇰🇷'},
            'fr': {'name': 'French', 'native_name': 'Français', 'flag': '🇫🇷'},
            'de': {'name': 'German', 'native_name': 'Deutsch', 'flag': '🇩🇪'},
            'it': {'name': 'Italian', 'native_name': 'Italiano', 'flag': '🇮🇹'},
            'zh': {'name': 'Chinese', 'native_name': '中文', 'flag': '🇨🇳'},
            'ar': {'name': 'Arabic', 'native_name': 'العربية', 'flag': '🇸🇦'},
            'hi': {'name': 'Hindi', 'native_name': 'हिन्दी', 'flag': '🇮🇳'},
        }
        
        current_lang_info = language_info.get(current_language, language_info['es'])
        
        return {
            'CURRENT_LANGUAGE_CODE': current_language,
            'CURRENT_LANGUAGE_INFO': current_lang_info,
            'IS_RTL_LANGUAGE': is_rtl,
            'LANGUAGE_DIRECTION': 'rtl' if is_rtl else 'ltr',
            'SUPPORTED_LANGUAGES_COUNT': len(language_info),
        }
        
    except Exception as e:
        logger.error(f"Error en language_context_processor: {str(e)}")
        return {
            'CURRENT_LANGUAGE_CODE': 'es',
            'CURRENT_LANGUAGE_INFO': {'name': 'Español', 'native_name': 'Español', 'flag': '🇪🇸'},
            'IS_RTL_LANGUAGE': False,
            'LANGUAGE_DIRECTION': 'ltr',
            'SUPPORTED_LANGUAGES_COUNT': 25,
        }