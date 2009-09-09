# -*- coding: utf-8 -*-
from django.forms import ModelForm
from contract.models import *
from django import forms
from settings import INSTALLED_APPS
from django.forms.models import inlineformset_factory

if 'django_project.project' in INSTALLED_APPS:
    from django_project.project.models import Project


class ContractForm(ModelForm):

    class Meta:
        model = Contract

        fields = (
                'description',
                'date',
                'company',
                'approved',
                'total_impact_value',
                'total_tax_value',
                'total_retention_value',
                'total',
        )

        if "projects" in INSTALLED_APPS:
            fields = fields + ('project',)


contract_details_formset = inlineformset_factory(
                                        Contract,
                                        ContractDetails,
                                        extra=1,
                                        fields=(
                                            'description',
                                            'quantity',
                                            'unity_cost',
                                            'tax',
                                            'retention',
                                            )
                                        )