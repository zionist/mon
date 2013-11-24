# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from apps.core import views

if 'django.contrib.admin' in settings.INSTALLED_APPS:
    admin.autodiscover()

urlpatterns = patterns('',
    url(r'^mo/', include('apps.mo.urls')),
    url(r'^obj/', include('apps.build.urls')),
    url(r'^obj/', include('apps.payment.urls')),
    url(r'^$', views.main, name='main'),
    url(r"^login/$", "django.contrib.auth.views.login",
        {"template_name": "login.html"},
        name="auth-login"),
    url(r"^logout/$", "django.contrib.auth.views.logout_then_login",
        {"login_url": "/login"}, name="logout")

)

if 'django.contrib.admin' in settings.INSTALLED_APPS and settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^admin/', include(admin.site.urls)),
    )
