# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import date, datetime
from django.db import models
from django.utils.translation import ugettext as _

FACE_LIST_CHOICES = ((0, _(u'Юридическое лицо')),  (1, _(u'Физическое лицо')),)
STATE_CHOICES = ((0, _(u'Сданный объект')),  (1, _(u'Строящийся объект')), (2, _(u'Участок под строительство')))
READINESS_CHOICES = ((0, _(u'Фундаментные работы')),  (1, _(u'Строительно-монтажные работы (указать этаж в комментариях)')), (2, _(u'Санитарно-технические работы')), (3, _(u'Отделочные работы')),   (4, _(u'Работы по благоустройству территории')), (5, _(u'Cдан в эксплуатацию')))
WATER_SETTLEMENT_CHOICES = ((0, _(u'Не указано')), (1, _(u'Центральное')),  (2, _(u'Индивидуальное')))
HOT_WATER_SUPPLY_CHOICES = ((0, _(u'Не указано')), (1, _(u'Центральное')),  (2, _(u'Индивидуальное')))
WATER_REMOVAL_CHOICES = ((0, _(u'Не указано')), (1, _(u'Центральное')),  (2, _(u'Индивидуальное')))
ELECTRIC_SUPPLY_CHOICES = ((0, _(u'Не указано')), (1, _(u'Центральное')),  (2, _(u'Индивидуальное')))
GAS_SUPPLY_CHOICES = ((0, _(u'Не указано')), (1, _(u'Центральное')),  (2, _(u'Индивидуальное')))
CREATION_FORM_CHOICES = ((0, _(u'Приобретение')),  (1, _(u'Долевое строительство')), (2, _(u'Строительство')),)
SEPARATE_CHOICES = ((0, _(u'Не указано')),  (1, _(u'Совместный')),  (2, _(u'Раздельный')),)
STAGE_CHOICES = ((0, _(u'Подача заявок')),  (1, _(u'Работа комиссии')),
                 (2, _(u'Размещение завершено, аукцион признан несостоявшимся, не допущена ни одна заявка')),
                 (3, _(u'Размещение завершено, аукцион признан несостоявшимся, не подана ни одна заявка')),
                 (4, _(u'Заключен контракт')), (5, _(u'Размещение отменено')))
PAYMENT_PERSPECTIVE_CHOICES = ((0, _(u'Перспективы освоения денежных средств, выделенных на текущий год. Без дополнительного финансирования')),
                               (1, _(u'Перспективы освоения ДОПОЛНИТЕЛЬНЫХ денежных средств, в текущем году.')),
                               (2, _(u'Перспективы освоения денежных средств в планируемом году.')))
PAYMENT_STATE_CHOICES = (((1, _(u'Платеж')), (2, _(u'Административный платеж')), ))
APPROVE_CHOICES = ((0, _(u'Не проверено')), (1, _(u'Требуется проверка')), (2, _(u'Проверено')), )
STOVE_CHOICES = ((0, _(u'Не указано')), (1, _(u'Газовая кухонная плита')), (2, _(u'Электрическая кухонная плита')), (3, _(u'Кухонная плита')), )
HEATING_CHOICES = ((0, _(u'Не указано')), (1, _(u'Центральное')),  (2, _(u'Индивидуальное поквартирное')),  (3, _(u'Автономное')))
SINK_CHOICES = ((0, _(u'Не указано')), (1, _(u'Раковина')), (2, _(u'Раковина со смесителем')), )
BATH_CHOICES = ((0, _(u'Не указано')), (1, _(u'Ванна')), (2, _(u'Ванна со смесителем')), )
AREA_CMP_CHOICES = ((0, _(u'Не менее')), (1, _(u'Равно')), )
BUDGET_CHOICES = ((1, _(u'Федеральный')),  (2, _(u'Краевой')), )

YES_NO_CHOICES = (("0", u"Нет"), ("1", u"Да"), ("", u"----"))

START_YEAR_DEFAULT = date(datetime.now().year - 1, 1, 1)
STOP_YEAR_DEFAULT = date(datetime.now().year + 4, 12, 31)


