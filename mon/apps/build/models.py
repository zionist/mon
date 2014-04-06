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

    protocols = models.FileField(null=True, blank=True, upload_to='img_files', help_text=_(u"Протоколы о подведении итогов торгов"),
        verbose_name=_(u"Протоколы о подведении итогов торгов"), )
    mun_contracts = models.FileField(null=True, blank=True, upload_to='img_files', help_text=_(u"Муниципальные контракты с приложениями"),
        verbose_name=_(u"Муниципальные контракты с приложениями."), )
    transmission_acts = models.FileField(null=True, blank=True, upload_to='img_files', help_text=_(u"Акты приема-передачи жилых помещений"),
        verbose_name=_(u"Акты приема-передачи жилых помещений"), )
    facility_permission = models.FileField(null=True, blank=True, upload_to='img_files', help_text=_(u"Разрешения на ввод объекта в эксплуатацию."),
        verbose_name=_(u"Разрешения на ввод объекта в эксплуатацию"), )
    land_right_stating = models.FileField(null=True, blank=True, upload_to='img_files', help_text=_(u"Правоустанавливающие документы на земельные участки"),
        verbose_name=_(u"Правоустанавливающие документы на земельные участки"), )
    building_permissions = models.FileField(null=True, blank=True, upload_to='img_files', help_text=_(u"Разрешения на строительство"),
        verbose_name=_(u"Разрешения на строительство"), )
    acceptance_acts = models.FileField(null=True, blank=True, upload_to='img_files', help_text=_(u"Акты о приемке выполненных работ (форма № КС-2)"),
        verbose_name=_(u"Акты о приемке выполненных работ (форма № КС-2)"), )
    cost_infos = models.FileField(null=True, blank=True, upload_to='img_files', help_text=_(u"Справки о стоимости выполненных работ и затрат (форма № КС-3)"),
        verbose_name=_(u"Справки о стоимости выполненных работ и затрат (форма № КС-3)"), )
    mo_certificate = models.FileField(null=True, blank=True, upload_to='img_files',
                                       help_text=_(u"Свидетельство о регистрации права собственности муниципального образования на жилое помещение"),
                                       verbose_name=_(u"Свидетельство о регистрации права собственности МО на жилое помещение"), )
    mun_act_to_fond = models.FileField(null=True, blank=True, upload_to='img_files',
                                        help_text=_(u"Муниципальный акт о включении приобретенного/построенного жилья в специализированный жилищный фонд для детей-сирот."),
                                        verbose_name=_(u"Муниципальный акт о включении жилья в спец. жил. фонд."), )
    tec_passport_tec_plan = models.FileField(null=True, blank=True, upload_to='img_files',
                                              help_text=_(u"Технический паспорт, технический план."),
                                              verbose_name=_(u"Технический паспорт, технический план."), )
    photos = models.FileField(null=True, blank=True, upload_to='img_files', help_text=_(u"Фотографии приобретенных жилых помещений."),
                               verbose_name=_(u"Фотографии приобретенных жилых помещений."), )
    mo_notice_to_citizen = models.FileField(null=True, blank=True, upload_to='img_files',
                                             help_text=_(u"Извещение от муниципального образования в адрес гражданина о предоставлении последнему жилого помещения."),
                                             verbose_name=_(u"Извещение от МО о предоставлении жилого помещения."), )
    approval_citizen_statement = models.FileField(null=True, blank=True, upload_to='img_files',
                                                   help_text=_(u"Заявление от гражданина о согласии в предоставлении жилого помещения."),
                                                   verbose_name=_(u"Заявление от гражданина о согласии в предоставлении жилого помещения."), )
    hiring_contract = models.FileField(null=True, blank=True, upload_to='img_files',
                                        help_text=_(u"Договор найма специализированного жилого помещения на каждого гражданина."),
                                        verbose_name=_(u"Договор найма специализированного жилого помещения на каждого гражданина."), )

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


class Contract(BaseContract, BaseCompareData):

    class Meta:
        app_label = "build"
        verbose_name = "Contract"
    def __unicode__(self):
        return '%s' % self.num

    developer = models.ForeignKey(Developer, help_text=_(u"Застройщик/Владелец"), verbose_name=_(u"Застройщик/Владелец"), null=True, blank=True, )
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
    budget = models.SmallIntegerField(help_text=u"Бюджет", verbose_name=u"Бюджет", null=True, blank=False, choices=BUDGET_CHOICES)


