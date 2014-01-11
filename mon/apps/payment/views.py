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

from .models import Payment
from .forms import PaymentForm, PaymentShowForm
from apps.mo.models import MO
from apps.user.models import CustomUser


@login_required
def add_payment(request):
    template = 'payment_creation.html'
    context = {'title': _(u'Добавление платежа')}
    prefix = 'pay'
    if request.method == "POST":
        form = PaymentForm(request.POST, request.FILES, prefix=prefix)
        if form.is_valid():
            form.save()
            return redirect('payments')
    else:
        form = PaymentForm(prefix=prefix)
    context.update({'form': form, 'prefix': prefix})
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def get_payments(request, pk=None):
    template = 'payments.html'
    context = {'title': _(u'Платежи')}
    if Payment.objects.all().exists():
        if pk:
            payment_object = Payment.objects.get(pk=pk)
            context.update({'object': payment_object})

        if not request.user.is_staff:
            mo = request.user.customuser.mo
            if mo:
                agreements = mo.departamentagreement_set.all()
                amount = sum([int(dep.subvention.amount) for dep in agreements if dep.subvention.amount])
                spent = sum([int(contract.summa) for contract in mo.contract_set.all() if contract.summa])
                percent = round(((float(spent)/amount) * 100), 3)
                economy = sum([int(auction.start_price) for auction in mo.auction_set.all() if auction.start_price]) - spent
                accounting = {'spent': spent, 'saved': amount - spent, 'percent': percent,
                              'sub_amount': amount, 'economy': economy}
                context.update({'accounting': accounting})
                objects = Payment.objects.filter(subvention__in=[dep.subvention for dep in agreements])
        else:
            objects = Payment.objects.all()
        page = request.GET.get('page', '1')
        paginator = Paginator(objects, 50)
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        context.update({'payment_list': objects})
    return render(request, template, context, context_instance=RequestContext(request))


@login_required
def get_accounting(request):
    template = 'payments.html'
    context = {'title': _(u'Платежи')}
    objects = []
    mos = MO.objects.all()
    for mo in mos:
        agreements = mo.departamentagreement_set.all()
        amount = sum([int(dep.subvention.amount) for dep in agreements if dep.subvention.amount])
        spent = sum([int(contract.summa) for contract in mo.contract_set.all() if contract.summa])
        percent = round(((float(spent)/amount) * 100), 3)
        economy = sum([int(auction.start_price) for auction in mo.auction_set.all() if auction.start_price]) - spent
        payments = []
        for dep in agreements:
            payments = payments + (list(dep.subvention.payment_set.all()))
        payment = sum([int(payment.amount) for payment in payments])
        accounting = {'payment': payment, 'spent': spent, 'saved': amount - spent,
                      'percent': percent, 'sub_amount': amount, 'economy': economy}
        objects.append({'mo': mo, 'accounting': accounting})
    context.update({'accountings': objects})
    return render(request, template, context, context_instance=RequestContext(request))


@login_required
def get_payment(request, pk, extra=None):
    context = {'title': _(u'Платежи')}
    payment = Payment.objects.get(pk=pk)
    form = PaymentShowForm(instance=payment)
    context.update({'object': payment, 'form': form})
    return render(request, 'payment.html', context, context_instance=RequestContext(request))


@login_required
def update_payment(request, pk, extra=None):
    context = {'title': _(u'Параметры платежа')}
    payment = Payment.objects.get(pk=pk)
    prefix = 'pay'
    if request.method == "POST":
        form = PaymentForm(request.POST, request.FILES, instance=payment, prefix=prefix)
        context.update({'object': payment, 'form': form, 'prefix': prefix})
        if form.is_valid():
            form.save()
            return redirect('payments')
        else:
            context.update({'object': payment, 'form': form, 'prefix': prefix})
            return render(request, 'payment_updating.html', context, context_instance=RequestContext(request))
    else:
        form = PaymentForm(instance=payment, prefix=prefix)
        context.update({'object': payment, 'form': form, 'prefix': prefix})
    return render(request, 'payment_updating.html', context, context_instance=RequestContext(request))


@login_required
def pre_delete_payment(request, pk):
    context = {'title': _(u'Удаление платежа')}
    payment = Payment.objects.get(pk=pk)
    context.update({'object': payment})
    return render_to_response("payment_deleting.html", context, context_instance=RequestContext(request))


@login_required
def delete_payment(request, pk):
    context = {'title': _(u'Удаление платежа')}
    payment = Payment.objects.get(pk=pk)
    if payment and 'delete' in request.POST:
        payment.delete()
        return redirect('payments')
    elif 'cancel' in request.POST:
        return redirect('payments')
    else:
        context.update({'error': _(u'Возникла ошибка при удалении платежа!')})
    return render_to_response("payment_deleting.html", context, context_instance=RequestContext(request))


