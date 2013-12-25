# -*- coding: utf-8 -*-
import time
from django.db import models
from django.utils.translation import ugettext as _
from apps.imgfile.models import File, Image

FACE_LIST_CHOICES = ((0, _(u'Юридическое лицо')),  (1, _(u'Физическое лицо')),)
STATE_CHOICES = ((0, _(u'Сданный объект')),  (1, _(u'Строящийся объект')), (2, _(u'Участок под строительство')))
READINESS_CHOICES = ((0, _(u'Фундаментные работы')),  (1, _(u'Строительно-монтажные работы (указать этаж в комментариях)')), (2, _(u'Санитарно-технические работы')), (3, _(u'Отделочные работы')),   (4, _(u'Работы по благоустройству территории')))
WATER_SETTLEMENT_CHOICES = ((0, _(u'Не указано')), (1, _(u'Центральное')),  (2, _(u'Индивидуальное')))
HOT_WATER_SUPPLY_CHOICES = ((0, _(u'Не указано')), (1, _(u'Центральное')),  (2, _(u'Индивидуальное')))
WATER_REMOVAL_CHOICES = ((0, _(u'Центральное')),  (1, _(u'Индивидуальное')))
ELECTRIC_SUPPLY_CHOICES = ((0, _(u'Центральное')),  (1, _(u'Индивидуальное')))
GAS_SUPPLY_CHOICES = ((0, _(u'Центральное')),  (1, _(u'Индивидуальное')))
CREATION_FORM_CHOICES = ((0, _(u'Приобретение')),  (1, _(u'Долевое строительство')), (2, _(u'Строительство')),)
SEPARATE_CHOICES = ((0, _(u'Не указано')),  (1, _(u'Совместный')),  (2, _(u'Раздельный')),)
STAGE_CHOICES = ((0, _(u'Подача заявок')),  (1, _(u'Работа комиссии')),
                 (2, _(u'Размещение завершено, аукцион признан несостоявшимся, не допущена ни одна заявка')),
                 (3, _(u'Размещение завершено, аукцион признан несостоявшимся, не подана ни одна заявка')),
                 (4, _(u'Заключен контракт')), (5, _(u'Размещение отменено')))
PAYMENT_PERSPECTIVE_CHOICES = ((0, _(u'Перспективы освоения денежных средств, выделенных на текущий год. Без дополнительного финансирования')),
                               (1, _(u'Перспективы освоения ДОПОЛНИТЕЛЬНЫХ денежных средств, в текущем году.')),
                               (2, _(u'Перспективы освоения денежных средств в планируемом году.')))
APPROVE_CHOICES = ((0, _(u'Не проверено')), (1, _(u'Требуется проверка')), (2, (u'Проверено')), )
STOVE_CHOICES = ((0, _(u'Не указано')), (1, _(u'Газовая кухонная плита')), (2, (u'Электрическая кухонная плита')), )
YES_NO_CHOICES = (("0", u"Нет"), ("1", u"Да"), ("", u"----"))



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

    name = models.CharField(help_text=_(u"Наименование"), null=True, max_length=2048, verbose_name=_(u"Наименование"), blank=True, )


class BaseModel(models.Model):

    class Meta:
        abstract = True

    creation_date = models.DateTimeField(auto_now=True, null=True, blank=True, )


class BaseBudget(models.Model):

    class Meta:
        abstract = True

    sub_sum = models.IntegerField(help_text=_(u"Размер предоставляемой в текущем году субвенции"), null=True, verbose_name=_(u"Размер предоставляемой в текущем году субвенции"), blank=True, )
    sub_orph_home = models.IntegerField(help_text=_(u"Размер субвенции, выделенной на предоставление жилых помещений детям сиротам"),
                                        verbose_name=_(u"Размер субвенции, выделенной на предоставление жилых помещений детям сиротам"),
                                        blank=True, null=True, )
    adm_coef = models.IntegerField(help_text=_(u"Размер коэффициента на администрирование расходов"), null=True, verbose_name=_(u"Размер коэффициента на администрирование расходов"), blank=True, )


