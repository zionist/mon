from django.conf.urls import patterns, include, url
from apps.imgfile import views


urlpatterns = patterns(
    'apps.build.views',

    url(r'^imgfile/questions_list/$', views.get_questions_list,
        name='questions-list'),
    url(r'^imgfile/questions_list_simple/$', views.get_questions_list_form_simple,
        name='questions-list-simple'),
    url(r'^imgfile/get_questions_list_form/$', views.get_questions_list_form,
        name='questions-list-form'),
    url(r'^imgfile/get_select_mo_form/$', views.get_select_mo_form,
        name='select-mo-form'),
    url(r'^imgfile/get_monitoring_info/(?P<pk>[0-9]+)/$', views.get_monitoring_info,
        name='get-monitoring-info'),
)
