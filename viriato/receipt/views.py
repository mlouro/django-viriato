# -*- coding: utf-8 -*-
# Receipt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
import datetime
from company.models import MyCompany
from contact.models import *

from receipt.models import *
from receipt.forms import *
from contract.models import *

from django.utils.translation import ugettext as _
from django.core.mail import send_mail

from settings import INSTALLED_APPS

from reportlab.pdfgen import canvas
from cStringIO import StringIO
from invoices.pdf_gen import *
from invoices.sendmail import *
from invoices.common import *

if 'projects' in INSTALLED_APPS:
    project = True
else:
    project = False

def index(request):
    receipts = Receipt.objects.order_by('creation_date').reverse()
    return render_to_response ("invoices/receipt_index.html",
                                {'receipts': receipts, },
                                context_instance=RequestContext(request)
                            )

@login_required
def receipt(request, object_id=0):
    try:
        my_company = MyCompany.objects.get(pk=1)
        tax = my_company.tax
        retention = my_company.retention
    except:
        tax = 0
        retention = 0

    if request.method == "POST":

        if object_id:
            receipt = Receipt.objects.get(pk=object_id)
            template_to_go = "edit_receipt.html"
        else:
            receipt = Receipt()
            template_to_go = "new_receipt.html"

        receipt_form = ReceiptForm(request.POST, prefix="con", instance=receipt)
        formset = receipt_formset(request.POST, request.FILES, instance=receipt, prefix="details")

        if receipt_form.is_valid() and formset.is_valid():
            new_receipt = receipt_form.save()
            formset.save()
            new_receipt.calculate() #Total's calculation
            return redirect (receipt)
        else:
            not_editable = receipt.sent
            return render_to_response ("invoices/" + template_to_go,
                                            {
                                                'receipt': receipt,
                                                'formset': formset,
                                                'receipt_form': receipt_form,
                                                'tax': tax,
                                                'retention': retention,
                                                'there_are_errors': True,
                                                'PROJECT': project,
                                                'receipt_is_not_editable': not_editable,
                                            },
                                            context_instance=RequestContext(request)
                    )
    elif object_id:
        receipt = Receipt.objects.get(pk=object_id)
        receipt_form = ReceiptForm(instance=receipt, prefix="con")
        formset = receipt_formset(instance=receipt, prefix="details")
        not_editable = receipt.sent

        return render_to_response ("invoices/edit_receipt.html",
                                    {
                                        'receipt': receipt,
                                        'receipt_form': receipt_form,
                                        'formset': formset,
                                        'tax': tax,
                                        'retention': retention,
                                        'receipt_is_not_editable': not_editable,
                                        'PROJECT': project,
                                    },
                                    context_instance=RequestContext(request)
                                )

    else:
        receipt_form = ReceiptForm(prefix='con')
        formset = receipt_formset(instance=Receipt(), prefix="details")

        return render_to_response ("invoices/new_receipt.html",
                                    {
                                        'receipt_form': receipt_form,
                                        'formset': formset,
                                        'tax': tax,
                                        'retention': retention,
                                        'there_are_errors': False,
                                        'PROJECT': project,
                                    },
                                    context_instance=RequestContext(request)
                                )

def download_document(request, object_id):
    receipt = Receipt.objects.get(pk=object_id)
    if not receipt.sent:
        receipt.mark_as_sent()

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=receipt%s.pdf' % (object_id)
    c = canvas.Canvas(response)
    c = create_pdf(c, object_id)
    c.showPage()
    c.save()
    return response

def send_document(request, object_id):
    from settings import ROOT_DIR
    path = ROOT_DIR+'/viriato/static/tmp/'
    filename = 'receipt%s.pdf' % (object_id)
    file_path = ('%s%s'%(path,filename))

    receipt = Receipt.objects.get(pk=object_id)
    if not receipt.sent:
        receipt.mark_as_sent()

    c = canvas.Canvas(file_path)
    c = create_pdf(c, object_id)
    c.showPage()
    c.save()

    if sendmail(file_path, object_id, MyCompany.objects.get(pk=1).title):
        return HttpResponse("Hello, world. You're at the poll index.")
    else:
        return HttpResponse("false")


def create_pdf(c, object_id):
    my_company = MyCompany.objects.get(pk=1)
    set_states(c, author=my_company.title, title="My Receipt")
    create_header(c, my_company)
    create_footer(c, my_company)
    receipt = Receipt.objects.get(pk=object_id)
    receipt_details = ReceiptDetails.objects.filter(receipt=object_id)
    client = Company.objects.get(pk=receipt.company)

    table_header = [_('Description'),'','', '', '', _('Quantity'), _('Unity Cost'), _('Imp. Value'), _('Tax'), _('Tax Value'), _('Retention'), _('Ret. Value'), _('Total')]

    table_body = []
    for rd in receipt_details:
        new_data = [rd.description[:50],'','','','', rd.quantity, rd.unity_cost, rd.total_impact_value, rd.tax, rd.tax_value, rd.retention, rd.retention_value, rd.total]
        table_body.append (new_data)

    table_footer = [_('Totals'),'', ' ' ,'',' ', ' ', ' ', receipt.total_impact_value, ' ', receipt.total_tax_value, ' ',receipt.total_retention_value, receipt.total]

    create_doc_main(c, object_id, client)
    create_doc_details(c, table_header, table_body, table_footer)

    return c


def sendmail(file_path, object_id, company_title):
    host, pwd, from_user, server = get_email_data()

    to='costavitorino@gmail.com'
    subj=_('Receipt from %s' % (company_title))
    msg=_('Sending receipt number %s' % (object_id))

    answer = send_mail(send_from=from_user, send_to=to, subject=subj, text=msg, file_path=file_path, server=server, host=host, pwd=pwd)
    return answer