# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from apps.core.models import BaseModel, BaseBuilding, BaseCompareData, Developer
from apps.mo.models import MO
from apps.imgfile.models import File, Image

class Ground(BaseBuilding, BaseCompareData):

    class Meta:
        app_label = "build"
        verbose_name = _(u"Земальный участок")
    def __unicode__(self):
        return '%s' % self.id

    cad_passport = models.ForeignKey(File, help_text=_(u"Выписка из кадастрового паспорта"), null=True, verbose_name=_(u"Выписка из кадастрового паспорта"), blank=True, related_name='cad_passport')
    developer = models.ForeignKey(Developer, help_text=_(u"Застройщик (владелец) объекта"), null=True, verbose_name=_(u"Застройщик (владелец) объекта"), blank=True, )
    # contract = models.ForeignKey(Contract, help_text=_(u"Заключенный контракт"), null=True, verbose_name=_(u"Заключенный контракт"), blank=True, )
    cad_num = models.CharField(help_text=_(u"Адрес или кадастровый номер участка"), null=True, max_length=2048, verbose_name=_(u"Адрес или кадастровый номер участка"), blank=True, )
    start_date = models.DateField(help_text=_(u"Предполагаемый срок начала строительства"), null=True, verbose_name=_(u"Предполагаемый срок начала строительства"), blank=True, )
    finish_date = models.DateField(help_text=_(u"Предполагаемый срок окончания строительства"), null=True, verbose_name=_(u"Предполагаемый срок окончания строительства"), blank=True, )
    mo = models.ForeignKey(MO, help_text=_(u"Муниципальное образование"),
        verbose_name=_(u"Муниципальное образование"), )


class Building(BaseBuilding, BaseCompareData):

    class Meta:
        app_label = "build"
        verbose_name = "Building"
    def __unicode__(self):
        return '%s' % self.id

    developer = models.ForeignKey(Developer, help_text=_(u"Застройщик (владелец) объекта"),
        verbose_name=_(u"Застройщик (владелец) объекта"), )
    mo = models.ForeignKey(MO, help_text=_(u"Муниципальное образование"),
        verbose_name=_(u"Муниципальное образование"), )
