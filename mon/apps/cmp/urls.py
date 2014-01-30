from django.conf.urls import patterns, include, url
from apps.cmp import views


urlpatterns = patterns(
    'apps.cmp.views',

    url(r'^auctions/all/$', views.get_auctions, name='auctions-all'),
    url(r'^auctions/$', views.get_mo_auctions, name='auctions'),
    url(r'^auctions/mo/(?P<pk>[0-9]+)/$', views.get_mo_auctions, name='mo-auctions'),
    url(r'^auction/add/$', views.add_auction, name='create-auction'),
    url(r'^auction/(?P<pk>[0-9]+)/$', views.get_auction, name='change-auction'),
    url(r'^auction/update/(?P<pk>[0-9]+)/$', views.update_auction, name='update-auction'),
    url(r'^auction/pre_delete/(?P<pk>[0-9]+)/$', views.pre_delete_auction, name='pre-delete-auction'),
    url(r'^auction/delete/(?P<pk>[0-9]+)/$', views.delete_auction, name='delete-auction'),

    url(r'^contracts/all/$', views.get_contracts, {'all': True}, name='contracts-all'),
    url(r'^contracts/$', views.get_contracts, name='contracts'),
    url(r'^contract/add/$', views.add_contract, name='create-contract'),
    url(r'^contract/(?P<pk>[0-9]+)/$', views.get_contract, name='change-contract'),
    url(r'^contract/update/(?P<pk>[0-9]+)/$', views.update_contract, name='update-contract'),
    url(r'^contract/pre_delete/(?P<pk>[0-9]+)/$', views.pre_delete_contract, name='pre-delete-contract'),
    url(r'^contract/delete/(?P<pk>[0-9]+)/$', views.delete_contract, name='delete-contract'),
    url(r'^contract/from_auction/(?P<pk>[0-9]+)/$', views.add_contract_from_auction, name='add-auction-contract'),

    url(r'^results/$', views.get_results, name='results'),
    url(r'^results/all/$', views.get_results,  {'all': True}, name='results-all'),
    url(r'^result/add/$', views.add_result, name='create-result'),
    url(r'^result/(?P<pk>[0-9]+)/$', views.get_result, name='change-result'),
    url(r'^result/update/(?P<pk>[0-9]+)/$', views.update_result, name='update-result'),
    url(r'^result/pre_delete/(?P<pk>[0-9]+)/$', views.pre_delete_result, name='pre-delete-result'),
    url(r'^result/delete/(?P<pk>[0-9]+)/$', views.delete_result, name='delete-result'),

    url(r'^result/person/(?P<pk>[0-9]*)/$', views.manage_person, name='manage-person'),
    url(r'^result/person/add$', views.manage_person, name='manage-person'),

    url(r'^cmp/contract/(?P<pk>[0-9]+)/$', views.cmp_contract, name='cmp-contract'),
    url(r'^cmp/contract/auction/(?P<pk>[0-9]+)/$', views.cmp_contract_auction, name='cmp-contract-auction'),
    url(r'^cmp/result/(?P<pk>[0-9]+)/$', views.cmp_result_building, name='cmp-result-building'),
    url(r'^cmp/result/contract/(?P<pk>[0-9]+)/$', views.cmp_result_contract, name='cmp-result-contract'),
)
