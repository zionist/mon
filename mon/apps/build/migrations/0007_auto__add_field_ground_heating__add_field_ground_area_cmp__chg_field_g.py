# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Ground.heating'
        db.add_column(u'build_ground', 'heating',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Ground.area_cmp'
        db.add_column(u'build_ground', 'area_cmp',
                      self.gf('django.db.models.fields.IntegerField')(default=1, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Ground.area'
        db.alter_column(u'build_ground', 'area', self.gf('django.db.models.fields.FloatField')(null=True))
        # Adding field 'Building.heating'
        db.add_column(u'build_building', 'heating',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Building.area_cmp'
        db.add_column(u'build_building', 'area_cmp',
                      self.gf('django.db.models.fields.IntegerField')(default=1, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Building.area'
        db.alter_column(u'build_building', 'area', self.gf('django.db.models.fields.FloatField')(null=True))
        # Adding field 'Contract.heating'
        db.add_column(u'build_contract', 'heating',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Contract.area_cmp'
        db.add_column(u'build_contract', 'area_cmp',
                      self.gf('django.db.models.fields.IntegerField')(default=1, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Contract.area'
        db.alter_column(u'build_contract', 'area', self.gf('django.db.models.fields.FloatField')(null=True))

    def backwards(self, orm):
        # Deleting field 'Ground.heating'
        db.delete_column(u'build_ground', 'heating')

        # Deleting field 'Ground.area_cmp'
        db.delete_column(u'build_ground', 'area_cmp')


        # Changing field 'Ground.area'
        db.alter_column(u'build_ground', 'area', self.gf('django.db.models.fields.IntegerField')(null=True))
        # Deleting field 'Building.heating'
        db.delete_column(u'build_building', 'heating')

        # Deleting field 'Building.area_cmp'
        db.delete_column(u'build_building', 'area_cmp')


        # Changing field 'Building.area'
        db.alter_column(u'build_building', 'area', self.gf('django.db.models.fields.IntegerField')(null=True))
        # Deleting field 'Contract.heating'
        db.delete_column(u'build_contract', 'heating')

        # Deleting field 'Contract.area_cmp'
        db.delete_column(u'build_contract', 'area_cmp')


        # Changing field 'Contract.area'
        db.alter_column(u'build_contract', 'area', self.gf('django.db.models.fields.IntegerField')(null=True))

    models = {
        'build.building': {
            'Meta': {'object_name': 'Building'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'approve_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'area_cmp': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'clinic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'complete_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['build.Contract']", 'null': 'True', 'blank': 'True'}),
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Developer']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'driveways': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'electric_supply': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'entrance_door': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'flat_num': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'flats_amount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'floors': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gas_supply': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hallway': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Hallway']", 'null': 'True', 'blank': 'True'}),
            'heating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hot_water_supply': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_doors': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'is_balcony': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_clother_drying': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_dustbin_area': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_heat_boiler': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_intercom': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_loggia': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_parking': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_playground': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_routes': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_water_boiler': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'kindergarden': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'kitchen': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Kitchen']", 'null': 'True', 'blank': 'True'}),
            'market': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mo.MO']"}),
            'offer': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'payment_perspective': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'permission': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'public_transport': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'readiness': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Room']", 'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'water_removal': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'water_settlement': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'wc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.WC']", 'null': 'True', 'blank': 'True'}),
            'window_constructions': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'build.contract': {
            'Meta': {'object_name': 'Contract'},
            'area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'area_cmp': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'clinic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'creation_form': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Developer']", 'null': 'True', 'blank': 'True'}),
            'docs': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['build.ContractDocuments']", 'null': 'True', 'blank': 'True'}),
            'driveways': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'electric_supply': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'entrance_door': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'flats_amount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'floors': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gas_supply': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hallway': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Hallway']", 'null': 'True', 'blank': 'True'}),
            'has_trouble_docs': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'heating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hot_water_supply': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_doors': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'is_balcony': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_clother_drying': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_dustbin_area': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_heat_boiler': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_intercom': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_loggia': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_parking': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_playground': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_routes': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_water_boiler': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'kindergarden': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'kitchen': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Kitchen']", 'null': 'True', 'blank': 'True'}),
            'market': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mo.MO']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'num': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'period_of_payment': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'public_transport': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Room']", 'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sign_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'summa': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'water_removal': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'water_settlement': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'wc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.WC']", 'null': 'True', 'blank': 'True'}),
            'window_constructions': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'build.contractdocuments': {
            'Meta': {'object_name': 'ContractDocuments'},
            'acceptance_acts': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'approval_citizen_statement': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'building_permissions': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'cost_infos': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'facility_permission': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'hiring_contract': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'land_right_stating': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mo_certificate': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mo_notice_to_citizen': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mun_act_to_fond': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mun_contracts': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'photos': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'protocols': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tec_passport_tec_plan': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'transmission_acts': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'build.ground': {
            'Meta': {'object_name': 'Ground'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'approve_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'area_cmp': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'cad_num': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'cad_passport': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'clinic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'complete_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['build.Contract']", 'null': 'True', 'blank': 'True'}),
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Developer']", 'null': 'True', 'blank': 'True'}),
            'driveways': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'electric_supply': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'entrance_door': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'finish_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'flats_amount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'floors': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gas_supply': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hallway': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Hallway']", 'null': 'True', 'blank': 'True'}),
            'heating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hot_water_supply': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_doors': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'is_balcony': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_clother_drying': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_dustbin_area': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_heat_boiler': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_intercom': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_loggia': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_parking': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_playground': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_routes': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_water_boiler': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'kindergarden': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'kitchen': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Kitchen']", 'null': 'True', 'blank': 'True'}),
            'market': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mo.MO']"}),
            'offer': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'payment_perspective': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'permission': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'public_transport': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'readiness': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Room']", 'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'water_removal': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'water_settlement': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'wc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.WC']", 'null': 'True', 'blank': 'True'}),
            'window_constructions': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
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
            'sink_with_mixer': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
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
            'bath_with_mixer': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'ceiling_hook': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'heaters': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_toilet': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_tower_dryer': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'lamp': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sink_with_mixer': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'smoke_filter': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sockets': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'switches': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        'core.developer': {
            'Meta': {'object_name': 'Developer'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'boss_position': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
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
        },
        'mo.mo': {
            'Meta': {'object_name': 'MO'},
            'common_amount': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'common_economy': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'common_percentage': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'common_spent': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'creation_form': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            'has_trouble': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'home_orphans': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['build']