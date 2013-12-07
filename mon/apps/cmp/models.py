# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from django.utils.translation import ugettext as _
from apps.core.models import BaseModel, BaseBuilding, BaseCompareData, BaseContract, BaseResult, Developer, \
    Room, Hallway, WC, Kitchen, Developer, STAGE_CHOICES
from apps.imgfile.models import File, Image

from apps.core.models import Room, Hallway, WC, Kitchen
from apps.build.models import Building, Ground, Contract
from apps.mo.models import MO


class Person(models.Model):

    class Meta:
        app_label = "cmp"
        verbose_name = "Person"
    def __unicode__(self):
        return '%s, %s' % (self.name, self.position)

    birth_date = models.DateField(help_text=_(u"Дата рождения"), null=True, verbose_name=_(u"Дата рождения"), blank=True, )
    name = models.CharField(help_text=_(u"ФИО"), null=True, max_length=2048, verbose_name=_(u"ФИО"), blank=True, )
    email = models.EmailField(help_text=_(u"Адрес электронной почты"), null=True, max_length=100, verbose_name=_(u"Адрес электронной почты"), blank=True, )
    contact_phone = models.CharField(help_text=_(u"Номер телефона"), null=True, max_length=100, verbose_name=_(u"Номер телефона"), blank=True, )
    position = models.CharField(help_text=_(u"Должность"), null=True, max_length=2048, verbose_name=_(u"Должность"), blank=True, )


class CompareData(BaseCompareData, ):

    class Meta:
        app_label = "cmp"
        verbose_name = "CompareData"
    def __unicode__(self):
        return '%s' % self.id

    # result = models.ForeignKey(Result, help_text=_(u"Результат осмотра"), null=True, verbose_name=_(u"Результат осмотра"), blank=True, )
    cmp_date = models.DateTimeField(help_text=_(u"Дата последней проверки"), verbose_name=_(u"Дата последней проверки"), blank=True, default=datetime.now())


class Result(BaseResult, ):

    class Meta:
        app_label = "cmp"
        verbose_name = "Осмотр"
    def __unicode__(self):
        return '%s' % self.id

    contract = models.ForeignKey(Contract, help_text=_(u"Реквизиты контракта"), null=True, verbose_name=_(u"Реквизиты контракта"), blank=True, )
    building = models.ForeignKey(Building, null=True, blank=True, help_text=_(u"Осмотренное строение"), verbose_name=_(u"Осмотренное строение"))
    ground = models.ForeignKey(Ground, null=True, blank=True, help_text=_(u"Осмотренный земельный участок"), verbose_name=_(u"Осмотренный земельный участок"))
    cmp_data = models.ForeignKey(CompareData, null=True, blank=True, )
    mo_pers = models.ForeignKey(Person, help_text=_(u"Участники от муниципального образования"), null=True, verbose_name=_(u"Участники от муниципального образования"), blank=True, related_name='mo_pers')
    establish_pers = models.ForeignKey(Person, help_text=_(u"Участники комиссии от учреждения"), null=True, verbose_name=_(u"Участники комиссии от учреждения"), blank=True, related_name='establish_pers')


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
    mo = models.ForeignKey(MO, help_text=_(u"Муниципальное образование"), verbose_name=_(u"Муниципальное образование"), )
    proposal_count = models.IntegerField(help_text=_(u"Количество поданных заявок"), verbose_name=_(u"Количество поданных заявок"),
        blank=True, default=0)
