# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ResultRoom'
        db.create_table(u'core_resultroom', (
            (u'room_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Room'], unique=True, primary_key=True)),
            ('switches', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('sockets', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('lamp', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('ceiling_hook', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('heaters', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('smoke_filter', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['ResultRoom'])

        # Adding model 'ResultKitchen'
        db.create_table(u'core_resultkitchen', (
            (u'kitchen_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Kitchen'], unique=True, primary_key=True)),
            ('switches', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('sockets', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('lamp', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('ceiling_hook', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('heaters', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('smoke_filter', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['ResultKitchen'])

        # Adding model 'ResultWC'
        db.create_table(u'core_resultwc', (
            (u'wc_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.WC'], unique=True, primary_key=True)),
            ('switches', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('sockets', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('lamp', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('ceiling_hook', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('heaters', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('smoke_filter', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['ResultWC'])

        # Adding model 'ResultHallway'
        db.create_table(u'core_resulthallway', (
            (u'hallway_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Hallway'], unique=True, primary_key=True)),
            ('switches', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('sockets', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('lamp', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('ceiling_hook', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('heaters', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('smoke_filter', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['ResultHallway'])

        # Deleting field 'BaseKitchen.switches'
        db.delete_column(u'core_basekitchen', 'switches')

        # Deleting field 'BaseKitchen.heaters'
        db.delete_column(u'core_basekitchen', 'heaters')

        # Deleting field 'BaseKitchen.lamp'
        db.delete_column(u'core_basekitchen', 'lamp')

        # Deleting field 'BaseKitchen.sockets'
        db.delete_column(u'core_basekitchen', 'sockets')

        # Deleting field 'BaseKitchen.smoke_filter'
        db.delete_column(u'core_basekitchen', 'smoke_filter')

        # Deleting field 'BaseKitchen.ceiling_hook'
        db.delete_column(u'core_basekitchen', 'ceiling_hook')

        # Deleting field 'BaseWC.switches'
        db.delete_column(u'core_basewc', 'switches')

        # Deleting field 'BaseWC.smoke_filter'
        db.delete_column(u'core_basewc', 'smoke_filter')

        # Deleting field 'BaseWC.sockets'
        db.delete_column(u'core_basewc', 'sockets')

        # Deleting field 'BaseWC.heaters'
        db.delete_column(u'core_basewc', 'heaters')

        # Deleting field 'BaseWC.ceiling_hook'
        db.delete_column(u'core_basewc', 'ceiling_hook')

        # Deleting field 'BaseWC.lamp'
        db.delete_column(u'core_basewc', 'lamp')

        # Deleting field 'BaseHallway.switches'
        db.delete_column(u'core_basehallway', 'switches')

        # Deleting field 'BaseHallway.heaters'
        db.delete_column(u'core_basehallway', 'heaters')

        # Deleting field 'BaseHallway.lamp'
        db.delete_column(u'core_basehallway', 'lamp')

        # Deleting field 'BaseHallway.smoke_filter'
        db.delete_column(u'core_basehallway', 'smoke_filter')

        # Deleting field 'BaseHallway.ceiling_hook'
        db.delete_column(u'core_basehallway', 'ceiling_hook')

        # Deleting field 'BaseHallway.sockets'
        db.delete_column(u'core_basehallway', 'sockets')

        # Deleting field 'BaseRoom.switches'
        db.delete_column(u'core_baseroom', 'switches')

        # Deleting field 'BaseRoom.heaters'
        db.delete_column(u'core_baseroom', 'heaters')

        # Deleting field 'BaseRoom.lamp'
        db.delete_column(u'core_baseroom', 'lamp')

        # Deleting field 'BaseRoom.smoke_filter'
        db.delete_column(u'core_baseroom', 'smoke_filter')

        # Deleting field 'BaseRoom.ceiling_hook'
        db.delete_column(u'core_baseroom', 'ceiling_hook')

        # Deleting field 'BaseRoom.sockets'
        db.delete_column(u'core_baseroom', 'sockets')


    def backwards(self, orm):
        # Deleting model 'ResultRoom'
        db.delete_table(u'core_resultroom')

        # Deleting model 'ResultKitchen'
        db.delete_table(u'core_resultkitchen')

        # Deleting model 'ResultWC'
        db.delete_table(u'core_resultwc')

        # Deleting model 'ResultHallway'
        db.delete_table(u'core_resulthallway')

        # Adding field 'BaseKitchen.switches'
        db.add_column(u'core_basekitchen', 'switches',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseKitchen.heaters'
        db.add_column(u'core_basekitchen', 'heaters',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseKitchen.lamp'
        db.add_column(u'core_basekitchen', 'lamp',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseKitchen.sockets'
        db.add_column(u'core_basekitchen', 'sockets',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseKitchen.smoke_filter'
        db.add_column(u'core_basekitchen', 'smoke_filter',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseKitchen.ceiling_hook'
        db.add_column(u'core_basekitchen', 'ceiling_hook',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseWC.switches'
        db.add_column(u'core_basewc', 'switches',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseWC.smoke_filter'
        db.add_column(u'core_basewc', 'smoke_filter',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseWC.sockets'
        db.add_column(u'core_basewc', 'sockets',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseWC.heaters'
        db.add_column(u'core_basewc', 'heaters',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseWC.ceiling_hook'
        db.add_column(u'core_basewc', 'ceiling_hook',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseWC.lamp'
        db.add_column(u'core_basewc', 'lamp',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseHallway.switches'
        db.add_column(u'core_basehallway', 'switches',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseHallway.heaters'
        db.add_column(u'core_basehallway', 'heaters',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseHallway.lamp'
        db.add_column(u'core_basehallway', 'lamp',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseHallway.smoke_filter'
        db.add_column(u'core_basehallway', 'smoke_filter',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseHallway.ceiling_hook'
        db.add_column(u'core_basehallway', 'ceiling_hook',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseHallway.sockets'
        db.add_column(u'core_basehallway', 'sockets',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseRoom.switches'
        db.add_column(u'core_baseroom', 'switches',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseRoom.heaters'
        db.add_column(u'core_baseroom', 'heaters',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseRoom.lamp'
        db.add_column(u'core_baseroom', 'lamp',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseRoom.smoke_filter'
        db.add_column(u'core_baseroom', 'smoke_filter',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseRoom.ceiling_hook'
        db.add_column(u'core_baseroom', 'ceiling_hook',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'BaseRoom.sockets'
        db.add_column(u'core_baseroom', 'sockets',
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
            'sink_with_mixer': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'wc_switches': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
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