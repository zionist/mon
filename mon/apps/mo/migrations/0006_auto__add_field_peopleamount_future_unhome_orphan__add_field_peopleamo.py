# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PeopleAmount.future_unhome_orphan'
        db.add_column(u'mo_peopleamount', 'future_unhome_orphan',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PeopleAmount.queue_by_list'
        db.add_column(u'mo_peopleamount', 'queue_by_list',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PeopleAmount.future_queue_by_list'
        db.add_column(u'mo_peopleamount', 'future_queue_by_list',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PeopleAmount.unhome_orphan_14_18'
        db.add_column(u'mo_peopleamount', 'unhome_orphan_14_18',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PeopleAmount.future_unhome_orphan_14_18'
        db.add_column(u'mo_peopleamount', 'future_unhome_orphan_14_18',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PeopleAmount.deals'
        db.add_column(u'mo_peopleamount', 'deals',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'PeopleAmount.recoverers'
        db.add_column(u'mo_peopleamount', 'recoverers',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'MO.name'
        db.alter_column(u'mo_mo', 'name', self.gf('django.db.models.fields.CharField')(default=0, unique=True, max_length=2048))
        # Adding unique constraint on 'MO', fields ['name']
        db.create_unique(u'mo_mo', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'MO', fields ['name']
        db.delete_unique(u'mo_mo', ['name'])

        # Deleting field 'PeopleAmount.future_unhome_orphan'
        db.delete_column(u'mo_peopleamount', 'future_unhome_orphan')

        # Deleting field 'PeopleAmount.queue_by_list'
        db.delete_column(u'mo_peopleamount', 'queue_by_list')

        # Deleting field 'PeopleAmount.future_queue_by_list'
        db.delete_column(u'mo_peopleamount', 'future_queue_by_list')

        # Deleting field 'PeopleAmount.unhome_orphan_14_18'
        db.delete_column(u'mo_peopleamount', 'unhome_orphan_14_18')

        # Deleting field 'PeopleAmount.future_unhome_orphan_14_18'
        db.delete_column(u'mo_peopleamount', 'future_unhome_orphan_14_18')

        # Deleting field 'PeopleAmount.deals'
        db.delete_column(u'mo_peopleamount', 'deals')

        # Deleting field 'PeopleAmount.recoverers'
        db.delete_column(u'mo_peopleamount', 'recoverers')


        # Changing field 'MO.name'
        db.alter_column(u'mo_mo', 'name', self.gf('django.db.models.fields.CharField')(max_length=2048, null=True))

    models = {
        'mo.departamentagreement': {
            'Meta': {'object_name': 'DepartamentAgreement'},
            'agreement_type': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'blank': 'True'}),
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
            'creation_form': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'}),
            'has_trouble': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'home_orphans': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2048'})
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
            'deals': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'future_queue_by_list': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'future_unhome_orphan': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'future_unhome_orphan_14_18': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mo.MO']", 'null': 'True', 'blank': 'True'}),
            'privilege_people': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'queue_by_list': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recoverers': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'unhome_orphan': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'unhome_orphan_14_18': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
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