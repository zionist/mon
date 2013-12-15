# -*- coding: utf-8 -*-
from copy import deepcopy
from django.db import models
from django.utils.translation import ugettext as _
from apps.core.models import BaseModel, BaseBuilding, BaseCompareData, BaseContract, Developer
from apps.mo.models import MO
from apps.imgfile.models import File, BaseImage


class ContractDocuments(BaseModel, BaseImage):

    class Meta:
        app_label = "cmp"
        verbose_name = "Contract Documents"
    def __unicode__(self):
        return '%s' % self.id

    protocols = models.ImageField(null=True, blank=True, upload_to='img_files', help_text=_(u"Протоколы о подведении итогов торгов"),
        verbose_name=_(u"Протоколы о подведении итогов торгов"), )
    mun_contracts = models.ImageField(null=True, blank=True, upload_to='img_files', help_text=_(u"Муниципальные контракты с приложениями"),
        verbose_name=_(u"Муниципальные контракты с приложениями."), )
    transmission_acts = models.ImageField(null=True, blank=True, upload_to='img_files', help_text=_(u"Акты приема-передачи жилых помещений"),
        verbose_name=_(u"Акты приема-передачи жилых помещений"), )
    facility_permission = models.ImageField(null=True, blank=True, upload_to='img_files', help_text=_(u"Разрешения на ввод объекта в эксплуатацию."),
        verbose_name=_(u"Разрешения на ввод объекта в эксплуатацию"), )
    land_right_stating = models.ImageField(null=True, blank=True, upload_to='img_files', help_text=_(u"Правоустанавливающие документы на земельные участки"),
        verbose_name=_(u"Правоустанавливающие документы на земельные участки"), )
    building_permissions = models.ImageField(null=True, blank=True, upload_to='img_files', help_text=_(u"Разрешения на строительство"),
        verbose_name=_(u"Разрешения на строительство"), )
    acceptance_acts = models.ImageField(null=True, blank=True, upload_to='img_files', help_text=_(u"Акты о приемке выполненных работ (форма № КС-2)"),
        verbose_name=_(u"Акты о приемке выполненных работ (форма № КС-2)"), )
    cost_infos = models.ImageField(null=True, blank=True, upload_to='img_files', help_text=_(u"Справки о стоимости выполненных работ и затрат (форма № КС-3)"),
        verbose_name=_(u"Справки о стоимости выполненных работ и затрат (форма № КС-3)"), )
    mo_certificate = models.ImageField(null=True, blank=True, upload_to='img_files',
                                       help_text=_(u"Свидетельство о регистрации права собственности муниципального образования на жилое помещение"),
                                       verbose_name=_(u"Свидетельство о регистрации права собственности МО на жилое помещение"), )
    mun_act_to_fond = models.ImageField(null=True, blank=True, upload_to='img_files',
                                        help_text=_(u"Муниципальный акт о включении приобретенного/построенного жилья в специализированный жилищный фонд для детей-сирот."),
                                        verbose_name=_(u"Муниципальный акт о включении жилья в спец. жил. фонд."), )
    tec_passport_tec_plan = models.ImageField(null=True, blank=True, upload_to='img_files',
                                              help_text=_(u"Технический паспорт, технический план."),
                                              verbose_name=_(u"Технический паспорт, технический план."), )
    photos = models.ImageField(null=True, blank=True, upload_to='img_files', help_text=_(u"Фотографии приобретенных жилых помещений."),
                               verbose_name=_(u"Фотографии приобретенных жилых помещений."), )
    mo_notice_to_citizen = models.ImageField(null=True, blank=True, upload_to='img_files',
                                             help_text=_(u"Извещение от муниципального образования в адрес гражданина о предоставлении последнему жилого помещения."),
                                             verbose_name=_(u"Извещение от МО о предоставлении жилого помещения."), )
    approval_citizen_statement = models.ImageField(null=True, blank=True, upload_to='img_files',
                                                   help_text=_(u"Заявление от гражданина о согласии в предоставлении жилого помещения."),
                                                   verbose_name=_(u"Заявление от гражданина о согласии в предоставлении жилого помещения."), )
    hiring_contract = models.ImageField(null=True, blank=True, upload_to='img_files',
                                        help_text=_(u"Договор найма специализированного жилого помещения на каждого гражданина."),
                                        verbose_name=_(u"Договор найма специализированного жилого помещения на каждого гражданина."), )

    def to_list(self):
        attrs = deepcopy(self.__dict__)
        l = [getattr(self, k[:-3]) for k in attrs if k and '_id' in k and getattr(self, k[:-3])]
        return l


class Contract(BaseContract, BaseCompareData):

    class Meta:
        app_label = "cmp"
        verbose_name = "Contract"
    def __unicode__(self):
        return '%s' % self.num

    developer = models.ForeignKey(Developer, help_text=_(u"Застройщик"), verbose_name=_(u"Застройщик"), null=True, blank=True, )
    summa = models.IntegerField(help_text=_(u"Сумма заключенного контракта"), null=True, verbose_name=_(u"Сумма заключенного контракта"), blank=True, )
    sign_date = models.DateField(help_text=_(u"Дата заключения контракта"), null=True, verbose_name=_(u"Дата заключения контракта"), blank=True, )
    mo = models.ForeignKey(MO, help_text=_(u"Муниципальное образование"), verbose_name=_(u"Муниципальное образование"), )
    docs = models.ForeignKey(ContractDocuments, help_text=_(u"Контрактная документация"), verbose_name=_(u"Контрактная документация"), )


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
                                  verbose_name=_(u"Застройщик (владелец) объекта"), null=True, blank=True, )
    mo = models.ForeignKey(MO, help_text=_(u"Муниципальное образование"), verbose_name=_(u"Муниципальное образование"),)
    contract = models.ForeignKey(Contract, blank=True, null=True, help_text=_(u"Данные заключенного контракта"),
                                 verbose_name=_(u"Данные заключенного контракта"), )
