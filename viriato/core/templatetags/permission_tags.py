# -*- coding: utf-8 -*-
# Navigation - currently active tab
from django import template

register = template.Library()

@register.simple_tag
def has_permission(request, pattern):
    import re
    print pattern
    if re.search(pattern, request.path):
        return 'class=\"active\"'
    return ''