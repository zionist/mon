from django.conf.urls import patterns, include, url
from apps.core import views


urlpatterns = patterns('',
    url(r'^css/generated/fonts.css',
        views.generate_fonts_css, name='generate-fonts-css'),
)