class BaseSubvention(models.Model):

    class Meta:
        abstract = True

    date = models.DateField(auto_now=True)
    amount = models.IntegerField(help_text=_(u"Общая сумма предоставляемой в текущем году субвенции"), null=True,
                                 verbose_name=_(u"Общая сумма предоставляемой в текущем году субвенции"), blank=True, )


class BaseDepartamentAgreement(BaseModel, ):

    class Meta:
        abstract = True

    date = models.DateField(help_text=_(u"Дата соглашения с министерством"), null=True,
                            verbose_name=_(u"Дата соглашения с министерством"), blank=True, )
    num = models.IntegerField(help_text=_(u"Номер соглашения с министерством"), null=True,
                              verbose_name=_(u"Номер соглашения с министерством"), blank=True, )
    subvention_performance = models.IntegerField(help_text=_(u"Показатель результативности предоставления субвенции "
                                                             u"(количество детей-сирот, подлежащих обеспечению жилыми "
                                                             u"помещениями в текущем году)"), null=True,
                                                 verbose_name=_(u"Показатель результативности предоставления субвенции "
                                                                u"(количество детей-сирот, подлежащих обеспечению "
                                                                u"жилыми помещениями в текущем году)"), blank=True, )


class BaseOrphan(models.Model):

    class Meta:
        abstract = True

    age = models.IntegerField(blank=True, null=True, choices=STAGE_CHOICES , )
    have_home = models.NullBooleanField(blank=True, )
    is_privilege = models.NullBooleanField(blank=True, )


class BaseBuilding(models.Model):

    class Meta:
        abstract = True

    approve_status = models.IntegerField(default=0, choices=APPROVE_CHOICES, verbose_name=_(u"Статус проверки документа"), help_text=_(u"Статус проверки документа"))
    state = models.IntegerField(default=1, help_text=_(u"Состояние"), verbose_name=_(u"Состояние"), choices=STATE_CHOICES , )
    address = models.TextField(help_text=_(u"Адрес"), null=True, verbose_name=_(u"Адрес"), blank=True, )
    complete_date = models.DateField(help_text=_(u"Срок сдачи в эксплуатацию"), null=True, verbose_name=_(u"Срок сдачи в эксплуатацию"), blank=True, )
    comment = models.TextField(help_text=_(u"Комментарий"), null=True, verbose_name=_(u"Комментарий"), blank=True, )
    readiness = models.IntegerField(help_text=_(u"Степень готовности"), null=True, blank=True, verbose_name=_(u"Степень готовности"), choices=READINESS_CHOICES , )
    payment_perspective = models.IntegerField(help_text=_(u"Перспектива освоения"), null=True, blank=True, verbose_name=_(u"Перспектива освоения"), choices=PAYMENT_PERSPECTIVE_CHOICES , )



class BaseContract(BaseName, ):

    class Meta:
        abstract = True

    num = models.CharField(help_text=_(u"Номер"), max_length=2048, verbose_name=_(u"Номер"), )
    has_trouble_docs = models.NullBooleanField(help_text=_(u"Замечания по документации"), verbose_name=_(u"Замечания по документации"), blank=True, null=True, )


class BaseResult(models.Model):

    class Meta:
        abstract = True

    doc_files = models.ForeignKey(File, help_text=_(u"Предоставленные документы"), null=True, verbose_name=_(u"Предоставленные документы"), blank=True, )
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

    num = models.CharField(max_length=2048, help_text=_(u"Номер платежа"), verbose_name=_(u"Номер платежа"),)
    date = models.DateField(auto_now=True, db_index=True, help_text=_(u"Дата совершения платежа"), verbose_name=_(u"Дата совершения платежа"),)
    amount = models.FloatField(null=True, blank=True, help_text=_(u"Сумма платежа"), verbose_name=_(u"Сумма платежа"),)


