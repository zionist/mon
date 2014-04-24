# -*- coding: utf-8 -*-

from datetime import datetime, date
from copy import deepcopy
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
from .forms import PaymentForm, PaymentShowForm, DateForm
from apps.mo.models import MO
from apps.user.models import CustomUser
from apps.core.views import to_xls


@login_required
def add_payment(request):
    template = 'payment_creation.html'
    context = {'title': _(u'Добавление платежа')}
    prefix = 'pay'
    if request.method == "POST":
        form = PaymentForm(request.POST, request.FILES, prefix=prefix, initial={'user_mo': request.user.customuser.mo})
        if form.is_valid():
            form.save()
            return redirect('payments')
    else:
        form = PaymentForm(prefix=prefix, initial={'user_mo': request.user.customuser.mo})
    context.update({'form': form, 'prefix': prefix})
    return render_to_response(template, context, context_instance=RequestContext(request))


def recount_accounting(mo, user=None, context=None, accounting=None, update=None, dates=None, payment_dates=None):
    '''
        dates - {'date__range': (timestamp, timestamp)}, from which get mo agreements
        payment_dates - {'date__range': (timestamp, timestamp)}, from which get mo payments by agreements
        user - request.user, if we don`t have from_dt
        update - True if we need to update mo accounting(each 00:00 by cron)
    '''
    objects = []
    accounting = accounting if accounting else {}
    context = context if context else {}

    if isinstance(mo, MO):
        agreements = mo.departamentagreement_set.all()
        if not update:
            objects = Payment.objects.filter(subvention__in=[dep.subvention for dep in agreements])

        kw = {}
        if dates:
            kw = dates
        if not dates and user and hasattr(user, 'customuser'):
            from_dt = user.customuser.get_user_date()
            to_dt = datetime(from_dt.year + 1, 1, 1)
            kw = {'date__range': (from_dt, to_dt)}

        agreements = agreements.filter(**kw)
        if not update:
            if not payment_dates:
                objects = objects.filter(**kw)
            else:
                objects = objects.filter(**payment_dates)

        if agreements:
            amount = sum([float(dep.subvention.amount) for dep in agreements if dep.subvention.amount])
            home_amount = 0.0
            adm_amount = 0.0
            for dep in agreements:
                if dep.subvention.reg_budget:
                    if dep.subvention.reg_budget.sub_orph_home:
                        home_amount += dep.subvention.reg_budget.sub_orph_home
                    if dep.subvention.reg_budget.adm_coef:
                        adm_amount += dep.subvention.reg_budget.adm_coef
                if dep.subvention.fed_budget:
                    if dep.subvention.fed_budget.sub_orph_home:
                        home_amount += dep.subvention.fed_budget.sub_orph_home
                    if dep.subvention.fed_budget.adm_coef:
                        adm_amount += dep.subvention.fed_budget.adm_coef

            reg_spent = sum([float(payment.amount) for payment in objects.filter(payment_state=1, payment_budget_state=2) if payment.amount])
            fed_spent = sum([float(payment.amount) for payment in objects.filter(payment_state=1, payment_budget_state=1) if payment.amount])
            reg_adm_spent = sum([float(payment.amount) for payment in objects.filter(payment_state=2, payment_budget_state=2) if payment.amount])
            fed_adm_spent = sum([float(payment.amount) for payment in objects.filter(payment_state=2, payment_budget_state=1) if payment.amount])
            spent = reg_spent + fed_spent
            adm_spent = reg_adm_spent + fed_adm_spent
            percent = round((float(spent/amount) * 100), 3) if amount else 0
            economy = sum([float(auction.start_price) for auction in mo.auction_set.all() if auction.start_price]) - spent
            accounting.update({'mo': mo, 'spent': spent, 'saved': amount - spent, 'percent': percent,
                               'sub_amount': amount, 'economy': economy, 'home_amount': home_amount,
                               'adm_amount': adm_amount, 'adm_spent': adm_spent,
                               'reg_spent': reg_spent, 'fed_spent': fed_spent})
            context.update({'accounting': accounting})
        if update and accounting:
            mo.update(**accounting)
    else:
        all_payments = []
        c_kwargs = deepcopy(payment_dates)
        for one_mo in mo:
            accounting = {}
            agreements = one_mo.departamentagreement_set.filter(**dates)
            contracts = one_mo.contract_set.filter(**c_kwargs)

            if agreements:
                amount = sum([float(dep.subvention.amount) for dep in agreements if dep.subvention.amount])
                accounting.update({'sub_amount': amount})
                if contracts:
                    spent = sum([float(contract.summa) for contract in contracts if contract.summa])
                    percent = round(((float(spent)/amount) * 100), 3) if spent and amount else 0
                    economy = sum([float(auction.start_price) for auction in one_mo.auction_set.filter(**payment_dates)
                                   if auction.start_price]) - spent
                    payment_dates.update({'contract__in': [contract.id for contract in contracts if contract]})
                    payments = Payment.objects.filter(**payment_dates)
                    payment = sum([float(payment.amount) for payment in payments])
                    all_payments = all_payments + list(payments)
                    accounting.update({'payment': payment, 'spent': spent, 'saved': amount - spent,
                                       'percent': percent, 'economy': economy})
            objects.append({'mo': one_mo, 'accounting': accounting})
            context.update({'accountings': objects, 'payment_list': all_payments, 'show_accounting_payments': True})
    return objects


