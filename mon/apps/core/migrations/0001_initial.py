# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BaseRoom'
        db.create_table(u'core_baseroom', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('switches', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('sockets', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('lamp', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('ceiling_hook', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('heaters', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('smoke_filter', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('core', ['BaseRoom'])

        # Adding model 'BaseKitchen'
        db.create_table(u'core_basekitchen', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('switches', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('sockets', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('lamp', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('ceiling_hook', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('heaters', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('smoke_filter', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('sink_with_mixer', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('core', ['BaseKitchen'])

        # Adding model 'BaseWC'
        db.create_table(u'core_basewc', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('switches', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('sockets', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('lamp', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('ceiling_hook', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('heaters', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('smoke_filter', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('is_tower_dryer', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('is_toilet', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('bath_with_mixer', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('sink_with_mixer', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('core', ['BaseWC'])

        # Adding model 'BaseHallway'
        db.create_table(u'core_basehallway', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('switches', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('sockets', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('lamp', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('ceiling_hook', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('heaters', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('smoke_filter', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('core', ['BaseHallway'])

        # Adding model 'Room'
        db.create_table(u'core_room', (
            (u'baseroom_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseRoom'], unique=True, primary_key=True)),
            ('floor', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('wall', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('ceiling', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal(u'core', ['Room'])

        # Adding model 'Kitchen'
        db.create_table(u'core_kitchen', (
            (u'basekitchen_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseKitchen'], unique=True, primary_key=True)),
            ('floor', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('wall', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('ceiling', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('stove', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal(u'core', ['Kitchen'])

        # Adding model 'WC'
        db.create_table(u'core_wc', (
            (u'basewc_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseWC'], unique=True, primary_key=True)),
            ('floor', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('wall', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('ceiling', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('separate', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal(u'core', ['WC'])

        # Adding model 'Hallway'
        db.create_table(u'core_hallway', (
            (u'basehallway_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseHallway'], unique=True, primary_key=True)),
            ('floor', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('wall', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('ceiling', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal(u'core', ['Hallway'])

        # Adding model 'Developer'
        db.create_table(u'core_developer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=2048, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=2048, null=True, blank=True)),
            ('face_list', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=2048, null=True, blank=True)),
            ('boss_position', self.gf('django.db.models.fields.CharField')(max_length=2048, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Developer'])

        # Adding model 'AuctionRoom'
        db.create_table(u'core_auctionroom', (
            (u'baseroom_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseRoom'], unique=True, primary_key=True)),
            ('floor', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default=0, max_length=256, blank=True)),
            ('wall', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default=0, max_length=256, blank=True)),
            ('ceiling', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default=0, max_length=256, blank=True)),
        ))
        db.send_create_signal(u'core', ['AuctionRoom'])

        # Adding model 'AuctionKitchen'
        db.create_table(u'core_auctionkitchen', (
            (u'basekitchen_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseKitchen'], unique=True, primary_key=True)),
            ('floor', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default=0, max_length=256, blank=True)),
            ('wall', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default=0, max_length=256, blank=True)),
            ('ceiling', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default=0, max_length=256, blank=True)),
            ('stove', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=16, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['AuctionKitchen'])

        # Adding model 'AuctionWC'
        db.create_table(u'core_auctionwc', (
            (u'basewc_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseWC'], unique=True, primary_key=True)),
            ('floor', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default=0, max_length=256, blank=True)),
            ('wall', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default=0, max_length=256, blank=True)),
            ('ceiling', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default=0, max_length=256, blank=True)),
            ('separate', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=16, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['AuctionWC'])

        # Adding model 'AuctionHallway'
        db.create_table(u'core_auctionhallway', (
            (u'basehallway_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.BaseHallway'], unique=True, primary_key=True)),
            ('floor', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default=0, max_length=256, blank=True)),
            ('wall', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default=0, max_length=256, blank=True)),
            ('ceiling', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default=0, max_length=256, blank=True)),
        ))
        db.send_create_signal(u'core', ['AuctionHallway'])


    def backwards(self, orm):
        # Deleting model 'BaseRoom'
        db.delete_table(u'core_baseroom')

        # Deleting model 'BaseKitchen'
        db.delete_table(u'core_basekitchen')

        # Deleting model 'BaseWC'
        db.delete_table(u'core_basewc')

        # Deleting model 'BaseHallway'
        db.delete_table(u'core_basehallway')

        # Deleting model 'Room'
        db.delete_table(u'core_room')

        # Deleting model 'Kitchen'
        db.delete_table(u'core_kitchen')

        # Deleting model 'WC'
        db.delete_table(u'core_wc')

        # Deleting model 'Hallway'
        db.delete_table(u'core_hallway')

        # Deleting model 'Developer'
        db.delete_table(u'core_developer')

        # Deleting model 'AuctionRoom'
        db.delete_table(u'core_auctionroom')

        # Deleting model 'AuctionKitchen'
        db.delete_table(u'core_auctionkitchen')

        # Deleting model 'AuctionWC'
        db.delete_table(u'core_auctionwc')

        # Deleting model 'AuctionHallway'
        db.delete_table(u'core_auctionhallway')


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
            'wall': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '0', 'max_length': '256', 'blank': 'True'})
        },
        'core.basehallway': {
            'Meta': {'object_name': 'BaseHallway'},
            'ceiling_hook': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'heaters': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lamp': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'smoke_filter': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sockets': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'switches': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        'core.basekitchen': {
            'Meta': {'object_name': 'BaseKitchen'},
            'ceiling_hook': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'heaters': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lamp': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sink_with_mixer': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'smoke_filter': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sockets': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'switches': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        'core.baseroom': {
            'Meta': {'object_name': 'BaseRoom'},
            'ceiling_hook': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'heaters': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lamp': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'smoke_filter': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sockets': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'switches': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        'core.basewc': {
            'Meta': {'object_name': 'BaseWC'},
            'bath_with_mixer': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'ceiling_hook': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'heaters': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_toilet': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_tower_dryer': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'lamp': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sink_with_mixer': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'smoke_filter': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sockets': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'switches': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        'core.developer': {
            'Meta': {'object_name': 'Developer'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'boss_position': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'face_list': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
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
            'wall': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        }
    }

    complete_apps = ['core']