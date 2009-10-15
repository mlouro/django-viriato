# -*- coding: utf-8 -*-
from django.template import Node, Library, TemplateSyntaxError, VariableDoesNotExist
from django.core.urlresolvers import reverse, resolve
from django.template.defaulttags import URLNode
from django.contrib.auth.decorators import user_passes_test

register = Library()

class LinkAllowedNode(Node):
    def __init__(self, url, name, permission):
        self.url = url
        self.permission = permission
        self.name = name


    def render(self, context):
        request = context['request']
        url = self.url.resolve(context)

        if self.permission and not request.user.has_perm(self.permission.resolve(context)):
            return ''

        import re
        if len(url) == 1:
            pattern = "^%s$" % url
        elif len(url) == 0:
            return ''
        else:
            pattern = "^%s" % url

        if re.match(pattern, request.path):
            return '<li><a href="%s" title="%s" class="active">%s</a></li>' % (url,self.name.resolve(context),self.name.resolve(context))
        return '<li><a href="%s" title="%s">%s</a></li>' % (url,self.name.resolve(context),self.name.resolve(context))


def get_link_if_allowed(parser, token):

    bits = token.split_contents()[1:]
    if len(bits) == 2:
        permission = ''
    elif len(bits) < 2 or len(bits) > 4:
        raise TemplateSyntaxError, "get_link_if_permssions tag takes two or three arguments {% get_link_if_allowed url title permission %}"
    else:
        permission = parser.compile_filter(bits[2])
    print bits[1]
    return LinkAllowedNode(parser.compile_filter(bits[0]),parser.compile_filter(bits[1]),permission)

get_link_if_allowed = register.tag(get_link_if_allowed)