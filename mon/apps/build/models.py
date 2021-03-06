# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import date
from django.db import models
from django.utils.translation import ugettext as _
from apps.core.models import BaseDocumentModel, BaseBuilding, BaseCompareData, BaseContract, \
    Developer, CREATION_FORM_CHOICES, BUDGET_CHOICES, STATE_CHOICES
from apps.mo.models import MO
from apps.imgfile.models import File, BaseFile, BaseFile
from apps.user.models import CustomUser
from django.forms.models import model_to_dict


class ContractDocuments(BaseDocumentModel, BaseFile):

    class Meta:
        app_label = "build"
        verbose_name = "Contract Documents"
    def __unicode__(self):
        return '%s' % self.id

    mun_contracts = models.FileField(null=True, blank=True, upload_to='img_files', help_text=_(u"Муниципальные контракты с приложениями"),
        verbose_name=_(u"Муниципальные контракты с приложениями."), )

    def to_list(self):
        attrs = deepcopy(self.__dict__)
        l = [getattr(self, k[:-3]) for k in attrs if k and '_id' in k and getattr(self, k[:-3])]
        return l

    def has_at_least_one_doc(self):
        attrs = deepcopy(self.__dict__)
        for k in attrs:
            if k and not '_id' in k and getattr(self, k) and \
               isinstance(getattr(self, k), models.fields.files.FieldFile):
                return True
        return False


class Contract(BaseContract):

    class Meta:
        app_label = "build"
        verbose_name = "Contract"
    def __unicode__(self):
        return '%s' % self.num

    developer = models.ForeignKey(Developer, help_text=_(u"Поставщик"), verbose_name=_(u"Поставщик"), null=True, blank=True, )
    summa = models.FloatField(help_text=_(u"Сумма заключенного контракта, всего, руб."), null=True, verbose_name=_(u"Сумма заключенного контракта, всего, руб."), blank=False, )
    summa_fed = models.FloatField(help_text=_(u"Сумма федеральных средств, руб."), null=True, verbose_name=_(u"Сумма федеральных средств, руб."), blank=False, )
    summa_reg = models.FloatField(help_text=_(u"Сумма краевых средств, руб."), null=True, verbose_name=_(u"Сумма краевых средств, руб."), blank=False, )
    summ_mo_money = models.FloatField(help_text=_(u"Сумма муниципальных средств, включенных в сумму контракта, руб."), null=True,
        verbose_name=_(u"Сумма муниципальных средств, включенных в сумму контракта, руб."), blank=False, )
    summ_without_mo_money = models.FloatField(help_text=_(u"Сумма заключенного контракта без учета средств МО, руб."), null=True,
        verbose_name=_(u"Сумма заключенного контракта без учета средств МО, руб."), blank=False, )
    date = models.DateField(help_text=_(u"Дата заключения контракта"), null=True, verbose_name=_(u"Дата заключения контракта"), blank=False, )
    period_of_payment = models.CharField(max_length=2048, help_text=_(u"Срок оплаты по условиям контракта"), null=True, verbose_name=_(u"Срок оплаты по условиям контракта"), blank=False, )
    creation_form = models.SmallIntegerField(help_text=_(u"Форма создания специализированного жилого фонда для детей-сирот"),
        verbose_name=_(u"Форма создания специализированного жилого фонда для детей-сирот"),
        blank=False, null=True, choices=CREATION_FORM_CHOICES)
    mo = models.ForeignKey(MO, help_text=_(u"Муниципальное образование"), verbose_name=_(u"Муниципальное образование"), )
    docs = models.ForeignKey(ContractDocuments, null=True, blank=True, help_text=_(u"Контрактная документация"), verbose_name=_(u"Контрактная документация"), )
    address = models.TextField(help_text=u"Адрес", verbose_name=u"Адрес", null=True, blank=False)
    flats_amount = models.IntegerField(help_text=_(u"Количество жилых помещений"), null=True, verbose_name=_(u"Количество жилых помещений"), blank=True, )
    area = models.FloatField(help_text=_(u"Общая площадь (кв. м)"), null=True, verbose_name=_(u"Общая площадь (кв. м)"), blank=False, )
    check_result_info = models.FileField(null=True, blank=True, upload_to='img_files', help_text=_(u"Информация по результатам проверки"),
                                     verbose_name=_(u"Информация по результатам проверки"), )