class CopyContract(BaseContract, BaseCompareData):
    developer = models.ForeignKey(Developer, help_text=_(u"Застройщик"), verbose_name=_(u"Застройщик"), null=True, blank=True, )
    summa = models.FloatField(help_text=_(u"Сумма заключенного контракта, всего, руб."), null=True, verbose_name=_(u"Сумма заключенного контракта, всего, руб."), blank=True, )
    summa_fed = models.FloatField(help_text=_(u"Сумма федеральных средств, руб."), null=True, verbose_name=_(u"Сумма федеральных средств, руб."), blank=True, )
    summa_reg = models.FloatField(help_text=_(u"Сумма краевых средств, руб."), null=True, verbose_name=_(u"Сумма краевых средств, руб."), blank=True, )
    summ_mo_money = models.FloatField(help_text=_(u"Сумма муниципальных средств, включенных в сумму контракта, руб."), null=True,
                                        verbose_name=_(u"Сумма муниципальных средств, включенных в сумму контракта, руб."), blank=True, )
    summ_without_mo_money = models.FloatField(help_text=_(u"Сумма заключенного контракта без учета средств МО, руб."), null=True,
                                                verbose_name=_(u"Сумма заключенного контракта без учета средств МО, руб."), blank=True, )
    date = models.DateField(help_text=_(u"Дата заключения контракта"), null=True, verbose_name=_(u"Дата заключения контракта"), blank=True, )
    period_of_payment = models.CharField(max_length=2048, help_text=_(u"Срок оплаты по условиям контракта"), null=True, verbose_name=_(u"Срок оплаты по условиям контракта"), blank=True, )
    creation_form = models.SmallIntegerField(help_text=_(u"Форма создания специализированного жилого фонда для детей-сирот"),
                                             verbose_name=_(u"Форма создания специализированного жилого фонда для детей-сирот"),
                                             blank=True, null=True, choices=CREATION_FORM_CHOICES)
    mo = models.ForeignKey(MO, help_text=_(u"Муниципальное образование"), verbose_name=_(u"Муниципальное образование"), )
    # docs = models.ForeignKey(ContractDocuments, null=True, blank=True, help_text=_(u"Контрактная документация"), verbose_name=_(u"Контрактная документация"), )
    budget = models.SmallIntegerField(help_text=u"Бюджет", verbose_name=u"Бюджет", null=True, blank=False, choices=BUDGET_CHOICES)

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
    developer = models.ForeignKey(Developer, on_delete=models.SET_NULL, help_text=_(u"Застройщик (владелец) объекта"), null=True, verbose_name=_(u"Застройщик (владелец) объекта"), blank=True, )
    mo = models.ForeignKey(MO, help_text=_(u"Муниципальное образование"), verbose_name=_(u"Муниципальное образование"),)
    contract = models.ForeignKey(Contract, blank=True, null=True, help_text=_(u"Данные заключенного контракта"), verbose_name=_(u"Данные заключенного контракта"), )

    start_date = models.DateField(help_text=_(u"Предполагаемый срок начала строительства"), null=True, verbose_name=_(u"Предполагаемый срок начала строительства"), blank=True, )
    finish_date = models.DateField(help_text=_(u"Предполагаемый срок окончания строительства"), null=True, verbose_name=_(u"Предполагаемый срок окончания строительства"), blank=True, )


class Building(BaseBuilding, BaseCompareData, BaseFile):
    cad_num = models.CharField(help_text=_(u"Кадастровый номер"), unique=True, db_index=True, max_length=2048, verbose_name=_(u"Кадастровый номер"))
    developer = models.ForeignKey(Developer, on_delete=models.SET_NULL, blank=True, null=True, help_text=_(u"Застройщик (владелец) объекта"), verbose_name=_(u"Застройщик (владелец) объекта"))
    mo = models.ForeignKey(MO, help_text=_(u"Муниципальное образование"), verbose_name=_(u"Муниципальное образование"), )
    contract = models.ForeignKey(Contract, blank=True, null=True, help_text=_(u"Данные заключенного контракта"), verbose_name=_(u"Данные заключенного контракта"), )

    flat_num = models.IntegerField(null=True, blank=True, help_text=u"Номер жилого помещения", verbose_name=u"Номер жилого помещения")

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
    developer = models.ForeignKey(Developer, on_delete=models.SET_NULL, blank=True, null=True, help_text=_(u"Застройщик (владелец) объекта"), verbose_name=_(u"Застройщик (владелец) объекта"))
    mo = models.ForeignKey(MO, help_text=_(u"Муниципальное образование"), blank=True, null=True, verbose_name=_(u"Муниципальное образование"), )
    contract = models.ForeignKey(Contract, blank=False, null=True, help_text=_(u"Данные заключенного контракта"), verbose_name=_(u"Данные заключенного контракта"), )

    flat_num = models.IntegerField(null=True, blank=True, help_text=u"Номер жилого помещения", verbose_name=u"Номер жилого помещения")

    class Meta:
        app_label = "build"
        verbose_name = _(u"Типовое строение")

    def __unicode__(self):
        if not self.address:
            return ""
        return "%s" % self.address
