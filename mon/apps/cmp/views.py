# -*- coding: utf-8 -*-

from datetime import datetime
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_list_or_404,\
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

from .models import Result, Auction, Person, CompareData
from .forms import ContractForm, ResultForm, AuctionForm, CompareDataForm, PersonForm, AuctionShowForm, ContractShowForm, \
    ResultShowForm, CompareDataShowForm
from apps.core.views import get_fk_forms, get_fk_show_forms, get_fk_cmp_forms
from apps.core.views import split_form
from apps.core.models import WC, Room, Hallway, Kitchen
from apps.build.models import Contract
from apps.build.forms import BuildingShowForm


def add_auction(request):
    template = 'auction_creation.html'
    context = {'title': _(u'Добавление аукциона')}
    prefix = 'auction'
    if request.method == "POST":
        form = AuctionForm(request.POST, prefix=prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(request=request)
        if form.is_valid() and room_f.is_valid() and hallway_f.is_valid() and wc_f.is_valid() and kitchen_f.is_valid():
            auction = form.save()
            auction.room = room_f.save()
            auction.hallway = hallway_f.save()
            auction.wc = wc_f.save()
            auction.kitchen = kitchen_f.save()
            auction.save(update_fields=['room', 'hallway', 'wc', 'kitchen'])
            return redirect('auctions')
        else:
            context.update({'form': form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f]})
            return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        form = AuctionForm(prefix=prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms()
        # move text_area fields to another form
        context.update({'form': form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                        'titles': [
                            Room._meta.verbose_name,
                            Hallway._meta.verbose_name,
                            WC._meta.verbose_name,
                            Kitchen._meta.verbose_name,
                            ]})
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def get_auctions(request, pk=None):
    template = 'auctions.html'
    context = {'title': _(u'Аукционы')}
    if Auction.objects.all().exists():
        objects = Auction.objects.all().order_by('stage')
        if pk:
            auction_object = Auction.objects.get(pk=pk)
            context.update({'object': auction_object})
        page = request.GET.get('page', '1')
        paginator = Paginator(objects, 50)
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        context.update({'auction_list': objects})
    return render(request, template, context, context_instance=RequestContext(request))


def get_auction(request, pk, extra=None):
    context = {'title': _(u'Параметры объекта')}
    auction = Auction.objects.get(pk=pk)
    if request.method == "POST":
        form = AuctionShowForm(request.POST, instance=auction)
        context.update({'form': form})
    else:
        form = AuctionShowForm(instance=auction)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_show_forms(parent=auction)
        context.update({'form': form, 'formsets': [room_f, hallway_f, wc_f, kitchen_f]})
    context.update({'object': auction})
    return render(request, 'auction.html', context, context_instance=RequestContext(request))


def update_auction(request, pk, extra=None):
    context = {'title': _(u'Параметры заказа')}
    auction = Auction.objects.get(pk=pk)
    prefix = 'auction'
    if request.method == "POST":
        form = AuctionForm(request.POST, prefix=prefix, instance=auction)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=auction, request=request)
        context.update({'object': auction, 'form': form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f]})
        if form.is_valid() and room_f.is_valid() and hallway_f.is_valid() and wc_f.is_valid() and kitchen_f.is_valid():
            form.save()
            for obj in [room_f, hallway_f, wc_f, kitchen_f]:
                obj.save()
            return redirect('auctions')
        else:
            context.update({'object': auction, 'form': form, 'prefix': prefix,
                            'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                            'titles': [
                                Room._meta.verbose_name,
                                Hallway._meta.verbose_name,
                                WC._meta.verbose_name,
                                Kitchen._meta.verbose_name,
                                ]})
            return render(request, 'auction_updating.html', context, context_instance=RequestContext(request))
    else:
        form = AuctionForm(instance=auction, prefix=prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=auction)
        context.update({'object': auction, 'form': form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
            'titles': [
                Room._meta.verbose_name,
                Hallway._meta.verbose_name,
                WC._meta.verbose_name,
                Kitchen._meta.verbose_name,
                ]})
    return render(request, 'auction_updating.html', context, context_instance=RequestContext(request))


def pre_delete_auction(request, pk):
    context = {'title': _(u'Удаление заказа')}
    auction = Auction.objects.get(pk=pk)
    context.update({'object': auction})
    return render_to_response("auction_deleting.html", context, context_instance=RequestContext(request))


