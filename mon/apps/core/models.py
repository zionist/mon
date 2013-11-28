# -*- coding: utf-8 -*-
import time
from django.db import models
from django.utils.translation import ugettext as _
from apps.imgfile.models import File, Image


STATE_CHOICES  = ((0, _(u'Сданный объект')),  (1, _(u'Строящийся объект')), (2, _(u'Участок под строительство')))
READINESS_CHOICES  = ((0, _(u'Фундаментные работы')),  (1, _(u'Строительно-монтажные работы (указать этаж)')), (2, _(u'Санитарно-технические работы')), (3, _(u'Отделочные работы')),   (4, _(u'Работы по благоустройству территории')))
FLOOR_CHOICES  = ((0, _(u'Ламинат')),  (1, _(u'Паркет')),  (2, _(u'Линолеум')), (3, _(u'Плитка')),   (4, _(u'Не указано')))
WALL_CHOICES  = ((0, _(u'Обои')),  (1, _(u'Водоэмульсионная краска')),  (2, _(u'Штукатурка')), (3, _(u'Плитка')),   (4, _(u'Не указано')))
CEILING_CHOICES  = ((0, _(u'Натяжной')),  (1, _(u'Штукатурка')),  (2, _(u'Не указано')))
INTERNAL_DOORS_CHOICES  = ((0, _(u'Деревянные')),  (1, _(u'Пластиковые')),  (2, _(u'Не указано')))
ENTRANCE_DOOR_CHOICES  = ((0, _(u'Деревянные')),  (1, _(u'Пластиковые')),  (2, _(u'Не указано')))
WINDOW_CONSTRUCTIONS_CHOICES  = ((0, _(u'Деревянные')),  (1, _(u'Пластиковые стеклопакеты')),  (2, _(u'Не указано')))
WATER_SETTLEMENT_CHOICES  = ((0, _(u'Центральное')),  (1, _(u'Индивидуальное')))
HOT_WATER_SUPPLY_CHOICES  = ((0, _(u'Центральное')),  (1, _(u'Индивидуальное')))
WATER_REMOVAL_CHOICES  = ((0, _(u'Центральное')),  (1, _(u'Индивидуальное')))
ELECTRIC_SUPPLY_CHOICES  = ((0, _(u'Центральное')),  (1, _(u'Индивидуальное')))
GAS_SUPPLY_CHOICES  = ((0, _(u'Центральное')),  (1, _(u'Индивидуальное')))
CREATION_FORM_CHOICES  = ((0, _(u'Приобретение')),  (1, _(u'Долевое строительство')), (2, _(u'Строительство')),)
SEPARATE_CHOICES  = ((0, _(u'Совместный')),  (1, _(u'Раздельный')),)
STAGE_CHOICES = ((0, _(u'Подача заявок')),  (1, _(u'Работа комиссии')), (2, _(u'Размещение завершено, аукцион признан несостоявшимся, не допущена ни одна заявка')), (3, _(u'Размещение завершено, аукцион признан несостоявшимся, не подана ни одна заявка')), (4, _(u'Заключен контракт')), (5, _(u'Размещение отменено')))
PAYMENT_PERSPECTIVE_CHOICES = ((0, _(u'Перспективы освоения денежных средств, выделенных на текущий год. Без дополнительного финансирования')),   (1, _(u'Перспективы освоения ДОПОЛНИТЕЛЬНЫХ денежных средств, в текущем году.')),  (2, _(u'Перспективы освоения денежных средств в планируемом году.')))

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
    sub_orph_home = models.IntegerField(help_text=_(u"Размер субвенции, выделенной на предоставление жилых помещений детям сиротам"), null=True, verbose_name=_(u"Размер субвенции, выделенной на предоставление жилых помещений детям сиротам"), blank=True, )
    adm_coef = models.IntegerField(help_text=_(u"Размер коэффициента на администрирование расходов"), null=True, verbose_name=_(u"Размер коэффициента на администрирование расходов"), blank=True, )


