# -*- coding: utf-8 -*-

import os
import webodt
import mimetypes
from copy import deepcopy
from webodt.converters import converter
from datetime import datetime
from copy import deepcopy

from django import forms
from django.http import HttpResponse, HttpResponseNotFound, \
    HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_list_or_404, \
    get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory, formset_factory, modelformset_factory
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required, login_required
from django.core.servers.basehttp import FileWrapper
from django.template import Context
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from apps.build.models import Building, Ground
from apps.build.forms import BuildingForm, BuildingShowForm, GroundForm, \
    GroundShowForm, BuildingSelectForm, BuildingMonitoringForm, \
    GroundMonitoringForm, BuildingSelectMonitoringForm
from apps.core.views import get_fk_forms, get_fk_show_forms, split_form
from apps.core.models import WC, Room, Hallway, Kitchen, BaseWC, BaseRoom, BaseHallway, BaseKitchen, Developer
from apps.core.forms import DeveloperForm, WCForm, RoomForm, HallwayForm, KitchenForm
from apps.user.models import CustomUser
from apps.mo.models import MO


@login_required
def select_monitoring_state(request):
    template = 'monitoring_creation.html'
    context = {'title': _(u'Добавление объекта мониторинга')}
    prefix = 'select_build'
    if request.method == "POST":
        select_form = BuildingSelectForm(request.POST, prefix=prefix)
        if select_form.is_valid():
            cd = select_form.cleaned_data
            if not cd.get('developer'):
                return redirect('add-monitoring-developer', state=int(cd.get('state')))
            dev_pk = cd.get('developer').pk
            return redirect('add-monitoring', state=cd.get('state'), dev_pk=dev_pk)
    else:
        form = BuildingSelectMonitoringForm(prefix=prefix)
    context.update({'select_form': form})
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def select_building_state(request):
    template = 'build_creation.html'
    context = {'title': _(u'Добавление объекта рынка жилья')}
    prefix = 'select_build'
    if request.method == "POST":
        select_form = BuildingSelectForm(request.POST, prefix=prefix)
        if select_form.is_valid():
            cd = select_form.cleaned_data
            if not cd.get('developer'):
                return redirect('add-building-developer', state=int(cd.get('state')))
            dev_pk = cd.get('developer').pk
            return redirect('add-building', state=cd.get('state'), dev_pk=dev_pk)
    else:
        form = BuildingSelectForm(prefix=prefix)
    context.update({'select_form': form})
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def add_building(request, dev_pk=None, state=None):
    template = 'build_creation.html'
    context = {'title': _(u'Добавление объекта рынка жилья')}
    prefix, dev_prefix, select_prefix = 'build', 'dev', 'select_build'
    context.update({'state': state})
    select = state
    form = None
    dev = Developer.objects.get(pk=dev_pk)
    context.update({'state': select, 'dev': dev_pk})
    if request.method == "POST" and 'build' in request.POST:
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(request=request)
        if select and int(select) == 2:
            form = GroundForm(request.POST, request.FILES, prefix=prefix)
            state_int = int(select)
        elif select and int(select) in [0, 1]:
            form = BuildingForm(request.POST, request.FILES, prefix=prefix)
            state_int = int(select)
        if not request.user.is_staff:
            form.fields.pop('approve_status')
            form.fields.pop('mo')
        if form.is_valid() and room_f.is_valid() and hallway_f.is_valid() and wc_f.is_valid() and kitchen_f.is_valid():
            building = form.save(commit=False)
            if not request.user.is_staff:
                building.mo = request.user.customuser.mo
            building.state = state_int
            building.developer = dev
            building.save()
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
            form = GroundForm(prefix=prefix)
        elif select and int(select) in [0, 1]:
            form = BuildingForm(prefix=prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms()
        form, text_area_form = split_form(form)
        if not request.user.is_staff:
            form.fields.pop('approve_status')
            form.fields.pop('mo')
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
def add_monitoring(request, dev_pk=None, state=None):
    template = 'monitoring_creation.html'
    context = {'title': _(u'Добавление объекта мониторинга')}
    prefix, dev_prefix, select_prefix = 'build', 'dev', 'select_build'
    context.update({'state': state})
    select = state
    form = None
    dev = Developer.objects.get(pk=dev_pk)
    context.update({'state': select, 'dev': dev_pk})
    if request.method == "POST" and 'build' in request.POST:
        if select and int(select) == 2:
            form = GroundMonitoringForm(request.POST, request.FILES,
                                        prefix=prefix)
            state_int = int(select)
        elif select and int(select) in [0, 1]:
            form = BuildingMonitoringForm(request.POST, request.FILES,
                                         prefix=prefix)
            state_int = int(select)
        # remove contract from adding. It will be avaible just on update
        form.fields.pop('contract')
        if not request.user.is_staff:
            form.fields.pop('approve_status')
            form.fields.pop('mo')
        if form.is_valid():
            building = form.save(commit=False)
            if not request.user.is_staff:
                building.mo = request.user.customuser.mo
            building.state = state_int
            building.developer = dev
            building.save()
            return redirect('monitorings')
        else:
            form, text_area_form = split_form(form)
            context.update({'form': form, 'text_area_fields': text_area_form, 'prefix': prefix, })
            return render_to_response(template, context, context_instance=RequestContext(request))
    elif request.method == "GET":
        if select and int(select) == 2:
            if request.user.is_superuser:
                form = GroundMonitoringForm(prefix=prefix)
            else:
                form = GroundMonitoringForm(prefix=prefix,
                    initial={'mo': request.user.customuser.mo})
        elif select and int(select) in [0, 1]:
            if request.user.is_superuser:
                form = BuildingMonitoringForm(prefix=prefix)
            else:
                form = BuildingMonitoringForm(prefix=prefix,
                    initial={'mo': request.user.customuser.mo})

        form, text_area_form = split_form(form)
        form.fields.pop('contract')
        if not request.user.is_staff:
            form.fields.pop('approve_status')
            form.fields.pop('mo')
        context.update({'form': form, 'text_area_fields': text_area_form, 'prefix': prefix,})
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def manage_developer(request, pk=None, state=None, ):
    template = 'developer_creation.html'
    context = {'title': _(u'Добавление застройщика(владельца) объекта')}
    if state:
        context.update({'state': int(state)})
    if not pk:
        form = DeveloperForm(request.POST or {})
        if form.is_valid() and 'dev' in request.POST:
            dev = form.save()
            if state:
                return redirect('add-building', state, dev.id)
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
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


@login_required
def manage_monitoring_developer(request, pk=None, state=None, ):
    template = 'monitoring_developer_creation.html'
    context = {'title': _(u'Добавление застройщика(владельца) объекта')}
    if state:
        context.update({'state': int(state)})
    if not pk:
        form = DeveloperForm(request.POST or {})
        if form.is_valid() and 'dev' in request.POST:
            dev = form.save()
            if state:
                return redirect('add-monitoring', state, dev.id)
            return redirect('monitorings')
    else:
        developer = Developer.objects.get(pk=pk)
        context.update({'object': developer})
        form = DeveloperForm(instance=developer)
        if request.method == "POST":
            form = DeveloperForm(request.POST, instance=developer)
            if form.is_valid() and 'dev' in request.POST:
                form.save()
                return redirect('monitorings')
            else:
                form = DeveloperForm(request.POST, instance=developer)
    context.update({'form': form})
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


@login_required()
def delete_developer(request, pk):
    if request.method != "GET":
        return HttpResponseNotFound("Not found")
    try:
        developer = Developer.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("Not found")
    developer.delete()
    return redirect("developers")


@login_required
def get_developers(request):
    template = 'developers.html'
    context = {'title': _(u'Застройщики(владельцы) объекта')}
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
def get_buildings(request, mo=None, strv=None, numv=None, all=False, template=None, title=None, null_contract=False):
    template = 'builds.html' if not template else template
    title = title if title else u' рынка жилья'
    kwargs = {}
    orkwargs = {}
    if all:
        context = {'title': _(u'Все объекты %s' % title)}
    if Building.objects.all().exists() or Ground.objects.all().exists():
        mo_obj=None
        objects, build_objects, ground_objects = [], [], []
        kwargs.update({'contract__isnull':null_contract})
        if mo:
            mo_obj = MO.objects.get(pk=mo)
        elif hasattr(request.user, 'customuser'):
            mo_obj = request.user.customuser.mo
            from_dt = request.user.customuser.get_user_date()
            if from_dt:
                kwargs.update({'start_year__lt': from_dt, 'finish_year__gt': from_dt})
        kwargs.update({'mo':mo_obj})
        context = {'title': _(u'Объекты %s %s' % (title, mo_obj.name))}
        if Building.objects.filter(**kwargs).exists():
            build_objects = Building.objects.filter(**kwargs).order_by('state')
        if Ground.objects.filter(**kwargs).exists():
            ground_objects = Ground.objects.filter(**kwargs).order_by('state')
        objects = [x for x in build_objects] + [x for x in ground_objects]
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


@login_required
def get_monitorings(request, mo=None, all=False):
    template = 'monitorings.html'
    title = u' мониторинга'
    return get_buildings(request, mo, all=all, template=template, title=title, null_contract=True)


@login_required
def get_building(request, pk, state=None, extra=None):
    context = {'title': _(u'Параметры объекта')}
    if state and int(state) == 2:
        build = Ground.objects.get(pk=pk)
        form = GroundForm(instance=build)
    else:
        build = Building.objects.get(pk=pk)
        form = BuildingForm(instance=build)
    if not request.user.is_staff:
        if build.mo != request.user.customuser.mo:
            return HttpResponseForbidden("Forbidden")
    if not request.user.is_staff:
        form.fields.pop('approve_status')
        form.fields.pop('mo')
    room_f, hallway_f, wc_f, kitchen_f = get_fk_show_forms(parent=build)
    context.update({'object': build, 'form': form, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                    'titles': [BaseRoom._meta.verbose_name, BaseHallway._meta.verbose_name, BaseWC._meta.verbose_name, BaseKitchen._meta.verbose_name]})
    return render(request, 'build.html', context, context_instance=RequestContext(request))


@login_required
def get_monitoring(request, pk, state=None, extra=None):
    context = {'title': _(u'Параметры объекта мониторинга')}
    if state and int(state) == 2:
        build = Ground.objects.get(pk=pk)
        form = GroundMonitoringForm(instance=build)
    else:
        build = Building.objects.get(pk=pk)
        form = BuildingMonitoringForm(instance=build)
    if not request.user.is_staff:
        if build.mo != request.user.customuser.mo:
            return HttpResponseForbidden("Forbidden")
    if not request.user.is_staff:
        form.fields.pop('approve_status')
        form.fields.pop('mo')
    context.update({'object': build, 'form': form,
                    'titles': [BaseRoom._meta.verbose_name, BaseHallway._meta.verbose_name, BaseWC._meta.verbose_name, BaseKitchen._meta.verbose_name]})
    return render(request, 'monitoring.html', context, context_instance=RequestContext(request))


@login_required
def approve_building(request, pk, state=None):
    """
    Send for approve (set approve status = 1)
    """
    if request.method == "GET":
        if state and int(state) == 2:
            build = Ground.objects.get(pk=pk)
        else:
            build = Building.objects.get(pk=pk)
        user = CustomUser.objects.get(pk=request.user.pk)
        if user.mo == build.mo:
            build.approve_status = 1
            build.save()

    return redirect('buildings')


@login_required
def update_building(request, pk, state=None, extra=None):
    context = {'title': _(u'Параметры объекта')}
    if state and int(state) == 2:
        build = Ground.objects.get(pk=pk)
    else:
        build = Building.objects.get(pk=pk)
    if not request.user.is_staff:
        if build.mo != request.user.customuser.mo:
            return HttpResponseForbidden("Forbidden")
    prefix, room_p, hallway_p, wc_p, kitchen_p = 'build', 'room_build', 'hallway_build', 'wc_build', 'kitchen_build'
    if request.method == "POST":
        if state and int(state) == 2:
            form = GroundForm(request.POST, request.FILES, prefix=prefix, instance=build)
        else:
            form = BuildingForm(request.POST, request.FILES, prefix=prefix, instance=build)
        # check access rules. Add approve_status from object to form
        if not request.user.is_staff:
            form.fields.pop('approve_status')
            form.fields.pop('mo')
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=build, request=request)
        if form.is_valid() and room_f.is_valid() and hallway_f.is_valid() and wc_f.is_valid() and kitchen_f.is_valid():
            new_build = form.save()
            new_build.room = room_f.save()
            if not request.user.is_staff:
                new_build.approve_status = build.approve_status
                new_build.mo = build.mo
                new_build.save()
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
        if not request.user.is_staff:
            form.fields.pop('approve_status')
            form.fields.pop('mo')
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


