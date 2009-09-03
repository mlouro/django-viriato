# -*- coding: utf-8 -*-
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from company.forms import *
from contact.forms import EmailFormSet, PhoneFormSet, InstantMessagingFormSet, AddressFormSet, WebsiteFormSet
from company.models import MyCompany
from contact.models import Company
from django.forms.models import modelformset_factory
from django.core import serializers



def company(request):

    try:
        company = MyCompany.objects.get(pk=1)
    except:
        company = MyCompany()

    if request.POST:

        company_form = MyCompanyForm(request.POST, instance=company)

        formset_list = {
                    'email_formset' : EmailFormSet(instance=company, data=request.POST),
                    'phone_formset' : PhoneFormSet(instance=company, data=request.POST),
                    'im_formset' : InstantMessagingFormSet(instance=company, data=request.POST),
                    'address_formset' : AddressFormSet(instance=company, data=request.POST),
                    'website_formset' : WebsiteFormSet(instance=company, data=request.POST),
                }

        if company_form.is_valid():
            company_form.save()

            for formset in formset_list:
                if formset_list[formset].is_valid():
                    formset_list[formset].save()
                    formset_list[formset] = type(formset_list[formset])(instance=company)
                else:
                    return render_to_response (
                                    "invoice/company.html",
                                    {
                                        "form": company_form,
                                        'formsets' : formset_list,
                                    },
                                    context_instance = RequestContext(request)
                                    )

            return render_to_response (
                                        "invoice/company.html",
                                        {
                                            "form": company_form,
                                            'formsets' : formset_list,
                                        },
                                        context_instance = RequestContext(request)
                                    )

        else:
            return render_to_response (
                                    "invoice/company.html",
                                    {
                                        "form": company_form,
                                        'formsets' : formset_list,
                                    },
                                    context_instance = RequestContext(request)
                                    )
    else:
        formset_list = {'email_formset' : EmailFormSet(instance=company),
                    'phone_formset' : PhoneFormSet(instance=company),
                    'im_formset' : InstantMessagingFormSet(instance=company),
                    'address_formset' : AddressFormSet(instance=company),
                    'website_formset' : WebsiteFormSet(instance=company),}

        company_form = MyCompanyForm(instance=company)
        return render_to_response (
                                    "invoice/company.html",
                                    {
                                        "form": company_form,
                                        'formsets' : formset_list,
                                    },
                                    context_instance = RequestContext(request)
                                    )

def company_ajax(request):
    """ Ajax Request """
    data = serializers.serialize('json', Company.objects.all(), ensure_ascii=False)
    return HttpResponse(data, mimetype='text/javascript')

