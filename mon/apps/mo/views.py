# -*- coding: utf-8 -*-

import xlwt
from datetime import datetime
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound, \
    HttpResponseForbidden
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
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test

from .models import MO, DepartamentAgreement, PeopleAmount, Subvention, FederalBudget, RegionalBudget, MaxFlatPrice
from .forms import MOForm, DepartamentAgreementForm, PeopleAmountForm, SubventionForm, FederalBudgetForm, \
    RegionalBudgetForm, MOShowForm, DepartamentAgreementShowForm, SubventionShowForm, FederalBudgetShowForm, \
    RegionalBudgetShowForm, MOPerformanceForm, SubventionMinusForm, MaxFlatPriceForm
from apps.build.models import Building, Ground, ContractDocuments
from apps.cmp.models import Auction, Contract
from apps.user.models import CustomUser
from apps.core.models import CREATION_FORM_CHOICES
from apps.payment.models import Payment


@user_passes_test(lambda u: u.is_superuser)
def add_mo(request):
    template = 'mo_creation.html'
    context = {'title': _(u'Добавление муниципального образования')}
    prefix, dep_prefix, sub_prefix, reg_prefix, fed_prefix = 'mo', 'dep_mo', 'sub_mo', 'reg_mo', 'fed_mo'
    if request.method == "POST":
        form = MOForm(request.POST, prefix=prefix)
        dep_form = DepartamentAgreementForm(request.POST, prefix=dep_prefix)
        sub_form = SubventionForm(request.POST, prefix=sub_prefix)
        fed_form = FederalBudgetForm(request.POST, prefix=fed_prefix)
        reg_form = RegionalBudgetForm(request.POST, prefix=reg_prefix)
        if form.is_valid() and dep_form.is_valid() and sub_form.is_valid() and fed_form.is_valid() and reg_form.is_valid():
            dep = dep_form.save()
            sub = sub_form.save()
            sub.fed_budget = fed_form.save()
            sub.reg_budget = reg_form.save()
            sub.save(update_fields=['fed_budget', 'reg_budget'])
            mo = form.save()
            if hasattr(sub.fed_budget, 'subvention_performance') and sub.fed_budget.subvention_performance:
                mo.home_orphans = int(mo.home_orphans) + int(sub.fed_budget.subvention_performance)
            if hasattr(sub.reg_budget, 'subvention_performance') and sub.fed_budget.subvention_performance:
                mo.home_orphans = int(mo.home_orphans) + int(sub.reg_budget.subvention_performance)
            mo.save(update_fields=['home_orphans'])
            dep.mo = mo
            dep.subvention = sub
            dep.save(update_fields=['subvention', 'mo'])
            return redirect('mos')
    else:
        form = MOForm(prefix=prefix)
        dep_form = DepartamentAgreementForm(prefix=dep_prefix)
        sub_form = SubventionForm(prefix=sub_prefix)
        fed_form = FederalBudgetForm(prefix=fed_prefix)
        reg_form = RegionalBudgetForm(prefix=reg_prefix)
    context.update({'form': form, 'dep_form': dep_form, 'sub_form': sub_form,
                    'formsets': [fed_form, reg_form], 'titles': [FederalBudget._meta.verbose_name, RegionalBudget._meta.verbose_name],
                    'prefix': prefix})
    return render_to_response(template, context, context_instance=RequestContext(request))


def recount_mos(mos=[], kwargs=None):
    cur_year = datetime.today().replace(month=1, day=1)
    kwargs = kwargs if kwargs else {'date__range': [cur_year, cur_year.replace(year=cur_year.year+1)]}
    for mo in mos:
        sum_flats_amount = sum([int(contract.flats_amount) for contract in mo.contract_set.filter(**kwargs) if contract.flats_amount])
        mo.flats_amount = sum_flats_amount
        agreements = mo.departamentagreement_set.filter(**kwargs)

        amount_sum = 0.0
        reg_amount_sum = 0.0
        fed_amount_sum = 0.0
        home_reg_orphans = 0
        home_fed_orphans = 0

        for agr in agreements:
            subvention = agr.subvention
            if subvention.amount:
                amount_sum += float(subvention.amount)
            if hasattr(subvention, 'reg_budget') and subvention.reg_budget:
                if subvention.reg_budget.sub_sum:
                    reg_amount_sum += float(subvention.reg_budget.sub_sum)
                if subvention.reg_budget.subvention_performance:
                    home_reg_orphans += int(subvention.reg_budget.subvention_performance)
            if hasattr(subvention, 'fed_budget') and subvention.fed_budget:
                if subvention.fed_budget.sub_sum:
                    fed_amount_sum += float(subvention.fed_budget.sub_sum)
                if subvention.fed_budget.subvention_performance:
                    home_fed_orphans += int(agr.subvention.fed_budget.subvention_performance)
        mo.common_amount = amount_sum
        mo.common_reg_amount = reg_amount_sum
        mo.common_fed_amount = fed_amount_sum
        mo.home_reg_orphans = home_reg_orphans
        mo.home_fed_orphans = home_fed_orphans
        mo.home_orphans = home_reg_orphans + home_fed_orphans
        mo.save()
    return True


@login_required
def get_recount_mo(request, pk=None):
    print 'recount'
    agreement_kwargs = {}
    if MO.objects.all().exists():
        if hasattr(request.user, 'customuser') and request.user.customuser.get_user_date():
            from_dt = request.user.customuser.get_user_date()
            to_dt = datetime(from_dt.year + 1, 1, 1)
            agreement_kwargs.update({'date__gt': from_dt, 'date__lt': to_dt})
        if pk:
            recount_mos(MO.objects.filter(pk=pk), kwargs=agreement_kwargs)
        else:
            recount_mos(MO.objects.all(), kwargs=agreement_kwargs)
    return get_mos(request, pk=pk)


@login_required
def get_mos(request, pk=None):
    title = _(u'Муниципальные образования')
    template = 'mos.html'
    context = {'title': title, 'show_recount': True}
    if MO.objects.all().exists():
        if pk:
            objects = MO.objects.filter(pk=pk)
            if objects:
                context.update({'object': objects[0]})
        else:
            objects = MO.objects.all().order_by('name')
        # sort city first
        sorted_objects = []
        for obj in objects:
            if obj.name.startswith(u"г."):
                sorted_objects.append(obj)
        for obj in objects:
            if not obj.name.startswith(u"г."):
                sorted_objects.append(obj)
        page = request.GET.get('page', '1')
        paginator = Paginator(sorted_objects, 50)
        try:
            sorted_objects = paginator.page(page)
        except PageNotAnInteger:
            sorted_objects = paginator.page(1)
        except EmptyPage:
            sorted_objects = paginator.page(paginator.num_pages)
        context.update({'mo_list': sorted_objects})
    return render(request, template, context, context_instance=RequestContext(request))


