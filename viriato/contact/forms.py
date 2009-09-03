# -*- coding: utf-8 -*-
from django.forms import ModelForm
from contact.models import Company, Person, Contact, Email, Phone, Website, Address, InstantMessaging
from django.contrib.contenttypes.generic import generic_inlineformset_factory
from django.forms.formsets import formset_factory

class PersonForm(ModelForm):
    class Meta:
        model = Person

class CompanyForm(ModelForm):
    class Meta:
        model = Company

class EmailForm(ModelForm):
    class Meta:
        model = Email
        exclude = ("content_type_id","object_id")


class SearchForm(ModelForm):
    pass

EmailFormSet = generic_inlineformset_factory(Email, extra=1)
PhoneFormSet = generic_inlineformset_factory(Phone, extra=1)
InstantMessagingFormSet = generic_inlineformset_factory(InstantMessaging, extra=1)
AddressFormSet = generic_inlineformset_factory(Address, extra=1)
WebsiteFormSet = generic_inlineformset_factory(Website, extra=1)
