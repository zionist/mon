# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from apps.core.models import BaseName, BaseBudget, BaseSubvention, BaseDepartamentAgreement, BaseOrphan, \
    CREATION_FORM_CHOICES
from apps.imgfile.models import File, Image


class RegionalBudget(BaseBudget, ):

    class Meta:
        app_label = "mo"
        verbose_name = _(u"Региональный бюджет")

    def __unicode__(self):
        return '%s' % self.id


class FederalBudget(BaseBudget, ):

    class Meta:
        app_label = "mo"
        verbose_name = _(u"Федеральный бюджет")

    def __unicode__(self):
        return '%s' % self.id


class Subvention(BaseSubvention, ):

    class Meta:
        app_label = "mo"
        verbose_name = "Subvention"

    def __unicode__(self):
        return '%s' % self.id

    fed_budget = models.ForeignKey(FederalBudget, help_text=_(u"Федеральный бюджет"), verbose_name=_(u"Федеральный бюджет"), blank=True, null=True, )
    reg_budget = models.ForeignKey(RegionalBudget, help_text=_(u"Краевой бюджет"), verbose_name=_(u"Краевой бюджет"), blank=True, null=True, )


class MO(BaseName, ):

    class Meta:
        app_label = "mo"
        verbose_name = _(u"Муниципальное образование")

    def __unicode__(self):
        return '%s' % self.name

    creation_form = models.IntegerField(help_text=_(u"Форма создания специализированного жилого фонда для детей-сирот"),
                                        verbose_name=_(u"Форма создания специализированного жилого фонда для детей-сирот"),
                                        blank=True, null=True, choices=CREATION_FORM_CHOICES , )
    has_trouble = models.NullBooleanField(blank=True, help_text=_(u"Есть замечания"), verbose_name=_(u"Есть замечания"))
    home_orphans = models.IntegerField(blank=True, default=0, help_text=_(u"Количество сирот, которым предоставлены жилые помещения"), verbose_name=_(u"Количество сирот, которым предоставлены жилые помещения"))


class DepartamentAgreement(BaseDepartamentAgreement, ):

    class Meta:
        app_label = "mo"
        verbose_name = _(u"Реквизиты соглашения с министерством")

    def __unicode__(self):
        return '%s' % self.id

    mo = models.ForeignKey(MO, blank=True, null=True, help_text=_(u"Наименование муниципального образования"), verbose_name=_(u"Наименование муниципального образования"), )
    subvention = models.ForeignKey(Subvention, blank=True, null=True, help_text=_(u"Субвенция"), verbose_name=_(u"Субвенция"), )


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

    privilege_people = models.IntegerField(help_text=_(u"Численность граждан, состоящих на льготном учете, по состоянию на текущий год."), null=True, verbose_name=_(u"Численность граждан, состоящих на льготном учете, по состоянию на текущий год."), blank=True, )
    unhome_orphan = models.IntegerField(help_text=_(u"Численность детей-сирот в возрасте от 18 до 23 лет и старше 23 лет, которые до "
                                                    u"1 января текущего года не реализовали свое право на получение жилого помещения "
                                                    u"в предыдущие годы (учитываются состоявшие и не состоявшие на льготном учете)."),
        null=True, verbose_name=_(u"Численность детей-сирот."), blank=True, )
    mo = models.ForeignKey(MO, help_text=_(u"Наименование муниципального образования"), verbose_name=_(u"Наименование муниципального образования"), )
