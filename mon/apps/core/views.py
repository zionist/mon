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
    RoomShowForm, HallwayShowForm, WCShowForm, KitchenShowForm, \
    AuctionRoomForm, AuctionHallwayForm, AuctionWCForm, AuctionKitchenForm, \
    AuctionRoomShowForm, AuctionHallwayShowForm, AuctionWCShowForm, AuctionKitchenShowForm


def main(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")
    context = {'title': _(u'Мониторинг')}
    return render(request, 'base_site.html', context)


def get_fk_forms(parent=None, request=None, multi=None):
    room_p, hallway_p, wc_p, kitchen_p = 'room_build', 'hallway_build', 'wc_build', 'kitchen_build'
    forms = [RoomForm, HallwayForm, WCForm, KitchenForm] if not multi else [AuctionRoomForm, AuctionHallwayForm, AuctionWCForm, AuctionKitchenForm]
    print('    multi', multi, forms)
    if not parent:
        if request and request.method == "POST":
            room_f = forms[0](request.POST, request.FILES, prefix=room_p)
            hallway_f = forms[1](request.POST, request.FILES, prefix=hallway_p)
            wc_f = forms[2](request.POST, request.FILES, prefix=wc_p)
            kitchen_f = forms[3](request.POST, request.FILES, prefix=kitchen_p)
        else:
            room_f = forms[0](prefix=room_p)
            hallway_f = forms[1](prefix=hallway_p)
            wc_f = forms[2](prefix=wc_p)
            kitchen_f = forms[3](prefix=kitchen_p)
    else:
        if request and request.method == "POST":
            room_f = forms[0](request.POST, request.FILES, prefix=room_p, instance=parent.room)
            hallway_f = forms[1](request.POST, request.FILES, prefix=hallway_p, instance=parent.hallway)
            wc_f = forms[2](request.POST, request.FILES, prefix=wc_p, instance=parent.wc)
            kitchen_f = forms[3](request.POST, request.FILES, prefix=kitchen_p, instance=parent.kitchen)
        else:
            room_f = forms[0](prefix=room_p, instance=parent.room)
            hallway_f = forms[1](prefix=hallway_p, instance=parent.hallway)
            wc_f = forms[2](prefix=wc_p, instance=parent.wc)
            kitchen_f = forms[3](prefix=kitchen_p, instance=parent.kitchen)
    return [room_f, hallway_f, wc_f, kitchen_f]


def get_fk_show_forms(parent=None, multi=None):
    room_p, hallway_p, wc_p, kitchen_p = 'room_build', 'hallway_build', 'wc_build', 'kitchen_build'
    forms = [RoomShowForm, HallwayShowForm, WCShowForm, KitchenShowForm] if not multi \
        else [AuctionRoomShowForm, AuctionHallwayShowForm, AuctionWCShowForm, AuctionKitchenShowForm]
    room_f = forms[0](prefix=room_p, instance=parent.room)
    hallway_f = forms[1](prefix=hallway_p, instance=parent.hallway)
    wc_f = forms[2](prefix=wc_p, instance=parent.wc)
    kitchen_f = forms[3](prefix=kitchen_p, instance=parent.kitchen)
    return [room_f, hallway_f, wc_f, kitchen_f]


def get_fk_cmp_forms(parent=None, cmp=None, multi=None):
    room_p, hallway_p, wc_p, kitchen_p = 'room_cmp', 'hallway_cmp', 'wc_cmp', 'kitchen_cmp'
    forms = [RoomShowForm, HallwayShowForm, WCShowForm, KitchenShowForm] if not multi \
        else [AuctionRoomForm, AuctionHallwayForm, AuctionWCForm, AuctionKitchenForm]
    room_f = forms[0](prefix=room_p, instance=parent.room, cmp_initial=cmp.room)
    hallway_f = forms[1](prefix=hallway_p, instance=parent.hallway, cmp_initial=cmp.hallway)
    wc_f = forms[2](prefix=wc_p, instance=parent.wc, cmp_initial=cmp.wc)
    kitchen_f = forms[3](prefix=kitchen_p, instance=parent.kitchen, cmp_initial=cmp.kitchen)
    return [room_f, hallway_f, wc_f, kitchen_f]


def split_form(form):
    """
    move text_area fields to another form
    :param form: forms.Form object
    :return: two forms. First form without fields with Textarea widget
        and second form which contains fields with Textarea widget
    """
    if form.instance.id and not form.is_bound:
        text_area_form = CustomForm()
        text_area_form.is_bound = False
        text_area_form.prefix = form.prefix
        text_area_form.initial = QueryDict({}).copy()
        data = form.initial.copy()
        for k, v in form.fields.iteritems():
            if isinstance(v, CharField) and isinstance(v.widget, Textarea):
                text_area_form.fields.update({k: form.fields.pop(k)})
                if data.get(k):
                    text_area_form.initial.update({k: data.get(k)})
                    del data[k]
        form.data = data
        return (form, text_area_form)
    if form.is_bound:
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
        text_area_form = CustomForm()
        for k, v in form.fields.iteritems():
            if isinstance(v, CharField) and isinstance(v.widget, Textarea):
                text_area_form.fields.update({k: form.fields.pop(k)})
        text_area_form.prefix = form.prefix
        return (form, text_area_form)
