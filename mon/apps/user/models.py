# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from apps.cmp.models import MO


class CustomUser(User):

    mo = models.ForeignKey(MO, help_text=_(u"Муниципальное образование"),
                           verbose_name=_(u"муниципальное образование"), blank=True, null=True)