@login_required
def get_payments(request, mo=None, all=False, xls=False):
    context = {'title': _(u'Платежи')}
    template = 'payments.html'
    prefix = 'acc_date'
    objects = []
    if Payment.objects.all().exists():
        if all:
            context = {'title': _(u'Все платежи')}
            if hasattr(request.user, 'customuser'):
                from_dt = request.user.customuser.get_user_date()
                if from_dt:
                    to_dt = datetime(from_dt.year + 1, 1, 1)
                    objects = Payment.objects.filter(date__range=(from_dt, to_dt))
                else:
                    objects = Payment.objects.all()
            else:
                objects = Payment.objects.all()
        elif hasattr(request.user, 'customuser') or mo:
            mo = request.user.customuser.mo if request.user.customuser.mo else MO.objects.get(pk=mo)
            context = {'title': _(u'Платежи %s') % mo.name}
            objects = recount_accounting(mo, user=request.user, context=context)
        if xls:
            return to_xls(request,  objects={PaymentForm: objects}, fk_forms = False)
        form = DateForm(prefix=prefix)
        context.update({'date_form': form})
        page = request.GET.get('page', '1')
        paginator = Paginator(objects, 50)
        try:
            objects_list = paginator.page(page)
        except PageNotAnInteger:
            objects_list = paginator.page(1)
        except EmptyPage:
            objects_list = paginator.page(paginator.num_pages)
        context.update({'payment_list': objects_list})
    return render(request, template, context, context_instance=RequestContext(request))


@login_required
def get_accounting(request, select=None):
    template = 'payments.html'
    context = {'title': _(u'Платежи')}
    prefix = 'acc_date'
    mos = MO.objects.all()
    kwargs = {}
    agr_kwargs = {}
    form = DateForm(prefix=prefix)
    context.update({'date_form': form})
    from_dt = request.user.customuser.get_user_date() if hasattr(request.user, 'customuser') else None
    if select and int(select) in [1, 2, 3, 4]:
        state = int(select)
        if state == 4:
            dt = datetime(datetime.now().year, 12, 31)
            dt = dt.replace(year=dt.year-1)
            prev = dt.replace(year=dt.year-1)
        elif state == 3:
            dt = datetime(datetime.now().year, 12, 31)
            prev = dt.replace(year=dt.year-1)
        elif state == 2:
            dt = datetime(datetime.now().year, datetime.now().month, 28)
            prev = dt.replace(month=dt.month-1) if dt.month > 1 else dt.replace(month=12)
        elif state == 1:
            dt = datetime.now()
            prev = dt.replace(day=dt.day-1)
        kwargs.update({'date__range': (prev, dt)})
        agr_kwargs.update({'date__range': (datetime(dt.year, 1, 1), datetime(dt.year, 12, 31))})
    elif not select and request.method == 'POST' and 'date_select' in request.POST:
        form = DateForm(request.POST, prefix=prefix)
        if form.is_valid():
            dt, prev = form.cleaned_data.get('dt'), form.cleaned_data.get('prev')
            kwargs.update({'date__range': (prev, dt)})
            agr_kwargs.update({'date__range': (prev, dt)})
        else:
            context.update({'date_form': form})
    elif not select and from_dt:
        to_dt = datetime(from_dt.year, 12, 31)
        kwargs.update({'date__range': (from_dt, to_dt)})
        agr_kwargs.update({'date__range': (from_dt, to_dt)})

    recount_accounting(mos, context=context, dates=agr_kwargs, payment_dates=kwargs)
    context.update({'hide_paginator': True})
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