class Choices(models.Model):
    name = models.CharField(help_text=u"Внутреннее имя списка выбора", blank=True,
                            verbose_name=u"Внутреннее имя списка выбора", max_length=2048)
    verbose_name = models.CharField(help_text=u"Имя списка выбора", null=True, blank=True,
                            verbose_name=u"Имя списка выбора", max_length=2048)
    class Meta:
        verbose_name = u"Список выбора"

    def __unicode__(self):
        return '%s' % self.verbose_name


class Choice(models.Model):

    class Meta:
        verbose_name = u"Выбор"
    choices = models.ForeignKey(Choices, help_text=u"Имя списка выбора", verbose_name="Имя списка выбора")
    num = models.IntegerField(help_text=u"Порядковый номер", verbose_name=u"Порядковый номер", blank=True, null=True)
    value = models.CharField(help_text=u"Значение", verbose_name=u"Значение", max_length=4096, blank=True, null=True)


class BaseName(models.Model):

    class Meta:
        abstract = True

    name = models.CharField(help_text=_(u"Наименование"), null=True, max_length=2048, verbose_name=_(u"Наименование"), blank=False, )


class BaseDocumentModel(models.Model):

    class Meta:
        abstract = True

    creation_date = models.DateTimeField(auto_now=True, null=True, blank=True, )


class BaseBudget(models.Model):

    class Meta:
        abstract = True

    sub_sum = models.FloatField(help_text=_(u"Размер предоставляемой в текущем году субвенции"), null=True, verbose_name=_(u"Размер предоставляемой в текущем году субвенции"), blank=True, )
    sub_orph_home = models.FloatField(help_text=_(u"Размер субвенции, выделенной на предоставление жилых помещений детям сиротам"),
                                        verbose_name=_(u"Размер субвенции, выделенной на предоставление жилых помещений детям сиротам"),
                                        blank=True, null=True, )
    adm_coef = models.FloatField(help_text=_(u"Размер коэффициента на администрирование расходов"), null=True, verbose_name=_(u"Размер коэффициента на администрирование расходов"), blank=True, )
    subvention_performance = models.IntegerField(help_text=_(u"Показатель результативности предоставления субвенции "
                                                             u"(количество детей-сирот, подлежащих обеспечению жилыми "
                                                             u"помещениями в текущем году)"), default=0,
                                                 verbose_name=_(u"Показатель результативности предоставления субвенции "
                                                               u"(количество детей-сирот, подлежащих обеспечению "
                                                               u"жилыми помещениями в текущем году)"), blank=True, )


class BaseSubvention(models.Model):

    class Meta:
        abstract = True

    date = models.DateField(auto_now=True)
    amount = models.FloatField(help_text=_(u"Общая сумма предоставляемой в текущем году субвенции"), null=True,
                                 verbose_name=_(u"Общая сумма предоставляемой в текущем году субвенции"), blank=True, )


class BaseDepartamentAgreement(BaseDocumentModel, ):

    class Meta:
        abstract = True

    start_year = models.DateField(help_text=_(u"Срок начала учета в системе"), verbose_name=_(u"Срок начала учета в системе"), blank=False, default=START_YEAR_DEFAULT)
    finish_year = models.DateField(help_text=_(u"Срок окончания учета в системе"), verbose_name=_(u"Срок окончания учета в системе"), blank=False, default=STOP_YEAR_DEFAULT)
    date = models.DateField(help_text=_(u"Дата соглашения с министерством"), null=True,
                            verbose_name=_(u"Дата соглашения с министерством"), blank=True, )
    num = models.IntegerField(help_text=_(u"Номер соглашения с министерством"), null=True,
                              verbose_name=_(u"Номер соглашения с министерством"), blank=True, )


class BaseOrphan(models.Model):

    class Meta:
        abstract = True

    age = models.IntegerField(blank=True, null=True, choices=STAGE_CHOICES , )
    have_home = models.NullBooleanField(blank=True, )
    is_privilege = models.NullBooleanField(blank=True, )


