# -*- coding: utf-8 -*-
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from company.models import MyCompany
from contact.models import Company
from django.forms.models import modelformset_factory
from django.core import serializers
from company.forms import *
from invoices.decorators import have_company

@login_required
def company(request):
    try:
        company = MyCompany.objects.get(pk=1)
    except:
        company = MyCompany()

    if request.POST:

        company_form = MyCompanyForm(request.POST, instance=company)

        formset_list = {
            'email_formset' : emails_formset(instance=company, prefix='emails', data=request.POST),
            'phone_formset' : phones_formset(instance=company, prefix='phones', data=request.POST),
            'im_formset' : ims_formset(instance=company, prefix='ims', data=request.POST),
            'address_formset' : addresses_formset(instance=company, prefix='addresses', data=request.POST),
            'website_formset' : websites_formset(instance=company, prefix='websites', data=request.POST),
        }

        if company_form.is_valid():
            company_form.save()

            for formset in formset_list:
                if formset_list[formset].is_valid():
                    formset_list[formset].save()
                    formset_list[formset] = type(formset_list[formset])(instance=company)
                else:
                    return render_to_response (
                                    "invoices/company.html",
                                    {
                                        "form": company_form,
                                        'formsets' : formset_list,
                                        'there_are_errors': True,
                                    },
                                    context_instance = RequestContext(request)
                                    )

            return render_to_response (
                                        "invoices/company.html",
                                        {
                                            "form": company_form,
                                            'formsets' : formset_list,

                                        },
                                        context_instance = RequestContext(request)
                                    )

        else:
            return render_to_response (
                                    "invoices/company.html",
                                    {
                                        "form": company_form,
                                        'formsets' : formset_list,
                                        'there_are_errors': True,
                                    },
                                    context_instance = RequestContext(request)
                                    )
    else:
        formset_list = {
            'email_formset' : emails_formset(instance=company, prefix='emails'),
            'phone_formset' : phones_formset(instance=company, prefix='phones'),
            'im_formset' : ims_formset(instance=company, prefix='ims'),
            'address_formset' : addresses_formset(instance=company, prefix='addresses'),
            'website_formset' : websites_formset(instance=company, prefix='websites'),
        }

        company_form = MyCompanyForm(instance=company)
        return render_to_response (
                                    "invoices/company.html",
                                    {
                                        "form": company_form,
                                        'formsets' : formset_list,
                                    },
                                    context_instance = RequestContext(request)
                                    )
@login_required
@have_company
def company_ajax(request):
    """ Ajax Request """
    data = serializers.serialize('json', Company.objects.all(), ensure_ascii=False)
    return HttpResponse(data, mimetype='text/javascript')