class CopyContract(BaseContract):
    developer = models.ForeignKey(Developer, help_text=_(u"Поставщик"), verbose_name=_(u"Поставщик"), null=True, blank=True, )
    summa = models.FloatField(help_text=_(u"Сумма заключенного контракта, всего, руб."), null=True, verbose_name=_(u"Сумма заключенного контракта, всего, руб."), blank=False, )
    summa_fed = models.FloatField(help_text=_(u"Сумма федеральных средств, руб."), null=True, verbose_name=_(u"Сумма федеральных средств, руб."), blank=False, )
    summa_reg = models.FloatField(help_text=_(u"Сумма краевых средств, руб."), null=True, verbose_name=_(u"Сумма краевых средств, руб."), blank=False, )
    summ_mo_money = models.FloatField(help_text=_(u"Сумма муниципальных средств, включенных в сумму контракта, руб."), null=True,
                                      verbose_name=_(u"Сумма муниципальных средств, включенных в сумму контракта, руб."), blank=False, )
    summ_without_mo_money = models.FloatField(help_text=_(u"Сумма заключенного контракта без учета средств МО, руб."), null=True,
                                              verbose_name=_(u"Сумма заключенного контракта без учета средств МО, руб."), blank=False, )
    date = models.DateField(help_text=_(u"Дата заключения контракта"), null=True, verbose_name=_(u"Дата заключения контракта"), blank=False, )
    period_of_payment = models.CharField(max_length=2048, help_text=_(u"Срок оплаты по условиям контракта"), null=True, verbose_name=_(u"Срок оплаты по условиям контракта"), blank=False, )
    creation_form = models.SmallIntegerField(help_text=_(u"Форма создания специализированного жилого фонда для детей-сирот"),
                                             verbose_name=_(u"Форма создания специализированного жилого фонда для детей-сирот"),
                                             blank=False, null=True, choices=CREATION_FORM_CHOICES)
    mo = models.ForeignKey(MO, help_text=_(u"Муниципальное образование"), verbose_name=_(u"Муниципальное образование"), )
    docs = models.ForeignKey(ContractDocuments, null=True, blank=True, help_text=_(u"Контрактная документация"), verbose_name=_(u"Контрактная документация"), )
    address = models.TextField(help_text=u"Адрес", verbose_name=u"Адрес", null=True, blank=False)
    flats_amount = models.IntegerField(help_text=_(u"Количество жилых помещений"), null=True, verbose_name=_(u"Количество жилых помещений"), blank=True, )
    area = models.FloatField(help_text=_(u"Общая площадь (кв. м)"), null=True, verbose_name=_(u"Общая площадь (кв. м)"), blank=False, )
    check_result_info = models.FileField(null=True, blank=True, upload_to='img_files', help_text=_(u"Информация по результатам проверки"),
                                         verbose_name=_(u"Информация по результатам проверки"), )

    class Meta:
        app_label = "build"
        verbose_name = _(u"Типовой контракт")

    def __unicode__(self):
        if not self.num:
            return ""
        return "%s" % self.num


