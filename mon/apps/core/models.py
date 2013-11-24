# -*- coding: utf-8 -*-
import time
from django.db import models
from django.utils.translation import ugettext as _
from apps.imgfile.models import File, Image


STATE_CHOICES  = ((0, _(u'Сданный объект')),  (1, _(u'Строящмйся объект')), (2, _(u'Участок под строительство')))
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

#class BaseModel(models.Model):
#    insert_date = models.DateTimeField(verbose_name=_(u'Created data and time'),
#                                       auto_now_add=True)
#
#    class Meta:
#        abstract = True
#
#
#class BaseBuilding(BaseModel):
#    state = models.SmallIntegerField(verbose_name=_(u'Building state'),
#                                     choices=STATE_CHOICES, default=1)
#
#    class Meta:
#        abstract = True

class BaseName(models.Model):

    class Meta:
        abstract = True
    def __unicode__(self):
        return '%s' % self.id

    name = models.CharField(help_text=_(u"Наименование"), null=True, max_length=2048, verbose_name=_(u"Наименование"), blank=True, )

class BaseModel(models.Model):

    class Meta:
        abstract = True
    def __unicode__(self):
        return '%s' % self.id

    creation_date = models.DateTimeField(auto_now=False, null=True, blank=True, )

class BaseBudget(models.Model):

    class Meta:
        abstract = True
    def __unicode__(self):
        return '%s' % self.id

    sub_sum = models.IntegerField(null=True, blank=True, )
    sub_orph_home = models.IntegerField(null=True, blank=True, )
    adm_coef = models.IntegerField(null=True, blank=True, )

class BaseSubvention(models.Model):

    class Meta:
        abstract = True
    def __unicode__(self):
        return '%s' % self.id

    amount = models.IntegerField(null=True, blank=True, )
    year = models.DateField(null=True, blank=True, )

class BaseDepartamentAgreement(BaseModel, ):

    class Meta:
        abstract = True
    def __unicode__(self):
        return '%s' % self.id

    num = models.IntegerField(null=True, blank=True, )
    date = models.DateField(null=True, blank=True, )
    subvention_performance = models.IntegerField(null=True, blank=True, )

class BaseOrphan(models.Model):

    class Meta:
        abstract = True
    def __unicode__(self):
        return '%s' % self.id

    age = models.IntegerField(blank=True, null=True, choices=STAGE_CHOICES, )
    have_home = models.NullBooleanField(blank=True, )
    is_privilege = models.NullBooleanField(blank=True, )



class BaseDeveloper(BaseName, ):

    class Meta:
        abstract = True
    def __unicode__(self):
        return '%s' % self.id

    face_list = models.IntegerField(null=True, blank=True, )
    address = models.CharField(help_text=_(u"Фактический адрес"), null=True, max_length=2048, verbose_name=_(u"Фактический адрес"), blank=True, )
    phone = models.CharField(help_text=_(u"Контактный телефон"), null=True, max_length=2048, verbose_name=_(u"Контактный телефон"), blank=True, )
    boss_position = models.CharField(help_text=_(u"Ф.И.О. и должность руководителя"), null=True, max_length=2048, verbose_name=_(u"Ф.И.О. и должность руководителя"), blank=True, )


class Developer(BaseDeveloper, ):

    class Meta:
        app_label = "build"
        verbose_name = "Developer"
    def __unicode__(self):
        return '%s' % self.id

    doc = models.ForeignKey(File, )
    image = models.ForeignKey(Image, )


class BasePayment(models.Model):

    class Meta:
        abstract = True
    def __unicode__(self):
        return '%s' % self.id

    amount = models.CharField(max_length=2048, null=True, blank=True, )
    date = models.DateField(null=True, blank=True, )


class BaseMaterials(models.Model):

    class Meta:
        abstract = True
    def __unicode__(self):
        return '%s' % self.id

    floor = models.IntegerField(blank=True, null=True, choices=FLOOR_CHOICES , )
    wall = models.IntegerField(blank=True, null=True, choices=WALL_CHOICES , )
    ceiling = models.IntegerField(blank=True, null=True, choices=CEILING_CHOICES , )


class BaseEngineerNetworks(models.Model):

    class Meta:
        abstract = True
    def __unicode__(self):
        return '%s' % self.id

    water_settlement = models.IntegerField(blank=True, null=True, choices=WATER_SETTLEMENT_CHOICES , )
    hot_water_supply = models.IntegerField(blank=True, null=True, choices=HOT_WATER_SUPPLY_CHOICES , )
    water_removal = models.IntegerField(blank=True, null=True, choices=WATER_REMOVAL_CHOICES , )
    electric_supply = models.IntegerField(blank=True, null=True, choices=ELECTRIC_SUPPLY_CHOICES , )
    gas_supply = models.NullBooleanField(blank=True, )


class BaseSocialObjects(models.Model):

    class Meta:
        abstract = True
    def __unicode__(self):
        return '%s' % self.id

    public_transport = models.IntegerField(null=True, blank=True, )
    market = models.IntegerField(null=True, blank=True, )
    kindergarden = models.IntegerField(null=True, blank=True, )
    school = models.IntegerField(null=True, blank=True, )
    clinic = models.IntegerField(null=True, blank=True, )


