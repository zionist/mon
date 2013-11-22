from django.conf.urls import patterns, include, url
from apps.build import views


urlpatterns = patterns(
    'apps.build.views',

    url(r'^builds/$', views.get_builds, name='builds'),
    url(r'^builds/add/$', views.add_build, name='create-build'),


)
