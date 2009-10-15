# -*- coding: utf-8 -*-
# Contract
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^/$', 'contract.views.index', name="contract_index"),
    url(r'^add/$', 'contract.views.contract', name="contract_add"),
    url(r'^download_document/(?P<object_id>\d+)/$', 'contract.views.download_document', name="download_document"),
    url(r'^send_document/(?P<object_id>\d+)/$', 'contract.views.send_document', name="send_document"),

    (r'^contracts_ajax/$', 'contract.views.contracts_ajax'),
    (r'^contract_details_ajax/$', 'contract.views.contract_details_ajax'),
    (r'^contract_detail_line_ajax/$', 'contract.views.contract_detail_line_ajax'),
    (r'^get_contract_inf/$', 'contract.views.get_contract_inf'),
    (r'^new_contract_items/$', 'contract.views.new_contract_items'),
    (r'^(?P<object_id>\d+)/$', 'contract.views.contract'),
    (r'^project_ajax/$', 'contract.views.project_ajax'),
    (r'^milestone_ajax/$', 'contract.views.milestone_ajax'),
)
