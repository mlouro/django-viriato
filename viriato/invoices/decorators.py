# -*- coding: utf-8 -*-
from company.models import *
from django.http import HttpResponseRedirect


def have_company(fn):
    def _check(request, *args, **kwargs):
        try:
            company = MyCompany.objects.get(pk=1)
        except:
            return HttpResponseRedirect('/invoices/company/')

        return fn(request, *args, **kwargs)
    return _check