class Ground(BaseBuilding, BaseCompareData, BaseFile):

    class Meta:
        app_label = "build"
        verbose_name = _(u"Земельный участок")

    def __unicode__(self):
        name = self.cad_num if self.cad_num else self.address
        return "%s" % name

    cad_num = models.CharField(help_text=_(u"Кадастровый номер участка"), unique=True, db_index=True, max_length=2048, verbose_name=_(u"Кадастровый номер участка"))
    cad_sum = models.FloatField(help_text=_(u"Кадастровая стоимость, руб."), null=True, verbose_name=_(u"Кадастровая стоимость, руб."), blank=True, )
    developer = models.ForeignKey(Developer, on_delete=models.SET_NULL, help_text=_(u"Застройщик (владелец) объекта"), null=True, verbose_name=_(u"Застройщик (владелец) объекта"), blank=True, )
    mo = models.ForeignKey(MO, help_text=_(u"Муниципальное образование"), verbose_name=_(u"Муниципальное образование"),)
    contract = models.ForeignKey(Contract, blank=True, null=True, help_text=_(u"Данные заключенного контракта"), verbose_name=_(u"Данные заключенного контракта"), )

    start_date = models.DateField(help_text=_(u"Предполагаемый срок начала строительства"), null=True, verbose_name=_(u"Предполагаемый срок начала строительства"), blank=True, )
    finish_date = models.DateField(help_text=_(u"Предполагаемый срок окончания строительства"), null=True, verbose_name=_(u"Предполагаемый срок окончания строительства"), blank=True, )


class Building(BaseBuilding, BaseCompareData, BaseFile):
    cad_num = models.CharField(help_text=_(u"Кадастровый номер"), db_index=True, max_length=2048, verbose_name=_(u"Кадастровый номер"), blank=False, null=True)
    cad_sum = models.FloatField(help_text=_(u"Кадастровая стоимость, руб."), null=True, verbose_name=_(u"Кадастровая стоимость, руб."), blank=True, )
    developer = models.ForeignKey(Developer, on_delete=models.SET_NULL, blank=True, null=True, help_text=_(u"Застройщик (владелец) объекта"), verbose_name=_(u"Застройщик (владелец) объекта"))
    mo = models.ForeignKey(MO, help_text=_(u"Муниципальное образование"), verbose_name=_(u"Муниципальное образование"), )
    contract = models.ForeignKey(Contract, blank=True, null=True, help_text=_(u"Данные заключенного контракта"), verbose_name=_(u"Данные заключенного контракта"), )

    flat_num = models.IntegerField(null=True, blank=True, help_text=u"Номер жилого помещения", verbose_name=u"Номер жилого помещения")
    driveway_num = models.IntegerField(null=True, blank=True, help_text=u"Подъезд", verbose_name=u"Подъезд")

    class Meta:
        app_label = "build"
        verbose_name = _(u"Строение")

    def __unicode__(self):
        if not self.address:
            return ""
        try:
            num = str(self.flat_num)
        except TypeError:
            num = ""
        address = ', '.join([self.address, num])
        return "%s" % address


class CopyBuilding(BaseBuilding, BaseCompareData, BaseFile):
    cad_num = models.CharField(help_text=_(u"Кадастровый номер"), null=True, max_length=2048, verbose_name=_(u"Кадастровый номер"), blank=True, )
    cad_sum = models.FloatField(help_text=_(u"Кадастровая стоимость, руб."), null=True, verbose_name=_(u"Кадастровая стоимость, руб."), blank=True, )
    developer = models.ForeignKey(Developer, on_delete=models.SET_NULL, blank=True, null=True, help_text=_(u"Застройщик (владелец) объекта"), verbose_name=_(u"Застройщик (владелец) объекта"))
    mo = models.ForeignKey(MO, help_text=_(u"Муниципальное образование"), blank=True, null=True, verbose_name=_(u"Муниципальное образование"), )
    contract = models.ForeignKey(Contract, blank=False, null=True, help_text=_(u"Данные заключенного контракта"), verbose_name=_(u"Данные заключенного контракта"), )

    flat_num = models.IntegerField(null=True, blank=True, help_text=u"Номер жилого помещения", verbose_name=u"Номер жилого помещения")
    driveway_num = models.IntegerField(null=True, blank=True, help_text=u"Подъезд", verbose_name=u"Подъезд")

    class Meta:
        app_label = "build"
        verbose_name = _(u"Типовое строение")

    def __unicode__(self):
        if not self.address:
            return ""
        return "%s" % self.address
