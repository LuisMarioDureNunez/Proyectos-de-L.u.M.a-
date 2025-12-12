from django import template

register = template.Library()

@register.filter(name='guaranies')
def formato_guaranies(value):
    """
    Convierte un número a formato de guaraníes
    """
    try:
        value = float(value)
        formatted = f"Gs. {value:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return formatted
    except (ValueError, TypeError):
        return f"Gs. {value}"

@register.filter(name='currency')
def currency(value):
    """
    Filtro alternativo para formato de moneda
    """
    return formato_guaranies(value)