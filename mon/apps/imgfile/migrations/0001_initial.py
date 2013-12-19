# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Image'
        db.create_table(u'imgfile_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('imgfile', ['Image'])

        # Adding model 'File'
        db.create_table(u'imgfile_file', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=2048, null=True, blank=True)),
        ))
        db.send_create_signal('imgfile', ['File'])


    def backwards(self, orm):
        # Deleting model 'Image'
        db.delete_table(u'imgfile_image')

        # Deleting model 'File'
        db.delete_table(u'imgfile_file')


    models = {
        'imgfile.file': {
            'Meta': {'object_name': 'File'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'imgfile.image': {
            'Meta': {'object_name': 'Image'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['imgfile']