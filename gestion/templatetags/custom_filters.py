from django import template
register = template.Library()

@register.filter(name='format_phone')
def format_phone(value):
    if not value: return ''
    phone = str(value).strip()
    return phone  # Por ahora, retornar el valor sin formatear
