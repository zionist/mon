# -*- coding: utf-8 -*-
import time
from django.db import models
from django.utils.translation import ugettext as _

BUILD_STATES = (
    (0, _(u'Is not finished')),
    (1, _(u'Is finished')),
    (2, _(u'Is ground')),
)


class BaseModel(models.Model):
    insert_date = models.DateTimeField(verbose_name=_(u'Created data and time'),
                                       auto_now_add=True)

    class Meta:
        abstract = True


class BaseBuilding(BaseModel):
    state = models.SmallIntegerField(verbose_name=_(u'Building state'),
                                     choices=BUILD_STATES, default=0)

    class Meta:
        abstract = True
