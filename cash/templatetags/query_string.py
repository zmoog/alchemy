"""
requires
TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.request',)

Source: http://www.djangosnippets.org/snippets/1243/
"""


from django import template
from django.utils.http import urlquote

register = template.Library()

def do_get_string(parser, token):
   try:
       tag_name, key, value = token.split_contents()
#         key = urlquote(key)
#         value = urlquote(value)
   except ValueError:
       return GetStringNode()

   if not (key[0] == key[-1] and key[0] in ('"', "'")):
       raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name

   return GetStringNode(key[1:-1], value)

class GetStringNode(template.Node):
   def __init__(self, key=None, value=None):
       self.key = key
       if value:
           self.value = template.Variable(value)

   def render(self, context):
       get = context.get('request').GET.copy()

       if self.key:
           actual_value = self.value.resolve(context)
           get.__setitem__(self.key, actual_value)

       return get.urlencode()

register.tag('get_string', do_get_string)