@login_required
def mos_select(request, pk=None, ):
    if not request.user.is_staff:
        return HttpResponseForbidden('Forbidden')
    if request.user.is_superuser:
        return redirect('mos')
    title = _(u'Выбор муниципального образования')
    template = 'mos_select.html'
    context = {'title': title}
    if MO.objects.all().exists():
        objects = MO.objects.all()
        if pk:
            mo_object = MO.objects.get(pk=pk)
            context.update({'object': mo_object})
        page = request.GET.get('page', '1')
        paginator = Paginator(objects, 50)
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        user = CustomUser.objects.get(pk=request.user.pk)
        obj_list = []
        for mo in objects:
            if user.mo == mo:
                setattr(mo, 'selected', True)
            else:
                setattr(mo, 'selected', False)
            obj_list.append(mo)
        context.update({'mo_list': obj_list})
    return render(request, template, context, context_instance=RequestContext(request))


@login_required
def select_mo(request, pk=None):
    if not request.user.is_staff:
        return HttpResponseForbidden('Forbidden')
    user = CustomUser.objects.get(pk=request.user.pk)
    mo = MO.objects.get(pk=pk)
    user.mo = mo
    user.save()
    if request.method != "GET":
        return HttpResponseNotFound("Not found")
    return redirect('change-mo', pk=mo.pk)


@login_required
def get_mo(request, pk, extra=None):
    context = {'title': _(u'Муниципальное образование')}
    mo = MO.objects.get(pk=pk)
    form = MOShowForm(instance=mo)
    # "select" mo
    selected_users = CustomUser.objects.filter(mo=mo).filter(is_staff=True).\
        exclude(is_superuser=True).exclude(username=request.user.username)
    if request.user.is_staff and not request.user.is_superuser:
        if selected_users:
            return HttpResponseForbidden(u"МО %s уже выбрано у пользователя %s" % (mo, selected_users[0]))
    if CustomUser.objects.filter(pk=request.user.pk).exists():
        user = CustomUser.objects.get(pk=request.user.pk)
        user.mo = mo
        user.save()
    context.update({'object': mo, 'form': form, 'agreement': True})
    dep_agreements = mo.departamentagreement_set.all()
    hide_menu = True if not request.user.is_superuser else False
    context.update({'hide_menu': hide_menu, 'agreements': dep_agreements})
#    context.update({'agreements': dep_agreements})
    return render(request, 'mo.html', context, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_superuser)
def update_mo(request, pk, extra=None):
    context = {'title': _(u'Параметры муниципального образования')}
    mo = MO.objects.get(pk=pk)
    prefix = 'mo'
    context.update({'object': mo, 'prefix': prefix})
    dep_agreements = mo.departamentagreement_set.all()
    show_argeement_table = True if dep_agreements.exists() else False
    #forms = []
    context.update({'hide_menu': True, 'agreement': show_argeement_table, 'agreements': dep_agreements})
    if request.method == "POST":
        form = MOForm(request.POST, instance=mo, prefix=prefix)
        context.update({'form': form})
        if form.is_valid():
            form.save()
            return redirect('mos')
        #i = 0
        #for dep_agreement in dep_agreements:
        #    sub = dep_agreement.subvention
        #    fed = sub.fed_budget
        #    reg = sub.reg_budget
        #    dep_prefix, sub_prefix, reg_prefix, fed_prefix = 'dep_mo_%s' % i, 'sub_mo_%s' % i, 'reg_mo_%s' % i, 'fed_mo_%s' % i
        #    i += 1
        #    dep_form = DepartamentAgreementForm(request.POST, instance=dep_agreement, prefix=dep_prefix)
        #    sub_form = SubventionForm(request.POST, instance=sub, prefix=sub_prefix)
        #    fed_form = FederalBudgetForm(request.POST, instance=fed, prefix=fed_prefix)
        #    reg_form = RegionalBudgetForm(request.POST, instance=reg, prefix=reg_prefix)
        #    forms.append({'dep_form': dep_form, 'sub_form': sub_form, 'formsets': [fed_form, reg_form],
        #                  'prefs': [dep_prefix, sub_prefix, reg_prefix, fed_prefix]})
        #    if form.is_valid() and dep_form.is_valid() and sub_form.is_valid() and fed_form.is_valid() and reg_form.is_valid():
        #        form.save()
        #        dep_form.save()
        #        fed_form.save()
        #        reg_form.save()
        #        sub_form.save()
        #    context.update({'forms': forms, 'titles': [FederalBudget._meta.verbose_name, RegionalBudget._meta.verbose_name]})
        #    return redirect('mos')
        #else:
        #    context.update({'forms': forms, 'titles': [FederalBudget._meta.verbose_name, RegionalBudget._meta.verbose_name]})
        #    return render(request, 'mo_updating.html', context, context_instance=RequestContext(request))
    else:
        form = MOForm(instance=mo, prefix=prefix)
        context.update({'form': form})
        #i = 0
        #for dep_agreement in dep_agreements:
        #    sub = dep_agreement.subvention
        #    fed = sub.fed_budget
        #    reg = sub.reg_budget
        #    dep_prefix, sub_prefix, reg_prefix, fed_prefix = 'dep_mo_%s' % i, 'sub_mo_%s' % i, 'reg_mo_%s' % i, 'fed_mo_%s' % i
        #    i += 1
        #    dep_form = DepartamentAgreementForm(instance=dep_agreement, prefix=dep_prefix)
        #    sub_form = SubventionForm(instance=sub, prefix=sub_prefix)
        #    fed_form = FederalBudgetForm(instance=fed, prefix=fed_prefix)
        #    reg_form = RegionalBudgetForm(instance=reg, prefix=reg_prefix)
        #    forms.append({'dep_form': dep_form, 'sub_form': sub_form, 'formsets': [fed_form, reg_form],
        #                  'prefs': [dep_prefix, sub_prefix, reg_prefix, fed_prefix]})
        #context.update({'forms': forms, 'titles': [FederalBudget._meta.verbose_name, RegionalBudget._meta.verbose_name]})
    return render(request, 'mo_updating.html', context, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_superuser)
def pre_delete_mo(request, pk):
    context = {'title': _(u'Удаление муниципального образования')}
    mo = MO.objects.get(pk=pk)
    context.update({'object': mo})
    return render_to_response("mo_deleting.html", context, context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_superuser)
