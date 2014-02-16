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

from .models import Result, AuctionDocuments, Auction, Person, CompareData
from .forms import ContractForm, ResultForm, AuctionForm, CompareDataForm, PersonForm, AuctionShowForm, ContractShowForm, \
    ResultShowForm, CompareDataShowForm, AuctionDocumentsForm, ContractDocumentsForm
from apps.core.views import get_fk_forms, get_fk_show_forms, get_fk_cmp_forms
from apps.core.views import split_form, set_fields_equal
from apps.core.models import BaseWC, BaseRoom, BaseHallway, BaseKitchen, WC, Room, Hallway, Kitchen
from apps.build.models import Contract, ContractDocuments
from apps.build.forms import BuildingShowForm, GroundShowForm
from apps.imgfile.models import Image
from apps.mo.models import MO


@login_required
def add_auction(request):
    template = 'auction_creation.html'
    context = {'title': _(u'Добавление аукциона')}
    prefix, images_prefix = 'auction', 'auction_images'
    if request.method == "POST":
        image_form = AuctionDocumentsForm(request.POST, request.FILES, prefix=images_prefix)
        form = AuctionForm(request.POST, request.FILES, prefix=prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(request=request, multi=True)
        if form.is_valid() and image_form.is_valid() and room_f.is_valid() and hallway_f.is_valid() and wc_f.is_valid() and kitchen_f.is_valid():
            auction = form.save()
            auction.docs = image_form.save()
            auction.room = room_f.save()
            auction.hallway = hallway_f.save()
            auction.wc = wc_f.save()
            auction.kitchen = kitchen_f.save()
            auction.save(update_fields=['room', 'hallway', 'wc', 'kitchen', 'docs'])
            return redirect('auctions')
        else:
            context.update({'form': form, 'images': image_form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f]})
            return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        image_form = AuctionDocumentsForm(prefix=images_prefix)
        form = AuctionForm(prefix=prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(multi=True)
        # move text_area fields to another form
        context.update({'form': form, 'images': image_form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                        'titles': [
                            BaseRoom._meta.verbose_name,
                            BaseHallway._meta.verbose_name,
                            BaseWC._meta.verbose_name,
                            BaseKitchen._meta.verbose_name,
                            ]})
    return render_to_response(template, context, context_instance=RequestContext(request))


def count_flats(obj_set, vals, **kwargs):
    amount = 0
    val = ', '.join(vals) if len(vals) > 1 else vals[0]
    objs = obj_set.filter(**kwargs).values(val)
    for obj in objs:
        for val in vals:
            if obj.get(val):
                amount += int(obj.get(val))
    return amount


@login_required
def get_auctions(request, pk=None):
    template = 'auctions.html'
    context = {'title': _(u'Все аукционы')}
    if MO.objects.all().exists():
        mos = MO.objects.all().order_by('name')
        objects = []
        for mo in mos:
            amount_0 = mo.home_orphans
            amount_1 = mo.auction_set.filter(stage=0).count() if mo.auction_set.filter(stage=0).exists() else 0
            amount_2 = mo.auction_set.filter(stage=1).count() if mo.auction_set.filter(stage=1).exists() else 0
            amount_3 = mo.auction_set.filter(stage=3).count() if mo.auction_set.filter(stage=3).exists() else 0
            amount_4 = mo.auction_set.filter(stage=4).count() if mo.auction_set.filter(stage=4).exists() else 0
            objects.append({'id': mo.id, 'name': mo.name, 'creation_form': mo.creation_form, 'auctions': mo.auction_set,
                            'amount_0': amount_0, 'amount_1': amount_1, 'amount_2': amount_2, 'amount_3': amount_3,
                            'amount_4': amount_4})
        for obj in objects:
            for name in ['amount_1', 'amount_2', 'amount_3', 'amount_4']:
                obj.update({name: count_flats(obj.get('auctions'), vals=['flats_amount'], **{'stage': name[-1:]})})
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


@login_required
def get_mo_auctions(request, pk=None):
    context = {'title': _(u'Аукционы')}
    template = 'mo_auctions.html'
    if Auction.objects.all().exists():
        kwargs = {}
        mo_obj = None
        if pk:
            mo_obj = MO.objects.get(pk=pk)
            context = {'title': _(u'Аукционы %s' % mo_obj.name)}
        elif hasattr(request.user, 'customuser'):
            mo_obj = request.user.customuser.mo
            context = {'title': _(u'Аукционы %s' % mo_obj.name)}
            from_dt = request.user.customuser.get_user_date()
            if from_dt:
                kwargs.update({'start_year__lt': from_dt, 'finish_year__gt': from_dt})
        else:
            context = {'title': _(u'Все аукционы')}
        context.update({'object': mo_obj})
        kwargs.update({'mo': mo_obj})
        objects = Auction.objects.filter(**kwargs).order_by('stage')
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


@login_required
def get_auction(request, pk, extra=None):
    context = {'title': _(u'Параметры аукциона')}
    auction = Auction.objects.get(pk=pk)
    prefix, images_prefix = 'auction', 'auction_images'
    if request.method == "POST":
        form = AuctionShowForm(request.POST, instance=auction)
        context.update({'form': form})
    else:
        form = AuctionShowForm(prefix=prefix, instance=auction)
        image_form = AuctionDocumentsForm(prefix=images_prefix, instance=auction.docs)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_show_forms(parent=auction, multi=True)
        context.update({'form': form, 'images': image_form, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                        'titles': [BaseRoom._meta.verbose_name, BaseHallway._meta.verbose_name,
                                   BaseWC._meta.verbose_name, BaseKitchen._meta.verbose_name,]})
    context.update({'object': auction})
    return render(request, 'auction.html', context, context_instance=RequestContext(request))


@login_required
def update_auction(request, pk, extra=None):
    context = {'title': _(u'Параметры аукциона')}
    auction = Auction.objects.get(pk=pk)
    prefix, images_prefix = 'auction', 'auction_images'
    if request.method == "POST":
        form = AuctionForm(request.POST, request.FILES, prefix=prefix, instance=auction)
        image_form = AuctionDocumentsForm(request.POST, request.FILES, prefix=images_prefix, instance=auction.docs)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=auction, request=request, multi=True)
        context.update({'object': auction, 'form': form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f]})
        if form.is_valid() and image_form.is_valid() and room_f.is_valid() and hallway_f.is_valid() and wc_f.is_valid() and kitchen_f.is_valid():
            form.save()
            image_form.save()
            for obj in [room_f, hallway_f, wc_f, kitchen_f]:
                obj.save()
            return redirect('auctions')
        else:
            context.update({'object': auction, 'form': form, 'images': image_form, 'prefix': prefix,
                            'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                            'titles': [
                                BaseRoom._meta.verbose_name,
                                BaseHallway._meta.verbose_name,
                                BaseWC._meta.verbose_name,
                                BaseKitchen._meta.verbose_name,
                                ]})
            return render(request, 'auction_updating.html', context, context_instance=RequestContext(request))
    else:
        image_form = AuctionDocumentsForm(instance=auction.docs, prefix=images_prefix)
        form = AuctionForm(instance=auction, prefix=prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=auction, multi=True)
        context.update({'object': auction, 'form': form, 'images': image_form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                        'titles': [BaseRoom._meta.verbose_name, BaseHallway._meta.verbose_name,
                                   BaseWC._meta.verbose_name, BaseKitchen._meta.verbose_name]})
    return render(request, 'auction_updating.html', context, context_instance=RequestContext(request))


