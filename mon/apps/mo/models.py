# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from apps.core.models import BaseName, BaseBudget, BaseSubvention, BaseDepartamentAgreement, BaseOrphan, \
    CREATION_FORM_CHOICES
from apps.imgfile.models import File, Image


class RegionalBudget(BaseBudget, ):

    class Meta:
        app_label = "mo"
        verbose_name = "RegionalBudget"
    def __unicode__(self):
        return '%s' % self.id


class FederalBudget(BaseBudget, ):

    class Meta:
        app_label = "mo"
        verbose_name = "FederalBudget"
    def __unicode__(self):
        return '%s' % self.id


class Subvention(BaseSubvention, ):

    class Meta:
        app_label = "mo"
        verbose_name = "Subvention"
    def __unicode__(self):
        return '%s' % self.id

    fed_budget = models.ForeignKey(FederalBudget, help_text=_(u"Федеральный бюджет"), verbose_name=_(u"Федеральный бюджет"), )
    reg_budget = models.ForeignKey(RegionalBudget, help_text=_(u"Краевой бюджет"), verbose_name=_(u"Краевой бюджет"), )


class MO(BaseName, ):

    class Meta:
        app_label = "mo"
        verbose_name = "MO"
    def __unicode__(self):
        return '%s' % self.id

    creation_form = models.IntegerField(blank=True, null=True, choices=CREATION_FORM_CHOICES , )


class DepartamentAgreement(BaseDepartamentAgreement, ):

    class Meta:
        app_label = "mo"
        verbose_name = "DepartamentAgreement"
    def __unicode__(self):
        return '%s' % self.id

    mo = models.ForeignKey(MO, help_text=_(u"Наименование муниципального образования"), verbose_name=_(u"Наименование муниципального образования"), )
    subvention = models.ForeignKey(Subvention, help_text=_(u"Субвенция"), verbose_name=_(u"Субвенция"), )



class Orphan(BaseOrphan, ):

    class Meta:
        app_label = "mo"
        verbose_name = "Orphan"
    def __unicode__(self):
        return '%s' % self.id


class PeopleAmount(models.Model):

    class Meta:
        app_label = "mo"
        verbose_name = "PeopleAmount"
    def __unicode__(self):
        return '%s' % self.id

    privilege_people = models.IntegerField(null=True, blank=True, )
    unhome_orphan = models.IntegerField(null=True, blank=True, )