from django.conf.urls import patterns, include, url

import autocomplete_light
autocomplete_light.autodiscover()

from apps.build import views
from apps.build.forms import BuildingSelectForm, BuildingForm, GroundForm
from apps.core.forms import DeveloperForm, RoomForm, KitchenForm, WCForm, HallwayForm

CONDITION_DICT = {'1': views.show_developer, '6': views.show_ground, '7': views.show_building}

FORMS = [BuildingSelectForm, DeveloperForm, RoomForm, KitchenForm, WCForm, HallwayForm, GroundForm, BuildingForm]


urlpatterns = patterns(
    'apps.build.views',

    url(r'^buildings/$', views.get_buildings, name='buildings'),
    url(r'^building/add/$', views.select_building_state, name='create-building'),
    url(r'^building/add/(?P<state>[0-9]+)/(?P<dev_pk>[0-9]*)/$', views.add_building, name='add-building'),
    url(r'^building/building/(?P<pk>[0-9]+)/(?P<state>[0-9]*)/$', views.get_building, name='change-building'),
    url(r'^building/update/(?P<pk>[0-9]+)/(?P<state>[0-9]*)/$', views.update_building, name='update-building'),
    url(r'^building/copy/(?P<pk>[0-9]+)/$', views.copy_building, name='copy-building'),
    url(r'^building/approve/(?P<pk>[0-9]+)/(?P<state>[0-9]*)/$', views.approve_building, name='approve-building'),
    url(r'^building/pre_delete/(?P<pk>[0-9]+)/(?P<state>[0-9]*)/$', views.pre_delete_building, name='pre-delete-building'),
    url(r'^building/delete/(?P<pk>[0-9]+)/(?P<state>[0-9]*)/$', views.delete_building, name='delete-building'),
    url(r'^building/developer/(?P<pk>[0-9]*)/$', views.manage_developer, name='manage-developer'),
    url(r'^building/developer/delete/(?P<pk>[0-9]*)/$', views.delete_developer, name='delete-developer'),
    url(r'^building/developer/add$', views.manage_developer, name='manage-developer'),
    url(r'^building/developers/$', views.get_developers, name='developers'),
    url(r'^building/wizard/$', views.BuildCreationWizard.as_view(FORMS, condition_dict=CONDITION_DICT),
        name='create-building-wizard'),
)