def delete_auction(request, pk):
    context = {'title': _(u'Удаление заказа')}
    auction = Auction.objects.get(pk=pk)
    if auction and 'delete' in request.POST:
        auction.room.delete()
        auction.hallway.delete()
        auction.wc.delete()
        auction.kitchen.delete()
        auction.delete()
        return redirect('auctions')
    elif 'cancel' in request.POST:
        return redirect('auctions')
    else:
        context.update({'error': _(u'Возникла ошибка при удалении заказа!')})
    return render_to_response("auction_deleting.html", context, context_instance=RequestContext(request))


def add_contract(request):
    template = 'contract_creation.html'
    context = {'title': _(u'Добавление контракта')}
    prefix = 'contract'
    if request.method == "POST":
        form = ContractForm(request.POST, prefix=prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(request=request)
        if form.is_valid() and room_f.is_valid() and hallway_f.is_valid() and wc_f.is_valid() and kitchen_f.is_valid():
            contract = form.save()
            contract.room = room_f.save()
            contract.hallway = hallway_f.save()
            contract.wc = wc_f.save()
            contract.kitchen = kitchen_f.save()
            contract.save(update_fields=['room', 'hallway', 'wc', 'kitchen'])
            return redirect('contracts')
        else:
            context.update({'form': form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f]})
            return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        form = ContractForm(prefix=prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms()
        context.update({'form': form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                        'titles': [
                            Room._meta.verbose_name,
                            Hallway._meta.verbose_name,
                            WC._meta.verbose_name,
                            Kitchen._meta.verbose_name,
                            ]})
        return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def get_contracts(request, pk=None):
    template = 'contracts.html'
    context = {'title': _(u'Контракты')}
    if Contract.objects.all().exists():
        objects = Contract.objects.all()
        if pk:
            contract_object = Contract.objects.get(pk=pk)
            context.update({'object': contract_object})
        page = request.GET.get('page', '1')
        paginator = Paginator(objects, 50)
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        context.update({'contract_list': objects})
    return render(request, template, context, context_instance=RequestContext(request))


def get_contract(request, pk, extra=None):
    context = {'title': _(u'Параметры контракта')}
    contract = Contract.objects.get(pk=pk)
    if request.method == "POST":
        form = ContractShowForm(request.POST, instance=contract)
        context.update({'form': form})
    else:
        form = ContractShowForm(instance=contract)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_show_forms(parent=contract)
        context.update({'form': form, 'formsets': [room_f, hallway_f, wc_f, kitchen_f]})
    context.update({'object': contract})
    return render(request, 'contract.html', context, context_instance=RequestContext(request))


def update_contract(request, pk, extra=None):
    context = {'title': _(u'Параметры контракта')}
    contract = Contract.objects.get(pk=pk)
    prefix = 'contract'
    if request.method == "POST":
        form = ContractForm(request.POST, prefix=prefix, instance=contract)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=contract, request=request)
        context.update({'object': contract, 'form': form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f]})
        if form.is_valid() and room_f.is_valid() and hallway_f.is_valid() and wc_f.is_valid() and kitchen_f.is_valid():
            form.save()
            for obj in [room_f, hallway_f, wc_f, kitchen_f]:
                obj.save()
            return redirect('contracts')
        else:
            context.update({'object': contract, 'form': form, 'prefix': prefix,
                            'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                            'titles': [
                                Room._meta.verbose_name,
                                Hallway._meta.verbose_name,
                                WC._meta.verbose_name,
                                Kitchen._meta.verbose_name,
                                ]})
            return render(request, 'contract_updating.html', context, context_instance=RequestContext(request))
    else:
        form = ContractForm(instance=contract, prefix=prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=contract)
        context.update({'object': contract, 'form': form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                        'titles': [
                            Room._meta.verbose_name,
                            Hallway._meta.verbose_name,
                            WC._meta.verbose_name,
                            Kitchen._meta.verbose_name,
                            ]})
    return render(request, 'contract_updating.html', context, context_instance=RequestContext(request))


def pre_delete_contract(request, pk):
    context = {'title': _(u'Удаление контракта')}
    contract = Contract.objects.get(pk=pk)
    context.update({'object': contract})
    return render_to_response("contract_deleting.html", context, context_instance=RequestContext(request))