class BaseMaterials(models.Model):

    class Meta:
        abstract = True

    floor = models.IntegerField(help_text=_(u"Материал отделки пола"), default=0, blank=True, verbose_name=_(u"Материал отделки пола"), )
    wall = models.IntegerField(help_text=_(u"Материал отделки стен"), default=0, blank=True, verbose_name=_(u"Материал отделки стен") )
    ceiling = models.IntegerField(help_text=_(u"Материал отделки потолка"), default=0, blank=True, verbose_name=_(u"Материал отделки потолка"), )


class BaseEngineerNetworks(models.Model):

    class Meta:
        abstract = True

    water_removal = models.IntegerField(help_text=_(u"Водоотведение"), null=True, blank=True, verbose_name=_(u"Водоотведение"), choices=WATER_REMOVAL_CHOICES , )
    electric_supply = models.IntegerField(help_text=_(u"Электроснабжение"), null=True, blank=True, verbose_name=_(u"Электроснабжение"), choices=ELECTRIC_SUPPLY_CHOICES , )
    gas_supply = models.NullBooleanField(help_text=_(u"Газоснабжение"), blank=True, verbose_name=_(u"Газоснабжение"), choices=GAS_SUPPLY_CHOICES , )


class BaseWaterSupply(BaseEngineerNetworks):

    class Meta:
        abstract = True

    water_settlement = models.IntegerField(help_text=_(u"Водоподведение"), default=0, blank=True, verbose_name=_(u"Водоподведение"), choices=WATER_SETTLEMENT_CHOICES , )
    hot_water_supply = models.IntegerField(help_text=_(u"Горячее водоснабжение"), default=0, blank=True, verbose_name=_(u"Горячее водоснабжение"), choices=HOT_WATER_SUPPLY_CHOICES , )


class BaseSocialObjects(models.Model):

    class Meta:
        abstract = True

    public_transport = models.IntegerField(help_text=_(u"Ближайшая остановка общественного транспорта отдаленность, м"), null=True, verbose_name=_(u"Ближайшая остановка общественного транспорта отдаленность, м"), blank=True, )
    market = models.IntegerField(help_text=_(u"Магазин отдаленность, м"), null=True, verbose_name=_(u"Магазин отдаленность, м"), blank=True, )
    kindergarden = models.IntegerField(help_text=_(u"Детский сад отдаленность, м"), null=True, verbose_name=_(u"Детский сад отдаленность, м"), blank=True, )
    school = models.IntegerField(help_text=_(u"Школа отдаленность, м"), null=True, verbose_name=_(u"Школа отдаленность, м"), blank=True, )
    clinic = models.IntegerField(help_text=_(u"Поликлиника отдаленность, м"), null=True, verbose_name=_(u"Поликлиника отдаленность, м"), blank=True, )


class BaseTerritoryImprovement(models.Model):

    class Meta:
        abstract = True

    is_routes = models.NullBooleanField(help_text=_(u"Подъездные пути"), verbose_name=_(u"Подъездные пути"), blank=True, )
    is_playground = models.NullBooleanField(help_text=_(u"Детская площадка"), verbose_name=_(u"Детская площадка"), blank=True, )
    is_clother_drying = models.NullBooleanField(help_text=_(u"Площадка для сушки белья"), verbose_name=_(u"Площадка для сушки белья"), blank=True, )
    is_parking = models.NullBooleanField(help_text=_(u"Парковка"), verbose_name=_(u"Парковка"), blank=True, )
    is_dustbin_area = models.NullBooleanField(help_text=_(u"Площадка для мусорных контейнеров"), verbose_name=_(u"Площадка для мусорных контейнеров"), blank=True, )


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