@login_required
def update_monitoring(request, pk, state=None, extra=None):
    context = {'title': _(u'Параметры объекта мониторинга')}
    if state and int(state) == 2:
        build = Ground.objects.get(pk=pk)
    else:
        build = Building.objects.get(pk=pk)
    if not request.user.is_staff:
        if build.mo != request.user.customuser.mo:
            return HttpResponseForbidden("Forbidden")
    prefix = 'monitoring'
    if request.method == "POST":
        if state and int(state) == 2:
            form = GroundMonitoringForm(request.POST, request.FILES,
                                        prefix=prefix, instance=build)
        else:
            form = BuildingMonitoringForm(request.POST, request.FILES,
                                          prefix=prefix, instance=build)
        form.fields['contract'].required = False
        # check access rules. Add approve_status from object to form
        if not request.user.is_staff:
            form.fields.pop('contract')
            form.fields.pop('approve_status')
            form.fields.pop('mo')
        if form.is_valid():
            new_build = form.save()
            # "move" to objects
            if form.cleaned_data.get('contract'):
                new_build.contract = form.cleaned_data['contract']
                new_build.room = Room()
                new_build.room.save()
                new_build.room_id = new_build.room.pk
                new_build.hallway = Hallway()
                new_build.hallway.save()
                new_build.hallway_id = new_build.hallway.pk
                new_build.wc = WC()
                new_build.wc.save()
                new_build.wc_id = new_build.wc.pk
                new_build.kitchen = Kitchen()
                new_build.kitchen.save()
                new_build.kitchen_id = new_build.kitchen.pk
                new_build.save(update_fields=['room', 'kitchen', 'wc', 'hallway', 'contract'])
            if not request.user.is_staff:
                new_build.approve_status = build.approve_status
                new_build.mo = build.mo
                new_build.save()
            if request.user.is_superuser:
                return redirect('monitorings-all')
            else:
                return redirect('monitorings')
        else:
            form, text_area_form = split_form(form)
            context.update({'object': build, 'form': form,
                            'text_area_fields': text_area_form, 'prefix': prefix, })
            return render(request, 'monitoring_updating.html',
                          context, context_instance=RequestContext(request))
    else:
        if state and int(state) == 2:
            # load all mos to form choices if user works with not his mo selected
            if not request.user.is_superuser and request.user.customuser.mo == build.mo:
                form = GroundMonitoringForm(prefix=prefix, instance=build,
                                            initial={'mo': request.user.customuser.mo})
            else:
                form = GroundMonitoringForm(prefix=prefix, instance=build)
        else:
            if not request.user.is_superuser and request.user.customuser.mo == build.mo:
                form = BuildingMonitoringForm(prefix=prefix, instance=build,
                                              initial={'mo': request.user.customuser.mo})
            else:
                form = BuildingMonitoringForm(prefix=prefix, instance=build)
        if not request.user.is_staff:
            form.fields.pop('contract')
            form.fields.pop('approve_status')
            form.fields.pop('mo')
        form, text_area_form = split_form(form)
        context.update({'object': build, 'form': form,
                        'text_area_fields': text_area_form, 'prefix': prefix, })
        return render(request, 'monitoring_updating.html', context, context_instance=RequestContext(request))


