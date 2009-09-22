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

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from cStringIO import StringIO
from reportlab.lib import colors
from reportlab.platypus.flowables import Image


from receipt.models import *
from receipt.forms import *
from contract.models import *

from django.utils.translation import ugettext as _
from django.core.mail import send_mail

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
def receipt(request, object_id=0):

    print project

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
    buffer = StringIO()
    pdf = SimpleDocTemplate(buffer, pagesize = letter)
    pdf.build(create_document(object_id))
    response.write(buffer.getvalue())
    return response


def send_document(request, object_id):
    receipt = Receipt.objects.get(pk=object_id)
    if not receipt.sent:
        receipt.mark_as_sent()

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=receipt%s.pdf' % (object_id)
    buffer = StringIO()
    pdf = SimpleDocTemplate(buffer, pagesize = letter)
    pdf.build(create_document(object_id))
    response.write(buffer.getvalue())




    return response


def create_document(object_id):


    styleSheet = getSampleStyleSheet()
    style = styleSheet['BodyText']

    style = getSampleStyleSheet()

    content = []

#RLmap = Image(mapimg,width=23*inch,height=34*inch)
#RLmap.hAlign = "CENTER"
#RLmap.drawOn(c1,0.5*inch,0.5*inch)

    receipt = Receipt.objects.get(pk=object_id)

    my_company = MyCompany.objects.get(pk=1)
    logo = Image('static/%s' % (str(my_company.photo)), width=50, height=50)
    logo.hAlign = "RIGHT"
    content.append(logo)

    s1 = _('<b>Company</b>')
    s2 = my_company.title
    p = Paragraph('%s: %s' % (s1, s2), style["Normal"])
    content.append(p)

    content.append(Spacer(inch * .5, inch * .5))

    client = receipt.
    s1 = _('Client')

    p = Paragraph('', style["Normal"])
    content.append(p)
    content.append(Spacer(inch * .2, inch * .2))

    p = Paragraph('<u>Testando sublinhado</u>', style["Normal"])
    content.append(p)
    content.append(Spacer(inch * .2, inch * .2))

    document_details = []

    table_header = ['Description', 'Quantity', 'Unity Cost', 'Impact Value', 'Tax', 'Tax Value', 'Retention', 'Retention Value', 'Total']
    document_details.append(table_header)

    for rd in ReceiptDetails.objects.filter(receipt=object_id):
        new_data = [rd.description, rd.quantity, rd.unity_cost, rd.total_impact_value, rd.tax, rd.tax_value, rd.retention, rd.retention_value, rd.total]
        document_details.append(new_data)

    ts = [('ALIGN', (1,1), (-1,-1), 'CENTER'),
    ('LINEABOVE', (0,0), (-1,0), 1, colors.purple),
    ('LINEBELOW', (0,0), (-1,0), 1, colors.purple),
    ('FONT', (0,0), (-1,0), 'Times-Bold'),

    # The bottom row has one line above, and three lines below of
    # various colors and spacing.
    ('LINEABOVE', (0,-1), (-1,-1), 1, colors.purple),
    ('LINEBELOW', (0,-1), (-1,-1), 0.5, colors.purple,
      1, None, None, 4,1),
    ('LINEBELOW', (0,-1), (-1,-1), 1, colors.red),
    ('FONT', (0,-1), (-1,-1), 'Times-Bold')]

    table_footer = ['Totals', ' ', ' ', receipt.total_impact_value, ' ', receipt.total_tax_value, ' ',receipt.total_retention_value, receipt.total]
    document_details.append(table_footer)

    table = Table(document_details, style=ts)
    content.append(table)

    return content