class BaseBuilding(models.Model):

    class Meta:
        abstract = True

    start_year = models.DateField(help_text=_(u"Срок начала учета в системе"), verbose_name=_(u"Срок начала учета в системе"), blank=False, default=START_YEAR_DEFAULT)
    finish_year = models.DateField(help_text=_(u"Срок окончания учета в системе"), verbose_name=_(u"Срок окончания учета в системе"), blank=False, default=STOP_YEAR_DEFAULT)

    approve_status = models.IntegerField(default=2, choices=APPROVE_CHOICES, verbose_name=_(u"Статус проверки объекта"), help_text=_(u"Статус проверки документа"))
    state = models.IntegerField(default=1, help_text=_(u"Состояние"), verbose_name=_(u"Состояние"), choices=STATE_CHOICES , )
    address = models.TextField(help_text=_(u"Адрес"), null=True, verbose_name=_(u"Адрес"), blank=False, )
    complete_date = models.DateField(help_text=_(u"Срок сдачи в эксплуатацию"), null=True, verbose_name=_(u"Срок сдачи в эксплуатацию"), blank=True, )
    comment = models.TextField(help_text=_(u"Комментарий"), null=True, verbose_name=_(u"Комментарий"), blank=True, )
    readiness = models.IntegerField(help_text=_(u"Степень готовности"), null=True, blank=True, verbose_name=_(u"Степень готовности"), choices=READINESS_CHOICES , )
    payment_perspective = models.IntegerField(help_text=_(u"Перспектива освоения"), null=True, blank=True, verbose_name=_(u"Перспектива освоения"), choices=PAYMENT_PERSPECTIVE_CHOICES , )

    offer = models.FileField(null=True, blank=True, upload_to='img_files', help_text=_(u"Коммерческое предложение"), verbose_name=_(u"Коммерческое предложение"))
    permission = models.FileField(null=True, blank=True, upload_to='img_files', help_text=_(u"Разрешение на строительство"), verbose_name=_(u"Разрешение на строительство"))
    cad_passport = models.FileField(null=True, blank=True, upload_to='img_files', help_text=_(u"Выписка из кадастрового паспорта"), verbose_name=_(u"Выписка из кадастрового паспорта"))


class BaseContract(BaseName):

    class Meta:
        abstract = True

    start_year = models.DateField(help_text=_(u"Срок начала учета в системе"), verbose_name=_(u"Срок начала учета в системе"), blank=False, default=START_YEAR_DEFAULT)
    finish_year = models.DateField(help_text=_(u"Срок окончания учета в системе"), verbose_name=_(u"Срок окончания учета в системе"), blank=False, default=STOP_YEAR_DEFAULT)

    num = models.CharField(help_text=_(u"Номер"), max_length=2048, verbose_name=_(u"Номер"), )
    has_trouble_docs = models.NullBooleanField(help_text=_(u"Замечания по документации"), verbose_name=_(u"Замечания по документации"), blank=True, null=True, )


class BaseResult(models.Model):

    class Meta:
        abstract = True

    start_year = models.DateField(help_text=_(u"Срок начала учета в системе"), verbose_name=_(u"Срок начала учета в системе"), blank=False, default=START_YEAR_DEFAULT)
    finish_year = models.DateField(help_text=_(u"Срок окончания учета в системе"), verbose_name=_(u"Срок окончания учета в системе"), blank=False, default=STOP_YEAR_DEFAULT)

    check_date = models.DateField(help_text=_(u"Дата следующей проверки"), null=True, verbose_name=_(u"Дата следующей проверки"), blank=True, )
    doc_list = models.CharField(help_text=_(u"Перечень предоставленных документов"), null=True, max_length=2048, verbose_name=_(u"Перечень предоставленных документов"), blank=True, )
    readiness = models.IntegerField(help_text=_(u"Степень готовности"), null=True, blank=True, verbose_name=_(u"Степень готовности"), choices=READINESS_CHOICES , )
    recommend = models.CharField(help_text=_(u"Рекомендации"), null=True, max_length=2048, verbose_name=_(u"Рекомендации"), blank=True, )


