# math_filters.py - Filtros matemáticos personalizados para templates
from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplica el valor por el argumento"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def div(value, arg):
    """Divide el valor por el argumento"""
    try:
        if float(arg) == 0:
            return 0
        return float(value) / float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def add_percentage(value):
    """Convierte un valor decimal a porcentaje (multiplica por 100)"""
    try:
        return float(value) * 100
    except (ValueError, TypeError):
        return 0

@register.filter
def to_degrees(value):
    """Convierte un valor de 0-5 a grados de 0-360"""
    try:
        # Convierte calificación de 0-5 a grados de 0-360
        return (float(value) / 5.0) * 360
    except (ValueError, TypeError):
        return 0

@register.filter
def percentage_to_degrees(value):
    """Convierte porcentaje a grados"""
    try:
        return (float(value) / 100.0) * 360
    except (ValueError, TypeError):
        return 0

@register.filter
def rating_to_degrees(value):
    """Convierte calificación de 0-5 a grados para círculo de progreso"""
    try:
        # Calificación de 0-5 convertida a grados (0-360)
        rating = float(value)
        if rating > 5:
            rating = 5
        elif rating < 0:
            rating = 0
        return (rating / 5.0) * 360
    except (ValueError, TypeError):
        return 0

@register.filter
def subtract(value, arg):
    """Resta el argumento del valor"""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def abs_value(value):
    """Valor absoluto"""
    try:
        return abs(float(value))
    except (ValueError, TypeError):
        return 0

@register.filter
def round_to(value, decimals):
    """Redondea a un número específico de decimales"""
    try:
        return round(float(value), int(decimals))
    except (ValueError, TypeError):
        return 0

@register.filter
def format_guaranies(value):
    """Formatea un número como guaraníes paraguayos"""
    try:
        number = float(value)
        # Formato paraguayo: punto para miles, coma para decimales
        formatted = f"{number:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"Gs. {formatted}"
    except (ValueError, TypeError):
        return "Gs. 0"

@register.filter
def percentage_bar(value, max_value=5):
    """Convierte un valor a porcentaje para barras de progreso"""
    try:
        percentage = (float(value) / float(max_value)) * 100
        return min(100, max(0, percentage))
    except (ValueError, TypeError):
        return 0