from django import forms
from django.utils.translation import ugettext as _


class Feedback(forms.Form):    
    name = forms.CharField(label=_("Name"))
    email = forms.EmailField(label=_("Email"))
    phone = forms.CharField(label=_("Phone No. (optionally)"), required=False)
    message = forms.CharField(label=_("Message"))