def delete_mo(request, pk):
    context = {'title': _(u'Удаление муниципального образования')}
    mo = MO.objects.get(pk=pk)
    if mo and 'delete' in request.POST:
        dep_agreement = DepartamentAgreement.objects.get(mo=pk)
        sub = dep_agreement.subvention
        fed = sub.fed_budget
        reg = sub.reg_budget
        sub.delete()
        fed.delete()
        reg.delete()
        mo.delete()
        dep_agreement.delete()
        return redirect('mos')
    elif 'cancel' in request.POST:
        return redirect('mos')
    else:
        context.update({'error': _(u'Возникла ошибка при удалении муниципального образования!')})
    return render_to_response("mo_deleting.html", context, context_instance=RequestContext(request))


@login_required
def add_agreement(request, pk, state=None):
    template = 'mo_adding_agreement.html'
    context = {}
    mo = MO.objects.get(pk=pk)
    context.update({'object': mo})
    agreement_type = int(state) if state else 0
    title = _(u'Добавление соглашения с министерством')
    if agreement_type == 1:
        title = _(u'Добавление дополнительного соглашения с министерством о прибавлении средств')
    elif agreement_type == 2:
        title = _(u'Добавление дополнительного соглашения с министерством о вычете средств')
    context.update({'title': title})
    prefix, dep_prefix, sub_prefix, reg_prefix, fed_prefix = 'mo', 'dep_mo', 'sub_mo', 'reg_mo', 'fed_mo'
    if request.method == "POST":
        form = MOShowForm(request.POST, prefix=prefix, instance=mo)
        dep_form = DepartamentAgreementForm(request.POST, prefix=dep_prefix)
        sub_form = SubventionForm(request.POST, prefix=sub_prefix)
        fed_form = FederalBudgetForm(request.POST, prefix=fed_prefix)
        reg_form = RegionalBudgetForm(request.POST, prefix=reg_prefix)
        if form.is_valid() and dep_form.is_valid() and sub_form.is_valid() and fed_form.is_valid() and reg_form.is_valid():
            dep = dep_form.save()
            sub = sub_form.save()
            sub.fed_budget = fed_form.save()
            sub.reg_budget = reg_form.save()
            sub.save(update_fields=['fed_budget', 'reg_budget'])
            dep.subvention = sub
            if hasattr(sub.fed_budget, 'subvention_performance') and sub.fed_budget.subvention_performance:
                mo.home_orphans = int(mo.home_orphans) + int(sub.fed_budget.subvention_performance)
            if hasattr(sub.reg_budget, 'subvention_performance') and sub.fed_budget.subvention_performance:
                mo.home_orphans = int(mo.home_orphans) + int(sub.reg_budget.subvention_performance)
            mo.save(update_fields=['home_orphans'])
            dep.mo = mo
            dep.agreement_type = agreement_type
            dep.save(update_fields=['subvention', 'mo', 'agreement_type'])
            return redirect('mos')
    else:
        form = MOShowForm(prefix=prefix, instance=mo)
        dep_form = DepartamentAgreementForm(prefix=dep_prefix)
        sub_form = SubventionForm(prefix=sub_prefix)
        fed_form = FederalBudgetForm(prefix=fed_prefix)
        reg_form = RegionalBudgetForm(prefix=reg_prefix)
    context.update({'form': form, 'dep_form': dep_form, 'state': agreement_type, 'sub_form': sub_form, 'formsets': [fed_form, reg_form],
                    'titles': [FederalBudget._meta.verbose_name, RegionalBudget._meta.verbose_name],
                    'prefix': prefix})
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def add_dop_agreement(request, pk, state=None):
    template = 'mo_adding_agreement.html'
    agreement_type = int(state)
    title = _(u'Добавление дополнительного соглашения с министерством') if agreement_type == 1 \
            else _(u'Добавление письма о вычете средств')
    context = {'title': title}
    mo = MO.objects.get(pk=pk)
    prefix, dep_prefix, sub_prefix = 'mo', 'dep_mo', 'sub_mo'
    form = MOShowForm(prefix=prefix, instance=mo)
    context.update({'object': mo, 'form': form})
    if request.method == "POST":
        dep_form = DepartamentAgreementForm(request.POST, prefix=dep_prefix, initial={'prev_mo': mo})
        sub_form = SubventionForm(request.POST, prefix=sub_prefix) if agreement_type == 1 else SubventionMinusForm(request.POST, prefix=sub_prefix)
        if dep_form.is_valid() and sub_form.is_valid():
            dep = dep_form.save()
            sub = sub_form.save()
            if agreement_type != 1 and sub.amount and int(sub.amount) > 0:
                sub.amount = -sub.amount
                sub.save(update_fields=['amount'])
            dep.subvention = sub
            dep.mo = mo
            dep.agreement_type = agreement_type
            dep.save(update_fields=['subvention', 'mo', 'agreement_type'])
            return redirect('mos')
    else:
        dep_form = DepartamentAgreementForm(prefix=dep_prefix, initial={'prev_mo': mo})
        sub_form = SubventionForm(prefix=sub_prefix) if agreement_type == 1 else SubventionMinusForm(prefix=sub_prefix)
    context.update({'form': form, 'dep_form': dep_form, 'sub_form': sub_form, 'state': agreement_type, 'prefix': prefix,
                    'titles': [FederalBudget._meta.verbose_name, RegionalBudget._meta.verbose_name]})
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def update_agreement(request, pk, extra=None, state=None):
    if state and int(state) in [1, 2]:
        return update_dop_agreement(request, pk, state)
    context = {'title': _(u'Соглашение с министерством'), 'state': state}
    dep_agreement = DepartamentAgreement.objects.get(pk=pk)
    prefix = 'dep'
    context.update({'object': dep_agreement, 'agreement': True, 'update': True, 'prefix': prefix})
    forms = []
    fed_form, reg_form = None, None
    if request.method == "POST":
        sub = dep_agreement.subvention
        fed = sub.fed_budget
        reg = sub.reg_budget
        dep_prefix, sub_prefix, reg_prefix, fed_prefix = 'dep_mo', 'sub_mo', 'reg_mo', 'fed_mo'
        dep_form = DepartamentAgreementForm(request.POST, instance=dep_agreement, prefix=dep_prefix)
        sub_form = SubventionForm(request.POST, instance=sub, prefix=sub_prefix)
        fed_form = RegionalBudgetForm(request.POST, instance=fed, prefix=fed_prefix)
        reg_form = RegionalBudgetForm(request.POST, instance=reg, prefix=reg_prefix)
        forms.append({'dep_form': dep_form, 'sub_form': sub_form, 'formsets': [fed_form, reg_form],
                      'prefs': [dep_prefix, sub_prefix, reg_prefix, fed_prefix]})
        if dep_form.is_valid() and sub_form.is_valid() and fed_form.is_valid() and reg_form.is_valid():
            dep_form.save()
            sub_form.save()
            fed_form.save()
            reg_form.save()
            return redirect('mos')
        else:
            context.update({'forms': forms, 'titles': [FederalBudget._meta.verbose_name, RegionalBudget._meta.verbose_name]})
            return render(request, 'mo_updating.html', context, context_instance=RequestContext(request))
    else:
        sub = dep_agreement.subvention
        dep_prefix, sub_prefix, reg_prefix, fed_prefix = 'dep_mo', 'sub_mo', 'reg_mo', 'fed_mo'
        dep_form = DepartamentAgreementForm(instance=dep_agreement, prefix=dep_prefix)
        sub_form = SubventionForm(instance=sub, prefix=sub_prefix)
        fed_form = FederalBudgetForm(instance=sub.fed_budget, prefix=fed_prefix)
        reg_form = RegionalBudgetForm(instance=sub.reg_budget, prefix=reg_prefix)
        forms.append({'dep_form': dep_form, 'sub_form': sub_form, 'formsets': [fed_form, reg_form],
                      'prefs': [dep_prefix, sub_prefix, reg_prefix, fed_prefix]})
        context.update({'forms': forms, 'titles': [FederalBudget._meta.verbose_name, RegionalBudget._meta.verbose_name]})
    return render(request, 'mo_updating.html', context, context_instance=RequestContext(request))


