# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'BaseWC.wc_switches'
        db.delete_column(u'core_basewc', 'wc_switches')


    def backwards(self, orm):
        # Adding field 'BaseWC.wc_switches'
        db.add_column(u'core_basewc', 'wc_switches',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)


    models = {
        u'core.auctionhallway': {
            'Meta': {'object_name': 'AuctionHallway', '_ormbases': ['core.BaseHallway']},
            u'basehallway_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.BaseHallway']", 'unique': 'True', 'primary_key': 'True'}),
            'ceiling': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '0', 'max_length': '256', 'blank': 'True'}),
            'floor': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '0', 'max_length': '256', 'blank': 'True'}),
            'wall': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '0', 'max_length': '256', 'blank': 'True'})
        },
        u'core.auctionkitchen': {
            'Meta': {'object_name': 'AuctionKitchen', '_ormbases': ['core.BaseKitchen']},
            u'basekitchen_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.BaseKitchen']", 'unique': 'True', 'primary_key': 'True'}),
            'ceiling': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '0', 'max_length': '256', 'blank': 'True'}),
            'floor': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '0', 'max_length': '256', 'blank': 'True'}),
            'stove': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'wall': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '0', 'max_length': '256', 'blank': 'True'})
        },
        u'core.auctionroom': {
            'Meta': {'object_name': 'AuctionRoom', '_ormbases': ['core.BaseRoom']},
            u'baseroom_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.BaseRoom']", 'unique': 'True', 'primary_key': 'True'}),
            'ceiling': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '0', 'max_length': '256', 'blank': 'True'}),
            'floor': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '0', 'max_length': '256', 'blank': 'True'}),
            'wall': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '0', 'max_length': '256', 'blank': 'True'})
        },
        u'core.auctionwc': {
            'Meta': {'object_name': 'AuctionWC', '_ormbases': ['core.BaseWC']},
            u'basewc_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.BaseWC']", 'unique': 'True', 'primary_key': 'True'}),
            'ceiling': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '0', 'max_length': '256', 'blank': 'True'}),
            'floor': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '0', 'max_length': '256', 'blank': 'True'}),
            'separate': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'wall': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '0', 'max_length': '256', 'blank': 'True'}),
            'wc_ceiling': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'wc_floor': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'wc_wall': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        'core.basehallway': {
            'Meta': {'object_name': 'BaseHallway'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'core.basekitchen': {
            'Meta': {'object_name': 'BaseKitchen'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sink_with_mixer': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'core.baseroom': {
            'Meta': {'object_name': 'BaseRoom'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'core.basewc': {
            'Meta': {'object_name': 'BaseWC'},
            'bath_with_mixer': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_toilet': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_tower_dryer': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sink_with_mixer': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        u'core.choice': {
            'Meta': {'object_name': 'Choice'},
            'choices': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Choices']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'null': 'True', 'blank': 'True'})
        },
        u'core.choices': {
            'Meta': {'object_name': 'Choices'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'blank': 'True'}),
            'verbose_name': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'})
        },
        'core.developer': {
            'Meta': {'object_name': 'Developer'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'boss_position': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'face_list': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'})
        },
        u'core.hallway': {
            'Meta': {'object_name': 'Hallway', '_ormbases': ['core.BaseHallway']},
            u'basehallway_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.BaseHallway']", 'unique': 'True', 'primary_key': 'True'}),
            'ceiling': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'floor': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'wall': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        u'core.kitchen': {
            'Meta': {'object_name': 'Kitchen', '_ormbases': ['core.BaseKitchen']},
            u'basekitchen_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.BaseKitchen']", 'unique': 'True', 'primary_key': 'True'}),
            'ceiling': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'floor': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'stove': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'wall': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        u'core.resulthallway': {
            'Meta': {'object_name': 'ResultHallway', '_ormbases': [u'core.Hallway']},
            'ceiling_hook': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'hallway_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Hallway']", 'unique': 'True', 'primary_key': 'True'}),
            'heaters': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'lamp': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'smoke_filter': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sockets': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'switches': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        u'core.resultkitchen': {
            'Meta': {'object_name': 'ResultKitchen', '_ormbases': [u'core.Kitchen']},
            'ceiling_hook': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'heaters': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'kitchen_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Kitchen']", 'unique': 'True', 'primary_key': 'True'}),
            'lamp': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'smoke_filter': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sockets': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'switches': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        u'core.resultroom': {
            'Meta': {'object_name': 'ResultRoom', '_ormbases': [u'core.Room']},
            'ceiling_hook': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'heaters': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'lamp': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'room_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Room']", 'unique': 'True', 'primary_key': 'True'}),
            'smoke_filter': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sockets': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'switches': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        u'core.resultwc': {
            'Meta': {'object_name': 'ResultWC', '_ormbases': [u'core.WC']},
            'ceiling_hook': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'heaters': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'lamp': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'smoke_filter': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sockets': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'switches': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'wc_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.WC']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'core.room': {
            'Meta': {'object_name': 'Room', '_ormbases': ['core.BaseRoom']},
            u'baseroom_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.BaseRoom']", 'unique': 'True', 'primary_key': 'True'}),
            'ceiling': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'floor': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'wall': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        u'core.wc': {
            'Meta': {'object_name': 'WC', '_ormbases': ['core.BaseWC']},
            u'basewc_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.BaseWC']", 'unique': 'True', 'primary_key': 'True'}),
            'ceiling': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'floor': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'separate': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'wall': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'wc_ceiling': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'wc_floor': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'wc_wall': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        }
    }

    complete_apps = ['core']