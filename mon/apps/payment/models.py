# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from apps.core.models import BasePayment
from apps.imgfile.models import File, Image
from apps.cmp.models import Contract
from apps.mo.models import Subvention


class Payment(BasePayment, ):

    class Meta:
        app_label = "payment"
        verbose_name = "Payment"
    def __unicode__(self):
        return '%s' % self.id

    contract = models.ForeignKey(Contract, )
    subvention = models.ForeignKey(Subvention, )
    attribute = models.ForeignKey(File, )