@login_required
def update_dop_agreement(request, pk, state):
    agreement_type = int(state)
    title = _(u'Редактирование дополнительного соглашения с министерством') if agreement_type == 1\
            else _(u'Редактирование письма о вычете средств')
    context = {'title': title, 'state': agreement_type}
    dep_agreement = DepartamentAgreement.objects.get(pk=pk)
    prefix = 'dep'
    context.update({'object': dep_agreement, 'agreement': True, 'prefix': prefix})
    forms = []
    dep_prefix, sub_prefix = 'dep_mo', 'sub_mo'
    if request.method == "POST":
        sub = dep_agreement.subvention
        dep_form = DepartamentAgreementForm(request.POST, instance=dep_agreement, prefix=dep_prefix, initial={'prev_mo': dep_agreement.mo})
        sub_form = SubventionForm(request.POST, instance=sub, prefix=sub_prefix) if agreement_type == 1 \
                   else SubventionMinusForm(request.POST, instance=sub, prefix=sub_prefix)
        forms.append({'dep_form': dep_form, 'sub_form': sub_form,
                      'prefs': [dep_prefix, sub_prefix]})
        if dep_form.is_valid() and sub_form.is_valid():
            dep_form.save()
            sub_form.save()
            return redirect('mos')
        else:
            context.update({'forms': forms, 'titles': [FederalBudget._meta.verbose_name, RegionalBudget._meta.verbose_name]})
            return render(request, 'mo_updating.html', context, context_instance=RequestContext(request))
    else:
        sub = dep_agreement.subvention
        dep_prefix, sub_prefix = 'dep_mo', 'sub_mo'
        dep_form = DepartamentAgreementForm(instance=dep_agreement, prefix=dep_prefix, initial={'prev_mo': dep_agreement.mo})
        sub_form = SubventionForm(instance=sub, prefix=sub_prefix) if agreement_type == 1\
                   else SubventionMinusForm(instance=sub, prefix=sub_prefix)
        forms.append({'dep_form': dep_form, 'sub_form': sub_form,
                      'prefs': [dep_prefix, sub_prefix]})
        context.update({'forms': forms, 'titles': [FederalBudget._meta.verbose_name, RegionalBudget._meta.verbose_name]})
    return render(request, 'mo_updating.html', context, context_instance=RequestContext(request))


@login_required
def get_agreement(request, pk):
    context = {}
    dep_agreement = DepartamentAgreement.objects.get(pk=pk)
    typ = int(dep_agreement.agreement_type)
    if typ == 1:
        title = _(u'Дополнительное соглашение с министерством')
    elif typ == 2:
        title = _(u'Письмо о вычете средств')
    else:
        title = _(u'Соглашение с министерством')
    context.update({'title': title})
    form = DepartamentAgreementShowForm(instance=dep_agreement)
    context.update({'object': dep_agreement, 'form': form})
    sub = dep_agreement.subvention
    fed = sub.fed_budget
    reg = sub.reg_budget

    sub_form = SubventionShowForm(instance=sub)
    fed_form = FederalBudgetShowForm(instance=fed)
    reg_form = RegionalBudgetShowForm(instance=reg)
    forms = ({'sub_form': sub_form, 'formsets': [fed_form, reg_form]})
    context.update({'forms': forms, 'titles': [FederalBudget._meta.verbose_name, RegionalBudget._meta.verbose_name]})
    return render(request, 'mo.html', context, context_instance=RequestContext(request))


@login_required
def pre_delete_agreement(request, pk):
    context = {'title': _(u'Удаление соглашения с министерством')}
    dep = DepartamentAgreement.objects.get(pk=pk)
    context.update({'object': dep})
    return render_to_response("agreement_deleting.html", context, context_instance=RequestContext(request))


@login_required
def delete_agreement(request, pk):
    context = {'title': _(u'Удаление соглашения с министерством')}
    dep = DepartamentAgreement.objects.get(pk=pk)
    if dep and 'delete' in request.POST:
        sub = dep.subvention
        if sub:
            fed = sub.fed_budget
            reg = sub.reg_budget

            if fed:
                fed.delete()
            if reg:
                reg.delete()
            sub.delete()
        dep.delete()
        return redirect('mos')
    elif 'cancel' in request.POST:
        return redirect('mos')
    else:
        context.update({'error': _(u'Возникла ошибка при удалении соглашения с министерством!')})
    return render_to_response("agreement_deleting.html", context, context_instance=RequestContext(request))


