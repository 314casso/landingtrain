# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils.encoding import force_unicode
import datetime
import os
from volga.settings import MEDIA_ROOT
import unicodecsv as csv
from django.utils.translation import ugettext as _

# Create your views here.

def landing(request):    
    movements_data = get_movements_data()    
    context = {
        'title': force_unicode('Рускон'),
        'movements_data': movements_data,
    }    
    return render(request, 'landing.html', context)

def get_movements_data():
    RECORDS = 10        
    filename = os.path.join(MEDIA_ROOT, 'data', 'datalink.csv')
    fh = open(filename, "r")
    dict_reader = csv.DictReader(fh)    
    key_mapper = {
                   u'Статус': 'status', 
                   u'Номер поезда': 'train_number',
                   u'Место отправления': 'place_of_departure',
                   u'Дата отправления': 'departure_date',
                   u'Место назначения': 'destination',
                   u'Дата прибытия': 'date_of_arrival',              
                 }
    
    data_keys = ('departure_date', 'date_of_arrival')
    
    data_trans = {
                    u'прием заявок': _("Accepting applications"),
                    u'отправлен': _("Sent"),
                    u'прибыл': _("Arrived"),
                    u'новороссийск': _("Novorossiysk"),
                    u'тольятти': _("Togliatti"),                    
                  }
    
    result = []
    for line in dict_reader:
        newline = {}
        for key, value in line.iteritems():
            newkey = key_mapper[key]                                     
            if newkey in data_keys:
                newline[newkey] = datetime.datetime.strptime(value, "%d.%m.%Y").date()
            else:
                key_trans = force_unicode(value).lower()
                newline[newkey] = data_trans[key_trans] if key_trans in data_trans else value 
        result.append(newline)
    
    result.reverse()  
    return result[:RECORDS]     