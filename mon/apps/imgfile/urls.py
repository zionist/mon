from django.conf.urls import patterns, include, url
from apps.imgfile import views


urlpatterns = patterns(
    'apps.build.views',

    url(r'^imgfile/questions_list/(?P<pk>[0-9]+)/$', views.get_questions_list, name='get-questions-list'),
)
