# -*- coding: utf-8 -*-

from datetime import datetime
from copy import deepcopy
from django.db import models
from django.utils.translation import ugettext as _
from apps.core.models import BaseDocumentModel, BaseBuilding, BaseAuctionData, BaseCompareData, BaseContract, BaseResult, Developer,\
    ResultRoom, ResultHallway, ResultWC, ResultKitchen, Developer, STAGE_CHOICES, BaseAuction

from apps.build.models import Building, Ground, Contract
from apps.mo.models import MO
from apps.user.models import CustomUser


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

    cmp_date = models.DateTimeField(help_text=_(u"Дата последней проверки"), verbose_name=_(u"Дата последней проверки"), blank=True, default=datetime.now())


class Result(BaseResult, ):

    class Meta:
        app_label = "cmp"
        verbose_name = "Осмотр"
    def __unicode__(self):
        return '%s' % self.id

    contract = models.ForeignKey(Contract, help_text=_(u"Реквизиты контракта"), null=True, verbose_name=_(u"Реквизиты контракта"), blank=True, )
    building = models.ForeignKey(Building, null=True, blank=True, help_text=_(u"Осмотренное строение"), verbose_name=_(u"Осмотренное строение"))
    mo = models.ForeignKey(MO, null=True, blank=False, help_text=_(u"Муниципальное образование"), verbose_name=_(u"Муниципальное образование"), )
    ground = models.ForeignKey(Ground, null=True, blank=True, help_text=_(u"Осмотренный земельный участок"), verbose_name=_(u"Осмотренный земельный участок"))
    cmp_data = models.ForeignKey(CompareData, null=True, blank=True, )
    mo_pers = models.CharField(max_length=16384, help_text=_(u"Участники от муниципального образования"), null=True, verbose_name=_(u"Участники от муниципального образования"), blank=True)
    establish_pers = models.CharField(max_length=16384, help_text=_(u"Участники комиссии от учреждения"), null=True, verbose_name=_(u"Участники комиссии от учреждения"), blank=True)
    doc_files = models.FileField(null=True, blank=True, upload_to='img_files', help_text=_(u"Предоставленные документы"), verbose_name=_(u"Предоставленные документы"))


class Auction(BaseAuction, BaseAuctionData,):
    contract = models.ForeignKey(Contract, help_text=_(u"Данные по заключенному контракту"), null=True, verbose_name=_(u"Данные по заключенному контракту"), blank=True, )
    mo = models.ForeignKey(MO, help_text=_(u"Муниципальное образование"), verbose_name=_(u"Муниципальное образование"), )

    class Meta:
        app_label = "cmp"
        verbose_name = "Auction"

    def __unicode__(self):
        return '%s' % self.id

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d

class CopyAuction(BaseAuction, BaseAuctionData,):
    contract = models.ForeignKey(Contract, help_text=_(u"Данные по заключенному контракту"), null=True, verbose_name=_(u"Данные по заключенному контракту"), blank=True, )
    mo = models.ForeignKey(MO, help_text=_(u"Муниципальное образование"), verbose_name=_(u"Муниципальное образование"), )

    class Meta:
        app_label = "cmp"
        verbose_name = "CopyAuction"

    def __unicode__(self):
        return '%s' % self.id

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d
