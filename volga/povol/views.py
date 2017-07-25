# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils.encoding import force_unicode
from povol.services import get_movements_data, add_lead
from povol.forms import Feedback
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.utils.translation import ugettext as _


# Create your views here.

def landing(request):    
    movements_data = get_movements_data    
    context = {
        'title': force_unicode('Рускон'),
        'movements_data': movements_data,
    }   
    return render(request, 'landing.html', context)


@csrf_exempt
def feedback(request):
    form = Feedback(request.POST)
    if form.is_valid():
        add_lead(form.cleaned_data)
        return JsonResponse({'status': True})
    error_list = []
    for key, value in form.errors.iteritems():
        label = u'%s' % form[key].label 
        errors = u' ,'.join(value)
        error_list.append(u'%s: %s' % (label, errors))        
    return JsonResponse({'errors': '<br>'.join(error_list), 'status': False}, safe=False) 


# class zJvK0lo5EAE19EM9IsodLN44KABh6N4L:
#     ERROR = 0
#     def GET(self):
#         return u'Error, please use post request'
#     def POST(self):
#         form = web2lead()
#         if not form.validates():
#             return self.ERROR
#         else:
#             # form.d.boe and form['boe'].value are equivalent ways of
#             # extracting the validated arguments from the form.
#             try:
#                 add_lead(form.d.name, form.d.email, form.d.message)
#                 return 1
#             except:
#                 return self.ERROR

   