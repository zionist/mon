# -*- coding: utf-8 -*-

import webodt
import mimetypes
from copy import deepcopy
from webodt.converters import converter
from datetime import datetime

from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_list_or_404, \
    get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory, formset_factory, modelformset_factory
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required, login_required
from django.core.servers.basehttp import FileWrapper
from django.template import Context
from django import forms

from apps.build.models import Building, Ground
from apps.build.forms import BuildingForm, BuildingShowForm, GroundForm, GroundShowForm, BuildingSelectForm
from apps.core.views import get_fk_forms, get_fk_show_forms, split_form
from apps.core.models import WC, Room, Hallway, Kitchen, BaseWC, BaseRoom, BaseHallway, BaseKitchen, Developer
from apps.core.forms import DeveloperForm
from apps.user.models import CustomUser


def select_building_state(request):
    template = 'build_creation.html'
    context = {'title': _(u'Добавление объекта рынка жилья')}
    prefix = 'select_build'
    if request.method == "POST":
        select_form = BuildingSelectForm(request.POST, prefix=prefix)
        if select_form.is_valid():
            cd = select_form.cleaned_data
            dev_pk = cd.get('developer').pk if cd.get('developer') else None
            return add_building(request, dev_pk, cd.get('state'))
    else:
        form = BuildingSelectForm(prefix=prefix)
    context.update({'select_form': form})
    return render_to_response(template, context, context_instance=RequestContext(request))


def add_building(request, dev_pk=None, state=None):
    template = 'build_creation.html'
    context = {'title': _(u'Добавление объекта рынка жилья')}
    prefix, dev_prefix, select_prefix = 'build', 'dev', 'select_build'
    context.update({'state': state})
    select = state
    form = None
    dev=None
    if dev_pk:
        context.update({'dev': dev_pk})
        dev = Developer.objects.get(pk=dev_pk)
    if request.method == "POST" and 'build' in request.POST:
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(request=request)
        if select and int(select) == 2:
            form = GroundForm(request.POST, prefix=prefix)
            state_int = int(select)
        elif select and int(select) in [0, 1]:
            form = BuildingForm(request.POST, prefix=prefix)
            state_int = int(select)
        if not dev:
            dev_form = DeveloperForm(request.POST, prefix=dev_prefix)
            context.update({'dev_form': dev_form})
            if dev_form.is_valid():
                dev = dev_form.save()
            else:
                form, text_area_form = split_form(form)
                context.update({'form': form, 'text_area_fields': text_area_form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f]})
                return render_to_response(template, context, context_instance=RequestContext(request))
        if form.is_valid() and room_f.is_valid() and hallway_f.is_valid() and wc_f.is_valid() and kitchen_f.is_valid():
            building = form.save(commit=False)
            building.state = state_int
            building.developer = dev
            building.save()
            print building.state, building.developer, building.room
            building.room = room_f.save()
            building.hallway = hallway_f.save()
            building.wc = wc_f.save()
            building.kitchen = kitchen_f.save()
            building.save(update_fields=['room', 'kitchen', 'wc', 'hallway'])
            return redirect('buildings')
        else:
            form, text_area_form = split_form(form)
            context.update({'form': form, 'text_area_fields': text_area_form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f]})
            return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        if select and int(select) == 2:
            form = GroundForm(request.POST, prefix=prefix)
        elif select and int(select) in [0, 1]:
            form = BuildingForm(request.POST, prefix=prefix)
        if not dev:
            dev_form = DeveloperForm(prefix=dev_prefix)
            context.update({'dev_form': dev_form})
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms()
        form, text_area_form = split_form(form)
        context.update({'form': form, 'text_area_fields': text_area_form, 'prefix': prefix,
                        'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                        'titles': [
                            BaseRoom._meta.verbose_name,
                            BaseHallway._meta.verbose_name,
                            BaseWC._meta.verbose_name,
                            BaseKitchen._meta.verbose_name,
                        ]})
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def manage_developer(request, pk=None):
    template = 'developer_creation.html'
    context = {'title': _(u'Добавление застройщика(владельца) объекта')}
    if not pk:
        form = DeveloperForm(request.POST or {})
        if form.is_valid() and 'dev' in request.POST:
            form.save()
            return redirect('buildings')
    else:
        developer = Developer.objects.get(pk=pk)
        context.update({'object': developer})
        form = DeveloperForm(instance=developer)
        if request.method == "POST":
            form = DeveloperForm(request.POST, instance=developer)
            if form.is_valid() and 'dev' in request.POST:
                form.save()
                return redirect('buildings')
            else:
                form = DeveloperForm(request.POST, instance=developer)
    context.update({'form': form})
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def get_developers(request):
    template = 'developers.html'
    context = {'title': _(u'Застройщики(владельца) объекта')}
    if Developer.objects.all().exists():
        developers = Developer.objects.all()
        page = request.GET.get('page', '1')
        paginator = Paginator(developers, 50)
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        context.update({'developer_list': objects})
    return render(request, template, context,
                  context_instance=RequestContext(request))

