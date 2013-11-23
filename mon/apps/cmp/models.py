# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from apps.core.models import BaseModel, BaseBuilding, BaseCompareData, BaseContract, BaseResult, Developer, \
    Room, Hallway, WC, Kitchen, Developer, STAGE_CHOICES
from apps.imgfile.models import File, Image
from apps.build.models import Building, Ground


class Contract(BaseContract, ):

    class Meta:
        app_label = "cmp"
        verbose_name = "Contract"
    def __unicode__(self):
        return '%s' % self.id

    developer = models.ForeignKey(Developer, help_text=_(u"ФИО и должность руководителя"), verbose_name=_(u"ФИО и должность руководителя"), )
    building = models.ForeignKey(Building, help_text=_(u"Строение"), verbose_name=_(u"Строение"), )
    ground = models.ForeignKey(Ground, help_text=_(u"Земельный участок"), verbose_name=_(u"Земельный участок"), )
    summa = models.IntegerField(null=True, blank=True, )
    sign_date = models.DateField(auto_now=True, null=True, blank=True, )


class Person(models.Model):

    class Meta:
        app_label = "cmp"
        verbose_name = "Person"
    def __unicode__(self):
        return '%s' % self.id

    name = models.CharField(help_text=_(u"ФИО"), null=True, max_length=2048, verbose_name=_(u"ФИО"), blank=True, )
    position = models.CharField(help_text=_(u"Должноть"), null=True, max_length=2048, verbose_name=_(u"Должноть"), blank=True, )
    birth_date = models.DateField(auto_now=False, null=True, blank=True, )


class CompareData(BaseCompareData, ):

    class Meta:
        app_label = "cmp"
        verbose_name = "CompareData"
    def __unicode__(self):
        return '%s' % self.id

    cmp_date = models.DateTimeField(auto_now=False, null=True, blank=True, )


class Result(BaseResult, ):

    class Meta:
        app_label = "cmp"
        verbose_name = "Result"
    def __unicode__(self):
        return '%s' % self.id

    contract = models.ForeignKey(Contract, help_text=_(u"Реквизиты контракта"), verbose_name=_(u"Реквизиты контракта"), )
    building = models.ForeignKey(Building, )
    ground = models.ForeignKey(Ground, )
    cmp_data = models.ForeignKey(CompareData, )
    mo_pers = models.ForeignKey(Person, related_name='mo_pers')
    establish_pers = models.ForeignKey(Person, related_name='establish_pers')


class Auction(BaseContract, BaseCompareData,):

    class Meta:
        app_label = "cmp"
        verbose_name = "Auction"
    def __unicode__(self):
        return '%s' % self.id

    contract = models.ForeignKey(Contract, help_text=_(u"Данные по заключенному контракту"),
        verbose_name=_(u"Данные по заключенному контракту"), )
    flat_amount = models.IntegerField(null=True, blank=True, )
    flat_area = models.IntegerField(null=True, blank=True, )
    start_price = models.FloatField(null=True, blank=True, )
    public_date = models.DateField(auto_now=True, null=True, blank=True, )
    open_date = models.DateTimeField(auto_now=True, null=True, blank=True, )
    stage = models.IntegerField(blank=True, null=True, choices=STAGE_CHOICES, )
