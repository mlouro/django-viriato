# -*- coding: utf-8 -*-
# Contract
from django.db import models
from django.db.models import Sum
from settings import INSTALLED_APPS
from contact.models import Company
import datetime
from django.db.models import Sum

if "projects" in INSTALLED_APPS:
    from projects.models.project import Project


class Contract(models.Model):
    company = models.ForeignKey(Company)
    description = models.CharField(max_length=255)
    date = models.DateField(blank=True, null=True)
    total_impact_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_tax_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_retention_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    approved = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)

    if "projects" in INSTALLED_APPS:
        project = models.ForeignKey(Project, blank=True, null=True)
    else:
        project = models.IntegerField(blank=True, null=True)

    def get_absolute_url(self):
        return "/invoices/contract/%s/" % (self.id)

    def __unicode__(self):
        return "%s %s %s" % ( self.id, self.description, self.company)

    def save(self, force_insert=False, force_update=False):

        self.date = datetime.datetime.now()
        super(Contract, self).save(force_insert, force_update) # Call the "real" save() method.

    def calculate(self):
        contract = ContractDetails.objects.filter(contract=self.id)
        self.total_impact_value = contract.aggregate(Sum('impact_value'))['impact_value__sum']
        self.total_tax_value = contract.aggregate(Sum('tax_value'))['tax_value__sum']
        self.total_retention_value = contract.aggregate(Sum('retention_value'))['retention_value__sum']
        self.total = contract.aggregate(Sum('total'))['total__sum']
        try:
            self.total = self.total_impact_value + self.total_tax_value - self.total_retention_value
        except TypeError: # Preventing deletion of all bill details
            self.total_impact_value = 0
            self.total_tax_value = 0
            self.total_retention_value = 0
            self.total_bill = 0

        self.save()

    def to_pay(self):
        tot_payed = ContractDetails.objects.filter(contract=self.id).aggregate(Sum('total_payed'))['total_payed__sum']
        return self.total - tot_payed


class ContractDetails(models.Model):
    contract = models.ForeignKey(Contract)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unity_cost = models.DecimalField(max_digits=15, decimal_places=2)
    tax = models.DecimalField(max_digits=5, decimal_places=2)
    tax_value = models.DecimalField(max_digits=15, decimal_places=2)
    retention = models.DecimalField(max_digits=5, decimal_places=2)
    retention_value = models.DecimalField(max_digits=15, decimal_places=2)
    impact_value = models.DecimalField(max_digits=15, decimal_places=2)
    total = models.DecimalField(max_digits=15, decimal_places=2)
    total_payed = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    payed = models.BooleanField(default=False)


    def __unicode__(self):
        return self.description

    def save(self, force_insert=False, force_update=False):
        self.impact_value = self.unity_cost * self.quantity
        self.tax_value = self.impact_value * (self.tax/100)
        self.retention_value = self.impact_value * (self.retention/100)

        self.total = self.impact_value - self.retention_value + self.tax_value

        super(ContractDetails, self).save(force_insert, force_update) # Call the "real" save() method.
