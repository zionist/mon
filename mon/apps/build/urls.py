from django.conf.urls import patterns, include, url
from apps.build import views
import autocomplete_light
autocomplete_light.autodiscover()


urlpatterns = patterns(
    'apps.build.views',

    url(r'^buildings/$', views.get_buildings, name='buildings'),
    url(r'^buildings/(?P<mo>[0-9]+)/$', views.get_buildings, name='buildings'),
    url(r'^buildings/all/$', views.get_buildings, {'all': True}, name='buildings-all'),
    url(r'^building/add/$', views.select_building_state, name='create-building'),
    url(r'^building/add/(?P<state>[0-9]+)/(?P<dev_pk>[0-9]*)/$', views.add_building, name='add-building'),
    url(r'^monitorings/$', views.get_monitorings, name='monitorings'),
    url(r'^monitorings/(?P<mo>[0-9]+)/$', views.get_monitorings, name='monitorings'),
    url(r'^monitorings/all/$', views.get_monitorings, {'all': True}, name='monitorings-all'),
    url(r'^monitoring/add/$', views.select_monitoring_state, name='create-monitoring'),
    url(r'^monitoring/monitoring/(?P<pk>[0-9]+)/(?P<state>[0-9]*)/$', views.get_monitoring,
        name='change-monitoring'),
    url(r'^monitoring/update/(?P<pk>[0-9]+)/(?P<state>[0-9]*)/$', views.update_monitoring, name='update-monitoring'),
    url(r'^monitoring/add/(?P<state>[0-9]+)/(?P<dev_pk>[0-9]*)/$', views.add_monitoring, name='add-monitoring'),
    url(r'^building_copies/$', views.get_building_copies, name='building_copies'),
    url(r'^building_copies/(?P<mo>[0-9]+)/$', views.get_building_copies, name='building_copies'),
    url(r'^building_copies/all/$', views.get_building_copies, {'all': True}, name='building_copies-all'),
    url(r'^building_copy/delete/(?P<pk>[0-9]+)/$', views.delete_building_copy, name='delete-building_copy'),
    url(r'^building_copy/update/(?P<pk>[0-9]+)/$', views.update_building_copy, name='update-building_copy'),
    url(r'^monitoring/pre_delete/(?P<pk>[0-9]+)/(?P<state>[0-9]*)/$', views.pre_delete_monitoring, name='pre-delete-monitoring'),
    url(r'^monitoring/delete/(?P<pk>[0-9]+)/(?P<state>[0-9]*)/$', views.delete_monitoring, name='delete-monitoring'),
    url(r'^building/building/(?P<pk>[0-9]+)/(?P<state>[0-9]*)/$', views.get_building, name='change-building'),
    url(r'^building/update/(?P<pk>[0-9]+)/(?P<state>[0-9]*)/$', views.update_building, name='update-building'),
    url(r'^building/copy/(?P<pk>[0-9]+)/$', views.copy_building, name='copy-building'),
    url(r'^building/approve/(?P<pk>[0-9]+)/(?P<state>[0-9]*)/$', views.approve_building, name='approve-building'),
    url(r'^building/pre_delete/(?P<pk>[0-9]+)/(?P<state>[0-9]*)/$', views.pre_delete_building, name='pre-delete-building'),
    url(r'^building/delete/(?P<pk>[0-9]+)/(?P<state>[0-9]*)/$', views.delete_building, name='delete-building'),
    url(r'^building/developer/(?P<pk>[0-9]*)/(?P<state>[0-9]?)/$', views.manage_developer, name='manage-developer'),
    url(r'^building/developer/$', views.manage_developer, name='manage-developer'),
    url(r'^building/developer/(?P<state>[0-9]?)/$', views.manage_developer, name='manage-developer'),
    url(r'^building/developer/delete/(?P<pk>[0-9]*)/$', views.delete_developer, name='delete-developer'),
    url(r'^building/developer/add/(?P<state>[0-9]?)/$', views.manage_developer, name='add-building-developer'),
    url(r'^monitoring/developer/add/(?P<state>[0-9]?)/$',
        views.manage_monitoring_developer, name='add-monitoring-developer'),
    url(r'^monitoring/developer/(?P<pk>[0-9]*)/(?P<state>[0-9]?)/$', views.manage_monitoring_developer, name='manage-monitoring-developer'),
    url(r'^building/developers/$', views.get_developers, name='developers'),
)