def delete_contract(request, pk):
    context = {'title': _(u'Удаление контракта')}
    contract = Contract.objects.get(pk=pk)
    if contract and 'delete' in request.POST:
        contract.room.delete()
        contract.hallway.delete()
        contract.wc.delete()
        contract.kitchen.delete()
        contract.delete()
        return redirect('contracts')
    elif 'cancel' in request.POST:
        return redirect('contracts')
    else:
        context.update({'error': _(u'Возникла ошибка при удалении контракта!')})
    return render_to_response("contract_deleting.html", context, context_instance=RequestContext(request))


def add_result(request):
    template = 'result_creation.html'
    context = {'title': _(u'Добавление результатов осмотра')}
    prefix, cmp_prefix = 'result', 'cmp_result'
    if request.method == "POST":
        form = ResultForm(request.POST, prefix=prefix)
        cmp_form = CompareDataForm(request.POST, prefix=cmp_prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(request=request)
        if form.is_valid() and cmp_form.is_valid() and room_f.is_valid() and hallway_f.is_valid() and wc_f.is_valid() and kitchen_f.is_valid():
            result = form.save()
            result.cmp_data = cmp_form.save()
            result.cmp_data.room = room_f.save()
            result.cmp_data.hallway = hallway_f.save()
            result.cmp_data.wc = wc_f.save()
            result.cmp_data.kitchen = kitchen_f.save()
            result.cmp_data.save(update_fields=['room', 'hallway', 'wc', 'kitchen'])
            result.save(update_fields=['cmp_data'])
            return redirect('results')
        else:
            form, text_area_form = split_form(form)
            context.update({'form': form, 'text_area_fields': text_area_form, 'cmp_form': cmp_form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f]})
            return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        form = ResultForm(prefix=prefix)
        cmp_form = CompareDataForm(prefix=cmp_prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms()
        form, text_area_form = split_form(form)
        context.update({'form': form, 'cmp_form': cmp_form, 'text_area_fields': text_area_form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                        'titles': [
                                            Room._meta.verbose_name,
                                            Hallway._meta.verbose_name,
                                            WC._meta.verbose_name,
                                            Kitchen._meta.verbose_name,
                                        ]})
        return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def get_results(request, pk=None):
    template = 'results.html'
    context = {'title': _(u'Осмотры')}
    if Result.objects.all().exists():
        objects = Result.objects.all()
        if pk:
            result_object = Result.objects.get(pk=pk)
            context.update({'object': result_object})
        page = request.GET.get('page', '1')
        paginator = Paginator(objects, 50)
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        context.update({'result_list': objects})
    return render(request, template, context, context_instance=RequestContext(request))


def get_result(request, pk, extra=None):
    context = {'title': _(u'Параметры осмотра')}
    result = Result.objects.get(pk=pk)
    prefix, cmp_prefix = 'result', 'cmp_result'
    if request.method == "POST":
        form = ResultShowForm(request.POST, instance=result, prefix=prefix)
        cmp_form = CompareDataShowForm(request.POST, instance=result.cmp_data, prefix=cmp_prefix)
        context.update({'form': form, 'cmp_form': cmp_form})
    else:
        form = ResultShowForm(instance=result, prefix=prefix)
        cmp_form = CompareDataShowForm(instance=result.cmp_data, prefix=cmp_prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_show_forms(parent=result.cmp_data)
        context.update({'form': form, 'cmp_form': cmp_form, 'formsets': [room_f, hallway_f, wc_f, kitchen_f]})
    context.update({'object': result})
    return render(request, 'result.html', context, context_instance=RequestContext(request))


def update_result(request, pk, extra=None):
    context = {'title': _(u'Параметры осмотра')}
    result = Result.objects.get(pk=pk)
    prefix, cmp_prefix = 'result', 'cmp_result'
    if request.method == "POST":
        form = ResultForm(request.POST, instance=result, prefix=prefix)
        cmp_form = CompareDataForm(request.POST, instance=result.cmp_data, prefix=cmp_prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=result.cmp_data, request=request)
        context.update({'object': result, 'form': form, 'cmp_form': cmp_form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f]})
        if form.is_valid() and cmp_form.is_valid() and room_f.is_valid() and hallway_f.is_valid() and wc_f.is_valid() and kitchen_f.is_valid():
            form.save()
            cmp_form.save()
            for obj in [room_f, hallway_f, wc_f, kitchen_f]:
                obj.save()
            return redirect('results')
        else:
            form, text_area_form = split_form(form)
            context.update({'object': result, 'form': form, 'text_area_fields': text_area_form, 'cmp_form': cmp_form, 'prefix': prefix,
                            'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                           'titles': [
                                            Room._meta.verbose_name,
                                            Hallway._meta.verbose_name,
                                            WC._meta.verbose_name,
                                            Kitchen._meta.verbose_name,
                                        ]})
            return render(request, 'result_updating.html', context, context_instance=RequestContext(request))
    else:
        form = ResultForm(instance=result, prefix=prefix)
        form, text_area_form = split_form(form)
        cmp_form = CompareDataForm(instance=result.cmp_data, prefix=cmp_prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=result.cmp_data)
        context.update({'object': result, 'form': form, 'text_area_fields': text_area_form, 'cmp_form': cmp_form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
               'titles': [
                                    Room._meta.verbose_name,
                                    Hallway._meta.verbose_name,
                                    WC._meta.verbose_name,
                                    Kitchen._meta.verbose_name,
                                ]})
        return render(request, 'result_updating.html', context, context_instance=RequestContext(request))


