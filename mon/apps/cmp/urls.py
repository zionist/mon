from django.conf.urls import patterns, include, url
from apps.cmp import views


urlpatterns = patterns(
    'apps.cmp.views',

    url(r'^auctions/$', views.get_auctions, name='auctions'),
    url(r'^auction/add/$', views.add_auction, name='create-auction'),
    url(r'^auction/(?P<pk>[0-9]+)/$', views.get_auction, name='change-auction'),
    url(r'^auction/update/(?P<pk>[0-9]+)/$', views.update_auction, name='update-auction'),
    url(r'^auction/pre_delete/(?P<pk>[0-9]+)/$', views.pre_delete_auction, name='pre-delete-auction'),
    url(r'^auction/delete/(?P<pk>[0-9]+)/$', views.delete_auction, name='delete-auction'),
)