class BaseSubvention(models.Model):

    class Meta:
        abstract = True

    date = models.DateField(null=True, blank=True, )
    amount = models.IntegerField(help_text=_(u"Общая сумма субвенции"), null=True, verbose_name=_(u"Общая сумма субвенции"), blank=True, )


class BaseDepartamentAgreement(BaseModel, ):

    class Meta:
        abstract = True

    date = models.DateField(help_text=_(u"Дата"), null=True, verbose_name=_(u"Дата"), blank=True, )
    num = models.IntegerField(help_text=_(u"Номер"), null=True, verbose_name=_(u"Номер"), blank=True, )
    subvention_performance = models.IntegerField(help_text=_(u"Показатель результативности предоставления субвенции (количество детей-сирот, подлежащих обеспечению жилыми человек заполнение помещениями в текущем году)"), null=True, verbose_name=_(u"Показатель результативности предоставления субвенции (количество детей-сирот, подлежащих обеспечению жилыми человек заполнение помещениями в текущем году)"), blank=True, )


class BaseOrphan(models.Model):

    class Meta:
        abstract = True

    age = models.IntegerField(blank=True, null=True, choices=STAGE_CHOICES , )
    have_home = models.NullBooleanField(blank=True, )
    is_privilege = models.NullBooleanField(blank=True, )


class BaseBuilding(models.Model):

    class Meta:
        abstract = True

#    offer = models.ForeignKey(File, help_text=_(u"Коммерческое предложение"), null=True, verbose_name=_(u"Коммерческое предложение"), blank=True, related_name='offer')
#    permission = models.ForeignKey(File, help_text=_(u"Разрешение"), null=True, verbose_name=_(u"Разрешение"), blank=True, related_name='permission')
    state = models.IntegerField(help_text=_(u"Состояние"), verbose_name=_(u"Состояние"), choices=STATE_CHOICES , )
    address = models.TextField(help_text=_(u"Адрес"), null=True, verbose_name=_(u"Адрес"), blank=True, )
    complete_date = models.DateField(help_text=_(u"Срок сдачи в эксплуатацию"), null=True, verbose_name=_(u"Срок сдачи в эксплуатацию"), blank=True, )
    comment = models.TextField(help_text=_(u"Комментарий"), null=True, verbose_name=_(u"Комментарий"), blank=True, )
    readiness = models.IntegerField(help_text=_(u"Степень готовности"), null=True, blank=True, verbose_name=_(u"Степень готовности"), choices=READINESS_CHOICES , )
    payment_perspective = models.IntegerField(help_text=_(u"Перспектива освоения"), null=True, blank=True, verbose_name=_(u"Перспектива осноения"), choices=PAYMENT_PERSPECTIVE_CHOICES , )


class BaseContract(BaseName, ):

    class Meta:
        abstract = True

    num = models.CharField(help_text=_(u"Номер"), null=True, max_length=2048, verbose_name=_(u"Номер"), blank=True, )


class BaseResult(models.Model):

    class Meta:
        abstract = True

    doc_files = models.ForeignKey(File, help_text=_(u"Предоставленные документы"), null=True, verbose_name=_(u"Предоставленные документы"), blank=True, )
    check_date = models.DateField(help_text=_(u"Дата проверки"), null=True, verbose_name=_(u"Дата проверки"), blank=True, )
    doc_list = models.CharField(help_text=_(u"Перечень предоставленных документов"), null=True, max_length=2048, verbose_name=_(u"Перечень предоставленных документов"), blank=True, )
    recommend = models.CharField(help_text=_(u"Рекомендации"), null=True, max_length=2048, verbose_name=_(u"Рекомендации"), blank=True, )


class BaseImage(models.Model):

    class Meta:
        abstract = True

    image = models.FileField(max_length=2048, null=True, blank=True, )


class BaseFile(models.Model):

    class Meta:
        abstract = True

    file = models.FileField(max_length=2048, null=True, blank=True, )


