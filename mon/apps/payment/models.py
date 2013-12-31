# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from apps.core.models import BasePayment
from apps.imgfile.models import File, Image, BaseImage
from apps.cmp.models import Contract
from apps.mo.models import Subvention
from apps.user.models import CustomUser


class Payment(BasePayment, BaseImage):

    class Meta:
        app_label = "payment"
        verbose_name = "Payment"
    def __unicode__(self):
        return '%s: %s' % (self.date, self.amount)

    contract = models.ForeignKey(Contract, help_text=_(u"Данные по заключенному контракту"),
                                 verbose_name=_(u"Данные по заключенному контракту"), )
    subvention = models.ForeignKey(Subvention, help_text=_(u"Данные по расходуемой субвенции"),
                                   verbose_name=_(u"Данные по расходуемой субвенции"),)
    pay_order = models.ImageField(null=True, blank=True, upload_to='img_files', help_text=_(u"Платежное поручение"),
                                  verbose_name=_(u"Платежное поручение"), )
    owner = models.ForeignKey(CustomUser, null=True, blank=True,
                              help_text=_(u"Владелец платежа"),
                              verbose_name=_(u"Владелец платежа"))