class BaseDeveloper(BaseName, ):

    class Meta:
        abstract = True

    phone = models.CharField(help_text=_(u"Контактный телефон"), null=True, max_length=2048, verbose_name=_(u"Контактный телефон"), blank=True, )
    face_list = models.IntegerField(help_text=_(u"Юридическое/Физическое лицо"), null=True, blank=True,
                                    verbose_name=_(u"Юридическое/Физическое лицо"), choices=FACE_LIST_CHOICES,)
    address = models.CharField(help_text=_(u"Фактический адрес"), null=True, max_length=2048, verbose_name=_(u"Фактический адрес"), blank=True, )
    boss_position = models.CharField(help_text=_(u"Ф.И.О. и должность руководителя"), max_length=2048, verbose_name=_(u"Ф.И.О. и должность руководителя"), )


class BasePayment(models.Model):

    class Meta:
        abstract = True

    approve_status = models.IntegerField(default=2, choices=APPROVE_CHOICES, verbose_name=_(u"Статус проверки платежа"), help_text=_(u"Статус проверки платежа"))
    num = models.CharField(max_length=2048, help_text=_(u"Номер документа, подтверждающего платеж"), verbose_name=_(u"Номер документа, подтверждающего платеж"),)
    date = models.DateField(db_index=True, help_text=_(u"Дата совершения платежа"), verbose_name=_(u"Дата совершения платежа"),)
    amount = models.FloatField(null=True, blank=True, help_text=_(u"Сумма платежа (руб.)"), verbose_name=_(u"Сумма платежа (руб.)"),)
    payment_state = models.SmallIntegerField(default=1, help_text=_(u"Тип платежа"), verbose_name=_(u"Тип платежа"), choices=PAYMENT_STATE_CHOICES)


