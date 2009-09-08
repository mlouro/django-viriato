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

from receipt.models import *
from receipt.forms import *
from contract.models import *


def index(request):
    receipts = Receipt.objects.all()
    return render_to_response ("/invoices/index.html",
                                {'receipts': receipts, },
                                context_instance=RequestContext(request)
                            )

#@login_required
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
        else:
            print receipt
            return render_to_response ("/invoices/" + template_to_go,
                                            {
                                                'receipt': receipt,
                                                'formset': formset,
                                                'receipt_form': receipt_form,
                                                'tax': tax,
                                                'retention': retention,
                                                'there_are_errors': True,
                                            },
                                            context_instance=RequestContext(request)
                    )

        return redirect (receipt)

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
                                    },
                                    context_instance=RequestContext(request)
                                )

def receipt_document(request, object_id):
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=somefilename22.pdf'

    style = getSampleStyleSheet()
    buffer = StringIO()
    pdf = SimpleDocTemplate(buffer, pagesize = letter)
    content = []

    receipt = Receipt.objects.get(pk=object_id)

    p = Paragraph('<b>Testando o negrsadsadsito</b>', style["Normal"])
    content.append(p)
    content.append(Spacer(inch * .2, inch * .2))

    p = Paragraph('<i>Testando o itálico</i>', style["Normal"])
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
#receipt = models.ForeignKey(Receipt)
    #contract_detail = models.ForeignKey(ContractDetails, null=True, blank=True)
    #description = models.CharField(max_length=255)
    #quantity = models.IntegerField(default=0,)
    #unity_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    #tax = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    #tax_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    #retention = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    #retention_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    #total_impact_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    #total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    #to_pay
    print content

    pdf.build(content)


    response.write(buffer.getvalue())
    return response