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
from apps.core.models import Room, Hallway, WC, Kitchen
from apps.build.forms import BuildingForm, BuildingShowForm


def add_building(request):
    template = 'build_creation.html'
    context = {'title': _(u'Добавление строительного объекта')}
    prefix, room_p, hallway_p, wc_p, kitchen_p = 'build', 'room_build', 'hallway_build', 'wc_build', 'kitchen_build'
    RoomInlineFormSet = modelformset_factory(Room, can_delete=False)
    HallwayInlineFormSet = modelformset_factory(Hallway, can_delete=False)
    WCInlineFormSet = modelformset_factory(WC, can_delete=False)
    KitchenInlineFormSet = modelformset_factory(Kitchen, can_delete=False)
    if request.method == "POST":
        form = BuildingForm(request.POST, prefix=prefix)
        room_f = RoomInlineFormSet(request.POST, request.FILES, prefix=room_p)
        hallway_f = HallwayInlineFormSet(request.POST, request.FILES, prefix=hallway_p)
        wc_f = WCInlineFormSet(request.POST, request.FILES, prefix=wc_p)
        kitchen_f = KitchenInlineFormSet(request.POST, request.FILES, prefix=kitchen_p)
        if form.is_valid() and room_f.is_valid() and hallway_f.is_valid() and wc_f.is_valid() and kitchen_f.is_valid():
            building = form.save(commit=False)
            room_f.save()
            hallway_f.save()
            wc_f.save()
            kitchen_f.save()
            building.save()
            return redirect('buildings')
        else:
            context.update({'form': form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f]})
            return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        form = BuildingForm(prefix=prefix)
        room_f = RoomInlineFormSet(prefix=room_p)
        hallway_f = HallwayInlineFormSet(prefix=hallway_p)
        wc_f = WCInlineFormSet(prefix=wc_p)
        kitchen_f = KitchenInlineFormSet(prefix=kitchen_p)
    context.update({'form': form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                    'titles': ['Room', 'Hallway', 'WC', 'Kitchen']})
    return render_to_response(template, context, context_instance=RequestContext(request))


class BuildingListView(ListView):
    model = Building
    template_name = "builds.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(BuildingListView, self).get_context_data(**kwargs)
        context["title"] = _(u'Строительные материалы')
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BuildingListView, self).dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        data = self.request.GET.copy()
        if data.get("pk"):
            return Building.objects.get(pk=data.get("pk"))
        if data.get("strv"):
            return Building.objects.get(address__icontains=data.get("strv"))
        if data.get("numv"):
            return Building.objects.get(state=data.get("numv"))
        else:
            return super(BuildingListView, self).get_queryset(*args, **kwargs)


@login_required
def get_buildings(request, pk=None, strv=None, numv=None):
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


def get_building(request, pk, extra=None):
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


def update_building(request, pk, extra=None):
    context = {'title': _(u'Параметры объекта')}
    build = Building.objects.get(pk=pk)
    if request.method == "POST":
        form = BuildingForm(request.POST, instance=build)
        context.update({'form': form})
        if form.is_valid():
            form.save()
            return redirect('buildings')
    else:
        form = BuildingForm(instance=build)
        context.update({'form': form})
    context.update({'object': build})
    return render(request, 'build_updating.html', context, context_instance=RequestContext(request))


def pre_delete_building(request, pk, extra=None):
    pass


def delete_building(request, pk, extra=None):
    pass