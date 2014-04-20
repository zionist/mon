# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

import autocomplete_light
autocomplete_light.autodiscover()

from apps.mo import views


urlpatterns = patterns(
    'apps.mo.views',

    url(r'^mos/$', views.get_mos, name='mos'),
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


)
