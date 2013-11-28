# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_list_or_404, \
    get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory, formset_factory, modelformset_factory
from django.core.urlresolvers import reverse
from django.forms import Form as CustomForm
from django.forms.fields import CharField
from django.forms.widgets import Textarea
from django.http.request import QueryDict

from .forms import RoomForm, HallwayForm, WCForm, KitchenForm, \
    RoomShowForm, HallwayShowForm, WCShowForm, KitchenShowForm


def main(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")
    context = {'title': _(u'Мониторинг')}
    return render(request, 'base_site.html', context)


def get_fk_forms(parent=None, request=None):
    room_p, hallway_p, wc_p, kitchen_p = 'room_build', 'hallway_build', 'wc_build', 'kitchen_build'
    if not parent:
        if request and request.method == "POST":
            room_f = RoomForm(request.POST, request.FILES, prefix=room_p)
            hallway_f = HallwayForm(request.POST, request.FILES, prefix=hallway_p)
            wc_f = WCForm(request.POST, request.FILES, prefix=wc_p)
            kitchen_f = KitchenForm(request.POST, request.FILES, prefix=kitchen_p)
        else:
            room_f = RoomForm(prefix=room_p)
            hallway_f = HallwayForm(prefix=hallway_p)
            wc_f = WCForm(prefix=wc_p)
            kitchen_f = KitchenForm(prefix=kitchen_p)
    else:
        if request and request.method == "POST":
            room_f = RoomForm(request.POST, request.FILES, prefix=room_p, instance=parent.room)
            hallway_f = HallwayForm(request.POST, request.FILES, prefix=hallway_p, instance=parent.hallway)
            wc_f = WCForm(request.POST, request.FILES, prefix=wc_p, instance=parent.wc)
            kitchen_f = KitchenForm(request.POST, request.FILES, prefix=kitchen_p, instance=parent.kitchen)
        else:
            room_f = RoomForm(prefix=room_p, instance=parent.room)
            hallway_f = HallwayForm(prefix=hallway_p, instance=parent.hallway)
            wc_f = WCForm(prefix=wc_p, instance=parent.wc)
            kitchen_f = KitchenForm(prefix=kitchen_p, instance=parent.kitchen)
    return [room_f, hallway_f, wc_f, kitchen_f]


def get_fk_show_forms(parent=None):
    room_p, hallway_p, wc_p, kitchen_p = 'room_build', 'hallway_build', 'wc_build', 'kitchen_build'
    room_f = RoomShowForm(prefix=room_p, instance=parent.room)
    hallway_f = HallwayShowForm(prefix=hallway_p, instance=parent.hallway)
    wc_f = WCShowForm(prefix=wc_p, instance=parent.wc)
    kitchen_f = KitchenShowForm(prefix=kitchen_p, instance=parent.kitchen)
    return [room_f, hallway_f, wc_f, kitchen_f]


def split_form(form, is_bound):
    """
    :param form: forms.Form object
    :param is_bound: Form is bound or unbound to data
    :return: two forms. First form without fields with Textarea widget
        and second form which contains fields with Textarea widget
    """
    # move text_area fields to another form
    if is_bound:
        text_area_form = CustomForm()
        text_area_form.is_bound = True
        text_area_form.prefix = form.prefix
        text_area_form.data = QueryDict({}).copy()
        data = form.data.copy()
        for k, v in form.fields.iteritems():
            if isinstance(v, CharField) and isinstance(v.widget, Textarea):
                text_area_form.fields.update({k: form.fields.pop(k)})
                k = "%s-%s" % (form.prefix, k)
                if data.get(k):
                    text_area_form.data.update({k: data.get(k)})
                    del data[k]
        form.data = data
        return (form, text_area_form)
    else:
        text_area_form = CustomForm()
        for k, v in form.fields.iteritems():
            if isinstance(v, CharField) and isinstance(v.widget, Textarea):
                text_area_form.fields.update({k: form.fields.pop(k)})
        text_area_form.prefix = form.prefix
        return (form, text_area_form)
