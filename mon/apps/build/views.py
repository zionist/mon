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

from apps.build.models import Building
from apps.build.forms import BuildingForm, BuildingShowForm


def add_build(request):
    template = 'build_creation.html'
    context = {'title': _(u'Добавление строительного объекта')}
    prefix = 'build'
    if request.method == "POST":
        form = BuildingForm(request.POST, prefix=prefix)
        if form.is_valid():
            build = form.save(commit=False)
            build.save()
            return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        form = BuildingForm(prefix=prefix)
    context.update({'form': form, 'prefix': prefix})
    return render_to_response(template, context, context_instance=RequestContext(request))


def get_builds(request, pk=None, strv=None, numv=None):
    template = 'builds.html'
    context = {'title': _(u'Строительные объекты')}
    if Building.objects.all().exists():
        objects = Building.objects.all()
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
        context.update({'objects_list': objects})
    return render(request, template, context, context_instance=RequestContext(request))


def get_build(request, pk, extra=None):
    context = {'title': _(u'Параметры объекта')}
    build = Building.objects.get(pk=pk)
    if request.method == "POST":
        form = BuildingShowForm(request.POST, instance=build)
        context.update({'form': form})
    else:
        form = BuildingShowForm(instance=build)
        context.update({'form': form})
    context.update({'object': build})
    return render(request, 'build.html', context, context_instance=RequestContext(request))


def update_build(request, pk, extra=None):
    context = {'title': _(u'Параметры объекта')}
    build = Building.objects.get(pk=pk)
    if request.method == "POST":
        form = BuildingForm(request.POST, instance=build)
        context.update({'form': form})
        if form.is_valid():
            form.save()
            return redirect('builds')
    else:
        form = BuildingForm(instance=build)
        context.update({'form': form})
    context.update({'object': build})
    return render(request, 'build_updating.html', context, context_instance=RequestContext(request))


def pre_delete_build(request, pk, extra=None):
    pass


def delete_build(request, pk, extra=None):
    pass