@login_required
def get_filter(request, num, extra=None):
    context = {'title': _(u'Результат выборки')}
    template = 'filter.html'
    num = int(num) if num else 0
    objects = None
    if num == 0:
        template = '/main/'
        context.update({'title': _(u'По запросу соответствий не найдено, попробуйте изменить фильтр')})
    elif num == 1:
        # Фильтр готовых объектов по всем муниципальным образованиям
        objects = Building.objects.filter(state=0)
        template = '../../build/templates/builds.html'
        context.update({'building_list': objects})
    elif num == 2:
        # Фильтр строящихся объектов по всем муниципальным образованиям (3.2)
        objects = Building.objects.filter(state=1)
        template = '../../build/templates/builds.html'
        context.update({'building_list': objects})
    elif num == 3:
        # Фильтр земельных участков по всем муниципальным образованиям (3.3)
        objects = Ground.objects.filter(state=2)
        template = '../../build/templates/builds.html'
        context.update({'building_list': objects})
    elif num == 4:
        # 4 Фильтр муниципальных образований, которым выделены средства из федерального бюджета (1.2.4.2)
        subs = Subvention.objects.filter(fed_budget__sub_orph_home__gt=0).values('id')
        objects = MO.objects.filter(departamentagreement__subvention__in=[sub.get('id') for sub in subs])
        template = '../../mo/templates/mos.html'
        context.update({'mo_list': objects})
    elif num == 5:
        # 5 Фильтр муниципальных образований, которым выделены средства из краевого бюджета (1.2.4.1)
        subs = Subvention.objects.filter(reg_budget__sub_orph_home__gt=0).values('id')
        objects = MO.objects.filter(departamentagreement__subvention__in=[sub.get('id') for sub in subs])
        template = '../../mo/templates/mos.html'
        context.update({'mo_list': objects})
    elif num == 6:
        # 6 Фильтр всех муниципальных образований, которые заключили контракты с возможностью просмотра подробных сведений по каждому контракту (4.7)
        objects = MO.objects.filter(contract__summa__gt=0).distinct()
        template = '../../mo/templates/mos.html'
        context.update({'mo_list': objects, 'mo_contracts': True})
    elif num == 7:
        # 7 Фильтр муниципальных образований, размещение заказа которых находится на этапе подачи заявок (4.7)
        objects = Auction.objects.filter(stage=0)
        template = '../../cmp/templates/mo_auctions.html'
        context.update({'auction_list': objects})
    elif num == 8:
        # 8 Фильтр муниципальных образований, размещение заказа которых находится на этапе работы комиссии (4.7)
        objects = Auction.objects.filter(stage=1)
        template = '../../cmp/templates/mo_auctions.html'
        context.update({'auction_list': objects})
    elif num == 9:
        # 9 Фильтр муниципальных образований, размещение заказа которых завершено по причине отсутствия участников (4.7)
        objects = Auction.objects.filter(stage=3)
        template = '../../cmp/templates/mo_auctions.html'
        context.update({'auction_list': objects})
    elif num == 10:
        # 10 Фильтр муниципальных образований, размещение заказа которых завершено, подана одна заявка (4.7)
        objects = Auction.objects.filter(proposal_count=1)
        template = '../../cmp/templates/mo_auctions.html'
        context.update({'auction_list': objects})
    elif num == 11:
        # 11 Фильтр муниципальных образований, размещение заказа которых завершено, не допущена ни одна заявка (4.7)
        objects = Auction.objects.filter(stage=2)
        template = '../../cmp/templates/mo_auctions.html'
        context.update({'auction_list': objects})
    elif num == 12:
        # 12 Фильтр муниципальных образований, размещение заказа которых отменено (4.7)
        objects = Auction.objects.filter(stage=5)
        template = '../../cmp/templates/mo_auctions.html'
        context.update({'auction_list': objects})
    elif num == 16:
        # 16 Фильтр муниципальных образований, к которым есть замечания
        objects = MO.objects.filter(has_trouble=True)
        template = '../../mo/templates/mos.html'
        context.update({'mo_list': objects})
    elif num == 17:
        # 17 Фильтр муниципальных образований, к которым нет замечаний
        objects = MO.objects.filter(has_trouble=False)
        template = '../../mo/templates/mos.html'
        context.update({'mo_list': objects})
    elif num == 18:
        # 18 Фильтр муниципальных образований, у которых отсутствуют документы по заключенным контрактам
        docs = ContractDocuments.objects.all()
        undocs = [x for x in docs if not x.has_at_least_one_doc()]
        objects = MO.objects.filter(contract__docs__in=undocs)
        template = '../../mo/templates/mos.html'
        context.update({'mo_list': objects})
    elif num == 19:
        # 19 МО, которые освоили выделенную субвенцию в полном объеме
        objects = MO.objects.filter(common_percentage__gt=99)
        template = '../../mo/templates/mos.html'
        context.update({'mo_list': objects})
    elif num == 20:
        # 20 МО, которые предоставили жилые помещения детям-сиротам
        objects = MO.objects.filter(pk__in=[mo.pk for mo in MO.objects.filter(home_orphans__gte=0)])
        template = '../../mo/templates/mos.html'
        context.update({'mo_list': objects})
        forms = []
        if request.method == 'POST':
            success = 0
            for mo in objects:
                form = MOPerformanceForm(request.POST, instance=mo, prefix='mo_%s' % mo.pk)
                forms.append(form)
                if form.is_valid():
                    form.save()
                    success += 1
                if success == len(forms):
                    redirect('mos')
        else:
            for mo in objects:
                if not mo.home_orphans or mo.home_orphans == 0:
                    mo.home_orphans = sum([(int(dep.subvention.fed_budget.subvention_performance) + int(dep.subvention.reg_budget.subvention_performance))
                                           for dep in mo.departamentagreement_set.filter(agreement_type=0)])
                    mo.save(update_fields=['home_orphans'])
                forms.append(MOPerformanceForm(instance=mo, prefix='mo_%s' % mo.pk))
        context.update({'formset': forms})
    elif num == 21:
        # 21 МО, которые имеют перспективы освоения дополнительных денежных средств на текущий год.
        objects = MO.objects.filter(common_percentage__lte=99)
        template = '../../mo/templates/mos.html'
        context.update({'mo_list': objects})
    if not objects:
        context.update({'errorlist': _(u'Объекты, соответствующие запросу, не найдены')})
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def xls_work_table(request):

    # create
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('untitled')

    # custom colors
    xlwt.add_palette_colour("c_light_grey", 0x21)
    xlwt.add_palette_colour("c_light_green", 0x22)
    xlwt.add_palette_colour("c_light_blue", 0x23)
    book.set_colour_RGB(0x21, 230, 230, 230)
    book.set_colour_RGB(0x22, 200, 255, 200)
    book.set_colour_RGB(0x23, 174, 255, 227)

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
    grey_style = xlwt.easyxf(
        "pattern: pattern solid, fore_colour c_light_grey;"
        "border: left thin, right thin, top thin, bottom thin;"
        "align: vertical center, horizontal center, wrap True;"
    )
    green_style = xlwt.easyxf(
        "pattern: pattern solid, fore_colour c_light_green;"
        "border: left thin, right thin, top thin, bottom thin;"
        "align: vertical center, horizontal center, wrap True;"
    )
    blue_style = xlwt.easyxf(
        "pattern: pattern solid, fore_colour c_light_blue;"
        "border: left thin, right thin, top thin, bottom thin;"
        "align: vertical center, horizontal center, wrap True;"
    )

    ## make header
    header_height = 8
    now = datetime.now()

    # МО
    col = 0
    sheet.write_merge(0, 0, 1, 3, u'МО', style_bold)
    sheet.write_merge(0, header_height, col, col, u'№', style_bold)
    col += 1
    sheet.write_merge(1, header_height, col, col, u'Наименование муниципального образования', green_style)
    col += 1
    sheet.write_merge(1, header_height, col, col, u"Форма создания специализированного жилищного фонда"
                                  u" (С - строительство, ДС - долевое строительство "
                                  u"П - приобретение)", green_style)
    col += 1
    sheet.write_merge(1, header_height, col, col, u"Численность граждан от 18 лет и старше, включенных в список", green_style)
    col += 1
    # Краевой бюджет
    sheet.write_merge(0, 0, col, col + 6, u'Краевой бюджет (по состоянию на %d.%d.%d %d:%d)' % \
        (now.day, now.month, now.year, now.hour, now.minute), style_bold)
    sheet.write_merge(1, header_height, col, col, u'Количество жилых помещений', green_style)
    col += 1
    sheet.write_merge(1, header_height, col, col, u'Сумма с учетом коэффициента на администрирование', green_style)
    col += 1
    sheet.write_merge(1, header_height, col, col, u'Сумма без учета коэффицента на администрирование', green_style)
    col += 1
    sheet.write_merge(1, header_height, col, col, u'Профинансировано министерством', green_style)
    col += 1
    sheet.write_merge(1, header_height, col, col, u'Кассовый расход', green_style)
    col += 1
    sheet.write_merge(1, header_height, 9, 9, u'% исполнения по кассовому расходу', green_style)
    col += 1
    sheet.write_merge(1, header_height, col, col, u'Остаток неосвоенных средств', green_style)
    col += 1

    # Федеральный бюджет
    sheet.write_merge(0, 0, col, col + 6, u'Федеральный бюджет (по состоянию на %d.%d.%d %d:%d)' % \
                                  (now.day, now.month, now.year, now.hour, now.minute), style_bold)
    sheet.write_merge(1, header_height, col, col, u'Количество жилых помещений', blue_style)
    col += 1
    sheet.write_merge(1, header_height, col, col, u'Сумма с учетом коэффициента на администрирование', blue_style)
    col += 1
    sheet.write_merge(1, header_height, col, col, u'Сумма без учета коэффицента на администрирование', blue_style)
    col += 1
    sheet.write_merge(1, header_height, col, col, u'Профинансировано министерством', blue_style)
    col += 1
    sheet.write_merge(1, header_height, col, col, u'Кассовый расход', blue_style)
    col += 1
    sheet.write_merge(1, header_height, col, col, u'% исполнения по кассовому расходу', blue_style)
    col += 1
    sheet.write_merge(1, header_height, col, col, u'Остаток неосвоенных средств', blue_style)
    col += 1

    # Итого
    sheet.write_merge(0, 0, col, col + 2, u'Итого федеральный и краевой бюджет', style_bold)
    sheet.write_merge(1, header_height, col, col, u'Количество жилых помещений', style_plain)
    col += 1
    sheet.write_merge(1, header_height, col, col, u'Сумма с учетом коэффициента на администрирование', style_plain)
    col += 1
    sheet.write_merge(1, header_height, col, col, u'Кассовый расход', style_plain)
    col += 1

    # Заключенные контракты
    sheet.write_merge(0, 0, col, col + 5, u'Заключенные контракты', style_bold)
    sheet.write_merge(1, header_height, col, col, u'Количество жилых помещений', grey_style)
    col += 1
    sheet.write_merge(1, header_height, col, col, u'Сумма по заключенным контрактам (без учета средств МО)', grey_style)
    col += 1
    sheet.write_merge(1, header_height, col, col, u'Сумма муниципальных средств, включенных в сумму контракта', grey_style)
    col += 1
    sheet.write_merge(1, header_height, col, col, u'Сумма по заключенным контрактам (ИТОГО)', grey_style)
    col += 1
    sheet.write_merge(1, header_height, col, col, u'% исполнения от суммы предусмотренной субвенции', grey_style)
    col += 1
    sheet.write_merge(1, header_height, col, col, u'Экономия по результатам заключенных контрактов', grey_style)
    col += 1

    # fill table
    row = header_height + 1
    num = 1
    user_year = datetime.today().year
    object_kwargs = {}
    payment_kwargs = {}
    agreement_kwargs = {}
    if hasattr(request.user, 'customuser') and request.user.customuser.get_user_date():
        user_year = request.user.customuser.get_user_date().year
        from_dt = datetime(user_year, 01, 01)
        to_dt = datetime(user_year, 12, 31)
        agreement_kwargs.update({'date__gt': from_dt, 'date__lt': to_dt})
        payment_kwargs.update({'date__gt': from_dt, 'date__lt': to_dt})
        object_kwargs = {'start_year__lt': request.user.customuser.get_user_date(),
                         'finish_year__gt': request.user.customuser.get_user_date()}
    payment_kwargs.update({} )
    # sort city first
    sorted_objects = []
    objects = MO.objects.all().order_by('name')
    for obj in objects:
        if obj.name.startswith(u"г."):
            sorted_objects.append(obj)
    for obj in objects:
        if not obj.name.startswith(u"г."):
            sorted_objects.append(obj)
    for mo in sorted_objects:
        col = 0
        sheet.write(row, col, u"%s" % num)
        col += 1

        sheet.write(row, col, mo.name)
        col += 1

        mo_createion_form_map = {
            u"Приобретение": u"П",
            u"Долевое строительство": u"ДС",
            U"Строительство": u"C",
            }
        sheet.write(row, col, u", ".join([mo_createion_form_map[c[1]] for c in CREATION_FORM_CHOICES if mo.creation_form and unicode(c[0]) in mo.creation_form.split(',')]))
        col += 1

        # Численность граждан от 18 лет и старше, включенных в список
        sheet.write(row, col, mo.planing_home_orphans)
        col += 1

        ## Краевой бюджет
        # Количество жилых помещений
        query = mo.departamentagreement_set.filter(**agreement_kwargs)
        reg_subvention_performance = sum([agr.subvention.reg_budget.subvention_performance or 0 for agr in query.all() if agr.subvention and agr.subvention.reg_budget])
        sheet.write(row, col, reg_subvention_performance)
        col += 1

        # Краевой бюджет сумма с учетом коэф администрирования
        reg_sum_with_k = 0
        reg_sum_without_k = 0
        for arg in query.all():
            if arg.subvention.reg_budget:
                if arg.subvention.reg_budget.sub_sum:
                    reg_sum_without_k += arg.subvention.reg_budget.sub_sum
                    reg_sum_with_k += arg.subvention.reg_budget.sub_sum
                if arg.subvention.reg_budget.adm_coef:
                    reg_sum_with_k += arg.subvention.reg_budget.adm_coef
        # count additional agreements as part of reg budget
        #for arg in query.exclude(agreement_type=0):
        #    if arg.subvention.amount:
        #        reg_sum_with_k += arg.subvention.amount
        sheet.write(row, col, u"%s " % reg_sum_with_k)
        col += 1

        # Краевой бюджет сумма без учета коэф администрирования
        sheet.write(row, col, u"%s " % reg_sum_without_k)
        col += 1

        # Профинансировано министерством
        reg_minis_sum = sum([agr.subvention.reg_budget.minis_sum or 0 for agr in query.all() if agr.subvention and agr.subvention.reg_budget])
        sheet.write(row, col, reg_minis_sum)
        col += 1

        # Краевой бюджет кассовый расход
        reg_spend_amount = sum([p.get("amount") or 0 for p in Payment.objects.filter(payment_budget_state=2,
            **payment_kwargs).filter(contract__mo=mo).values("amount")])
        sheet.write(row, col, u"%s " % reg_spend_amount)
        col += 1

        # % исполнения по кассовому расходу
        percent_reg_rest_of_unspended = 0
        if reg_sum_with_k and reg_spend_amount:
            percent_reg_rest_of_unspended = (float(reg_spend_amount) / float(reg_sum_with_k)) * 100
        sheet.write(row, col, u"%s " % percent_reg_rest_of_unspended + u"%")
        col += 1

        # Остаток неосвоенных средств
        reg_rest_of_unspended = reg_sum_with_k - reg_spend_amount
        sheet.write(row, col, u"%s " % reg_rest_of_unspended)
        col += 1

        ## Федеральный бюджет
        # Количество жилых помещений
        query = mo.departamentagreement_set.filter(**agreement_kwargs)
        fed_subvention_performance = sum([agr.subvention.fed_budget.subvention_performance or 0 for agr in query.all() if agr.subvention and agr.subvention.fed_budget])
        sheet.write(row, col, fed_subvention_performance)
        col += 1

        # Федеральный бюджет сумма с учетом коэф администрирования
        fed_sum_with_k = 0
        fed_sum_without_k = 0
        for arg in query.all():
            if arg.subvention.fed_budget:
                if arg.subvention.fed_budget.sub_sum:
                    fed_sum_without_k += arg.subvention.fed_budget.sub_sum
                    fed_sum_with_k += arg.subvention.fed_budget.sub_sum
                if arg.subvention.fed_budget.adm_coef:
                    fed_sum_with_k += arg.subvention.fed_budget.adm_coef
        sheet.write(row, col, u"%s " % fed_sum_with_k)
        col += 1

        # Федеральный бюджет сумма без учета коэф администрирования
        sheet.write(row, col, u"%s " % fed_sum_without_k)
        col += 1

        # Профинансировано министерством ?
        fed_minis_sum = sum([agr.subvention.fed_budget.minis_sum or 0 for agr in query.all() if agr.subvention and agr.subvention.fed_budget])
        sheet.write(row, col, fed_minis_sum)
        col += 1

        # Федеральный бюджет кассовый расход
        fed_spend_amount = sum([p.get("amount") or 0 for p in Payment.objects.filter(payment_budget_state=1,
            **payment_kwargs).filter(contract__mo=mo).values("amount")])
        sheet.write(row, col, u"%s " % fed_spend_amount)
        col += 1

        # % исполнения по кассовому расходу
        percent_fed_rest_of_unspended = 0
        if fed_sum_with_k and fed_spend_amount:
            percent_fed_rest_of_unspended = (float(fed_spend_amount) / float(fed_sum_with_k)) * 100
        sheet.write(row, col, u"%s " % percent_fed_rest_of_unspended + u"%")
        col += 1

        # Остаток неосвоенных средств
        fed_rest_of_unspended = fed_sum_with_k - fed_spend_amount
        sheet.write(row, col, u"%s " % fed_rest_of_unspended)
        col += 1

        ## sums
        # Количество жилых помещений
        sum_flats_amount = reg_subvention_performance + fed_subvention_performance
        sheet.write(row, col, sum_flats_amount)
        col += 1

        # Сумма с учетом коэффицента администрирования
        sum_sum_with_k = reg_sum_with_k + fed_sum_with_k
        sheet.write(row, col, u"%s " % sum_sum_with_k)
        col += 1


        # Кассовый расход
        sum_spend_amount = reg_spend_amount + fed_spend_amount
        sheet.write(row, col, u"%s " % sum_spend_amount)
        col += 1

        ## contracts
        # Количество жилых помещений
        contracts_flats_amount = 0
        contracts_summ = 0
        contracts_summ_without_mo_money = 0
        contracts_summ_mo_money = 0
        query = mo.contract_set.filter(**object_kwargs).values("flats_amount", "summa",
                                             "summ_without_mo_money", "summ_mo_money")
        for contract in query:
            if contract["flats_amount"]:
                contracts_flats_amount += contract["flats_amount"]
            # Сумма по заключенным контрактам ИТОГО
            if contract["summa"]:
                contracts_summ += contract["summa"]
            # Сумма по заключенным контрактам (без учета средств МО)
            if contract["summ_without_mo_money"]:
                contracts_summ_without_mo_money += contract["summ_without_mo_money"]
            # Сумма муниципальных средств, включенных в сумму контракта
            if contract["summ_mo_money"]:
                contracts_summ_mo_money += contract["summ_mo_money"]


        # Количество жилых помещений
        sheet.write(row, col, contracts_flats_amount)
        col += 1

        # Сумма по заключенным контрактам (без учета средств МО)
        sheet.write(row, col, contracts_summ_without_mo_money)
        col += 1

        # Сумма муниципальных средств, включенных в сумму контракта
        sheet.write(row, col, contracts_summ_mo_money)
        col += 1

        # Сумма по заключенным контрактам ИТОГО
        sheet.write(row, col, contracts_summ)
        col += 1

        # % исполнения от суммы предусмотренной субвенции (сумма субвенций)
        percent_rest_of_unspended_contract = 0
        if reg_sum_with_k and fed_sum_with_k and reg_spend_amount:
            percent_rest_of_unspended_contract = (float(contracts_summ) / float(reg_sum_with_k + fed_spend_amount)) * 100
        sheet.write(row, col, u"%s " % percent_rest_of_unspended_contract + u"%")
        col += 1

        # Экономия по результатам заключенных контрактов
        max_flat_price = MaxFlatPrice.objects.get(year=user_year)
        contracts_economy = contracts_flats_amount * max_flat_price.max_price - contracts_summ
        contracts_economy = contracts_economy if contracts_economy > 0 else 0
        sheet.write(row, col, contracts_economy)
        col += 1

        row += 1
        num += 1

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=list.xls'
    book.save(response)
    return response

