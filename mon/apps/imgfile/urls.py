from django.conf.urls import patterns, include, url
from apps.imgfile import views


urlpatterns = patterns(
    'apps.build.views',

    url(r'^imgfile/questions_list/$', views.get_questions_list, name='get-questions-list'),
)