@login_required()
def copy_building(request, pk):

    def copy_object(obj):
        new_obj = deepcopy(obj)
        new_obj.id = None
        new_obj.pk = None
        return new_obj

    if request.method != "GET":
        return HttpResponseNotFound()
    try:
        building = Building.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('Not found')

    new_building = copy_object(building)
    if new_building.flat_num:
        new_building.flat_num += 1
    new_building.room = copy_object(building.room)
    new_building.room.save()
    new_building.room_id = new_building.room.id
    new_building.hallway = copy_object(building.hallway)
    new_building.hallway.save()
    new_building.hallway_id = new_building.hallway.id
    new_building.wc = copy_object(building.wc)
    new_building.wc.save()
    new_building.wc_id = new_building.wc.id
    new_building.kitchen = copy_object(building.kitchen)
    new_building.kitchen.save()
    new_building.kitchen_id = new_building.kitchen.id
    new_building.save()
    return redirect('update-building', pk=new_building.pk,
                    state=new_building.state)


@login_required
def pre_delete_building(request, pk, state=None):
    context = {'title': _(u'Удаление объекта рынка жилья')}
    if state and int(state) == 2:
        build = Ground.objects.get(pk=pk)
    else:
        build = Building.objects.get(pk=pk)
    if not request.user.is_staff:
        if build.mo != request.user.customuser.pk:
            return HttpResponseForbidden("Forbidden")
    context.update({'object': build})
    return render_to_response("build_deleting.html", context, context_instance=RequestContext(request))


