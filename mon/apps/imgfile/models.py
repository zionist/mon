# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _


class BaseImage(models.Model):

    class Meta:
        abstract = True
    def __unicode__(self):
        return '%s' % self.id


class BaseFile(models.Model):

    class Meta:
        abstract = True
    def __unicode__(self):
        return '%s' % self.id


class Image(BaseImage, ):

    class Meta:
        app_label = "imgfile"
        verbose_name = "Image"
    def __unicode__(self):
        return '%s' % self.id


class File(BaseFile, ):

    class Meta:
        app_label = "imgfile"
        verbose_name = "File"
    def __unicode__(self):
        return '%s' % self.id