class BaseDeveloper(BaseName, ):

    class Meta:
        abstract = True

    face_list = models.IntegerField(help_text=_(u"Юридическое лицо/Физическое лицо"), null=True, verbose_name=_(u"Юридическое лицо/Физическое лицо"), blank=True, )
    address = models.CharField(help_text=_(u"Фактический адрес"), null=True, max_length=2048, verbose_name=_(u"Фактический адрес"), blank=True, )
    phone = models.CharField(help_text=_(u"Контактный телефон"), null=True, max_length=2048, verbose_name=_(u"Контактный телефон"), blank=True, )
    boss_position = models.CharField(help_text=_(u"Ф.И.О. и должность руководителя"), null=True, max_length=2048, verbose_name=_(u"Ф.И.О. и должность руководителя"), blank=True, )


class BasePayment(models.Model):

    class Meta:
        abstract = True

    date = models.DateField(null=True, blank=True, )
    amount = models.CharField(max_length=2048, null=True, blank=True, )


class BaseMaterials(models.Model):

    class Meta:
        abstract = True

    floor = models.IntegerField(help_text=_(u"Материал отделки пола"), null=True, blank=True, verbose_name=_(u"Материал отделки пола"), choices=FLOOR_CHOICES , )
    wall = models.IntegerField(help_text=_(u"Материал отделки стен"), null=True, blank=True, verbose_name=_(u"Материал отделки стен"), choices=WALL_CHOICES , )
    ceiling = models.IntegerField(help_text=_(u"Материал отделки потолка"), null=True, blank=True, verbose_name=_(u"Материал отделки потолка"), choices=CEILING_CHOICES , )


class BaseEngineerNetworks(models.Model):

    class Meta:
        abstract = True

    water_settlement = models.IntegerField(help_text=_(u"Водоподведение"), null=True, blank=True, verbose_name=_(u"Водоподведение"), choices=WATER_SETTLEMENT_CHOICES , )
    hot_water_supply = models.IntegerField(help_text=_(u"Горячее водоснабжение"), null=True, blank=True, verbose_name=_(u"Горячее водоснабжение"), choices=HOT_WATER_SUPPLY_CHOICES , )
    water_removal = models.IntegerField(help_text=_(u"Водоотведение"), null=True, blank=True, verbose_name=_(u"Водоотведение"), choices=WATER_REMOVAL_CHOICES , )
    electric_supply = models.IntegerField(help_text=_(u"Электроснабжение"), null=True, blank=True, verbose_name=_(u"Электроснабжение"), choices=ELECTRIC_SUPPLY_CHOICES , )
    gas_supply = models.NullBooleanField(help_text=_(u"Газоснабжение"), blank=True, verbose_name=_(u"Газоснабжение"), choices=GAS_SUPPLY_CHOICES , )


class BaseSocialObjects(models.Model):

    class Meta:
        abstract = True

    public_transport = models.IntegerField(help_text=_(u"Ближайшая остановка общественного транспорта"), null=True, verbose_name=_(u"Ближайшая остановка общественного транспорта"), blank=True, )
    market = models.IntegerField(help_text=_(u"Магазин"), null=True, verbose_name=_(u"Магазин"), blank=True, )
    kindergarden = models.IntegerField(help_text=_(u"Детский сад"), null=True, verbose_name=_(u"Детский сад"), blank=True, )
    school = models.IntegerField(help_text=_(u"Школа"), null=True, verbose_name=_(u"Школа"), blank=True, )
    clinic = models.IntegerField(help_text=_(u"Поликлиника"), null=True, verbose_name=_(u"Поликлиника"), blank=True, )


class BaseTerritoryImprovement(models.Model):

    class Meta:
        abstract = True

    is_routes = models.NullBooleanField(help_text=_(u"Подъездные"), verbose_name=_(u"Подъездные"), blank=True, )
    is_playground = models.NullBooleanField(help_text=_(u"Детская площадка"), verbose_name=_(u"Детская площадка"), blank=True, )
    is_clother_drying = models.NullBooleanField(help_text=_(u"Площадка для сушки белья"), verbose_name=_(u"Площадка для сушки белья"), blank=True, )
    is_parking = models.NullBooleanField(help_text=_(u"Парковка"), verbose_name=_(u"Парковка"), blank=True, )
    is_dustbin_area = models.NullBooleanField(help_text=_(u"Площадка для мусорных контейнеров"), verbose_name=_(u"Площадка для мусорных контейнеров"), blank=True, )