@login_required
def get_buildings(request, pk=None, strv=None, numv=None):
    template = 'builds.html'
    context = {'title': _(u'Объекты рынка жилья')}
    if Building.objects.all().exists() or Ground.objects.all().exists():
        objects, build_objects, ground_objects = [], [], []
        if Building.objects.all().exists():
            build_objects = Building.objects.all().order_by('state')
            get = Building.objects.get
        if Ground.objects.all().exists():
            ground_objects = Ground.objects.all().order_by('state')
            get = Ground.objects.get
        objects = [x for x in build_objects] + [x for x in ground_objects]
        if pk or strv or numv:
            if pk:
                build_object = get(pk=pk)
            if strv:
                build_object = get(address__icontains=strv)
            if numv:
                build_object = get(state=numv)
            context.update({'object': build_object})
        page = request.GET.get('page', '1')
        paginator = Paginator(objects, 50)
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        context.update({'building_list': objects})
    return render(request, template, context, context_instance=RequestContext(request))


def get_building(request, pk, state=None, extra=None):
    context = {'title': _(u'Параметры объекта')}
    if state and int(state) == 2:
        build = Ground.objects.get(pk=pk)
        form = GroundForm(instance=build)
    else:
        build = Building.objects.get(pk=pk)
        form = BuildingForm(instance=build)
    if not request.user.is_staff or not request.user.is_superuser:
        form.fields.pop('approve_status')
    room_f, hallway_f, wc_f, kitchen_f = get_fk_show_forms(parent=build)
    context.update({'object': build, 'form': form, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                    'titles': [BaseRoom._meta.verbose_name, BaseHallway._meta.verbose_name, BaseWC._meta.verbose_name, BaseKitchen._meta.verbose_name]})
    return render(request, 'build.html', context, context_instance=RequestContext(request))


def approve_building(request, pk):
    """
    Send for approve (set approve status = 1)
    """
    if request.method == "GET":
        build = Building.objects.get(pk=pk)
        user = CustomUser.objects.get(pk=request.user.pk)
        if user.mo == build.mo:
            build.approve_status = 1
            build.save()

    return redirect('buildings')


def update_building(request, pk, state=None, extra=None):
    context = {'title': _(u'Параметры объекта')}
    if state and int(state) == 2:
        build = Ground.objects.get(pk=pk)
    else:
        build = Building.objects.get(pk=pk)
    prefix, room_p, hallway_p, wc_p, kitchen_p = 'build', 'room_build', 'hallway_build', 'wc_build', 'kitchen_build'
    if request.method == "POST":
        if state and int(state) == 2:
            form = GroundForm(request.POST, prefix=prefix, instance=build)
        else:
            form = BuildingForm(request.POST, prefix=prefix, instance=build)
        # check access rules. Add approve_status from object to form
        if not request.user.is_staff or not request.user.is_superuser:
            form.fields.update({'approve_status': forms.IntegerField()})
            data = form.data.copy()
            data['%s-approve_status' % form.prefix] = u'%s' % build.approve_status
            form.data = data
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=build, request=request)
        if form.is_valid() and room_f.is_valid() and hallway_f.is_valid() and wc_f.is_valid() and kitchen_f.is_valid():
            form.save()
            for obj in [room_f, hallway_f, wc_f, kitchen_f]:
                obj.save()
            return redirect('buildings')
        else:
            form, text_area_form = split_form(form)
            context.update({'object': build, 'form': form,  'text_area_fields': text_area_form, 'prefix': prefix,
                            'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                            'titles': [
                                BaseRoom._meta.verbose_name,
                                BaseHallway._meta.verbose_name,
                                BaseWC._meta.verbose_name,
                                BaseKitchen._meta.verbose_name,
                                ]})
            return render(request, 'build_updating.html', context, context_instance=RequestContext(request))
    else:
        if state and int(state) == 2:
            form = GroundForm(prefix=prefix, instance=build)
        else:
            form = BuildingForm(prefix=prefix, instance=build)
        # remove approve_status field from view if not admin
        if not request.user.is_staff or not request.user.is_superuser:
            form.fields.pop('approve_status')
        form, text_area_form = split_form(form)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=build)
        context.update({'object': build, 'form': form,  'text_area_fields': text_area_form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                        'titles': [
                            BaseRoom._meta.verbose_name,
                            BaseHallway._meta.verbose_name,
                            BaseWC._meta.verbose_name,
                            BaseKitchen._meta.verbose_name,
                            ]})
        return render(request, 'build_updating.html', context, context_instance=RequestContext(request))


def pre_delete_building(request, pk, state=None):
    context = {'title': _(u'Удаление объекта рынка жилья')}
    if state and int(state) == 2:
        build = Ground.objects.get(pk=pk)
    else:
        build = Building.objects.get(pk=pk)
    context.update({'object': build})
    return render_to_response("build_deleting.html", context, context_instance=RequestContext(request))


def delete_building(request, pk, state=None):
    context = {'title': _(u'Удаление объекта рынка жилья')}
    if state and int(state) == 2:
        build = Ground.objects.get(pk=pk)
    else:
        build = Building.objects.get(pk=pk)
    if build and 'delete' in request.POST:
        build.room.delete()
        build.hallway.delete()
        build.wc.delete()
        build.kitchen.delete()
        return redirect('buildings')
    elif 'cancel' in request.POST:
        return redirect('buildings')
    else:
        context.update({'error': _(u'Возникла ошибка при удалении объекта рынка жилья!')})
    return render_to_response("build_deleting.html", context, context_instance=RequestContext(request))