@login_required
def pre_delete_auction(request, pk):
    context = {'title': _(u'Удаление заказа')}
    auction = Auction.objects.get(pk=pk)
    context.update({'object': auction})
    return render_to_response("auction_deleting.html", context, context_instance=RequestContext(request))


@login_required
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


@login_required
def add_contract(request):
    template = 'contract_creation.html'
    context = {'title': _(u'Добавление контракта')}
    prefix, images_prefix = 'contract', 'contract_images'
    if request.method == "POST":
        form = ContractForm(request.POST, request.FILES, prefix=prefix)
        image_form = ContractDocumentsForm(request.POST, request.FILES, prefix=images_prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(request=request)
        if form.is_valid() and image_form.is_valid() and room_f.is_valid() and hallway_f.is_valid() and wc_f.is_valid() and kitchen_f.is_valid():
            contract = form.save()
            contract.docs = image_form.save()
            contract.room = room_f.save()
            contract.hallway = hallway_f.save()
            contract.wc = wc_f.save()
            contract.kitchen = kitchen_f.save()
            contract.save(update_fields=['room', 'hallway', 'wc', 'kitchen', 'docs'])
            return redirect('contracts')
        else:
            context.update({'form': form, 'prefix': prefix, 'images': image_form, 'formsets': [room_f, hallway_f, wc_f, kitchen_f]})
            return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        image_form = ContractDocumentsForm(prefix=images_prefix)
        form = ContractForm(prefix=prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms()
        context.update({'form': form, 'prefix': prefix, 'images': image_form, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                        'titles': [
                            BaseRoom._meta.verbose_name,
                            BaseHallway._meta.verbose_name,
                            BaseWC._meta.verbose_name,
                            BaseKitchen._meta.verbose_name,
                            ]})
        return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def add_contract_from_auction(request, pk):
    template = 'contract_creation.html'
    context = {'title': _(u'Добавление контракта по параметрам аукциона')}
    prefix, images_prefix = 'contract', 'contract_images'
    auction = Auction.objects.get(pk=pk)
    kwargs = auction.to_dict()
    contract_kwargs = {}
    for k, v in kwargs.iteritems():
        if not 'id' in k and type(v) in ['str', 'unicode', 'int']:
            contract_kwargs.update({k: v})
    #if contract_kwargs:
    contract = Contract.objects.create(**contract_kwargs)
    room_kwargs, hallway_kwargs, wc_kwargs, kitchen_kwargs = auction.room.to_dict(), auction.hallway.to_dict(), auction.wc.to_dict(), auction.kitchen.to_dict(),
    room, hallway, wc, kitchen = Room.objects.create(**room_kwargs), Hallway.objects.create(**room_kwargs), WC.objects.create(**wc_kwargs), Kitchen.objects.create(**kitchen_kwargs),
    parent = {'room': room, 'kitchen': kitchen, 'wc': wc, 'hallway': hallway}
    if request.method == "POST":
        form = ContractForm(request.POST, request.FILES, prefix=prefix, instance=contract)
        image_form = ContractDocumentsForm(request.POST, request.FILES, prefix=images_prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(request=request, parent=parent)
        if form.is_valid() and image_form.is_valid() and room_f.is_valid() and hallway_f.is_valid() and wc_f.is_valid() and kitchen_f.is_valid():
            contract = form.save()
            contract.docs = image_form.save()
            contract.room = room_f.save()
            contract.hallway = hallway_f.save()
            contract.wc = wc_f.save()
            contract.kitchen = kitchen_f.save()
            contract.save(update_fields=['room', 'hallway', 'wc', 'kitchen', 'docs'])
            auction.contract = contract
            auction.save(update_fields=['contract'])
            return redirect('contracts')
        else:
            context.update({'form': form, 'prefix': prefix, 'images': image_form, 'formsets': [room_f, hallway_f, wc_f, kitchen_f]})
            return render_to_response(template, context, context_instance=RequestContext(request))
    else:
        image_form = ContractDocumentsForm(prefix=images_prefix)
        form = ContractForm(prefix=prefix, instance=contract)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=parent)
        context.update({'form': form, 'prefix': prefix, 'images': image_form, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                        'titles': [
                            BaseRoom._meta.verbose_name,
                            BaseHallway._meta.verbose_name,
                            BaseWC._meta.verbose_name,
                            BaseKitchen._meta.verbose_name,
                            ]})
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def get_contracts(request, mo=None, all=False):
    template = 'contracts.html'
    kwargs = {}

    mo_obj = None
    if mo:
        mo_obj = MO.objects.get(pk=mo)
    elif hasattr(request.user, 'customuser'):
        mo_obj = request.user.customuser.mo

    if hasattr(request.user, 'customuser') and request.user.customuser.get_user_date():
        from_dt = request.user.customuser.get_user_date()
        kwargs.update({'start_year__lt': from_dt, 'finish_year__gt': from_dt})

    if all:
        context = {'title': _(u'Все контракты')}
    elif mo_obj:
        context = {'title': _(u'Контракты %s' % (mo_obj))}
        kwargs.update({'mo': mo_obj})

    if Contract.objects.filter(**kwargs).exists():
        objects = Contract.objects.filter(**kwargs)
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


@login_required
def get_contract(request, pk, extra=None):
    context = {'title': _(u'Параметры контракта')}
    contract = Contract.objects.get(pk=pk)
    images_prefix = 'contract_images'
    if request.method == "POST":
        form = ContractShowForm(request.POST, instance=contract)
        context.update({'form': form})
    else:
        image_form = ContractDocumentsForm(prefix=images_prefix, instance=contract.docs)
        form = ContractShowForm(instance=contract)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_show_forms(parent=contract)
        context.update({'form': form, 'formsets': [room_f, hallway_f, wc_f, kitchen_f], 'images': image_form,
                        'titles': [
                            BaseRoom._meta.verbose_name,
                            BaseHallway._meta.verbose_name,
                            BaseWC._meta.verbose_name,
                            BaseKitchen._meta.verbose_name,
                            ]})

    context.update({'object': contract})
    return render(request, 'contract.html', context, context_instance=RequestContext(request))


@login_required
def update_contract(request, pk, extra=None):
    context = {'title': _(u'Параметры контракта')}
    contract = Contract.objects.get(pk=pk)
    prefix, images_prefix = 'contract', 'contract_images'
    if request.method == "POST":
        form = ContractForm(request.POST, request.FILES, prefix=prefix, instance=contract)
        image_form = ContractDocumentsForm(request.POST, request.FILES, prefix=images_prefix, instance=contract.docs)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=contract, request=request)
        context.update({'object': contract, 'form': form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f]})
        if form.is_valid() and image_form.is_valid() and room_f.is_valid() and hallway_f.is_valid() and wc_f.is_valid() and kitchen_f.is_valid():
            image_form.save()
            form.save()
            for obj in [room_f, hallway_f, wc_f, kitchen_f]:
                obj.save()
            return redirect('contracts')
        else:
            context.update({'object': contract, 'form': form, 'prefix': prefix, 'images': image_form,
                            'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                            'titles': [
                                BaseRoom._meta.verbose_name,
                                BaseHallway._meta.verbose_name,
                                BaseWC._meta.verbose_name,
                                BaseKitchen._meta.verbose_name,
                                ]})
            return render(request, 'contract_updating.html', context, context_instance=RequestContext(request))
    else:
        image_form = ContractDocumentsForm(instance=contract.docs, prefix=images_prefix)
        form = ContractForm(instance=contract, prefix=prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=contract)
        context.update({'object': contract, 'form': form, 'images': image_form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                        'titles': [
                            BaseRoom._meta.verbose_name,
                            BaseHallway._meta.verbose_name,
                            BaseWC._meta.verbose_name,
                            BaseKitchen._meta.verbose_name,
                            ]})
    return render(request, 'contract_updating.html', context, context_instance=RequestContext(request))


