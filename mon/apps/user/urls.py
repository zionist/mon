from django.conf.urls import patterns, include, url
from apps.user import views


urlpatterns = patterns(
    'apps.user.views',

    url(r'^users/$', views.get_users, name='users'),
    url(r'^user/add/$', views.add_user, name='create-user'),
    url(r'^user/update/(?P<pk>[0-9]+)/$', views.update_user, name='update-user'),
    url(r'^user/pre_delete/(?P<pk>[0-9]+)/$', views.pre_delete_user, name='pre-delete-user'),
    url(r'^user/delete/(?P<pk>[0-9]+)/$', views.delete_user, name='delete-user'),

    url(r'^user/date/(?P<pk>[0-9]+)/(?P<select>[0-9]+)/$', views.update_user_date, name='select-user-date'),

    url(r'^choices/update/(?P<pk>[0-9]+)/$', views.update_choices, name='update-choices'),
    url(r'^choices/$', views.get_choices, name='choices'),
    )
