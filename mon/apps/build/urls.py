from django.conf.urls import patterns, include, url
from apps.build import views


urlpatterns = patterns(
    'apps.build.views',

    # url(r'^builds/$', views.get_builds, name='builds'),
    url(r'^builds/$', views.BuildingListView.as_view(), name='builds'),
    url(r'^builds/add/$', views.add_build, name='create-build'),
    url(r'^builds/build/(?P<pk>[0-9]+)/$', views.get_build, name='change-build'),
    url(r'^builds/upd/(?P<pk>[0-9]+)/$', views.update_build, name='update-build'),
    url(r'^builds/pre/(?P<pk>[0-9]+)/$', views.pre_delete_build, name='pre-delete-object'),
    url(r'^builds/del/(?P<pk>[0-9]+)/$', views.delete_build, name='delete-object'),
)
