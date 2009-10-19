# -*- coding: utf-8 -*-
# Receipt
from django.forms import ModelForm
from receipt.models import *
from settings import INSTALLED_APPS
from django.forms.models import inlineformset_factory
from django import forms
from django.utils.translation import ugettext as _
from django.forms.util import ErrorList


if 'projects' in INSTALLED_APPS:
    from projects.models.project import Project


class ReceiptForm(ModelForm):
    contract = forms.ModelChoiceField(label="",
                                queryset=Contract.objects.all(),
                                widget=forms.HiddenInput,
                                required=False,
            )
    id = forms.CharField(
        widget=forms.HiddenInput,
        required = False,
    )

    class Meta:
        model = Receipt

        fields = (
                'id',
                'contract',
                'green_receipt',
                'description',
                'company',
                'total_impact_value',
                'total_tax_value',
                'total_retention_value',
                'total',
            )

        if "projects" in INSTALLED_APPS:
            fields = fields + ('project',)

    def clean(self):
        data = self.cleaned_data
        if Receipt.objects.filter( green_receipt = data["green_receipt"]):#.exclude(id = data["id"])
            msg = _(u"Green receipt already exists")
            self._errors["green_receipt"] = ErrorList([msg])
            del data["green_receipt"]

        return data

class ReceiptDetailsFormset(ModelForm):
    contract_detail = forms.ModelChoiceField(
                        queryset=ContractDetails.objects.all(),
                        widget=forms.HiddenInput,
                        required=False,
                    )
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'txt_description',}))
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'class':'txt_quantity',}))
    unity_cost = forms.DecimalField(max_digits=15, decimal_places=2, widget=forms.TextInput(attrs={'class':'txt_unity_cost',}))
    tax = forms.DecimalField(max_digits=15, decimal_places=2, widget=forms.TextInput(attrs={'class':'txt_tax',}))
    retention = forms.DecimalField(max_digits=15, decimal_places=2, widget=forms.TextInput(attrs={'class':'txt_retention',}))
    total = forms.DecimalField(max_digits=15, decimal_places=2, widget=forms.TextInput(attrs={'class':'txt_total', 'readonly':'true',}))
    to_pay = forms.DecimalField(max_digits=15, decimal_places=2, widget=forms.TextInput(attrs={'class':'txt_to_pay',}))
    total_payed = forms.DecimalField(max_digits=15, decimal_places=2,required=False, widget=forms.HiddenInput(attrs={'class':'txt_total_payed',}))

    class Meta:
        model = ReceiptDetails

        fields = (
            'description',
            'quantity',
            'unity_cost',
            'tax',
            'retention',
            'total',
            'to_pay',
            'total_payed',
            'contract_detail',
        )



receipt_formset = inlineformset_factory(
                                        Receipt,
                                        ReceiptDetails,
                                        extra=1,
                                        form = ReceiptDetailsFormset,
                                        )
