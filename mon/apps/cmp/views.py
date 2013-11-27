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

from .models import Contract, Result, Auction, Person
from .forms import ContractForm, ResultForm, AuctionForm, CompareDataForm, PersonForm, AuctionShowForm
from apps.core.views import get_fk_forms, get_fk_show_forms


def add_auction(request):
    template = 'auction_creation.html'
    context = {'title': _(u'Добавление заказа')}
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
    context.update({'form': form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                    'titles': ['Room', 'Hallway', 'WC', 'Kitchen']})
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
                            'titles': ['Room', 'Hallway', 'WC', 'Kitchen']})
            return render(request, 'auction_updating.html', context, context_instance=RequestContext(request))
    else:
        form = AuctionForm(instance=auction, prefix=prefix)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=auction)
        context.update({'object': auction, 'form': form, 'prefix': prefix, 'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                        'titles': ['Room', 'Hallway', 'WC', 'Kitchen']})
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
        return redirect('auctions')
    elif 'cancel' in request.POST:
        return redirect('auctions')
    else:
        context.update({'error': _(u'Возникла ошибка при удалении заказа!')})
    return render_to_response("auction_deleting.html", context, context_instance=RequestContext(request))