@login_required
def pre_delete_contract(request, pk):
    context = {'title': _(u'Удаление контракта')}
    contract = Contract.objects.get(pk=pk)
    context.update({'object': contract})
    return render_to_response("contract_deleting.html", context, context_instance=RequestContext(request))


@login_required
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


@login_required
def add_result(request):
    template = 'result_creation.html'
    context = {'title': _(u'Добавление результатов выезда в МО')}
    prefix, cmp_prefix = 'result', 'cmp_result'
    if request.method == "POST":
        form = ResultForm(request.POST, request.FILES, prefix=prefix)
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
                        'titles': [BaseRoom._meta.verbose_name, BaseHallway._meta.verbose_name,
                                   BaseWC._meta.verbose_name, BaseKitchen._meta.verbose_name]})
        return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def get_results(request, mo=None, all=False):
    template = 'results.html'
    kwargs = {}

    mo_obj = None
    if mo:
        mo_obj = MO.objects.get(pk=mo)
    elif hasattr(request.user, 'customuser'):
        mo_obj = request.user.customuser.mo

    if hasattr(request.user, 'customuser') and request.user.customuser.get_user_date():
        from_dt = request.user.customuser.get_user_date()
        kwargs.update({'start_year__lt': from_dt, 'finish_year__gt': from_dt})

    if all:
        context = {'title': _(u'Все выезды')}
    elif mo_obj:
        context = {'title': _(u'Выезды в %s' % (mo_obj))}
        kwargs.update({'mo': mo_obj})

    if Result.objects.filter(**kwargs).exists():
        objects = Result.objects.filter(**kwargs)
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


