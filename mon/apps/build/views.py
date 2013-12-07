# -*- coding: utf-8 -*-

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

from apps.build.models import Building
from apps.build.forms import BuildingForm, BuildingShowForm
from apps.core.views import get_fk_forms, get_fk_show_forms, split_form
from apps.core.models import WC, Room, Hallway, Kitchen, Developer
from apps.core.forms import DeveloperForm


def add_building(request):
    template = 'build_creation.html'
    context = {'title': _(u'Добавление объекта рынка жилья')}
    prefix = 'build'
    if request.method == "POST":
        form = BuildingForm(request.POST, prefix=prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(request=request)
        if form.is_valid() and room_f.is_valid() and hallway_f.is_valid() and wc_f.is_valid() and kitchen_f.is_valid():
            building = form.save()
            building.room = room_f.save()
            building.hallway = hallway_f.save()
            building.wc = wc_f.save()
            building.kitchen = kitchen_f.save()
            building.save(update_fields=['room', 'hallway', 'wc', 'kitchen'])
            return redirect('buildings')
        else:
            form, text_area_form = split_form(form)
            context.update({'form': form, 'text_area_fields': text_area_form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f]})
            return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        form = BuildingForm(prefix=prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms()
        form, text_area_form = split_form(form)
        context.update({'form': form, 'text_area_fields': text_area_form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                        'titles': [
                            Room._meta.verbose_name,
                            Hallway._meta.verbose_name,
                            WC._meta.verbose_name,
                            Kitchen._meta.verbose_name,
                        ]})
    return render_to_response(template, context, context_instance=RequestContext(request))


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
def get_buildings(request, pk=None, strv=None, numv=None):
    template = 'builds.html'
    context = {'title': _(u'Объекты рынка жилья')}
    if Building.objects.all().exists():
        objects = Building.objects.all().order_by('state')
        if pk or strv or numv:
            if pk:
                build_object = Building.objects.get(pk=pk)
            if strv:
                build_object = Building.objects.get(address__icontains=strv)
            if numv:
                build_object = Building.objects.get(state=numv)
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


def get_building(request, pk, extra=None):
    context = {'title': _(u'Параметры объекта')}
    build = Building.objects.get(pk=pk)
    form = BuildingForm(instance=build)
    room_f, hallway_f, wc_f, kitchen_f = get_fk_show_forms(parent=build)
    context.update({'object': build, 'form': form, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                    'titles': [Room._meta.verbose_name, Hallway._meta.verbose_name, WC._meta.verbose_name, Kitchen._meta.verbose_name]})
    return render(request, 'build.html', context, context_instance=RequestContext(request))


def update_building(request, pk, extra=None):
    context = {'title': _(u'Параметры объекта')}
    build = Building.objects.get(pk=pk)
    prefix, room_p, hallway_p, wc_p, kitchen_p = 'build', 'room_build', 'hallway_build', 'wc_build', 'kitchen_build'
    if request.method == "POST":
        form = BuildingForm(request.POST, prefix=prefix, instance=build)
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
                                Room._meta.verbose_name,
                                Hallway._meta.verbose_name,
                                WC._meta.verbose_name,
                                Kitchen._meta.verbose_name,
                                ]})
            return render(request, 'build_updating.html', context, context_instance=RequestContext(request))
    else:
        form = BuildingForm(instance=build, prefix=prefix)
        form, text_area_form = split_form(form)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=build)
        context.update({'object': build, 'form': form,  'text_area_fields': text_area_form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                        'titles': [
                            Room._meta.verbose_name,
                            Hallway._meta.verbose_name,
                            WC._meta.verbose_name,
                            Kitchen._meta.verbose_name,
                            ]})
        return render(request, 'build_updating.html', context, context_instance=RequestContext(request))


def pre_delete_building(request, pk):
    context = {'title': _(u'Удаление объекта рынка жилья')}
    build = Building.objects.get(pk=pk)
    context.update({'object': build})
    return render_to_response("build_deleting.html", context, context_instance=RequestContext(request))


def delete_building(request, pk):
    context = {'title': _(u'Удаление объекта рынка жилья')}
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