class BaseMaterials(models.Model):

    class Meta:
        abstract = True

    floor = models.IntegerField(help_text=_(u"Материал отделки пола"), default=0, blank=True, verbose_name=_(u"Материал отделки пола"), )
    wall = models.IntegerField(help_text=_(u"Материал отделки стен"), default=0, blank=True, verbose_name=_(u"Материал отделки стен") )
    ceiling = models.IntegerField(help_text=_(u"Материал отделки потолка"), default=0, blank=True, verbose_name=_(u"Материал отделки потолка"), )

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(BaseMaterials, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d


class BaseEngineerNetworks(models.Model):

    class Meta:
        abstract = True

    gas_supply = models.IntegerField(help_text=_(u"Газоснабжение"), null=True, blank=True, default=0, verbose_name=_(u"Газоснабжение"), choices=GAS_SUPPLY_CHOICES , )

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(BaseEngineerNetworks, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d


class BaseWaterSupply(BaseEngineerNetworks):

    class Meta:
        abstract = True

    water_removal = models.IntegerField(help_text=_(u"Водоотведение"), null=True, blank=True, verbose_name=_(u"Водоотведение"), choices=WATER_REMOVAL_CHOICES , )
    water_settlement = models.IntegerField(help_text=_(u"Водоподведение"), default=0, blank=True, verbose_name=_(u"Водоподведение"), choices=WATER_SETTLEMENT_CHOICES , )
    hot_water_supply = models.IntegerField(help_text=_(u"Горячее водоснабжение"), default=0, blank=True, verbose_name=_(u"Горячее водоснабжение"), choices=HOT_WATER_SUPPLY_CHOICES , )
    heating = models.IntegerField(help_text=_(u"Отопление"), null=True, blank=True, verbose_name=_(u"Отопление"), choices=GAS_SUPPLY_CHOICES , )
    electric_supply = models.IntegerField(help_text=_(u"Электроснабжение"), null=True, blank=True, verbose_name=_(u"Электроснабжение"), choices=ELECTRIC_SUPPLY_CHOICES , )

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(BaseWaterSupply, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d


class BaseSocialObjects(models.Model):

    class Meta:
        abstract = True

    public_transport = models.IntegerField(help_text=_(u"Ближайшая остановка общественного транспорта отдаленность, м"), null=True, verbose_name=_(u"Ближайшая остановка общественного транспорта отдаленность, м"), blank=True, )
    market = models.IntegerField(help_text=_(u"Магазин отдаленность, м"), null=True, verbose_name=_(u"Магазин отдаленность, м"), blank=True, )
    kindergarden = models.IntegerField(help_text=_(u"Детский сад отдаленность, м"), null=True, verbose_name=_(u"Детский сад отдаленность, м"), blank=True, )
    school = models.IntegerField(help_text=_(u"Школа отдаленность, м"), null=True, verbose_name=_(u"Школа отдаленность, м"), blank=True, )
    clinic = models.IntegerField(help_text=_(u"Поликлиника отдаленность, м"), null=True, verbose_name=_(u"Поликлиника отдаленность, м"), blank=True, )

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(BaseSocialObjects, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d


class BaseTerritoryImprovement(models.Model):

    class Meta:
        abstract = True

    is_routes = models.NullBooleanField(help_text=_(u"Подъездные пути"), verbose_name=_(u"Подъездные пути"), blank=True, )
    is_playground = models.NullBooleanField(help_text=_(u"Детская площадка"), verbose_name=_(u"Детская площадка"), blank=True, )
    is_clother_drying = models.NullBooleanField(help_text=_(u"Площадка для сушки белья"), verbose_name=_(u"Площадка для сушки белья"), blank=True, )
    is_parking = models.NullBooleanField(help_text=_(u"Парковка"), verbose_name=_(u"Парковка"), blank=True, )
    is_dustbin_area = models.NullBooleanField(help_text=_(u"Площадка для мусорных контейнеров"), verbose_name=_(u"Площадка для мусорных контейнеров"), blank=True, )

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(BaseTerritoryImprovement, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d


class BaseCommonChars(BaseWaterSupply, BaseSocialObjects, BaseTerritoryImprovement, ):

    class Meta:
        abstract = True

    is_water_boiler = models.NullBooleanField(help_text=_(u"Водонагревательный прибор (бойлер)"), verbose_name=_(u"Водонагревательный прибор (бойлер)"), blank=True, )
    is_heat_boiler = models.NullBooleanField(help_text=_(u"Отопительный котел"), verbose_name=_(u"Отопительный котел"), blank=True, )
    is_intercom = models.NullBooleanField(help_text=_(u"Домофон"), verbose_name=_(u"Домофон"), blank=True, )
    is_loggia = models.NullBooleanField(help_text=_(u"Наличие лоджии"), verbose_name=_(u"Наличие лоджии"), blank=True, )
    is_balcony = models.NullBooleanField(help_text=_(u"Наличие балкона"), verbose_name=_(u"Наличие балкона"), blank=True, )
    internal_doors = models.IntegerField(help_text=_(u"Материал межкомнатных дверей"), default=0, blank=True, verbose_name=_(u"Материал межкомнатных дверей"), )
    entrance_door = models.IntegerField(help_text=_(u"Материал входной двери"), default=0, blank=True, verbose_name=_(u"Материал входной двери"), )
    window_constructions = models.IntegerField(help_text=_(u"Материал оконных конструкций"), default=0, blank=True, verbose_name=_(u"Материал оконных конструкций"), )

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(BaseCommonChars, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d


class BaseDevices(models.Model):

    class Meta:
        abstract = True

    switches = models.NullBooleanField(help_text=_(u"Выключатели"), verbose_name=_(u"Выключатели"), blank=True, )
    sockets = models.NullBooleanField(help_text=_(u"Розетки"), verbose_name=_(u"Розетки"), blank=True, )
    lamp = models.NullBooleanField(help_text=_(u"Электропатрон"), verbose_name=_(u"Электропатрон"), blank=True, )
    ceiling_hook = models.NullBooleanField(help_text=_(u"Потолочный крюк"), verbose_name=_(u"Потолочный крюк"), blank=True, )
    heaters = models.NullBooleanField(help_text=_(u"Отопительные приборы"), verbose_name=_(u"Отопительные приборы"), blank=True, )
    smoke_filter = models.NullBooleanField(help_text=_(u"Дымоулавливатель"), verbose_name=_(u"Дымоулавливатель"), blank=True, )

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(BaseDevices, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d


# common classes
class BaseRoom(BaseDevices):

    class Meta:
        app_label = "core"
        verbose_name = "Комната"

    def __unicode__(self):
        return '%s' % self.id

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(BaseRoom, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d


class BaseKitchen(BaseDevices):
    sink_with_mixer = models.IntegerField(help_text=_(u"Раковина"), default=0, blank=True, null=True, verbose_name=_(u"Раковина"), choices=SINK_CHOICES)

    class Meta:
        app_label = "core"
        verbose_name = "Кухня"

    def __unicode__(self):
        return '%s' % self.id

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(BaseKitchen, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d


class BaseWC(BaseDevices, ):
    is_tower_dryer = models.NullBooleanField(help_text=_(u"Полотенцесушитель"), verbose_name=_(u"Полотенцесушитель"), blank=True, )
    is_toilet = models.NullBooleanField(help_text=_(u"Унитаз"), verbose_name=_(u"Унитаз"), blank=True, )
    bath_with_mixer = models.IntegerField(help_text=_(u"Ванна"), default=0, blank=True, null=True, verbose_name=_(u"Ванна"), choices=BATH_CHOICES)
    sink_with_mixer = models.IntegerField(help_text=_(u"Раковина"), default=0, blank=True, null=True, verbose_name=_(u"Раковина"), choices=SINK_CHOICES)
    wc_switches = models.NullBooleanField(help_text=_(u"Выключатели в туалете"), verbose_name=_(u"Выключатели в туалете"), blank=True, )

    class Meta:
        app_label = "core"
        verbose_name = "Санузел"

    def __unicode__(self):
        return '%s' % self.id

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(BaseWC, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d


class BaseHallway(BaseDevices, ):

    class Meta:
        app_label = "core"
        verbose_name = u"Прихожая"

    def __unicode__(self):
        return '%s' % self.id

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(BaseHallway, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d


class Room(BaseMaterials, BaseRoom):
    class Meta:
        verbose_name = u"Комната"

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(Room, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d


class Kitchen(BaseMaterials, BaseKitchen):
    stove = models.IntegerField(default=0, blank=True, help_text=_(u"Кухонная плита"), verbose_name=_(u"Кухонная плита"), choices=STOVE_CHOICES)

    class Meta:
        verbose_name = u"Кухня"

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(Kitchen, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d


class WC(BaseMaterials, BaseWC, ):
    separate = models.IntegerField(default=0, blank=True, help_text=_(u"Санузел"), verbose_name=_(u"Санузел"), choices=SEPARATE_CHOICES)
    wc_floor = models.IntegerField(help_text=_(u"Материал отделки пола в туалете"), default=0, blank=True, verbose_name=_(u"Материал отделки пола в туалете"), )
    wc_wall = models.IntegerField(help_text=_(u"Материал отделки стен в туалете"), default=0, blank=True, verbose_name=_(u"Материал отделки стен в туалете") )
    wc_ceiling = models.IntegerField(help_text=_(u"Материал отделки потолка в туалете"), default=0, blank=True, verbose_name=_(u"Материал отделки потолка в туалете"), )

    class Meta:
        verbose_name = u"Ванная комната"

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(WC, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d


class Hallway(BaseMaterials, BaseHallway, ):
    class Meta:
        verbose_name = u"Прихожая"

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(Hallway, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d


class Developer(BaseDeveloper, ):

    class Meta:
        app_label = "core"
        verbose_name = "Developer"

    def __unicode__(self):
        name = self.name if self.name else self.address
        return '%s' % name


class BaseCompareData(BaseCommonChars, ):

    class Meta:
        abstract = True

    floors = models.IntegerField(help_text=_(u"Этажность"), null=True, verbose_name=_(u"Этажность"), blank=True, )
    driveways = models.IntegerField(help_text=_(u"Подъездность"), null=True, verbose_name=_(u"Подъездность"), blank=True, )
    flats_amount = models.IntegerField(help_text=_(u"Количество однокомнатных жилых помещений (площадью не менее 33 кв. м)"), null=True, verbose_name=_(u"Количество однокомнатных жилых помещений (площадью не менее 33 кв. м)"), blank=True, )
    area_cmp = models.IntegerField(help_text=_(u"Общая площадь не менее/равна"), verbose_name=_(u"Общая площадь не менее/равна"), default=1, blank=False, null=True, choices=AREA_CMP_CHOICES)
    area = models.FloatField(help_text=_(u"Общая площадь (кв. м)"), null=True, verbose_name=_(u"Общая площадь (кв. м)"), blank=False, )

    room = models.ForeignKey(Room, null=True, blank=True, )
    wc = models.ForeignKey(WC, null=True, blank=True, )
    hallway = models.ForeignKey(Hallway, null=True, blank=True, )
    kitchen = models.ForeignKey(Kitchen, null=True, blank=True, )

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(BaseCompareData, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d


class BaseMultiMaterials(models.Model):

    class Meta:
        abstract = True

    floor = models.CommaSeparatedIntegerField(max_length=256, help_text=_(u"Материал отделки пола"), default=0, blank=True, verbose_name=_(u"Материал отделки пола"))
    wall = models.CommaSeparatedIntegerField(max_length=256, help_text=_(u"Материал отделки стен"), default=0, blank=True, verbose_name=_(u"Материал отделки стен"))
    ceiling = models.CommaSeparatedIntegerField(max_length=256, help_text=_(u"Материал отделки потолка"), default=0, blank=True, verbose_name=_(u"Материал отделки потолка"))

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(BaseMultiMaterials, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d


class BaseMultiWaterSupply(BaseEngineerNetworks):

    class Meta:
        abstract = True

    electric_supply = models.CommaSeparatedIntegerField(max_length=256, help_text=_(u"Электроснабжение"), null=True, blank=True, verbose_name=_(u"Электроснабжение"), )
    water_removal = models.CommaSeparatedIntegerField(max_length=256, help_text=_(u"Водоотведение"), null=True, blank=True, verbose_name=_(u"Водоотведение"), )
    water_settlement = models.CommaSeparatedIntegerField(max_length=256, help_text=_(u"Водоподведение"), null=True, blank=True, verbose_name=_(u"Водоподведение"), )
    hot_water_supply = models.CommaSeparatedIntegerField(max_length=256, help_text=_(u"Горячее водоснабжение"), null=True, blank=True, verbose_name=_(u"Горячее водоснабжение"), )
    heating = models.CommaSeparatedIntegerField(max_length=256, help_text=_(u"Отопление"), null=True, blank=True, verbose_name=_(u"Отопление"), )

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(BaseMultiWaterSupply, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d


class AuctionRoom(BaseMultiMaterials, BaseRoom):
    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(AuctionRoom, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d


class AuctionKitchen(BaseMultiMaterials, BaseKitchen):
    stove = models.CommaSeparatedIntegerField(max_length=16, null=True, blank=True, help_text=_(u"Кухонная плита"), verbose_name=_(u"Кухонная плита"))

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(AuctionKitchen, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d


class AuctionWC(BaseMultiMaterials, BaseWC):
    separate = models.CommaSeparatedIntegerField(max_length=16, null=True, blank=True, help_text=_(u"Санузел"), verbose_name=_(u"Санузел"))
    wc_floor = models.CommaSeparatedIntegerField(max_length=256, help_text=_(u"Материал отделки пола в туалете"), null=True, blank=True, verbose_name=_(u"Материал отделки пола в туалете"), )
    wc_wall = models.CommaSeparatedIntegerField(max_length=256, help_text=_(u"Материал отделки стен в туалете"), null=True, blank=True, verbose_name=_(u"Материал отделки стен в туалете") )
    wc_ceiling = models.CommaSeparatedIntegerField(max_length=256, help_text=_(u"Материал отделки потолка в туалете"), null=True, blank=True, verbose_name=_(u"Материал отделки потолка в туалете"), )

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(AuctionWC, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d


class AuctionHallway(BaseMultiMaterials, BaseHallway):
    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(AuctionHallway, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d


class BaseAuctionData(BaseSocialObjects, BaseMultiWaterSupply, BaseTerritoryImprovement, ):

    class Meta:
        abstract = True

    flats_amount = models.IntegerField(help_text=_(u"Количество жилых помещений по номеру заказа"), null=True, verbose_name=_(u"Количество жилых помещений по номеру заказа"), blank=False, )
    area_cmp = models.IntegerField(help_text=_(u"Общая площадь не менее/равна"), verbose_name=_(u"Общая площадь не менее/равна"), default=1, blank=False, null=True, choices=AREA_CMP_CHOICES)
    area = models.FloatField(help_text=_(u"Площадь жилых помещений по номеру заказа (кв. м)"), null=True, verbose_name=_(u"Площадь жилых помещений по номеру заказа (кв. м)"), blank=False, )
    floors = models.IntegerField(help_text=_(u"Этажность"), null=True, verbose_name=_(u"Этажность"), blank=True, )
    driveways = models.IntegerField(help_text=_(u"Подъездность"), null=True, verbose_name=_(u"Подъездность"), blank=True, )

    is_water_boiler = models.NullBooleanField(help_text=_(u"Водонагревательный прибор (бойлер)"), verbose_name=_(u"Водонагревательный прибор (бойлер)"), blank=True, )
    is_heat_boiler = models.NullBooleanField(help_text=_(u"Отопительный котел"), verbose_name=_(u"Отопительный котел"), blank=True, )
    is_intercom = models.NullBooleanField(help_text=_(u"Домофон"), verbose_name=_(u"Домофон"), blank=True, )
    is_loggia = models.NullBooleanField(help_text=_(u"Наличие лоджии"), verbose_name=_(u"Наличие лоджии"), blank=True, )
    is_balcony = models.NullBooleanField(help_text=_(u"Наличие балкона"), verbose_name=_(u"Наличие балкона"), blank=True, )
    internal_doors = models.CommaSeparatedIntegerField(max_length=256, help_text=_(u"Материал межкомнатных дверей"),
                                                       default=0, blank=True, verbose_name=_(u"Материал межкомнатных дверей"))
    entrance_door = models.CommaSeparatedIntegerField(max_length=256, help_text=_(u"Материал входной двери"),
                                                      default=0, blank=True, verbose_name=_(u"Материал входной двери"))
    window_constructions = models.CommaSeparatedIntegerField(max_length=256, help_text=_(u"Материал оконных конструкций"),
                                                             default=0, blank=True, verbose_name=_(u"Материал оконных конструкций"))

    stage = models.IntegerField(help_text=_(u"Этап размещения заказа"), null=True, blank=False, verbose_name=_(u"Этап размещения заказа"), choices=STAGE_CHOICES , )
    start_price = models.FloatField(help_text=_(u"Начальная (максимальная) цена руб."), null=True, verbose_name=_(u"Начальная (максимальная) цена руб."), blank=False, )
    date = models.DateField(help_text=_(u"Дата размещения извещения о торгах (Дата опубликования заказа) дд.мм.гггг"),  null=True, verbose_name=_(u"Дата размещения извещения о торгах (Дата опубликования заказа) дд.мм.гггг"),  blank=False, )
    open_date = models.DateTimeField(help_text=_(u"Дата и время проведения открытого аукциона (последнего события при размещении заказа, при отмене размещения, либо завершении аукциона)"),  null=True, verbose_name=_(u"Дата и время проведения открытого аукциона (последнего события при размещении заказа, при отмене размещения, либо завершении аукциона)"),  blank=False, )
    proposal_count = models.IntegerField(help_text=_(u"Количество поданных заявок"), verbose_name=_(u"Количество поданных заявок"), blank=True, default=0)

    room = models.ForeignKey(AuctionRoom, null=True, blank=True, )
    wc = models.ForeignKey(AuctionWC, null=True, blank=True, )
    hallway = models.ForeignKey(AuctionHallway, null=True, blank=True, )
    kitchen = models.ForeignKey(AuctionKitchen, null=True, blank=True, )

    def to_dict(self):
        attrs = deepcopy(self.__dict__)
        d = super(BaseAuctionData, self).to_dict() or {}
        for k in attrs:
            if not '__' in k and getattr(self, k):
                d.update({k: getattr(self, k)})
        return d
