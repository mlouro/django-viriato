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

from reportlab.pdfgen import canvas
from cStringIO import StringIO
from invoices.pdf_gen import *
from invoices.sendmail import *
from invoices.common import *

from django.utils.translation import ugettext as _
from invoices.decorators import have_company

if 'projects' in INSTALLED_APPS:
    project = True
else:
    project = False


@login_required
@have_company
def index(request):
    contracts = Contract.objects.order_by('date').reverse()
    return render_to_response ("invoices/contract_index.html",
                                {'contracts': contracts, },
                                context_instance=RequestContext(request)
                            )

@login_required
@have_company
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
            if contract.approved == False:
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
                                        'there_are_errors': True,
                                    },
                                    context_instance=RequestContext(request)
        )

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

@login_required
@have_company
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

@login_required
@have_company
def milestone_ajax(request):
    """
        Ajax Request to be used in Project's project
        If it's possible to relate projects with companys, should be used a filter to get the results from Project
    """
    project_id = request.POST['project_id']
    data = serializers.serialize('json', Milestone.objects.filter(project=project_id), ensure_ascii=False)
    return HttpResponse(data, mimetype='text/javascript')

@login_required
@have_company
def contracts_ajax(request):
    #filter(approved=True)
    data = serializers.serialize('json', Contract.objects.filter(approved=True, finished=False), ensure_ascii=False)
    return HttpResponse(data, mimetype='text/javascript')

@login_required
@have_company
def contract_details_ajax(request):
    contract_id = int(request.POST['contract_id'])
    if contract_id < 0:
        first_contract = Contract.objects.filter(approved=True, finished=False)[:1]
        data = serializers.serialize('json', ContractDetails.objects.filter(contract=first_contract[0].id), ensure_ascii=False)
    else:
        data = serializers.serialize('json', ContractDetails.objects.filter(contract=contract_id, payed=False), ensure_ascii=False)
    return HttpResponse(data, mimetype='text/javascript')

@login_required
@have_company
def contract_detail_line_ajax(request):
    selected_items = list(request.POST['selected_items'].split('|'))
    data = serializers.serialize('json', ContractDetails.objects.filter(pk__in=selected_items), ensure_ascii=False)
    return HttpResponse(data, mimetype='text/javascript')

@login_required
@have_company
def get_contract_inf(request):
    id = request.POST['id']
    data = serializers.serialize('json', Contract.objects.filter(pk=id), ensure_ascii=False)
    return HttpResponse(data, mimetype='text/javascript')

@login_required
@have_company
def new_contract_items(request):
    from django.db.models import Q
    from django import forms

    existing_ids = request.POST['existing_ids']
    contract_id = request.POST['contract_id']
    ids = list(existing_ids.split('|'))

    data = serializers.serialize('json', ContractDetails.objects.filter(~Q(pk__in=ids), contract=contract_id, payed=False), ensure_ascii=False)
    return HttpResponse(data, mimetype='text/javascript')

@login_required
@have_company
def download_document(request, object_id):
    contract = Contract.objects.get(pk=object_id)

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=contract%s.pdf' % (object_id)
    c = canvas.Canvas(response)
    c = create_pdf(c, object_id)
    c.showPage()
    c.save()
    return response


def send_document(request, object_id):
    from settings import ROOT_DIR
    path = ROOT_DIR+'/viriato/static/tmp/'
    filename = 'contract%s.pdf' % (object_id)
    file_path = [('%s%s'%(path,filename)),]

    contract = Contract.objects.get(pk=object_id)

    c = canvas.Canvas(file_path[0])
    c = create_pdf(c, object_id)
    c.showPage()
    c.save()

    client = Company.objects.get(pk=contract.company)

    if sendmail(file_path, object_id, MyCompany.objects.get(pk=1), client):
        message=_('Contract sent with success!')
    else:
        message = _('Errors while sending the contract!')
    return render_to_response ("invoices/last_output.html",
                                    {
                                        'message': message,
                                    },
                                    context_instance=RequestContext(request)
                                )


def create_pdf(c, object_id):
    my_company = MyCompany.objects.get(pk=1)
    set_states(c, author=my_company.title, title="My Contract")
    create_header(c, my_company)
    create_footer(c, my_company)
    contract = Contract.objects.get(pk=object_id)
    contract_details = ContractDetails.objects.filter(contract=object_id)
    client = Company.objects.get(pk=contract.company)

    table_header = [_('Description'),'','', '', '', _('Quantity'), _('Unity Cost'), _('Imp. Value'), _('Tax'), _('Tax Value'), _('Retention'), _('Ret. Value'), _('Total')]

    table_body = []
    for rd in contract_details:
        new_data = [rd.description[:50],'','','','', rd.quantity, rd.unity_cost, rd.impact_value, rd.tax, rd.tax_value, rd.retention, rd.retention_value, rd.total]
        table_body.append (new_data)

    for rd in contract_details:
        new_data = [rd.description[:50],'','','','', rd.quantity, rd.unity_cost, rd.impact_value, rd.tax, rd.tax_value, rd.retention, rd.retention_value, rd.total]


    table_footer = [_('Totals'),'', ' ' ,'',' ', ' ', ' ', contract.total_impact_value, ' ', contract.total_tax_value, ' ',contract.total_retention_value, contract.total]

    create_doc_main(c, object_id, client, receipt=False)
    create_doc_details(c, table_header, table_body, table_footer)

    return c

def sendmail(file_path, object_id, company, client):
    host, pwd, from_user, server = get_email_data()

    length = len(str(client.emails.all()[:1]))
    to = str(client.emails.all()[:1])[9:length-2]

    subj=_('Contract from %s' % (company.title))
    msg=_('Sending contract number %s' % (object_id))

    answer = send_mail(send_from=from_user, send_to=to, subject=subj, text=msg, file_path=file_path, server=server, host=host, pwd=pwd)
    return answer