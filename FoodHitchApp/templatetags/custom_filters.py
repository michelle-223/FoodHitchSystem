from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Return the value for the key from the dictionary, or None if not found."""
    return dictionary.get(key)
