# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from apps.core.models import BaseName, BaseBudget, BaseSubvention, BaseDepartamentAgreement, BaseOrphan, \
    CREATION_FORM_CHOICES

AGREEMENT_TYPE_CHOICES = ((0, _(u'Соглашение с министерством')), (1, _(u'Дополнительное соглашение с министерством')),
                           (2, _(u'Письмо о вычете средств')),)


class RegionalBudget(BaseBudget, ):

    class Meta:
        app_label = "mo"
        verbose_name = _(u"Краевой бюджет")

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

    def get_dep(self):
        if self.departamentagreement_set.all().exists():
            return self.departamentagreement_set.all()[0]
        return ' '

    def __unicode__(self):
        string = '%s' + _(u' по соглашению №') + '%s'
        return string % (self.amount, self.get_dep())

    fed_budget = models.ForeignKey(FederalBudget, help_text=_(u"Федеральный бюджет"), verbose_name=_(u"Федеральный бюджет"), blank=True, null=True, )
    reg_budget = models.ForeignKey(RegionalBudget, help_text=_(u"Краевой бюджет"), verbose_name=_(u"Краевой бюджет"), blank=True, null=True, )


class MO(models.Model):

    class Meta:
        app_label = "mo"
        verbose_name = _(u"Муниципальное образование")

    def __unicode__(self):
        return '%s' % self.name

    name = models.CharField(help_text=_(u"Наименование"), max_length=2048, verbose_name=_(u"Наименование"), unique=True)
    creation_form = models.CommaSeparatedIntegerField(max_length=24, help_text=_(u"Форма создания специализированного жилого фонда для детей-сирот"),
                                        verbose_name=_(u"Форма создания специализированного жилого фонда для детей-сирот"),
                                        blank=True, null=True, )
    has_trouble = models.NullBooleanField(blank=True, null=True, help_text=_(u"Есть замечания"), verbose_name=_(u"Есть замечания"))
    home_orphans = models.IntegerField(blank=True, default=0, help_text=_(u"Количество сирот, которым предоставлены жилые помещения"), verbose_name=_(u"Количество сирот, которым предоставлены жилые помещения"))
    common_economy = models.FloatField(blank=True, null=True, default=0, help_text=_(u"Общая эканомия по субвенциям"), verbose_name=_(u"Общая эканомия по субвенциям"))
    common_percentage = models.FloatField(blank=True, null=True, default=0, help_text=_(u"Общий процент освоения субвенции"), verbose_name=_(u"Общий процент освоения субвенции"))
    common_spent = models.FloatField(blank=True, null=True, default=0, help_text=_(u"Общая сумма потраченной субвенции"), verbose_name=_(u"Общая сумма потраченной субвенции"))
    common_amount = models.FloatField(blank=True, null=True, default=0, help_text=_(u"Общая сумма субвенции"), verbose_name=_(u"Общая сумма субвенции"))
    flats_amount = models.IntegerField(blank=True, null=True, default=0, help_text=_(u"Количество квартир по заключенным контрактам"), verbose_name=_(u"Количество квартир по заключенным контрактам"))


class DepartamentAgreement(BaseDepartamentAgreement, ):

    class Meta:
        app_label = "mo"
        verbose_name = _(u"Реквизиты соглашения с министерством")

    def __unicode__(self):
        return '%s' % self.num

#    flats_amount = models.IntegerField(blank=True, default=0, help_text=_(u"Количество выделенных квартир на текущий год"), verbose_name=_(u"Количество выделенных квартир на текущий год"))
    mo = models.ForeignKey(MO, blank=True, null=True, help_text=_(u"Наименование муниципального образования"), verbose_name=_(u"Наименование муниципального образования"), )
    subvention = models.ForeignKey(Subvention, blank=True, null=True, help_text=_(u"Субвенция"), verbose_name=_(u"Субвенция"), )
    agreement_type= models.SmallIntegerField(help_text=_(u"Тип соглашения"), blank=True, verbose_name=_(u"Тип соглашения"),
        choices=AGREEMENT_TYPE_CHOICES, default=0)


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
                                                    null=True, verbose_name=_(u"Численность не получивших жильё детей-сирот."), blank=True, )
    future_unhome_orphan = models.IntegerField(null=True, verbose_name=_(u"Численность не получивших жильё детей-сирот (по прогнозу)."), blank=True,
        help_text=_(u"ЧПрогнозируемая численность детей-сирот в возрасте от 18 до 23 лет и старше 23 лет, которые до "
                    u"1 января текущего года не реализовали свое право на получение жилого помещения "
                    u"в предыдущие годы (учитываются состоявшие и не состоявшие на льготном учете)."))
    queue_by_list = models.IntegerField(verbose_name=_(u"Очередь по списку (количество человек)"), null=True, blank=True,
        help_text=_(u"Очередь по списку (количество человек)"))
    future_queue_by_list = models.IntegerField(verbose_name=_(u"Очередь по прогнозу (количество человек)"), null=True, blank=True,
        help_text=_(u"Очередь по прогнозу (количество человек)"))
    unhome_orphan_14_18 = models.IntegerField(verbose_name=_(u"Кол-во несовершеннолетних от 14 до 18 (количество человек)"), null=True, blank=True,
        help_text=_(u"Кол-во несовершеннолетних от 14 до 18 (количество человек)"))
    future_unhome_orphan_14_18 = models.IntegerField(verbose_name=_(u"Кол-во несовершеннолетних от 14 до 18 по прогнозу (количество человек)"), null=True, blank=True,
        help_text=_(u"Кол-во несовершеннолетних от 14 до 18 по прогнозу (количество человек)"))
    deals = models.IntegerField(verbose_name=_(u"Кол-во учетных дел от 14 до 18, переданных в ГКУ КК КМЦ ОЖДС (%)"), null=True, blank=True,
        help_text=_(u"Кол-во учетных дел от 14 до 18 переданных муниципальным образованием в ГКУ КК КМЦ ОЖДС (% от прогнозной численности)"))
    recoverers = models.IntegerField(verbose_name=_(u"Взыскателей по исполнительным производствам (количество человек)"), null=True, blank=True,
        help_text=_(u"Взыскателей по исполнительным производствам (количество человек)"))

    mo = models.ForeignKey(MO, blank=True, null=True, help_text=_(u"Наименование муниципального образования"), verbose_name=_(u"Наименование муниципального образования"), )