@login_required
def get_result(request, pk, extra=None):
    context = {'title': _(u'Параметры выезда')}
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


@login_required
def update_result(request, pk, extra=None):
    context = {'title': _(u'Параметры выезда')}
    result = Result.objects.get(pk=pk)
    prefix, cmp_prefix = 'result', 'cmp_result'
    if request.method == "POST":
        form = ResultForm(request.POST, request.FILES, instance=result, prefix=prefix)
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
            context.update({'object': result, 'form': form, 'text_area_fields': text_area_form, 'cmp_form': cmp_form,
                            'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                            'titles': [BaseRoom._meta.verbose_name, BaseHallway._meta.verbose_name,
                                       BaseWC._meta.verbose_name, BaseKitchen._meta.verbose_name]})
            return render(request, 'result_updating.html', context, context_instance=RequestContext(request))
    else:
        form = ResultForm(instance=result, prefix=prefix)
        form, text_area_form = split_form(form)
        cmp_form = CompareDataForm(instance=result.cmp_data, prefix=cmp_prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=result.cmp_data)
        context.update({'object': result, 'form': form, 'text_area_fields': text_area_form, 'cmp_form': cmp_form,
                        'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                        'titles': [BaseRoom._meta.verbose_name, BaseHallway._meta.verbose_name,
                                   BaseWC._meta.verbose_name, BaseKitchen._meta.verbose_name]})
        return render(request, 'result_updating.html', context, context_instance=RequestContext(request))


