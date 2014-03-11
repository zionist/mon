# -*- coding: utf-8 -*-

import os
import webodt
import mimetypes
import xlwt
from copy import deepcopy
from webodt.converters import converter
from datetime import datetime

from django import forms
from django.http import HttpResponse, HttpResponseNotFound, \
    HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden, \
    QueryDict
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_list_or_404, \
    get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory, formset_factory, \
    modelformset_factory, model_to_dict
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required, login_required
from django.core.servers.basehttp import FileWrapper
from django.template import Context
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db.models.fields.related import ForeignKey as FkFieldType

from apps.build.models import Building, Ground, CopyBuilding
from apps.build.forms import BuildingForm, BuildingShowForm, GroundForm, \
    GroundShowForm, BuildingSelectForm, BuildingMonitoringForm, CopyBuildingForm, \
    GroundMonitoringForm, BuildingSelectMonitoringForm, BuildingUpdateForm, GroundUpdateForm, \
    CopyForm
from apps.core.views import get_fk_forms, get_fk_show_forms, split_form, copy_object
from apps.core.models import WC, Room, Hallway, Kitchen, BaseWC, BaseRoom, BaseHallway, BaseKitchen, Developer
from apps.core.forms import DeveloperForm, WCForm, RoomForm, HallwayForm, KitchenForm
from apps.user.models import CustomUser
from apps.cmp.models import Contract
from apps.mo.models import MO
from apps.core.templatetags.extras import get_choice_or_value


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
def select_building_state(request, contract=None):
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
    state_int = None
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
            if not request.user.is_staff and hasattr(request.user, 'customuser'):
                building.mo = request.user.customuser.mo
            building.state = state_int if state_int else 0
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
        initial_kw = {}
        if hasattr(request.user, 'customuser'):
            initial_kw.update({'mo': request.user.customuser.mo})
        if select and int(select) == 2:
            form = GroundForm(prefix=prefix, initial=initial_kw)
        elif select and int(select) in [0, 1]:
            form = BuildingForm(prefix=prefix, initial=initial_kw)
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
    state_int = None
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
            # set deafult approve status - required check
            if not request.user.is_staff:
                building.approve_status = 0
            if not request.user.is_staff:
                building.mo = request.user.customuser.mo
            building.state = state_int if state_int else 0
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
def manage_developer(request, pk=None, state=None,
                     template='developer_creation.html',  monitoring=False):
    context = {'title': _(u'Добавление застройщика(владельца) объекта')}
    if state:
        context.update({'state': int(state)})
    if not pk:
        form = DeveloperForm(request.POST or {})
        if form.is_valid() and 'dev' in request.POST:
            dev = form.save()
            if state:
                if monitoring:
                    return redirect('add-monitoring', state, dev.id)
                else:
                    return redirect('add-building', state, dev.id)
            if monitoring:
                return redirect('monitorings')
            else:
                return redirect('buildings')
    else:
        developer = Developer.objects.get(pk=pk)
        context.update({'object': developer})
        form = DeveloperForm(instance=developer)
        if request.method == "POST":
            form = DeveloperForm(request.POST, instance=developer)
            if form.is_valid() and 'dev' in request.POST:
                form.save()
                if monitoring:
                    return redirect('monitorings')
                else:
                    return redirect('buildings')
            else:
                form = DeveloperForm(request.POST, instance=developer)
    context.update({'form': form})
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


@login_required
def manage_monitoring_developer(request, pk=None, state=None, ):
    return manage_developer(request, pk, state,
                            template='monitoring_developer_creation.html',
                            monitoring=True)


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


@login_required()
def delete_building_copy(request, pk):
    if request.method != "GET":
        return HttpResponseNotFound("Not found")
    try:
        copy = CopyBuilding.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("Not found")
    copy.room.delete()
    copy.hallway.delete()
    copy.wc.delete()
    copy.kitchen.delete()
    copy.delete()
    return redirect("building_copies")


@login_required()
def update_building_copy(request, pk):
    # TODO: add file moving code
    if request.method != "GET":
        return HttpResponseNotFound("Not found")
    try:
        copy = CopyBuilding.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("Not found")
    form = CopyBuildingForm(prefix='build', instance=copy)
    prefix, dev_prefix, select_prefix = 'build', 'dev', 'select_build'
    room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=copy)
    form, text_area_form = split_form(form)
    context = {'title': _(u'Добавление рынка жилья')}
    context.update({'state': copy.state, 'dev': copy.developer.pk})
    context.update({'object': copy, 'form': form,
                    'text_area_fields': text_area_form, 'prefix': prefix,
                    'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                    'titles': [
                        BaseRoom._meta.verbose_name,
                        BaseHallway._meta.verbose_name,
                        BaseWC._meta.verbose_name,
                        BaseKitchen._meta.verbose_name,
                        ]})
    delete_building_copy(request, copy.pk)
    return render(request, 'build_creation.html', context,
                  context_instance=RequestContext(request))


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
def get_buildings(request, mo=None, all=False, template=None,
                  title=None, null_contract=False, copies=False, xls=False):
    template = 'builds.html' if not template else template
    title = title if title else u' рынка жилья'
    context = {'title': _(u'Объекты %s' % (title))}
    objects, build_objects, ground_objects = [], [], []
    kwargs = {}
    kwargs.update({'contract__isnull': null_contract})

    mo_obj = None
    if mo:
        mo_obj = MO.objects.get(pk=mo)
    elif hasattr(request.user, 'customuser'):
        mo_obj = request.user.customuser.mo

    if hasattr(request.user, 'customuser') and request.user.customuser.get_user_date():
        from_dt = request.user.customuser.get_user_date()
        kwargs.update({'start_year__lt': from_dt, 'finish_year__gt': from_dt})

    if all:
        context = {'title': _(u'Все объекты %s' % title)}
    elif mo_obj:
        context = {'title': _(u'Объекты %s' % (title))}
        kwargs.update({'mo': mo_obj})

    if copies:
        if CopyBuilding.objects.filter(**kwargs).exists():
            build_objects = CopyBuilding.objects.filter(**kwargs).order_by('address')
    else:
        if Building.objects.filter(**kwargs).exists():
            build_objects = Building.objects.filter(**kwargs).order_by('address')
        if Ground.objects.filter(**kwargs).exists():
            ground_objects = Ground.objects.filter(**kwargs).order_by('address')

    objects = [x for x in build_objects] + [x for x in ground_objects]
    # return xls list
    if xls:
        return to_xls(request,  objects={BuildingForm: build_objects,
                                         GroundForm: ground_objects})
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


