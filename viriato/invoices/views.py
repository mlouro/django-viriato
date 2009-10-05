# -*- coding: utf-8 -*-
# invoices
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.utils.translation import ugettext as _

from receipt.models import *
from contract.models import *

@login_required
def index(request):
    receipts = Receipt.objects.order_by('creation_date').reverse()[:10]
    contracts = Contract.objects.order_by('date').reverse()[:10]
    return render_to_response ("invoices/index.html",
                                {
                                    'receipts': receipts,
                                    'contracts': contracts,
                                },
                                context_instance=RequestContext(request)
                            )

