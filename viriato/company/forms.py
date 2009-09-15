# -*- coding: utf-8 -*-
from django.contrib.contenttypes.generic import generic_inlineformset_factory
from django.forms.formsets import formset_factory
from django import forms
from django.forms import ModelForm

from company.models import *

class MyCompanyForm(ModelForm):

    class Meta:
        model = MyCompany
