# -*- coding: utf-8 -*-
# Contract
from contract.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
import datetime
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect
from contract.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
from contract.forms import *
import datetime
from django.http import HttpResponseRedirect
from company.models import MyCompany
from django.core import serializers
from receipt.models import ReceiptDetails
from django.db.models import Sum

#Corrigidos
from projects.models.milestone import Milestone
from settings import INSTALLED_APPS


if 'projects' in INSTALLED_APPS:
    project = True
else:
    project = False


def index(request):
    receipts = Receipt.objects.all()
    return render_to_response ("/invoices/index.html",
                                {'receipts': receipts, },
                                context_instance=RequestContext(request)
                            )

#@login_required
def contract(request, object_id=0):

    try:
        my_company = MyCompany.objects.get(pk=1)
        tax = my_company.tax
        retention = my_company.retention
    except:
        tax = 0
        retention = 0

    if request.method == "POST":

        if object_id:
            contract = Contract.objects.get(pk=object_id)
            template_to_go = "edit_contract.html"
        else:
            contract = Contract()
            template_to_go = "new_contract.html"

        contract_form = ContractForm(request.POST, prefix="con", instance=contract)
        formset = contract_details_formset(
            request.POST,
            request.FILES,
            instance = contract,
            prefix = "details",
        )

        if contract_form.is_valid() and formset.is_valid():
            new_contract = contract_form.save()
            formset.save()
            new_contract.calculate() #Total's calculation

        else:
            return render_to_response ("invoices/" + template_to_go,
                                    {
                                        'formset': formset,
                                        'contract_form': contract_form,
                                        'tax': tax,
                                        'retention': retention,
                                        'contract': contract,
                                        'PROJECT': project,
                                        'approved': contract.approved,
                                    },
                                    context_instance=RequestContext(request)
        )


        #return HttpResponseRedirect('/invoices/contracts')#Atention: New destination needed
        return redirect (contract)


    elif object_id:
        contract = Contract.objects.get(pk=object_id)
        contract_form = ContractForm(instance=contract, prefix="con")
        formset = contract_details_formset(instance=contract, prefix="details")

        return render_to_response ("invoices/edit_contract.html",
                                    {
                                        'contract_form': contract_form,
                                        'formset': formset,
                                        'tax': tax,
                                        'retention': retention,
                                        'contract': contract,
                                        'PROJECT': project,
                                        'approved': contract.approved,
                                    },
                                    context_instance=RequestContext(request)
                                )

    else:
        contract_form = ContractForm(prefix='con')
        formset = contract_details_formset(instance=Contract(), prefix="details")

        return render_to_response ("invoices/new_contract.html",
                                    {
                                        'contract_form': contract_form,
                                        'formset': formset,
                                        'tax': tax,
                                        'retention': retention,
                                        'PROJECT': project,
                                        'approved': False,
                                    },
                                    context_instance=RequestContext(request)
                                )


def project_ajax(request):
    """
        Ajax Request to be used in Project's project
        If it's possible to relate projects with companys, should be used a filter to get the results from Project
    """
    company_id = request.POST['company_id']
    if company_id:
        #If there is a project_id then insert a filter
        data = serializers.serialize('json', Project.objects.all(), ensure_ascii=False)
    else:
        data = serializers.serialize('json', Project.objects.all(), ensure_ascii=False)
    return HttpResponse(data, mimetype='text/javascript')


def milestone_ajax(request):
    """
        Ajax Request to be used in Project's project
        If it's possible to relate projects with companys, should be used a filter to get the results from Project
    """
    project_id = request.POST['project_id']
    data = serializers.serialize('json', Milestone.objects.filter(project=project_id), ensure_ascii=False)
    return HttpResponse(data, mimetype='text/javascript')


def contracts_ajax(request):
    #filter(approved=True)
    data = serializers.serialize('json', Contract.objects.filter(approved=True), ensure_ascii=False)
    return HttpResponse(data, mimetype='text/javascript')


def contract_details_ajax(request):
    contract_id = request.POST['contract_id']
    data = serializers.serialize('json', ContractDetails.objects.filter(contract=contract_id, payed=False), ensure_ascii=False)
    return HttpResponse(data, mimetype='text/javascript')


def contract_detail_line_ajax(request):
    selected_items = list(request.POST['selected_items'].split('|'))
    data = serializers.serialize('json', ContractDetails.objects.filter(pk__in=selected_items), ensure_ascii=False)
    return HttpResponse(data, mimetype='text/javascript')


def get_contract_inf(request):
    id = request.POST['id']
    data = serializers.serialize('json', Contract.objects.filter(pk=id), ensure_ascii=False)
    return HttpResponse(data, mimetype='text/javascript')


def new_contract_items(request):
    from django.db.models import Q
    from django import forms

    existing_ids = request.POST['existing_ids']
    contract_id = request.POST['contract_id']
    ids = list(existing_ids.split('|'))

    data = serializers.serialize('json', ContractDetails.objects.filter(~Q(pk__in=ids), contract=contract_id, payed=False), ensure_ascii=False)
    return HttpResponse(data, mimetype='text/javascript')