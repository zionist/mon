# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from apps.mo.models import MO

DATE_CHOICES = ((0, ''), (1, '2012'), (2, '2013'), (3, '2014'),
                (4, '2015'), (5, '2016'), (6, '2017'),
                (7, '2018'), (8, '2019'), (9, '2020'))
DICT_DATE_CHOICES = dict(DATE_CHOICES)


class CustomUser(User):

    mo = models.ForeignKey(MO, help_text=_(u"Муниципальное образование"),
        verbose_name=_(u"муниципальное образование"), blank=True, null=True)
    date = models.PositiveSmallIntegerField(verbose_name=_(u"Дата для фильтра"), blank=True, null=True,
        choices=DATE_CHOICES)

    def get_user_date(self):
        if not self.date or self.date == 0:
            return None
        dat = int(DICT_DATE_CHOICES.get(self.date))
        return datetime(dat, 01, 01)

    def show_user_date(self):
        if not self.date or self.date == 0:
            return _(u"Не указано")
        return DICT_DATE_CHOICES.get(self.date)
