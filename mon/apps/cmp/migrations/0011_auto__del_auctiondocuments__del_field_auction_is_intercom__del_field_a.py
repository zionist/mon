# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'AuctionDocuments'
        db.delete_table(u'cmp_auctiondocuments')

        # Deleting field 'Auction.is_intercom'
        db.delete_column(u'cmp_auction', 'is_intercom')

        # Deleting field 'Auction.clinic'
        db.delete_column(u'cmp_auction', 'clinic')

        # Deleting field 'Auction.floors'
        db.delete_column(u'cmp_auction', 'floors')

        # Deleting field 'Auction.market'
        db.delete_column(u'cmp_auction', 'market')

        # Deleting field 'Auction.kindergarden'
        db.delete_column(u'cmp_auction', 'kindergarden')

        # Deleting field 'Auction.docs'
        db.delete_column(u'cmp_auction', 'docs_id')

        # Deleting field 'Auction.is_playground'
        db.delete_column(u'cmp_auction', 'is_playground')

        # Deleting field 'Auction.school'
        db.delete_column(u'cmp_auction', 'school')

        # Deleting field 'Auction.driveways'
        db.delete_column(u'cmp_auction', 'driveways')

        # Deleting field 'Auction.public_transport'
        db.delete_column(u'cmp_auction', 'public_transport')

        # Deleting field 'Auction.has_trouble_docs'
        db.delete_column(u'cmp_auction', 'has_trouble_docs')

        # Deleting field 'Auction.is_clother_drying'
        db.delete_column(u'cmp_auction', 'is_clother_drying')

        # Deleting field 'Auction.is_routes'
        db.delete_column(u'cmp_auction', 'is_routes')

        # Deleting field 'Auction.is_dustbin_area'
        db.delete_column(u'cmp_auction', 'is_dustbin_area')

        # Deleting field 'Auction.is_parking'
        db.delete_column(u'cmp_auction', 'is_parking')

        # Deleting field 'CopyAuction.is_intercom'
        db.delete_column(u'cmp_copyauction', 'is_intercom')

        # Deleting field 'CopyAuction.clinic'
        db.delete_column(u'cmp_copyauction', 'clinic')

        # Deleting field 'CopyAuction.floors'
        db.delete_column(u'cmp_copyauction', 'floors')

        # Deleting field 'CopyAuction.market'
        db.delete_column(u'cmp_copyauction', 'market')

        # Deleting field 'CopyAuction.kindergarden'
        db.delete_column(u'cmp_copyauction', 'kindergarden')

        # Deleting field 'CopyAuction.is_playground'
        db.delete_column(u'cmp_copyauction', 'is_playground')

        # Deleting field 'CopyAuction.school'
        db.delete_column(u'cmp_copyauction', 'school')

        # Deleting field 'CopyAuction.driveways'
        db.delete_column(u'cmp_copyauction', 'driveways')

        # Deleting field 'CopyAuction.public_transport'
        db.delete_column(u'cmp_copyauction', 'public_transport')

        # Deleting field 'CopyAuction.has_trouble_docs'
        db.delete_column(u'cmp_copyauction', 'has_trouble_docs')

        # Deleting field 'CopyAuction.is_clother_drying'
        db.delete_column(u'cmp_copyauction', 'is_clother_drying')

        # Deleting field 'CopyAuction.is_routes'
        db.delete_column(u'cmp_copyauction', 'is_routes')

        # Deleting field 'CopyAuction.is_dustbin_area'
        db.delete_column(u'cmp_copyauction', 'is_dustbin_area')

        # Deleting field 'CopyAuction.is_parking'
        db.delete_column(u'cmp_copyauction', 'is_parking')


    def backwards(self, orm):
        # Adding model 'AuctionDocuments'
        db.create_table(u'cmp_auctiondocuments', (
            ('max_price_substantiation_rec', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('notice', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('technical_specification', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('notice_rec', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('mun_contract_project', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('technical_specification_rec', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('max_price_substantiation', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('mun_contract_project_rec', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('cmp', ['AuctionDocuments'])

        # Adding field 'Auction.is_intercom'
        db.add_column(u'cmp_auction', 'is_intercom',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Auction.clinic'
        db.add_column(u'cmp_auction', 'clinic',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Auction.floors'
        db.add_column(u'cmp_auction', 'floors',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Auction.market'
        db.add_column(u'cmp_auction', 'market',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Auction.kindergarden'
        db.add_column(u'cmp_auction', 'kindergarden',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Auction.docs'
        db.add_column(u'cmp_auction', 'docs',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cmp.AuctionDocuments'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Auction.is_playground'
        db.add_column(u'cmp_auction', 'is_playground',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Auction.school'
        db.add_column(u'cmp_auction', 'school',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Auction.driveways'
        db.add_column(u'cmp_auction', 'driveways',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Auction.public_transport'
        db.add_column(u'cmp_auction', 'public_transport',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Auction.has_trouble_docs'
        db.add_column(u'cmp_auction', 'has_trouble_docs',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Auction.is_clother_drying'
        db.add_column(u'cmp_auction', 'is_clother_drying',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Auction.is_routes'
        db.add_column(u'cmp_auction', 'is_routes',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Auction.is_dustbin_area'
        db.add_column(u'cmp_auction', 'is_dustbin_area',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Auction.is_parking'
        db.add_column(u'cmp_auction', 'is_parking',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyAuction.is_intercom'
        db.add_column(u'cmp_copyauction', 'is_intercom',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyAuction.clinic'
        db.add_column(u'cmp_copyauction', 'clinic',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyAuction.floors'
        db.add_column(u'cmp_copyauction', 'floors',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyAuction.market'
        db.add_column(u'cmp_copyauction', 'market',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyAuction.kindergarden'
        db.add_column(u'cmp_copyauction', 'kindergarden',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyAuction.is_playground'
        db.add_column(u'cmp_copyauction', 'is_playground',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyAuction.school'
        db.add_column(u'cmp_copyauction', 'school',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyAuction.driveways'
        db.add_column(u'cmp_copyauction', 'driveways',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyAuction.public_transport'
        db.add_column(u'cmp_copyauction', 'public_transport',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyAuction.has_trouble_docs'
        db.add_column(u'cmp_copyauction', 'has_trouble_docs',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyAuction.is_clother_drying'
        db.add_column(u'cmp_copyauction', 'is_clother_drying',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyAuction.is_routes'
        db.add_column(u'cmp_copyauction', 'is_routes',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyAuction.is_dustbin_area'
        db.add_column(u'cmp_copyauction', 'is_dustbin_area',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CopyAuction.is_parking'
        db.add_column(u'cmp_copyauction', 'is_parking',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)


    models = {
        'build.building': {
            'Meta': {'object_name': 'Building'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'approve_status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'area': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'area_cmp': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'}),
            'build_state': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'build_year': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cad_num': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2048', 'db_index': 'True'}),
            'cad_passport': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'cad_sum': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
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
            'floor': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'floors': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gas_supply': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
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
            'market': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mo.MO']"}),
            'mo_fond_doc_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'mo_fond_doc_num': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ownership_doc_num': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ownership_year': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'payment_perspective': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'planing_floor': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'public_transport': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'readiness': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'start_year': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 1, 0, 0)'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'water_removal': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'water_settlement': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
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
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mun_contracts': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'build.ground': {
            'Meta': {'object_name': 'Ground'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'approve_status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'area': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'area_cmp': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'}),
            'build_state': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'build_year': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cad_num': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2048', 'db_index': 'True'}),
            'cad_passport': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'cad_sum': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
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
            'floor': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'floors': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gas_supply': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
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
            'market': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mo.MO']"}),
            'mo_fond_doc_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'mo_fond_doc_num': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ownership_doc_num': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ownership_year': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'payment_perspective': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'planing_floor': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'public_transport': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'readiness': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'start_year': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 1, 0, 0)'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'water_removal': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'water_settlement': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'window_constructions': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'cmp.auction': {
            'Meta': {'object_name': 'Auction'},
            'area': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'area_cmp': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'}),
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['build.Contract']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'electric_supply': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'entrance_door': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '0', 'max_length': '256', 'blank': 'True'}),
            'finish_year': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2018, 12, 31, 0, 0)'}),
            'flats_amount': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'gas_supply': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'hallway': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.AuctionHallway']", 'null': 'True', 'blank': 'True'}),
            'heating': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'hot_water_supply': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_doors': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '0', 'max_length': '256', 'blank': 'True'}),
            'is_balcony': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_heat_boiler': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_loggia': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_water_boiler': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'kitchen': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.AuctionKitchen']", 'null': 'True', 'blank': 'True'}),
            'mo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mo.MO']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True'}),
            'num': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'open_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'proposal_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.AuctionRoom']", 'null': 'True', 'blank': 'True'}),
            'stage': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'start_price': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'start_year': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 1, 0, 0)'}),
            'water_removal': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'water_settlement': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'wc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.AuctionWC']", 'null': 'True', 'blank': 'True'}),
            'window_constructions': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '0', 'max_length': '256', 'blank': 'True'})
        },
        'cmp.comparedata': {
            'Meta': {'object_name': 'CompareData'},
            'area': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'area_cmp': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'}),
            'clinic': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cmp_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 4, 21, 0, 0)', 'blank': 'True'}),
            'driveways': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'electric_supply': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'entrance_door': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'flats_amount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'floor': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'floors': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gas_supply': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
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
            'market': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'planing_floor': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'public_transport': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'water_removal': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'water_settlement': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'window_constructions': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'cmp.copyauction': {
            'Meta': {'object_name': 'CopyAuction'},
            'area': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'area_cmp': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'}),
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['build.Contract']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'electric_supply': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'entrance_door': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '0', 'max_length': '256', 'blank': 'True'}),
            'finish_year': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2018, 12, 31, 0, 0)'}),
            'flats_amount': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'gas_supply': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'hallway': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.AuctionHallway']", 'null': 'True', 'blank': 'True'}),
            'heating': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'hot_water_supply': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_doors': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '0', 'max_length': '256', 'blank': 'True'}),
            'is_balcony': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_heat_boiler': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_loggia': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_water_boiler': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'kitchen': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.AuctionKitchen']", 'null': 'True', 'blank': 'True'}),
            'mo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mo.MO']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True'}),
            'num': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'open_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'proposal_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.AuctionRoom']", 'null': 'True', 'blank': 'True'}),
            'stage': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'start_price': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'start_year': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 1, 0, 0)'}),
            'water_removal': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'water_settlement': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'wc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.AuctionWC']", 'null': 'True', 'blank': 'True'}),
            'window_constructions': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '0', 'max_length': '256', 'blank': 'True'})
        },
        'cmp.person': {
            'Meta': {'object_name': 'Person'},
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'})
        },
        'cmp.result': {
            'Meta': {'object_name': 'Result'},
            'building': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['build.Building']", 'null': 'True', 'blank': 'True'}),
            'check_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cmp_data': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cmp.CompareData']", 'null': 'True', 'blank': 'True'}),
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['build.Contract']", 'null': 'True', 'blank': 'True'}),
            'doc_files': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'doc_list': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'establish_pers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'establish_pers'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['cmp.Person']"}),
            'finish_year': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2018, 12, 31, 0, 0)'}),
            'ground': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['build.Ground']", 'null': 'True', 'blank': 'True'}),
            'hallway': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Hallway']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kitchen': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Kitchen']", 'null': 'True', 'blank': 'True'}),
            'mo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mo.MO']", 'null': 'True'}),
            'mo_pers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'mo_pers'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['cmp.Person']"}),
            'readiness': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recommend': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Room']", 'null': 'True', 'blank': 'True'}),
            'start_year': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 1, 1, 0, 0)'}),
            'wc': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.WC']", 'null': 'True', 'blank': 'True'})
        },
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2048'}),
            'planing_home_orphans': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cmp']