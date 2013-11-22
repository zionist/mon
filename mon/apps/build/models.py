# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from apps.core.models import BaseModel, BaseBuilding


class Building(BaseBuilding):
    address = models.CharField(verbose_name=_(u'Address'), max_length=300, blank=True, null=True)

    class Meta:
        app_label = 'build'
        verbose_name = _(u'Building')
        verbose_name_plural = _(u'Buildings')

    def __unicode__(self):
        return '%s' % self.address


class Ground(BaseBuilding):
    cad_number = models.CharField(verbose_name=_(u'Cadastral number'), max_length=300, unique=True)

    class Meta:
        app_label = 'build'
        verbose_name = _(u'Ground')
        verbose_name_plural = _(u'Grounds')

    def __unicode__(self):
        return '%s' % self.cad_number
