# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RegionalBudget'
        db.create_table(u'mo_regionalbudget', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sub_sum', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sub_orph_home', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('adm_coef', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('mo', ['RegionalBudget'])

        # Adding model 'FederalBudget'
        db.create_table(u'mo_federalbudget', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sub_sum', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sub_orph_home', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('adm_coef', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('mo', ['FederalBudget'])

        # Adding model 'Subvention'
        db.create_table(u'mo_subvention', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('fed_budget', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mo.FederalBudget'], null=True, blank=True)),
            ('reg_budget', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mo.RegionalBudget'], null=True, blank=True)),
        ))
        db.send_create_signal('mo', ['Subvention'])

        # Adding model 'MO'
        db.create_table(u'mo_mo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=2048, null=True, blank=True)),
            ('creation_form', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('has_trouble', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('home_orphans', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal('mo', ['MO'])

        # Adding model 'DepartamentAgreement'
        db.create_table(u'mo_departamentagreement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('num', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('subvention_performance', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('flats_amount', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('mo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mo.MO'], null=True, blank=True)),
            ('subvention', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mo.Subvention'], null=True, blank=True)),
        ))
        db.send_create_signal('mo', ['DepartamentAgreement'])

        # Adding model 'Orphan'
        db.create_table(u'mo_orphan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('have_home', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('is_privilege', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('mo', ['Orphan'])

        # Adding model 'PeopleAmount'
        db.create_table(u'mo_peopleamount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('privilege_people', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('unhome_orphan', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mo.MO'], null=True, blank=True)),
        ))
        db.send_create_signal('mo', ['PeopleAmount'])


    def backwards(self, orm):
        # Deleting model 'RegionalBudget'
        db.delete_table(u'mo_regionalbudget')

        # Deleting model 'FederalBudget'
        db.delete_table(u'mo_federalbudget')

        # Deleting model 'Subvention'
        db.delete_table(u'mo_subvention')

        # Deleting model 'MO'
        db.delete_table(u'mo_mo')

        # Deleting model 'DepartamentAgreement'
        db.delete_table(u'mo_departamentagreement')

        # Deleting model 'Orphan'
        db.delete_table(u'mo_orphan')

        # Deleting model 'PeopleAmount'
        db.delete_table(u'mo_peopleamount')


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