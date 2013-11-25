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

    developer = models.ForeignKey(Developer, help_text=_(u"ФИО и должность руководителя"), null=True, verbose_name=_(u"ФИО и должность руководителя"), blank=True, )
    building = models.ForeignKey(Building, help_text=_(u"Строение"), null=True, verbose_name=_(u"Строение"), blank=True, )
    ground = models.ForeignKey(Ground, help_text=_(u"Земельный участок"), null=True, verbose_name=_(u"Земельный участок"), blank=True, )
    summa = models.IntegerField(help_text=_(u"Сумма заключенного контракта"), null=True, verbose_name=_(u"Сумма заключенного контракта"), blank=True, )
    sign_date = models.DateField(help_text=_(u"Дата заключения контракта"), null=True, verbose_name=_(u"Дата заключения контракта"), blank=True, )



class Person(models.Model):

    class Meta:
        app_label = "cmp"
        verbose_name = "Person"
    def __unicode__(self):
        return '%s' % self.id

    birth_date = models.DateField(help_text=_(u"Дата рождения"), null=True, verbose_name=_(u"Дата рождения"), blank=True, )
    name = models.CharField(help_text=_(u"ФИО"), null=True, max_length=2048, verbose_name=_(u"ФИО"), blank=True, )
    position = models.CharField(help_text=_(u"Должность"), null=True, max_length=2048, verbose_name=_(u"Должность"), blank=True, )



class CompareData(BaseCompareData, ):

    class Meta:
        app_label = "cmp"
        verbose_name = "CompareData"
    def __unicode__(self):
        return '%s' % self.id

    result = models.ForeignKey(Result, help_text=_(u"Результат осмотра"), null=True, verbose_name=_(u"Результат осмотра"), blank=True, )
    cmp_date = models.DateTimeField(help_text=_(u"Дата последнего сравнения"), auto_now=True, null=True, verbose_name=_(u"Дата последнего сравнения"), blank=True, )



class Result(BaseResult, ):

    class Meta:
        app_label = "cmp"
        verbose_name = "Result"
    def __unicode__(self):
        return '%s' % self.id

    contract = models.ForeignKey(Contract, help_text=_(u"Реквизиты контракта"), null=True, verbose_name=_(u"Реквизиты контракта"), blank=True, )
    building = models.ForeignKey(Building, null=True, blank=True, )
    ground = models.ForeignKey(Ground, null=True, blank=True, )
    cmp_data = models.ForeignKey(CompareData, null=True, blank=True, )
    mo_pers = models.ForeignKey(Person, help_text=_(u"Участники от муниципального образования"), null=True, verbose_name=_(u"Участники от муниципального образования"), blank=True, )
    establish_pers = models.ForeignKey(Person, help_text=_(u"Участники комиссии от учреждения"), null=True, verbose_name=_(u"Участники комиссии от учреждения"), blank=True, )



class Auction(BaseContract, BaseCompareData,):

    class Meta:
        app_label = "cmp"
        verbose_name = "Auction"
    def __unicode__(self):
        return '%s' % self.id

    contract = models.ForeignKey(Contract, help_text=_(u"Данные по заключенному контракту"), null=True, verbose_name=_(u"Данные по заключенному контракту"), blank=True, )
    flat_amount = models.IntegerField(help_text=_(u"Количество квартир по номеру заказа"), null=True, verbose_name=_(u"Количество квартир по номеру заказа"), blank=True, )
    flat_area = models.IntegerField(help_text=_(u"Площадь квартир по номеру заказа"), null=True, verbose_name=_(u"Площадь квартир по номеру заказа"), blank=True, )
    start_price = models.FloatField(help_text=_(u"Начальная (максимальная) цена руб."), null=True, verbose_name=_(u"Начальная (максимальная) цена руб."), blank=True, )
    public_date = models.DateField(help_text=_(u"Дата размещения извещения о торгах (Дата опубликования заказа) дд.мм.гггг"), null=True, verbose_name=_(u"Дата размещения извещения о торгах (Дата опубликования заказа) дд.мм.гггг"), blank=True, )
    open_date = models.DateTimeField(help_text=_(u"Дата и время проведения открытого аукциона (последнего события при размещении заказа, при отмене размещения, либо завершении аукциона)"), auto_now=True, null=True, verbose_name=_(u"Дата и время проведения открытого аукциона (последнего события при размещении заказа, при отмене размещения, либо завершении аукциона)"), blank=True, )
    stage = models.IntegerField(help_text=_(u"Этап размещения заказа"), null=True, blank=True, verbose_name=_(u"Этап размещения заказа"), choices=STAGE_CHOICES , )

