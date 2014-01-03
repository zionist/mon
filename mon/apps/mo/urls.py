from django.conf.urls import patterns, include, url

import autocomplete_light
autocomplete_light.autodiscover()

from apps.mo import views


urlpatterns = patterns(
    'apps.mo.views',

    url(r'^mos/$', views.get_mos, name='mos'),
    url(r'^mo/add/$', views.add_mo, name='create-mo'),
    url(r'^mo/(?P<pk>[0-9]+)/$', views.get_mo, name='change-mo'),
    url(r'^mo/update/(?P<pk>[0-9]+)/$', views.update_mo, name='update-mo'),
    url(r'^mo/pre_delete/(?P<pk>[0-9]+)/$', views.pre_delete_mo, name='pre-delete-mo'),
    url(r'^mo/delete/(?P<pk>[0-9]+)/$', views.delete_mo, name='delete-mo'),

    url(r'^mo/filter/(?P<num>[0-9]+)/$', views.get_filter, name='filter'),

)
