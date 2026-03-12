from django import template

register = template.Library()

@register.filter
def splitlines(value):
    """Split text by newlines and return a list."""
    if not value:
        return []
    return value.splitlines()

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key."""
    return dictionary.get(key)

@register.filter
def subtract(value, arg):
    """Subtract arg from value."""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0