def pre_delete_result(request, pk):
    context = {'title': _(u'Удаление осмотра')}
    result = Result.objects.get(pk=pk)
    context.update({'object': result})
    return render_to_response("result_deleting.html", context, context_instance=RequestContext(request))


def delete_result(request, pk):
    context = {'title': _(u'Удаление осмотра')}
    result = Result.objects.get(pk=pk)
    if result and 'delete' in request.POST:
        result.cmp_data.delete()
        result.cmp_data.room.delete()
        result.cmp_data.hallway.delete()
        result.cmp_data.wc.delete()
        result.cmp_data.kitchen.delete()
        result.delete()
        return redirect('results')
    elif 'cancel' in request.POST:
        return redirect('results')
    else:
        context.update({'error': _(u'Возникла ошибка при удалении результатов осмотра!')})
    return render_to_response("result_deleting.html", context, context_instance=RequestContext(request))


def manage_person(request, pk=None):
    template = 'person_creation.html'
    context = {'title': _(u'Добавление участника осмотров')}
    if not pk:
        form = PersonForm(request.POST or {})
        if form.is_valid() and 'pers' in request.POST:
            form.save()
            return redirect('results')
    else:
        person = Person.objects.get(pk=pk)
        context.update({'object': person})
        form = PersonForm(instance=person)
        if request.method == "POST":
            form = PersonForm(request.POST, instance=person)
            if form.is_valid() and 'pers' in request.POST:
                form.save()
                return redirect('results')
            else:
                form = PersonForm(request.POST, instance=person)
    context.update({'form': form})
    return render_to_response(template, context, context_instance=RequestContext(request))


def cmp_contract(request, pk):
    context = {'title': _(u'Сравнение параметров')}
    contract = Contract.objects.get(pk=pk)

    form = ContractShowForm(instance=contract)
    room_f, hallway_f, wc_f, kitchen_f = get_fk_show_forms(parent=contract)
    context.update({'form': form, 'formsets': [room_f, hallway_f, wc_f, kitchen_f]})

    if contract.building_set.all().exists():
        cmp_obj = contract.building_set.all()[0]
    elif contract.ground_set.all().exists():
        cmp_obj = contract.ground_set.all()[0]
    else:
        context.update({'errorlist': _('No one matched object')})
        return render(request, 'cmp.html', context, context_instance=RequestContext(request))
    cmp_form = BuildingShowForm(instance=cmp_obj, cmp_initial=contract)
    room_cf, hallway_cf, wc_cf, kitchen_cf = get_fk_cmp_forms(parent=cmp_obj, cmp=contract)
    context.update({'cmp_form': cmp_form, 'cmp_formsets': [room_cf, hallway_cf, wc_cf, kitchen_cf]})

    context.update({'object': contract, 'cmp_object': cmp_obj,
                    'titles': [Room._meta.verbose_name, Hallway._meta.verbose_name,
                    WC._meta.verbose_name, Kitchen._meta.verbose_name]})
    return render(request, 'cmp.html', context, context_instance=RequestContext(request))