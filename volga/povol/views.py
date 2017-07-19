# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils.encoding import force_unicode

# Create your views here.

def landing(request):    
    context = {
        'title': force_unicode('Рускон'),
    }
    return render(request, 'landing.html', context)