class BaseCommonChars(BaseEngineerNetworks, BaseSocialObjects, BaseTerritoryImprovement, ):

    class Meta:
        abstract = True

    is_water_boiler = models.NullBooleanField(help_text=_(u"Водонагревательный прибор (бойлер)"), verbose_name=_(u"Водонагревательный прибор (бойлер)"), blank=True, )
    is_heat_boiler = models.NullBooleanField(help_text=_(u"Отопительный котел"), verbose_name=_(u"Отопительный котел"), blank=True, )
    is_intercom = models.NullBooleanField(help_text=_(u"Домофон"), verbose_name=_(u"Домофон"), blank=True, )
    is_loggia = models.NullBooleanField(help_text=_(u"Наличие лоджии"), verbose_name=_(u"Наличие лоджии"), blank=True, )
    is_balcony = models.NullBooleanField(help_text=_(u"Наличие балкона"), verbose_name=_(u"Наличие балкона"), blank=True, )
    internal_doors = models.IntegerField(help_text=_(u"Материал межкомнатных дверей"), null=True, blank=True, verbose_name=_(u"Материал межкомнатных дверей"), choices=INTERNAL_DOORS_CHOICES , )
    entrance_door = models.IntegerField(help_text=_(u"Материал входной двери"), null=True, blank=True, verbose_name=_(u"Материал входной двери"), choices=ENTRANCE_DOOR_CHOICES , )
    window_constructions = models.IntegerField(help_text=_(u"Материал оконных конструкций"), null=True, blank=True, verbose_name=_(u"Материал оконных конструкций"), choices=WINDOW_CONSTRUCTIONS_CHOICES , )


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
class Room(BaseMaterials, BaseDevices):

    class Meta:
        app_label = "core"
        verbose_name = "Room"
    def __unicode__(self):
        return '%s' % self.id


class Kitchen(BaseMaterials, BaseDevices):

    class Meta:
        app_label = "core"
        verbose_name = "Kitchen"
    def __unicode__(self):
        return '%s' % self.id

    gas_stove = models.NullBooleanField(help_text=_(u"Газовая кухонная плита"), verbose_name=_(u"Газовая кухонная плита"), blank=True, )
    electrix_stove = models.NullBooleanField(help_text=_(u"Электрическая кухонная плита"), verbose_name=_(u"Электрическая кухонная плита"), blank=True, )
    sink_with_mixer = models.NullBooleanField(help_text=_(u"Раковина со смесителем"), verbose_name=_(u"Раковина со смесителем"), blank=True, )


class WC(BaseMaterials, BaseDevices, ):

    class Meta:
        app_label = "core"
        verbose_name = "WC"
    def __unicode__(self):
        return '%s' % self.id

    separate = models.IntegerField(help_text=_(u"Санузел"), null=True, blank=True, verbose_name=_(u"Санузел"), choices=SEPARATE_CHOICES , )
    is_tower_dryer = models.NullBooleanField(help_text=_(u"Полотенцесушитель"), verbose_name=_(u"Полотенцесушитель"), blank=True, )
    is_toilet = models.NullBooleanField(help_text=_(u"Унитаз"), verbose_name=_(u"Унитаз"), blank=True, )
    bath_with_mixer = models.NullBooleanField(help_text=_(u"Ванна со смесителем"), verbose_name=_(u"Ванна со смесителем"), blank=True, )
    sink_with_mixer = models.NullBooleanField(help_text=_(u"Раковина со смесителем"), verbose_name=_(u"Раковина со смесителем"), blank=True, )


class Hallway(BaseMaterials, BaseDevices, ):

    class Meta:
        app_label = "core"
        verbose_name = "Hallway"
    def __unicode__(self):
        return '%s' % self.id


class Developer(BaseDeveloper, ):

    class Meta:
        app_label = "core"
        verbose_name = "Developer"
    def __unicode__(self):
        return '%s' % self.id

    doc = models.ForeignKey(File, null=True, blank=True, )
    image = models.ForeignKey(Image, null=True, blank=True, )


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