class BaseTerritoryImprovement(models.Model):

    class Meta:
        abstract = True
    def __unicode__(self):
        return '%s' % self.id

    is_routes = models.NullBooleanField(blank=True, )
    is_playground = models.NullBooleanField(blank=True, )
    is_clother_drying = models.NullBooleanField(blank=True, )
    is_parking = models.NullBooleanField(blank=True, )
    is_dustbin_area = models.NullBooleanField(blank=True, )


class BaseCommonChars(BaseSocialObjects, BaseEngineerNetworks, BaseTerritoryImprovement):

    class Meta:
        abstract = True
    def __unicode__(self):
        return '%s' % self.id

    is_water_boiler = models.NullBooleanField(blank=True, )
    is_heat_boiler = models.NullBooleanField(blank=True, )
    is_intercom = models.NullBooleanField(blank=True, )
    is_loggia = models.NullBooleanField(blank=True, )
    is_balcony = models.NullBooleanField(blank=True, )
    internal_doors = models.IntegerField(blank=True, null=True, choices=INTERNAL_DOORS_CHOICES , )
    entrance_door = models.IntegerField(blank=True, null=True, choices=ENTRANCE_DOOR_CHOICES , )
    window_constructions = models.IntegerField(blank=True, null=True, choices=WINDOW_CONSTRUCTIONS_CHOICES , )


class BaseDevices(models.Model):

    class Meta:
        abstract = True
    def __unicode__(self):
        return '%s' % self.id

    switches = models.NullBooleanField(blank=True, )
    sockets = models.NullBooleanField(blank=True, )
    lamp = models.NullBooleanField(blank=True, )
    ceiling_hook = models.NullBooleanField(blank=True, )
    heaters = models.NullBooleanField(blank=True, )
    smoke_filter = models.NullBooleanField(blank=True, )
    not_given = models.NullBooleanField(blank=True, )


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

    gas_stove = models.NullBooleanField(blank=True, )
    electrix_stove = models.NullBooleanField(blank=True, )
    sink_with_mixer = models.NullBooleanField(blank=True, )


class WC(BaseMaterials, BaseDevices):

    class Meta:
        app_label = "core"
        verbose_name = "WC"
    def __unicode__(self):
        return '%s' % self.id

    separate = models.IntegerField(blank=True, null=True, choices=SEPARATE_CHOICES , )
    is_tower_dryer = models.NullBooleanField(blank=True, )
    is_toilet = models.NullBooleanField(blank=True, )
    bath_with_mixer = models.NullBooleanField(blank=True, )
    sink_with_mixer = models.NullBooleanField(blank=True, )


class Hallway(BaseMaterials, BaseDevices):

    class Meta:
        app_label = "core"
        verbose_name = "Hallway"
    def __unicode__(self):
        return '%s' % self.id


class BaseBuilding(models.Model):

    class Meta:
        abstract = True
    def __unicode__(self):
        return '%s' % self.id

#    offer = models.ForeignKey(File, help_text=_(u"Коммерческое предложение"),
#        verbose_name=_(u"Коммерческое предложение"), related_name='offer')
#    permission = models.ForeignKey(File, related_name='permission')
    state = models.IntegerField(blank=True, null=True, choices=STATE_CHOICES , )
    address = models.CharField(help_text=_(u"Адрес"), null=True, max_length=2048, verbose_name=_(u"Адрес"), blank=True, )
    comment = models.CharField(max_length=2048, null=True, blank=True, )
    readiness = models.IntegerField(blank=True, null=True, choices=READINESS_CHOICES , )
    payment_perspective = models.IntegerField(null=True, blank=True, choices=PAYMENT_PERSPECTIVE_CHOICES , )
    complete_date = models.DateField(auto_now=True, null=True, blank=True, )


class BaseCompareData(Room, Kitchen, WC, Hallway, BaseCommonChars):

    class Meta:
        abstract = True
    def __unicode__(self):
        return '%s' % self.id

    floors = models.IntegerField(null=True, blank=True, )
    driveways = models.IntegerField(null=True, blank=True, )
    flats_amount = models.IntegerField(null=True, blank=True, )
    area = models.IntegerField(null=True, blank=True, )


class BaseContract(BaseName, ):

    class Meta:
        abstract = True
    def __unicode__(self):
        return '%s' % self.id

    num = models.CharField(help_text=_(u"Номер"), null=True, max_length=2048, verbose_name=_(u"Номер"), blank=True, )


class BaseResult(models.Model):

    class Meta:
        abstract = True
    def __unicode__(self):
        return '%s' % self.id

    doc_files = models.ForeignKey(File, help_text=_(u"Предоставленные документы"), verbose_name=_(u"Предоставленные документы"), )
    doc_list = models.CharField(help_text=_(u"Перечень предоставленных документов"), null=True, max_length=2048, verbose_name=_(u"Перечень предоставленных документов"), blank=True, )
    recommend = models.CharField(help_text=_(u"Рекомендации"), null=True, max_length=2048, verbose_name=_(u"Рекомендации"), blank=True, )
