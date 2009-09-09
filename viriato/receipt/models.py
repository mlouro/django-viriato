# -*- coding: utf-8 -*-
# Receipt
from django.db import models
from django.db.models import Sum
from settings import INSTALLED_APPS
from contact.models import Company
from contract.models import Contract, ContractDetails
import datetime


if "projects" in INSTALLED_APPS:
    from projects.models.project import Project


class Receipt(models.Model):
    company = models.ForeignKey(Company)
    contract = models.ForeignKey(Contract, blank=True, null=True)
    description = models.CharField(max_length=255)
    creation_date = models.DateField(blank=True, null=True)
    total_impact_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_tax_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_retention_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    sent = models.BooleanField(default=False)
    sent_date = models.DateField(blank=True, null=True)

    if "projects" in INSTALLED_APPS:
        project = models.ForeignKey(Project, blank=True, null=True)
    else:
        project = models.IntegerField(blank=True, null=True)


    def get_absolute_url(self):
        return "/invoices/receipt/%s/" % (self.id)

    def __unicode__(self):
        return "%s - %s %s" % ( self.id, self.description, self.company)


    def save(self, force_insert=False, force_update=False):
        self.creation_date = datetime.datetime.now()
        super(Receipt, self).save(force_insert, force_update) # Call the "real" save() method.


    def calculate(self):
        receipt = ReceiptDetails.objects.filter(receipt=self.id)
        self.total_impact_value = receipt.aggregate(Sum('total'))['total__sum']
        self.total_tax_value = receipt.aggregate(Sum('tax_value'))['tax_value__sum']
        self.total_retention_value = receipt.aggregate(Sum('retention_value'))['retention_value__sum']
        try:
            self.total = self.total_impact_value + self.total_tax_value - self.total_retention_value
        except TypeError: # Preventing deletion of all details
            self.total_impact_value = 0
            self.total_tax_value = 0
            self.total_retention_value = 0
            self.total = 0

        self.save()


class ReceiptDetails(models.Model):
    receipt = models.ForeignKey(Receipt)
    contract_detail = models.ForeignKey(ContractDetails, null=True, blank=True)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0,)
    unity_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    retention = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    retention_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_impact_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    to_pay = models.DecimalField(max_digits=15, decimal_places=2, default=0)


    def __unicode__(self):
        return self.description

    def save(self, force_insert=False, force_update=False):
        self.total_impact_value = self.unity_cost * self.quantity
        self.tax_value = self.total_impact_value * (self.tax/100)
        self.retention_value = self.total_impact_value * (self.retention/100)

        self.total = self.total_impact_value - self.retention_value + self.tax_value

        if self.contract_detail != None:
            self.contract_detail.total_payed += self.to_pay

            if self.contract_detail.total_payed >= self.contract_detail.total:
                self.contract_detail.payed = True

            self.contract_detail.save()

            nr_of_details = ContractDetails.objects.filter(contract=self.receipt.contract.id).count()
            nr_of_payed = ContractDetails.objects.filter(payed=True, contract=self.receipt.contract.id).count()

            if nr_of_details == nr_of_payed:
                self.receipt.contract.finished = True
                self.receipt.contract.save()

        super(ReceiptDetails, self).save(force_insert, force_update) # Call the "real" save() method.