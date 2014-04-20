# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'CopyContract.is_intercom'
        db.delete_column(u'build_copycontract', 'is_intercom')

        # Deleting field 'CopyContract.hot_water_supply'
        db.delete_column(u'build_copycontract', 'hot_water_supply')

        # Deleting field 'CopyContract.clinic'
        db.delete_column(u'build_copycontract', 'clinic')

        # Deleting field 'CopyContract.floors'
        db.delete_column(u'build_copycontract', 'floors')

        # Deleting field 'CopyContract.market'
        db.delete_column(u'build_copycontract', 'market')

        # Deleting field 'CopyContract.is_heat_boiler'
        db.delete_column(u'build_copycontract', 'is_heat_boiler')

        # Deleting field 'CopyContract.electric_supply'
        db.delete_column(u'build_copycontract', 'electric_supply')

        # Deleting field 'CopyContract.kindergarden'
        db.delete_column(u'build_copycontract', 'kindergarden')

        # Deleting field 'CopyContract.is_playground'
        db.delete_column(u'build_copycontract', 'is_playground')

        # Deleting field 'CopyContract.water_settlement'
        db.delete_column(u'build_copycontract', 'water_settlement')

        # Deleting field 'CopyContract.school'
        db.delete_column(u'build_copycontract', 'school')

        # Deleting field 'CopyContract.room'
        db.delete_column(u'build_copycontract', 'room_id')

        # Deleting field 'CopyContract.internal_doors'
        db.delete_column(u'build_copycontract', 'internal_doors')

        # Deleting field 'CopyContract.driveways'
        db.delete_column(u'build_copycontract', 'driveways')

        # Deleting field 'CopyContract.public_transport'
        db.delete_column(u'build_copycontract', 'public_transport')

        # Deleting field 'CopyContract.is_clother_drying'
        db.delete_column(u'build_copycontract', 'is_clother_drying')

        # Deleting field 'CopyContract.is_routes'
        db.delete_column(u'build_copycontract', 'is_routes')

        # Deleting field 'CopyContract.water_removal'
        db.delete_column(u'build_copycontract', 'water_removal')

        # Deleting field 'CopyContract.budget'
        db.delete_column(u'build_copycontract', 'budget')

        # Deleting field 'CopyContract.entrance_door'
        db.delete_column(u'build_copycontract', 'entrance_door')

        # Deleting field 'CopyContract.gas_supply'
        db.delete_column(u'build_copycontract', 'gas_supply')

        # Deleting field 'CopyContract.is_balcony'
        db.delete_column(u'build_copycontract', 'is_balcony')

        # Deleting field 'CopyContract.window_constructions'
        db.delete_column(u'build_copycontract', 'window_constructions')

        # Deleting field 'CopyContract.hallway'
        db.delete_column(u'build_copycontract', 'hallway_id')

        # Deleting field 'CopyContract.wc'
        db.delete_column(u'build_copycontract', 'wc_id')

        # Deleting field 'CopyContract.is_dustbin_area'
        db.delete_column(u'build_copycontract', 'is_dustbin_area')

        # Deleting field 'CopyContract.kitchen'
        db.delete_column(u'build_copycontract', 'kitchen_id')

        # Deleting field 'CopyContract.is_parking'
        db.delete_column(u'build_copycontract', 'is_parking')

        # Deleting field 'CopyContract.heating'
        db.delete_column(u'build_copycontract', 'heating')

        # Deleting field 'CopyContract.area_cmp'
        db.delete_column(u'build_copycontract', 'area_cmp')

        # Deleting field 'CopyContract.is_loggia'
        db.delete_column(u'build_copycontract', 'is_loggia')

        # Deleting field 'CopyContract.is_water_boiler'
        db.delete_column(u'build_copycontract', 'is_water_boiler')

        # Adding field 'CopyContract.docs'
        db.add_column(u'build_copycontract', 'docs',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['build.ContractDocuments'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.address'
        db.add_column(u'build_copycontract', 'address',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'CopyContract.is_intercom'
        db.add_column(u'build_copycontract', 'is_intercom',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.hot_water_supply'
        db.add_column(u'build_copycontract', 'hot_water_supply',
                      self.gf('django.db.models.fields.IntegerField')(default=0, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.clinic'
        db.add_column(u'build_copycontract', 'clinic',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.floors'
        db.add_column(u'build_copycontract', 'floors',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.market'
        db.add_column(u'build_copycontract', 'market',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.is_heat_boiler'
        db.add_column(u'build_copycontract', 'is_heat_boiler',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.electric_supply'
        db.add_column(u'build_copycontract', 'electric_supply',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.kindergarden'
        db.add_column(u'build_copycontract', 'kindergarden',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.is_playground'
        db.add_column(u'build_copycontract', 'is_playground',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.water_settlement'
        db.add_column(u'build_copycontract', 'water_settlement',
                      self.gf('django.db.models.fields.IntegerField')(default=0, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.school'
        db.add_column(u'build_copycontract', 'school',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.room'
        db.add_column(u'build_copycontract', 'room',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Room'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.internal_doors'
        db.add_column(u'build_copycontract', 'internal_doors',
                      self.gf('django.db.models.fields.IntegerField')(default=0, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.driveways'
        db.add_column(u'build_copycontract', 'driveways',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.public_transport'
        db.add_column(u'build_copycontract', 'public_transport',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.is_clother_drying'
        db.add_column(u'build_copycontract', 'is_clother_drying',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.is_routes'
        db.add_column(u'build_copycontract', 'is_routes',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.water_removal'
        db.add_column(u'build_copycontract', 'water_removal',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.budget'
        db.add_column(u'build_copycontract', 'budget',
                      self.gf('django.db.models.fields.SmallIntegerField')(null=True),
                      keep_default=False)

        # Adding field 'CopyContract.entrance_door'
        db.add_column(u'build_copycontract', 'entrance_door',
                      self.gf('django.db.models.fields.IntegerField')(default=0, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.gas_supply'
        db.add_column(u'build_copycontract', 'gas_supply',
                      self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.is_balcony'
        db.add_column(u'build_copycontract', 'is_balcony',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.window_constructions'
        db.add_column(u'build_copycontract', 'window_constructions',
                      self.gf('django.db.models.fields.IntegerField')(default=0, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.hallway'
        db.add_column(u'build_copycontract', 'hallway',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Hallway'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.wc'
        db.add_column(u'build_copycontract', 'wc',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.WC'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.is_dustbin_area'
        db.add_column(u'build_copycontract', 'is_dustbin_area',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.kitchen'
        db.add_column(u'build_copycontract', 'kitchen',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Kitchen'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.is_parking'
        db.add_column(u'build_copycontract', 'is_parking',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.heating'
        db.add_column(u'build_copycontract', 'heating',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.area_cmp'
        db.add_column(u'build_copycontract', 'area_cmp',
                      self.gf('django.db.models.fields.IntegerField')(default=1, null=True),
                      keep_default=False)

        # Adding field 'CopyContract.is_loggia'
        db.add_column(u'build_copycontract', 'is_loggia',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyContract.is_water_boiler'
        db.add_column(u'build_copycontract', 'is_water_boiler',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'CopyContract.docs'
        db.delete_column(u'build_copycontract', 'docs_id')

        # Deleting field 'CopyContract.address'
        db.delete_column(u'build_copycontract', 'address')


    models = {
        'build.building': {
            'Meta': {'object_name': 'Building'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'approve_status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'area': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'area_cmp': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'}),
            'cad_num': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2048', 'db_index': 'True'}),
            'cad_passport': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'clinic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'complete_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['build.Contract']", 'null': 'True', 'blank': 'True'}),
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Developer']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'driveways': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'electric_supply': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'entrance_door': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'finish_year': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2018, 12, 31, 0, 0)'}),
            'flat_num': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'flats_amount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'floors': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gas_supply': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
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
            'start_year': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 1, 0, 0)'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'water_removal': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'water_settlement': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'wc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.WC']", 'null': 'True', 'blank': 'True'}),
            'window_constructions': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'build.contract': {
            'Meta': {'object_name': 'Contract'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'area': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'creation_form': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Developer']", 'null': 'True', 'blank': 'True'}),
            'docs': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['build.ContractDocuments']", 'null': 'True', 'blank': 'True'}),
            'finish_year': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2018, 12, 31, 0, 0)'}),
            'flats_amount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'has_trouble_docs': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mo.MO']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True'}),
            'num': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'period_of_payment': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True'}),
            'start_year': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 1, 0, 0)'}),
            'summ_mo_money': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'summ_without_mo_money': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'summa': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'summa_fed': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'summa_reg': ('django.db.models.fields.FloatField', [], {'null': 'True'})
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
        'build.copybuilding': {
            'Meta': {'object_name': 'CopyBuilding'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'approve_status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'area': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'area_cmp': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'}),
            'cad_num': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'cad_passport': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'clinic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'complete_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['build.Contract']", 'null': 'True'}),
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Developer']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'driveways': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'electric_supply': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'entrance_door': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'finish_year': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2018, 12, 31, 0, 0)'}),
            'flat_num': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'flats_amount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'floors': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gas_supply': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
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
            'mo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mo.MO']", 'null': 'True', 'blank': 'True'}),
            'offer': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'payment_perspective': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'permission': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'public_transport': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'readiness': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Room']", 'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'start_year': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 1, 0, 0)'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'water_removal': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'water_settlement': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'wc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.WC']", 'null': 'True', 'blank': 'True'}),
            'window_constructions': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'build.copycontract': {
            'Meta': {'object_name': 'CopyContract'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'area': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'creation_form': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Developer']", 'null': 'True', 'blank': 'True'}),
            'docs': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['build.ContractDocuments']", 'null': 'True', 'blank': 'True'}),
            'finish_year': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2018, 12, 31, 0, 0)'}),
            'flats_amount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'has_trouble_docs': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mo.MO']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True'}),
            'num': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'period_of_payment': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True'}),
            'start_year': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 1, 0, 0)'}),
            'summ_mo_money': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'summ_without_mo_money': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'summa': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'summa_fed': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'summa_reg': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        'build.ground': {
            'Meta': {'object_name': 'Ground'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'approve_status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'area': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'area_cmp': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'}),
            'cad_num': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2048', 'db_index': 'True'}),
            'cad_passport': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'clinic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'complete_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['build.Contract']", 'null': 'True', 'blank': 'True'}),
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Developer']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'driveways': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'electric_supply': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'entrance_door': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'finish_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'finish_year': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2018, 12, 31, 0, 0)'}),
            'flats_amount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'floors': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gas_supply': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
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
            'start_year': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 1, 0, 0)'}),
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
            'bath_with_mixer': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'ceiling_hook': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'heaters': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_toilet': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_tower_dryer': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'lamp': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sink_with_mixer': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'smoke_filter': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sockets': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'switches': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'wc_switches': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
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
        },
        'mo.mo': {
            'Meta': {'object_name': 'MO'},
            'common_amount': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'common_economy': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'common_fed_amount': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'common_percentage': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'common_reg_amount': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'common_spent': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'creation_form': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            'flats_amount': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'has_trouble': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'home_fed_orphans': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'home_orphans': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'home_reg_orphans': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2048'})
        }
    }

    complete_apps = ['build']