@login_required
def pre_delete_result(request, pk):
    context = {'title': _(u'Удаление выезда')}
    result = Result.objects.get(pk=pk)
    context.update({'object': result})
    return render_to_response("result_deleting.html", context, context_instance=RequestContext(request))


@login_required
def delete_result(request, pk):
    context = {'title': _(u'Удаление выезда')}
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
        context.update({'error': _(u'Возникла ошибка при удалении результатов выезда!')})
    return render_to_response("result_deleting.html", context, context_instance=RequestContext(request))


@login_required
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


@login_required
def cmp_contract(request, pk):
    context = {'title': _(u'Сравнение параметров'),
               'object_title': _(u'Контракт'), 'cmp_object_title': _(u'Строительный объект')}
    contract = Contract.objects.get(pk=pk)

    contract_form = ContractShowForm(instance=contract)
    room_f, hallway_f, wc_f, kitchen_f = get_fk_show_forms(parent=contract)

    if contract.building_set.all().exists():
        cmp_obj = contract.building_set.all()[0]
        obj_form = BuildingShowForm(instance=cmp_obj, cmp_initial=contract)
    elif contract.ground_set.all().exists():
        cmp_obj = contract.ground_set.all()[0]
        obj_form = GroundShowForm(instance=cmp_obj, cmp_initial=contract)
    else:
        context.update({'errorlist': _('No one matched object')})
        return render(request, 'cmp.html', context, context_instance=RequestContext(request))

    object_update_url = reverse('update-contract', args=[contract.id, ])
    object_pre_delete_url = reverse('pre-delete-contract', args=[contract.id, ])
    cmp_obj_update_url = reverse('update-building', args=[cmp_obj.id, cmp_obj.state, ])
    cmp_obj_pre_delete_url = reverse('pre-delete-building', args=[cmp_obj.id, cmp_obj.state, ])
    context.update({'cmp_obj_update_url': cmp_obj_update_url,
                    'cmp_obj_pre_delete_url': cmp_obj_pre_delete_url})
    context.update({'object_update_url': object_update_url,
                    'object_pre_delete_url': object_pre_delete_url})

    room_cf, hallway_cf, wc_cf, kitchen_cf = get_fk_cmp_forms(parent=cmp_obj, cmp=contract)

    obj_form, contract_form = set_fields_equal(obj_form, contract_form)
    room_cf, room_f = set_fields_equal(room_cf, room_f)
    hallway_cf, hallway_f = set_fields_equal(hallway_cf, hallway_f)
    wc_cf, wc_f = set_fields_equal(wc_cf, wc_f)
    kitchen_cf, kitchen_f = set_fields_equal(kitchen_cf, kitchen_f)

    context.update({'cmp_form': obj_form, 'room_cf': room_cf, 'hallway_cf': hallway_cf,
                    'wc_cf': wc_cf, 'kitchen_cf': kitchen_cf, })
    context.update({'form': contract_form, 'room_f': room_f, 'hallway_f': hallway_f,
                    'wc_f': wc_f, 'kitchen_f': kitchen_f, })

    context.update({'object': contract, 'cmp_object': cmp_obj,
                    'titles': [BaseRoom._meta.verbose_name, BaseHallway._meta.verbose_name,
                               BaseWC._meta.verbose_name, BaseKitchen._meta.verbose_name]})
    return render(request, 'cmp.html', context, context_instance=RequestContext(request))


