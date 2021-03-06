# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MO.common_economy'
        db.add_column(u'mo_mo', 'common_economy',
                      self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True),
                      keep_default=False)

        # Adding field 'MO.common_percentage'
        db.add_column(u'mo_mo', 'common_percentage',
                      self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True),
                      keep_default=False)

        # Adding field 'MO.common_spent'
        db.add_column(u'mo_mo', 'common_spent',
                      self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True),
                      keep_default=False)

        # Adding field 'MO.common_amount'
        db.add_column(u'mo_mo', 'common_amount',
                      self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MO.common_economy'
        db.delete_column(u'mo_mo', 'common_economy')

        # Deleting field 'MO.common_percentage'
        db.delete_column(u'mo_mo', 'common_percentage')

        # Deleting field 'MO.common_spent'
        db.delete_column(u'mo_mo', 'common_spent')

        # Deleting field 'MO.common_amount'
        db.delete_column(u'mo_mo', 'common_amount')


    models = {
        'mo.departamentagreement': {
            'Meta': {'object_name': 'DepartamentAgreement'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'flats_amount': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mo.MO']", 'null': 'True', 'blank': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'subvention': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mo.Subvention']", 'null': 'True', 'blank': 'True'}),
            'subvention_performance': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
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
            'common_amount': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'common_economy': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'common_percentage': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'common_spent': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'creation_form': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'has_trouble': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'home_orphans': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'})
        },
        'mo.orphan': {
            'Meta': {'object_name': 'Orphan'},
            'age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'have_home': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_privilege': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        'mo.peopleamount': {
            'Meta': {'object_name': 'PeopleAmount'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mo.MO']", 'null': 'True', 'blank': 'True'}),
            'privilege_people': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'unhome_orphan': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
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
        }
    }

    complete_apps = ['mo']