# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Payment'
        db.create_table(u'payment_payment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('num', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now=True, db_index=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('contract', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmp.Contract'])),
            ('subvention', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mo.Subvention'])),
            ('pay_order', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('payment', ['Payment'])


    def backwards(self, orm):
        # Deleting model 'Payment'
        db.delete_table(u'payment_payment')


    models = {
        'cmp.contract': {
            'Meta': {'object_name': 'Contract'},
            'area': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'clinic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Developer']", 'null': 'True', 'blank': 'True'}),
            'docs': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmp.ContractDocuments']", 'null': 'True', 'blank': 'True'}),
            'driveways': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'electric_supply': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'entrance_door': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'flats_amount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'floors': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gas_supply': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'hallway': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Hallway']", 'null': 'True', 'blank': 'True'}),
            'has_trouble_docs': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
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
        'cmp.contractdocuments': {
            'Meta': {'object_name': 'ContractDocuments'},
            'acceptance_acts': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'approval_citizen_statement': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'building_permissions': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'cost_infos': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'facility_permission': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'hiring_contract': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'land_right_stating': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mo_certificate': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mo_notice_to_citizen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mun_act_to_fond': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mun_contracts': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'photos': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'protocols': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tec_passport_tec_plan': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'transmission_acts': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
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
        },
        'mo.federalbudget': {
            'Meta': {'object_name': 'FederalBudget'},
            'adm_coef': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sub_orph_home': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sub_sum': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'mo.mo': {
            'Meta': {'object_name': 'MO'},
            'creation_form': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'has_trouble': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'home_orphans': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'})
        },
        'mo.regionalbudget': {
            'Meta': {'object_name': 'RegionalBudget'},
            'adm_coef': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sub_orph_home': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sub_sum': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'mo.subvention': {
            'Meta': {'object_name': 'Subvention'},
            'amount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'fed_budget': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mo.FederalBudget']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reg_budget': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mo.RegionalBudget']", 'null': 'True', 'blank': 'True'})
        },
        'payment.payment': {
            'Meta': {'object_name': 'Payment'},
            'amount': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmp.Contract']"}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'pay_order': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'subvention': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mo.Subvention']"})
        }
    }

    complete_apps = ['payment']