# object instance: form for display
def to_xls(request, objects={}):
    # create
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('untitled')

    # styles
    style_plain = xlwt.easyxf(
        "font: height 180;"
        "border: left thin, right thin, top thin, bottom thin;"
        "align: vertical center, horizontal center, wrap True;"
    )
    style_bold = xlwt.easyxf(
        "font: bold 1, height 180;"
        "border: left thin, right thin, top thin, bottom thin;"
        "align: vertical center, horizontal center, wrap True;"
    )
    date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')


    # object fields should be same as form fields
    # get all types of objects

    room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(request=request)
    fk_forms = {u'Санузел': wc_f, u'Прихожая': hallway_f,
                u'Кухня': kitchen_f, u'Комната': room_f}
    row = 0
    for form, objs in objects.iteritems():
        if not objs:
            continue
        # make headers
        header_form = form()
        col = 0
        for field in header_form:
            sheet.write(row, col, field.label if field.label else field.name,
                        style_bold)
            col += 1
        for fk_name, fk_form in fk_forms.iteritems():
            for field in fk_form:
                sheet.write(row, col, u"%s %s" % (fk_name, field.label)
                    if field.label else u"%s %s" % (fk_name, field.name),
                            style_bold)
                col += 1
        # write values
        row += 1
        for obj in objs:
            col = 0
            obj_form = form(instance=obj)
            for field in obj_form:
                value = obj_form.initial.get(field.name)
                if isinstance(value, bool) and value:
                    value = u"Да"
                elif isinstance(value, bool) and not value:
                    value = u"Нет"
                elif not value:
                    value = u''
                else:
                    value = u"%s" % get_choice_or_value(obj_form, field.name)
                sheet.write(row, col, value)
                col += 1

            # write fk forms values
            room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=obj)
            fk_forms = {u'Санузел': wc_f, u'Прихожая': hallway_f,
                        u'Кухня': kitchen_f, u'Комната': room_f}
            for fk_name, fk_form in fk_forms.iteritems():
                for field in fk_form:
                    value = fk_form.initial.get(field.name)
                    if isinstance(value, bool) and value:
                        value = u"Да"
                    elif isinstance(value, bool) and not value:
                        value = u"Нет"
                    elif not value:
                        value = u''
                    else:
                        value = u"%s" % get_choice_or_value(fk_form,
                                                            field.name)
                    sheet.write(row, col, value)
                    col += 1
            row += 1

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=list.xls'
    book.save(response)
    # return HttpResponse("Ok")
    return response


@login_required
def get_monitorings(request, mo=None, all=False):
    template = 'monitorings.html'
    title = u' мониторинга'
    return get_buildings(request, mo, all=all, template=template, title=title, null_contract=True)


@login_required
def get_building_copies(request, mo=None, all=False):
    template = 'copies.html'
    title = u' копий'
    return get_buildings(request, mo, all=all, template=template,
                         title=title, null_contract=False, copies=True)


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
    context.update({'object': build, 'form': form, 'copyform': CopyForm(), 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
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
            form = GroundUpdateForm(request.POST, request.FILES, prefix=prefix, instance=build)
        else:
            form = BuildingUpdateForm(request.POST, request.FILES, prefix=prefix, instance=build)
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
        initial_kw = {'mo': build.mo}
        if state and int(state) == 2:
            form = GroundUpdateForm(prefix=prefix, instance=build, initial=initial_kw)
        else:
            form = BuildingUpdateForm(prefix=prefix, instance=build, initial=initial_kw)
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

    form = CopyForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data["amount"]
    if amount <= 0:
        return HttpResponse(u"Пожалуйста введите положительное целое число")

    try:
        building = Building.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('Not found')

    build_dict = forms.model_to_dict(building)

    for n in ['wc', 'kitchen', 'hallway', 'room', 'mo', 'contract', 'id', 'developer']:
        build_dict.pop(n)

    # does not work https://docs.djangoproject.com/en/dev/ref/models/querysets/ (bulk_create)
    # copies = []
    # for c in xrange(amount):
    #    copies.append(CopyBuilding(**build_dict))
    # CopyBuilding.objects.bulk_create(copies)

    for copy in xrange(amount):
        # fks
        copy = CopyBuilding(**build_dict)
        copy.mo = building.mo
        copy.contract = building.contract
        copy.developer = building.developer

        # create new fk related objects
        copy.room = copy_object(building.room)
        copy.room.save()
        copy.room_id = copy.room.id
        copy.hallway = copy_object(building.hallway)
        copy.hallway.save()
        copy.hallway_id = copy.hallway.id
        copy.wc = copy_object(building.wc)
        copy.wc.save()
        copy.wc_id = copy.wc.id
        copy.kitchen = copy_object(building.kitchen)
        copy.kitchen.save()
        copy.kitchen_id = copy.kitchen.id
        copy.save()
    return get_building_copies(request)


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