class BaseDevices(models.Model):

    class Meta:
        abstract = True

    switches = models.NullBooleanField(help_text=_(u"Выключатели"), verbose_name=_(u"Выключатели"), blank=True, )
    sockets = models.NullBooleanField(help_text=_(u"Розетки"), verbose_name=_(u"Розетки"), blank=True, )
    lamp = models.NullBooleanField(help_text=_(u"Электрическая лампа"), verbose_name=_(u"Электрическая лампа"), blank=True, )
    ceiling_hook = models.NullBooleanField(help_text=_(u"Потолочный крюк"), verbose_name=_(u"Потолочный крюк"), blank=True, )
    heaters = models.NullBooleanField(help_text=_(u"Отопительные приборы"), verbose_name=_(u"Отопительные приборы"), blank=True, )
    smoke_filter = models.NullBooleanField(help_text=_(u"Дымоулавливатель"), verbose_name=_(u"Дымоулавливатель"), blank=True, )
    #not_given = models.NullBooleanField(help_text=_(u"Не указано"), verbose_name=_(u"Не указано"), blank=True, )


# common classes
class BaseRoom(BaseDevices):

    class Meta:
        app_label = "core"
        verbose_name = "Комната"
    def __unicode__(self):
        return '%s' % self.id


class BaseKitchen(BaseDevices):

    class Meta:
        app_label = "core"
        verbose_name = "Кухня"
    def __unicode__(self):
        return '%s' % self.id

    sink_with_mixer = models.NullBooleanField(help_text=_(u"Раковина со смесителем"), verbose_name=_(u"Раковина со смесителем"), blank=True, )


class BaseWC(BaseDevices, ):

    class Meta:
        app_label = "core"
        verbose_name = "Санузел"
    def __unicode__(self):
        return '%s' % self.id

    is_tower_dryer = models.NullBooleanField(help_text=_(u"Полотенцесушитель"), verbose_name=_(u"Полотенцесушитель"), blank=True, )
    is_toilet = models.NullBooleanField(help_text=_(u"Унитаз"), verbose_name=_(u"Унитаз"), blank=True, )
    bath_with_mixer = models.NullBooleanField(help_text=_(u"Ванна со смесителем"), verbose_name=_(u"Ванна со смесителем"), blank=True, )
    sink_with_mixer = models.NullBooleanField(help_text=_(u"Раковина со смесителем"), verbose_name=_(u"Раковина со смесителем"), blank=True, )


class BaseHallway(BaseDevices, ):

    class Meta:
        app_label = "core"
        verbose_name = u"Прихожая"
    def __unicode__(self):
        return '%s' % self.id


class Room(BaseMaterials, BaseRoom):
    class Meta:
        verbose_name = u"Комната"


class Kitchen(BaseMaterials, BaseKitchen):
    stove = models.IntegerField(default=0, blank=True, help_text=_(u"Кухонная плита"), verbose_name=_(u"Кухонная плита"), choices=STOVE_CHOICES)
    class Meta:
        verbose_name = u"Кухня"


class WC(BaseMaterials, BaseWC, ):
    separate = models.IntegerField(default=0, blank=True, help_text=_(u"Санузел"), verbose_name=_(u"Санузел"), choices=SEPARATE_CHOICES)
    class Meta:
        verbose_name = u"Санузел"


class Hallway(BaseMaterials, BaseHallway, ):
    class Meta:
        verbose_name = u"Прихожая"


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
    flats_amount = models.IntegerField(help_text=_(u"Количество однокомнатных квартир (площадью не менее 33 кв. м, стоимостью не более 1 110 450 рублей)"), null=True, verbose_name=_(u"Количество однокомнатных квартир (площадью не менее 33 кв. м, стоимостью не более 1 110 450 рублей)"), blank=True, )
    area = models.IntegerField(help_text=_(u"Общая площадь"), null=True, verbose_name=_(u"Общая площадь"), blank=True, )
    room = models.ForeignKey(Room, null=True, blank=True, )
    wc = models.ForeignKey(WC, null=True, blank=True, )
    hallway = models.ForeignKey(Hallway, null=True, blank=True, )
    kitchen = models.ForeignKey(Kitchen, null=True, blank=True, )