@login_required
def pre_delete_monitoring(request, pk, state=None):
    context = {'title': _(u'Удаление объекта мониторинга')}
    if state and int(state) == 2:
        build = Ground.objects.get(pk=pk)
    else:
        build = Building.objects.get(pk=pk)
    if not request.user.is_staff:
        if build.mo != request.user.customuser.pk:
            return HttpResponseForbidden("Forbidden")
    context.update({'object': build})
    return render_to_response("monitoring_deleting.html", context, context_instance=RequestContext(request))


@login_required
def delete_building(request, pk, state=None):
    context = {'title': _(u'Удаление объекта')}
    if state and int(state) == 2:
        build = Ground.objects.get(pk=pk)
    else:
        build = Building.objects.get(pk=pk)
    if not request.user.is_staff:
        if build.mo != request.user.customuser.pk:
            return HttpResponseForbidden("Forbidden")
    if build and 'delete' in request.POST:
        build.room.delete()
        build.hallway.delete()
        build.wc.delete()
        build.kitchen.delete()
        build.delete()
        return redirect('buildings')
    elif 'cancel' in request.POST:
        return redirect('buildings')
    else:
        context.update({'error': _(u'Возникла ошибка при удалении объекта!')})
    return render_to_response("build_deleting.html", context, context_instance=RequestContext(request))


@login_required
def delete_monitoring(request, pk, state=None):
    context = {'title': _(u'Удаление объекта мониторинга')}
    if state and int(state) == 2:
        build = Ground.objects.get(pk=pk)
    else:
        build = Building.objects.get(pk=pk)
    if not request.user.is_staff:
        if build.mo != request.user.customuser.pk:
            return HttpResponseForbidden("Forbidden")
    if build and 'delete' in request.POST:
        build.delete()
        if request.user.is_superuser:
            redirect('monitorings-all')
        else:
            return redirect('monitorings')
    elif 'cancel' in request.POST:
        if request.user.is_superuser:
            redirect('monitorings-all')
        else:
            return redirect('monitorings')
    else:
        context.update({'error': _(u'Возникла ошибка при удалении объекта мониторинга!')})
    return render_to_response("monitoring_deleting.html", context, context_instance=RequestContext(request))
