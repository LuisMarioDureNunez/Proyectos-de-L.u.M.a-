from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def guaranies(value):
    """
    Formatea un número como moneda paraguaya (Guaraníes)
    Ejemplo: 1500000 -> "Gs. 1.500.000"
    """
    try:
        if value is None or value == '':
            return "Gs. 0"
        
        # Convertir a Decimal para manejar correctamente los números
        if isinstance(value, str):
            value = Decimal(value)
        elif not isinstance(value, Decimal):
            value = Decimal(str(value))
        
        # Formatear con separadores de miles
        formatted = f"{value:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        return f"Gs. {formatted}"
    
    except (ValueError, TypeError, Exception):
        return "Gs. 0"

@register.filter
def multiply(value, arg):
    """Multiplica dos valores"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def div(value, arg):
    """Divide dos valores"""
    try:
        if float(arg) == 0:
            return 0
        return float(value) / float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def add(value, arg):
    """Suma dos valores"""
    try:
        return float(value) + float(arg)
    except (ValueError, TypeError):
        return 0