@login_required
def cmp_contract_auction(request, pk):
    context = {'title': _(u'Сравнение параметров'),
               'object_title': _(u'Контракт'), 'cmp_object_title': _(u'Аукцион')}
    contract = Contract.objects.get(pk=pk)

    contract_form = ContractShowForm(instance=contract)
    room_f, hallway_f, wc_f, kitchen_f = get_fk_show_forms(parent=contract)

    if contract.auction_set.all().exists():
        cmp_obj = contract.auction_set.all()[0]
        auction_form = AuctionShowForm(instance=cmp_obj, cmp_initial=contract)
    else:
        context.update({'errorlist': _('No one matched object')})
        return render(request, 'cmp.html', context, context_instance=RequestContext(request))

    room_cf, hallway_cf, wc_cf, kitchen_cf = get_fk_cmp_forms(parent=cmp_obj, cmp=contract, multi=True)
    auction_form, contract_form = set_fields_equal(auction_form, contract_form)
    room_cf, room_f = set_fields_equal(room_cf, room_f)
    hallway_cf, hallway_f = set_fields_equal(hallway_cf, hallway_f)
    wc_cf, wc_f = set_fields_equal(wc_cf, wc_f)
    kitchen_cf, kitchen_f = set_fields_equal(kitchen_cf, kitchen_f)

    object_update_url = reverse('update-contract', args=[contract.id, ])
    object_pre_delete_url = reverse('pre-delete-contract', args=[contract.id, ])
    cmp_obj_update_url = reverse('update-auction', args=[cmp_obj.id, ])
    cmp_obj_pre_delete_url = reverse('pre-delete-auction', args=[cmp_obj.id, ])
    context.update({'cmp_obj_update_url': cmp_obj_update_url,
                    'cmp_obj_pre_delete_url': cmp_obj_pre_delete_url})
    context.update({'object_update_url': object_update_url,
                    'object_pre_delete_url': object_pre_delete_url})

    context.update({'cmp_form': auction_form, 'room_cf': room_cf, 'hallway_cf': hallway_cf,
                    'wc_cf': wc_cf, 'kitchen_cf': kitchen_cf, })
    context.update({'form': contract_form, 'room_f': room_f, 'hallway_f': hallway_f,
                    'wc_f': wc_f, 'kitchen_f': kitchen_f, })

    context.update({'object': contract, 'cmp_object': cmp_obj,
                    'titles': [BaseRoom._meta.verbose_name, BaseHallway._meta.verbose_name,
                               BaseWC._meta.verbose_name, BaseKitchen._meta.verbose_name]})
    return render(request, 'cmp.html', context, context_instance=RequestContext(request))


