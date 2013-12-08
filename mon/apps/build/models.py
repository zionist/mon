# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from apps.core.models import BaseModel, BaseBuilding, BaseCompareData, BaseContract, Developer
from apps.mo.models import MO
from apps.imgfile.models import File, Image


class Contract(BaseContract, BaseCompareData):

    class Meta:
        app_label = "cmp"
        verbose_name = "Contract"
    def __unicode__(self):
        return '%s' % self.id

    developer = models.ForeignKey(Developer, help_text=_(u"Застройщик"), null=True, verbose_name=_(u"Застройщик"), blank=True, )
    summa = models.IntegerField(help_text=_(u"Сумма заключенного контракта"), null=True, verbose_name=_(u"Сумма заключенного контракта"), blank=True, )
    sign_date = models.DateField(help_text=_(u"Дата заключения контракта"), null=True, verbose_name=_(u"Дата заключения контракта"), blank=True, )
    mo = models.ForeignKey(MO, help_text=_(u"Муниципальное образование"), verbose_name=_(u"Муниципальное образование"), )


class Ground(BaseBuilding, BaseCompareData):

    class Meta:
        app_label = "build"
        verbose_name = _(u"Земальный участок")

    def __unicode__(self):
        return self.cad_num

    cad_passport = models.ForeignKey(File, help_text=_(u"Выписка из кадастрового паспорта"), null=True, verbose_name=_(u"Выписка из кадастрового паспорта"), blank=True, related_name='cad_passport')
    developer = models.ForeignKey(Developer, help_text=_(u"Застройщик (владелец) объекта"), null=True, verbose_name=_(u"Застройщик (владелец) объекта"), blank=True, )
    cad_num = models.CharField(help_text=_(u"Адрес или кадастровый номер участка"), null=True, max_length=2048, verbose_name=_(u"Адрес или кадастровый номер участка"), blank=True, )
    start_date = models.DateField(help_text=_(u"Предполагаемый срок начала строительства"), null=True, verbose_name=_(u"Предполагаемый срок начала строительства"), blank=True, )
    finish_date = models.DateField(help_text=_(u"Предполагаемый срок окончания строительства"), null=True, verbose_name=_(u"Предполагаемый срок окончания строительства"), blank=True, )
    mo = models.ForeignKey(MO, help_text=_(u"Муниципальное образование"), verbose_name=_(u"Муниципальное образование"),)
    contract = models.ForeignKey(Contract, blank=True, null=True, help_text=_(u"Данные заключенного контракта"), verbose_name=_(u"Данные заключенного контракта"), )


class Building(BaseBuilding, BaseCompareData):

    class Meta:
        app_label = "build"
        verbose_name = _(u"Строение")

    def __unicode__(self):
        return "%s" % (self.address)

    offer = models.ForeignKey(File, help_text=_(u"Коммерческое предложение"), null=True, verbose_name=_(u"Коммерческое предложение"), blank=True, related_name='offer')
    permission = models.ForeignKey(File, help_text=_(u"Разрешение"), null=True, verbose_name=_(u"Разрешение"), blank=True, related_name='permission')
    developer = models.ForeignKey(Developer, help_text=_(u"Застройщик (владелец) объекта"),
                                  verbose_name=_(u"Застройщик (владелец) объекта"), )
    mo = models.ForeignKey(MO, help_text=_(u"Муниципальное образование"), verbose_name=_(u"Муниципальное образование"),)
    contract = models.ForeignKey(Contract, blank=True, null=True, help_text=_(u"Данные заключенного контракта"),
                                 verbose_name=_(u"Данные заключенного контракта"), )
