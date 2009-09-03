# -*- coding: utf-8 -*-
from django.contrib.contenttypes.generic import generic_inlineformset_factory
from django.forms.formsets import formset_factory
from django import forms
from django.forms import ModelForm

from company.models import *


class CompanyDataForm(forms.Form):
    name = forms.CharField(max_length=100)
    tax_value = forms.DecimalField(required=False)
    retention_value = forms.DecimalField(required=False)
    fiscal_number = forms.IntegerField()
    address = forms.CharField(max_length=200)
    phone = forms.IntegerField(required=False)
    
    
class MyCompanyForm(ModelForm):
    
    class Meta:
        model = MyCompany
   