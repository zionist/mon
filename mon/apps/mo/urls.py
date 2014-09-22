# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

import autocomplete_light
autocomplete_light.autodiscover()

from apps.mo import views


urlpatterns = patterns(
    'apps.mo.views',

    url(r'^mos/$', views.get_recount_mo, name='mos'),
    url(r'^mos/select/$', views.mos_select, name='select-mos'),
    url(r'^mo/select/(?P<pk>[0-9]+)/$', views.select_mo,  name='select-mo'),
    url(r'^mo/add/$', views.add_mo, name='create-mo'),
    url(r'^mo/add/(?P<pk>[0-9]+)/(?P<state>[0-2]+)/$', views.add_agreement, name='add-agreement-mo'),
    url(r'^mo/add/(?P<pk>[0-9]+)/(?P<state>[0-2]+)/$', views.add_dop_agreement, name='add-dop-agreement-mo'),
    url(r'^mo/(?P<pk>[0-9]+)/$', views.get_mo, name='change-mo'),
    url(r'^mo/update/(?P<pk>[0-9]+)/$', views.update_mo, name='update-mo'),
    url(r'^mo/pre_delete/(?P<pk>[0-9]+)/$', views.pre_delete_mo, name='pre-delete-mo'),
    url(r'^mo/delete/(?P<pk>[0-9]+)/$', views.delete_mo, name='delete-mo'),

    url(r'^mo/recount/(?P<pk>[0-9]*)/$', views.get_recount_mo, name='recount-mo'),

    url(r'^mo/dep/(?P<pk>[0-9]+)/$', views.get_agreement, name='change-agreement'),
    url(r'^mo/dep/update/(?P<pk>[0-9]+)/(?P<state>[0-9]+)/$', views.update_agreement, name='update-agreement'),
    url(r'^mo/dep/pre_delete/(?P<pk>[0-9]+)/$', views.pre_delete_agreement, name='pre-delete-agreement'),
    url(r'^mo/dep/delete/(?P<pk>[0-9]+)/$', views.delete_agreement, name='delete-agreement'),


    url(r'^mo/filter/(?P<num>[0-9]+)/$', views.get_filter, name='filter'),
    url(r'^mo/xls/work_table/$', views.xls_work_table, name='xls_work_table'),
    url(r'^mo/xls/contract_grapth/$', views.xls_contract_grapth, name='xls_contract_grapth'),
    url(r'^mo/xls/contract_grapth/contracts_nums$', views.xls_contract_grapth, {'render': "contracts_nums"}, name='xls_contract_grapth-contracts_nums'),
    url(r'^mo/xls/contract_grapth/percent_of_contracts_flats_amount_and_subvention_perfomance$', views.xls_contract_grapth, {'render': "percent_of_contracts_flats_amount_and_subvention_perfomance"}, name='xls_contract_grapth-percent_of_contracts_flats_amount_and_subvention_perfomance'),
    url(r'^mo/xls/contract_grapth/spend_amount$', views.xls_contract_grapth, {'render': "spend_amount"}, name='xls_contract_grapth-spend_amount'),
    url(r'^mo/xls/contract_grapth/percent_of_sum_with_k_and_spend_amount$', views.xls_contract_grapth, {'render': "percent_of_sum_with_k_and_spend_amount"}, name='xls_contract_grapth-percent_of_sum_with_k_and_spend_amount'),
    url(r'^mo/max_flat_price/add/$', views.add_max_flat_price, name='create-max_flat_price'),
    url(r'^mo/max_flat_price/update/(?P<pk>[0-9]+)/$', views.update_max_flat_price, name='create-max_flat_price'),
    url(r'^mo/max_flat_price/delete/(?P<pk>[0-9]+)/$', views.delete_max_flat_price, name='delete-max_flat_price'),
    url(r'^mo/max_flat_prices/$', views.get_max_flat_prices, name='max_flat_prices'),


)