@login_required
def add_max_flat_price(request):
    template = 'max_flat_price_creation.html'
    title = _(u'Максимальная стоимость квартиры')
    context = {'title': title}
    if not request.user.is_staff:
        return HttpResponseForbidden(u"Forbidden")
    if request.method == "POST":
        form = MaxFlatPriceForm(request.POST)
        if form.is_valid():
            object = form.save()
            return redirect('max_flat_prices')
    else:
        form = MaxFlatPriceForm()
    context.update({'form': form})
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def xls_contract_grapth(request):

    # create
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('untitled')

    # custom colors
    xlwt.add_palette_colour("c_light_grey", 0x21)
    xlwt.add_palette_colour("c_light_green", 0x22)
    xlwt.add_palette_colour("c_light_blue", 0x23)
    book.set_colour_RGB(0x21, 230, 230, 230)
    book.set_colour_RGB(0x22, 200, 255, 200)
    book.set_colour_RGB(0x23, 174, 255, 227)

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
    grey_style = xlwt.easyxf(
        "pattern: pattern solid, fore_colour c_light_grey;"
        "border: left thin, right thin, top thin, bottom thin;"
        "align: vertical center, horizontal center, wrap True;"
    )
    green_style = xlwt.easyxf(
        "pattern: pattern solid, fore_colour c_light_green;"
        "border: left thin, right thin, top thin, bottom thin;"
        "align: vertical center, horizontal center, wrap True;"
    )
    blue_style = xlwt.easyxf(
        "pattern: pattern solid, fore_colour c_light_blue;"
        "border: left thin, right thin, top thin, bottom thin;"
        "align: vertical center, horizontal center, wrap True;"
    )

    ## make header
    header_height = 7
    now = datetime.now()

    # МО
    col = 0
    sheet.write_merge(0, header_height, 0, 0, u'Наименование месяца', style_bold)
    sheet.write_merge(0, header_height, 1, 1, u'Количество контрактов, шт', style_bold)
    sheet.write_merge(0, header_height, 2, 2, u'%', style_bold)
    sheet.write_merge(0, header_height, 3, 3, u'Кассовый расход по освоению субвенций, руб.', style_bold)
    sheet.write_merge(0, header_height, 4, 4, u'%', style_bold)

    months = [
        {1: u'Январь'},
        {2: u'Февраль'},
        {3: u'Март'},
        {4: u'Апрель'},
        {5: u'Май'},
        {6: u'Июнь'},
        {7: u'Июль'},
        {8: u'Август'},
        {9: u'Сентябрь'},
        {10: u'Октябрь'},
        {11: u'Ноябрь'},
        {12: u'Декабрь'},
    ]

    agreement_kwargs = {}
    payment_kwargs = {}
    object_kwargs = {}
    if hasattr(request.user, 'customuser') and request.user.customuser.get_user_date():
        user_year = request.user.customuser.get_user_date().year
        from_dt = datetime(user_year, 01, 01)
        to_dt = datetime(user_year, 12, 31)
        payment_kwargs.update({'date__gt': from_dt, 'date__lt': to_dt})
        agreement_kwargs.update({'date__gt': from_dt, 'date__lt': to_dt})
        object_kwargs = {'start_year__lt': request.user.customuser.get_user_date(),
                         'finish_year__gt': request.user.customuser.get_user_date()}

    col = 0
    row = header_height + 1

    # count common data
    subvention_performance = 0
    sum_with_k = 0
    for mo in MO.objects.all():
        query = mo.departamentagreement_set.filter(**agreement_kwargs)
        reg_subvention_performance = sum([agr.subvention.reg_budget.subvention_performance or 0 for agr in query.all() if agr.subvention and agr.subvention.reg_budget])
        fed_subvention_performance = sum([agr.subvention.fed_budget.subvention_performance or 0 for agr in query.all() if agr.subvention and agr.subvention.fed_budget])
        subvention_performance += reg_subvention_performance
        subvention_performance += fed_subvention_performance
        for arg in query.all():
            if arg.subvention.reg_budget:
                if arg.subvention.reg_budget.sub_sum:
                    sum_with_k += arg.subvention.reg_budget.sub_sum
                if arg.subvention.reg_budget.adm_coef:
                    sum_with_k += arg.subvention.reg_budget.adm_coef
            if arg.subvention.fed_budget:
                if arg.subvention.fed_budget.sub_sum:
                    sum_with_k += arg.subvention.fed_budget.sub_sum
                if arg.subvention.fed_budget.adm_coef:
                    sum_with_k += arg.subvention.fed_budget.adm_coef

    # fill table
    for month in months:
        # Наименование месяца
        sheet.write(row, col, month.values()[0])
        # Количество контрактов
        contracts_num = Contract.objects.filter(**object_kwargs).filter(date__month=month.keys()[0]).count()
        sheet.write(row, col + 1, contracts_num)
        # Отношение количества жилых помещений в контрактах к показателю результативности субвенции (%)
        flats_amount = sum([amount.values()[0] or 0 for amount in Contract.objects.filter(**object_kwargs).filter(date__month=month.keys()[0]).values('flats_amount')])
        percent_of_contracts_flats_amount_and_subvention_perfomance = float(flats_amount) / float(subvention_performance) * 100
        sheet.write(row, col + 2, percent_of_contracts_flats_amount_and_subvention_perfomance)
        # Кассовый расход по освоению субвенций
        spend_amount = sum([p.get("amount") or 0 for p in Payment.objects.filter(**payment_kwargs).filter(date__month=month.keys()[0]).values("amount")])
        sheet.write(row, col + 3, spend_amount)
        # Отношение сумм субвенций к кассовому расходу (%)
        if not spend_amount:
            percent_of_sum_with_k_and_spend_amount = 0
        else:
            percent_of_sum_with_k_and_spend_amount = spend_amount / sum_with_k * 100
        sheet.write(row, col + 4, percent_of_sum_with_k_and_spend_amount)
        row += 1

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=list.xls'
    book.save(response)
    return response


@login_required
def update_max_flat_price(request, pk):
    template = 'max_flat_price_creation.html'
    title = _(u'Максимальная стоимость квартиры')
    context = {'title': title}
    if not request.user.is_staff:
        return HttpResponseForbidden(u"Forbidden")
    if request.method == "POST":
        form = MaxFlatPriceForm(request.POST)
        if form.is_valid():
            object = form.save()
    else:
        object = MaxFlatPrice.objects.get(pk=pk)
        form = MaxFlatPriceForm(instance=object)
    context.update({'form': form})
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def delete_max_flat_price(request, pk):
    title = _(u'Максимальная стоимость квартиры')
    context = {'title': title}
    if not request.user.is_staff:
        return HttpResponseForbidden(u"Forbidden")
    object = MaxFlatPrice.objects.get(pk=pk)
    object.delete()
    return redirect('max_flat_prices')


@login_required
def get_max_flat_prices(request):
    template = 'max_flat_prices.html'
    title = _(u'Максимальная стоимость квартиры')
    context = {'title': title}
    objects = MaxFlatPrice.objects.all()
    context.update({'objects': objects})
    return render_to_response(template, context, context_instance=RequestContext(request))
