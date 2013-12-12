from django.conf.urls import patterns, include, url
from apps.imgfile import views


urlpatterns = patterns(
    'apps.build.views',

    url(r'^imgfile/questions_list/$', views.get_questions_list,
        name='questions-list'),
    url(r'^imgfile/get_questions_list_form/$', views.get_questions_list_form,
        name='questions-list-form'),
    url(r'^imgfile/get_select_mo_form/$', views.get_select_mo_form,
        name='select-mo-form'),
)
