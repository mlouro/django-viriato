# -*- coding: utf-8 -*-
from company.models import MyCompany
from invoices.decorators import have_company
from django.contrib.auth.decorators import login_required


@login_required
@have_company
def get_email_data():
    company = MyCompany.objects.get(pk=1)
    host = company.host
    pwd = company.pwd
    from_user= company.from_user
    server = company.server

    #host = 'viriatoletter@gmail.com'
    #pwd = '<alexandre>'
    #from_user='viriatoletter@gmail.com'
    #server="smtp.gmail.com"

    return host, pwd, from_user, server