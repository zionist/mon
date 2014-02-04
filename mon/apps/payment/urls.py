from django.conf.urls import patterns, include, url
from apps.payment import views


urlpatterns = patterns(
    'apps.payment.views',

    url(r'^payments/$', views.get_payments, name='payments'),
    url(r'^payments/(?P<mo>[0-9]+)/$', views.get_payments, name='payments'),
    url(r'^payments/all$', views.get_payments, {'all': True}, name='payments-all'),
    url(r'^payments/mo_selected/$', views.get_payments, {'mo_selected': True},
        name='mo-payments'),
    url(r'^payment/acc/(?P<select>[0-9]+)$', views.get_accounting, name='accounting'),
    url(r'^payment/acc/$', views.get_accounting, name='date-accounting'),
    url(r'^payment/add/$', views.add_payment, name='create-payment'),
    url(r'^payment/(?P<pk>[0-9]+)/$', views.get_payment, name='change-payment'),
    url(r'^payment/update/(?P<pk>[0-9]+)/$', views.update_payment, name='update-payment'),
    url(r'^payment/pre_delete/(?P<pk>[0-9]+)/$', views.pre_delete_payment,
        name='pre-delete-payment'),
    url(r'^payment/delete/(?P<pk>[0-9]+)/$', views.delete_payment, name='delete-payment'),

)