@login_required
def cmp_result_building(request, pk):
    context = {'title': _(u'Сравнение параметров'),
               'object_title': _(u'Результат'), 'cmp_object_title': _(u'Строительный объект')}
    res = Result.objects.get(pk=pk)
    result = res.cmp_data

    form = CompareDataShowForm(instance=result)
    room_f, hallway_f, wc_f, kitchen_f = get_fk_show_forms(parent=result)
    context.update({'form': form, 'formsets': [room_f, hallway_f, wc_f, kitchen_f]})

    if res.building:
        cmp_obj = res.building
        cmp_form = BuildingShowForm(instance=cmp_obj, cmp_initial=result)
    elif res.ground:
        cmp_obj = res.ground
        cmp_form = GroundShowForm(instance=cmp_obj, cmp_initial=result)
    else:
        context.update({'errorlist': _('No one matched object')})
        return render(request, 'cmp.html', context, context_instance=RequestContext(request))

    object_update_url = reverse('update-result', args=[res.id, ])
    object_pre_delete_url = reverse('pre-delete-result', args=[res.id, ])
    cmp_obj_update_url = reverse('update-building', args=[cmp_obj.id, cmp_obj.state, ])
    cmp_obj_pre_delete_url = reverse('pre-delete-building', args=[cmp_obj.id, cmp_obj.state, ])
    context.update({'cmp_obj_update_url': cmp_obj_update_url,
                    'cmp_obj_pre_delete_url': cmp_obj_pre_delete_url})
    context.update({'object_update_url': object_update_url,
                    'object_pre_delete_url': object_pre_delete_url})


    room_cf, hallway_cf, wc_cf, kitchen_cf = get_fk_cmp_forms(parent=cmp_obj, cmp=result)
    cmp_form, form = set_fields_equal(cmp_form, form)
    room_cf, room_f = set_fields_equal(room_cf, room_f)
    hallway_cf, hallway_f = set_fields_equal(hallway_cf, hallway_f)
    wc_cf, wc_f = set_fields_equal(wc_cf, wc_f)
    kitchen_cf, kitchen_f = set_fields_equal(kitchen_cf, kitchen_f)

    context.update({'cmp_form': cmp_form, 'room_cf': room_cf, 'hallway_cf': hallway_cf,
                    'wc_cf': wc_cf, 'kitchen_cf': kitchen_cf, })
    context.update({'form': form, 'room_f': room_f, 'hallway_f': hallway_f,
                    'wc_f': wc_f, 'kitchen_f': kitchen_f, })

    context.update({'object': result, 'cmp_object': cmp_obj,
                    'titles': [BaseRoom._meta.verbose_name, BaseHallway._meta.verbose_name,
                               BaseWC._meta.verbose_name, BaseKitchen._meta.verbose_name]})
    return render(request, 'cmp.html', context, context_instance=RequestContext(request))


@login_required
def cmp_result_contract(request, pk):
    context = {'title': _(u'Сравнение параметров'),
               'object_title': _(u'Результат'), 'cmp_object_title': _(u'Контракт')}
    res = Result.objects.get(pk=pk)
    result = res.cmp_data
    contract = res.contract

    form = CompareDataShowForm(instance=result)
    room_f, hallway_f, wc_f, kitchen_f = get_fk_show_forms(parent=result)
    context.update({'form': form, 'formsets': [room_f, hallway_f, wc_f, kitchen_f]})

    if contract:
        cmp_obj = contract
        cmp_form = ContractShowForm(instance=cmp_obj, cmp_initial=result)
    else:
        context.update({'errorlist': _('No one matched object')})
        return render(request, 'cmp.html', context, context_instance=RequestContext(request))

    object_update_url = reverse('update-result', args=[res.id, ])
    object_pre_delete_url = reverse('pre-delete-result', args=[res.id, ])
    cmp_obj_update_url = reverse('update-contract', args=[cmp_obj.id, ])
    cmp_obj_pre_delete_url = reverse('pre-delete-contract', args=[cmp_obj.id, ])
    context.update({'cmp_obj_update_url': cmp_obj_update_url,
                    'cmp_obj_pre_delete_url': cmp_obj_pre_delete_url})
    context.update({'object_update_url': object_update_url,
                    'object_pre_delete_url': object_pre_delete_url})

    room_cf, hallway_cf, wc_cf, kitchen_cf = get_fk_cmp_forms(parent=cmp_obj, cmp=result)
    cmp_form, form = set_fields_equal(cmp_form, form)
    room_cf, room_f = set_fields_equal(room_cf, room_f)
    hallway_cf, hallway_f = set_fields_equal(hallway_cf, hallway_f)
    wc_cf, wc_f = set_fields_equal(wc_cf, wc_f)
    kitchen_cf, kitchen_f = set_fields_equal(kitchen_cf, kitchen_f)

    context.update({'cmp_form': cmp_form, 'room_cf': room_cf, 'hallway_cf': hallway_cf,
                    'wc_cf': wc_cf, 'kitchen_cf': kitchen_cf, })
    context.update({'form': form, 'room_f': room_f, 'hallway_f': hallway_f,
                    'wc_f': wc_f, 'kitchen_f': kitchen_f, })

    context.update({'object': result, 'cmp_object': cmp_obj,
                    'titles': [BaseRoom._meta.verbose_name, BaseHallway._meta.verbose_name,
                               BaseWC._meta.verbose_name, BaseKitchen._meta.verbose_name]})
    return render(request, 'cmp.html', context, context_instance=RequestContext(request))
