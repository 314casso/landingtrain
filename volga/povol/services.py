# -*- coding: utf-8 -*-
import datetime
import os
from volga.settings import MEDIA_ROOT
import unicodecsv as csv
from django.utils.translation import ugettext as _
import requests
from requests_ntlm import HttpNtlmAuth
from volga.local_settings import CRM_API
import urlparse
from django.utils.encoding import force_unicode


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
                    u'прием заявок': _("Booking are open"),
                    u'прием заявок завершен': _("Booking are closed"),
                    u'отправлен': _("Dispatched out"),
                    u'прибыл': _("Has arrived"),
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


def add_lead(data):
    session = requests.Session()
    login = '{domain}\\{login}'.format(**CRM_API)
    session.auth = HttpNtlmAuth(login, CRM_API['password'], session)
    url =  urlparse.urljoin(CRM_API['url'], 'leads') 
    values = {
            'subject':  u'Запрос по услуге Поволжский экспресс',
            'emailaddress1': data['email'],
            'lastname': data['name'],
            'telephone1': data['phone'],
            'description': u'%s' % data['message'],
            'leadsourcecode': 100000004,
            'ownerid@odata.bind': "/teams(8d10cfd9-b06e-e611-80c8-00505693217d)",
              }
    r = session.post(url, json=values)
    return r