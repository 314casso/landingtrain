# -*- coding: utf-8 -*-
from django import template
import datetime
import random
from django.utils.safestring import mark_safe
from django.core.urlresolvers import resolve, reverse
from django.utils.translation import activate, get_language


register = template.Library()
    
   
@register.simple_tag
def get_copyright():
    return u'© 1997—%s' % datetime.datetime.now().year


@register.filter()
def human_lang(lang):
    mapper = {'en': u'Eng', 'ru': u'Рус'}
    return mapper[lang]


def encode_string(value):
    """
    Encode a string into it's equivalent html entity.
    
    The tag will randomly choose to represent the character as a hex digit or
    decimal digit.
    """    
    e_string = "" 
    for a in value:
        t = random.randint(0,1)
        if t:
            en = "&#x%x;" % ord(a)
        else:
            en = "&#%d;" % ord(a)
        e_string += en 
    return e_string


@register.filter()
def hide_email(email):    
    name = email
    mailto_link = u'<a href="mai\'+\'lto:%s">%s</a>' % (encode_string(email), encode_string(name))

    value = '<script type="text/javascript">// <![CDATA['+"\n \
           \tdocument.write('%s')\n \
           \t// ]]></script>\n" % (mailto_link)
    return mark_safe(value)


@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, *args, **kwargs):
    """
    Get active page's url by a specified language
    Usage: {% change_lang 'en' %}
    """

    path = context['request'].path
    url_parts = resolve( path )

    url = path
    cur_language = get_language()
    try:
        activate(lang)
        url = reverse( url_parts.view_name, kwargs=url_parts.kwargs )
    finally:
        activate(cur_language)


    return "%s" % url