class BaseMultiMaterials(models.Model):

    class Meta:
        abstract = True

    floor = models.CommaSeparatedIntegerField(max_length=256, help_text=_(u"Материал отделки пола"), default=0, blank=True, verbose_name=_(u"Материал отделки пола"))
    wall = models.CommaSeparatedIntegerField(max_length=256, help_text=_(u"Материал отделки стен"), default=0, blank=True, verbose_name=_(u"Материал отделки стен"))
    ceiling = models.CommaSeparatedIntegerField(max_length=256, help_text=_(u"Материал отделки потолка"), default=0, blank=True, verbose_name=_(u"Материал отделки потолка"))


class BaseMultiWaterSupply(BaseEngineerNetworks):

    class Meta:
        abstract = True

    water_settlement = models.CommaSeparatedIntegerField(max_length=256, help_text=_(u"Водоподведение"), null=True, blank=True, verbose_name=_(u"Водоподведение"), )
    hot_water_supply = models.CommaSeparatedIntegerField(max_length=256, help_text=_(u"Горячее водоснабжение"), null=True, blank=True, verbose_name=_(u"Горячее водоснабжение"), )


class AuctionRoom(BaseMultiMaterials, BaseRoom):
    pass


class AuctionKitchen(BaseMultiMaterials, BaseKitchen):
    stove = models.CommaSeparatedIntegerField(max_length=16, null=True, blank=True, help_text=_(u"Кухонная плита"), verbose_name=_(u"Кухонная плита"))


class AuctionWC(BaseMultiMaterials, BaseWC):
    separate = models.CommaSeparatedIntegerField(max_length=16, null=True, blank=True, help_text=_(u"Санузел"), verbose_name=_(u"Санузел"))


class AuctionHallway(BaseMultiMaterials, BaseHallway):
    pass


class BaseAuctionData(BaseMultiWaterSupply, BaseSocialObjects, BaseTerritoryImprovement, ):

    class Meta:
        abstract = True

    flats_amount = models.IntegerField(help_text=_(u"Количество квартир по номеру заказа"), null=True, verbose_name=_(u"Количество квартир по номеру заказа"), blank=True, )
    area = models.IntegerField(help_text=_(u"Площадь квартир по номеру заказа"), null=True, verbose_name=_(u"Площадь квартир по номеру заказа"), blank=True, )
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

    stage = models.IntegerField(help_text=_(u"Этап размещения заказа"), null=True, blank=True, verbose_name=_(u"Этап размещения заказа"), choices=STAGE_CHOICES , )
    start_price = models.FloatField(help_text=_(u"Начальная (максимальная) цена руб."), null=True, verbose_name=_(u"Начальная (максимальная) цена руб."), blank=True, )
    public_date = models.DateField(help_text=_(u"Дата размещения извещения о торгах (Дата опубликования заказа) дд.мм.гггг"), null=True, verbose_name=_(u"Дата размещения извещения о торгах (Дата опубликования заказа) дд.мм.гггг"), blank=True, )
    open_date = models.DateTimeField(help_text=_(u"Дата и время проведения открытого аукциона (последнего события при размещении заказа, при отмене размещения, либо завершении аукциона)"), null=True, verbose_name=_(u"Дата и время проведения открытого аукциона (последнего события при размещении заказа, при отмене размещения, либо завершении аукциона)"), blank=True, )
    proposal_count = models.IntegerField(help_text=_(u"Количество поданных заявок"), verbose_name=_(u"Количество поданных заявок"), blank=True, default=0)

    room = models.ForeignKey(AuctionRoom, null=True, blank=True, )
    wc = models.ForeignKey(AuctionWC, null=True, blank=True, )
    hallway = models.ForeignKey(AuctionHallway, null=True, blank=True, )
    kitchen = models.ForeignKey(AuctionKitchen, null=True, blank=True, )
