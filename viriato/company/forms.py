# -*- coding: utf-8 -*-
from django.forms.models import inlineformset_factory
from django import forms
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from company.models import *

class MyCompanyForm(ModelForm):

    class Meta:
        model = MyCompany


emails_formset = inlineformset_factory(
                                        MyCompany,
                                        Email,
                                        extra=1,
                                    )


addresses_formset = inlineformset_factory(
                                        MyCompany,
                                        Address,
                                        extra=1,
                                    )


phones_formset = inlineformset_factory(
                                        MyCompany,
                                        Phone,
                                        extra=1,
                                    )


websites_formset = inlineformset_factory(
                                        MyCompany,
                                        Website,
                                        extra=1,
                                    )


ims_formset = inlineformset_factory(
                                        MyCompany,
                                        InstantMessaging,
                                        extra=1,
                                    )

contact_types_formset = modelformset_factory(
                                        ContactTypes,
                                    )