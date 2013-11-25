from django.conf.urls import patterns, include, url
from apps.build import views


urlpatterns = patterns(
    'apps.build.views',

    # url(r'^builds/$', views.get_builds, name='builds'),
    url(r'^building/$', views.BuildingListView.as_view(), name='buildings'),
    url(r'^building/add/$', views.add_building, name='create-building'),
    url(r'^building/building/(?P<pk>[0-9]+)/$', views.get_building, name='change-building'),
    url(r'^building/update/(?P<pk>[0-9]+)/$', views.update_building, name='update-building'),
    url(r'^building/pre_delete/(?P<pk>[0-9]+)/$', views.pre_delete_building, name='pre-delete-building'),
    url(r'^building/delete/(?P<pk>[0-9]+)/$', views.delete_building, name='delete-building'),
)
