# -*- coding: utf-8 -*-

import xlwt
from datetime import datetime
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
from django.contrib.auth.decorators import permission_required, login_required

from .models import MO, DepartamentAgreement, PeopleAmount, Subvention, FederalBudget, RegionalBudget
from .forms import MOForm, DepartamentAgreementForm, PeopleAmountForm, SubventionForm, FederalBudgetForm, \
    RegionalBudgetForm, MOShowForm, DepartamentAgreementShowForm, SubventionShowForm, FederalBudgetShowForm, \
    RegionalBudgetShowForm, MOPerformanceForm, SubventionMinusForm
from apps.build.models import Building, Ground, ContractDocuments
from apps.cmp.models import Auction
from apps.user.models import CustomUser
from apps.core.models import CREATION_FORM_CHOICES
from apps.payment.models import Payment


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


@login_required
def get_mos(request, pk=None):
    title = _(u'Муниципальные образования')
    template = 'mos.html'
    context = {'title': title}
    agreement_kwargs = {}
    if hasattr(request.user, 'customuser') and request.user.customuser.get_user_date():
        from_dt = request.user.customuser.get_user_date()
        to_dt = datetime(from_dt.year + 1, 01, 01)
        agreement_kwargs.update({'date__gt': from_dt, 'date__lt': to_dt})
    if MO.objects.all().exists():
        objects = MO.objects.all().order_by('name')
        for obj in objects:
            query = obj.departamentagreement_set.filter(**agreement_kwargs)
            agreement = query.filter(agreement_type=0)[0] if query.filter(agreement_type=0).exists() else None
            reg_subvention_performance = agreement.subvention.reg_budget.subvention_performance if agreement and agreement.subvention.reg_budget else 0
            fed_subvention_performance = agreement.subvention.fed_budget.subvention_performance if agreement and agreement.subvention.fed_budget else 0
            sum_flats_amount = reg_subvention_performance + fed_subvention_performance
            setattr(obj, "home_orphans", sum_flats_amount)
            amount_sum = 0
            for arg in query.filter(agreement_type=0):
                if arg.subvention.amount:
                    amount_sum += arg.subvention.amount
            setattr(obj, "common_amount", amount_sum)
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
        context.update({'mo_list': objects})
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


@login_required
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


@login_required
def pre_delete_mo(request, pk):
    context = {'title': _(u'Удаление муниципального образования')}
    mo = MO.objects.get(pk=pk)
    context.update({'object': mo})
    return render_to_response("mo_deleting.html", context, context_instance=RequestContext(request))


@login_required
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
def add_agreement(request, pk):
    template = 'mo_adding_agreement.html'
    context = {'title': _(u'Добавление соглашения с министерством')}
    mo = MO.objects.get(pk=pk)
    context.update({'object': mo})
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
            dep.save(update_fields=['subvention', 'mo'])
            return redirect('mos')
    else:
        form = MOShowForm(prefix=prefix, instance=mo)
        dep_form = DepartamentAgreementForm(prefix=dep_prefix)
        sub_form = SubventionForm(prefix=sub_prefix)
        fed_form = FederalBudgetForm(prefix=fed_prefix)
        reg_form = RegionalBudgetForm(prefix=reg_prefix)
    context.update({'form': form, 'dep_form': dep_form, 'sub_form': sub_form, 'formsets': [fed_form, reg_form],
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
        objects = MO.objects.filter(contract__summa__gt=0)
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
        objects = MO.objects.filter(has_trouble=True)
        template = '../../payment/templates/payments.html'
        context.update({'payment_list': objects})
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
        objects = MO.objects.filter(has_trouble=True)
        template = '../../mo/templates/mos.html'
        context.update({'mo_list': objects})
    if not objects:
        context.update({'errorlist': _(u'Объекты, соответствующие запросу, не найдены')})
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def xls_work_table(request):

    import time
    start = time.time()

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
    sheet.write_merge(0, 0, 1, 2, u'МО', style_bold)
    sheet.write_merge(0, header_height, 0, 0, u'№', style_bold)

    sheet.write_merge(1, header_height, 1, 1, u'Наименование муниципального образования', green_style)
    sheet.write_merge(1, header_height, 2, 2, u"Форма создания специализированного жилищного фонда"
                                  u" (С - строительство, ДС - долевое строительство "
                                  u"П - приобретение)", green_style)
    # Краевой бюджет
    sheet.write_merge(0, 0, 3, 9, u'Краевой бюджет (по состоянию на %d.%d.%d %d:%d)' % \
        (now.day, now.month, now.year, now.hour, now.minute), style_bold)
    sheet.write_merge(1, header_height, 3, 3, u'Количество жилых помещений', green_style)
    sheet.write_merge(1, header_height, 4, 4, u'Сумма с учетом коэффициента на администрирование', green_style)
    sheet.write_merge(1, header_height, 5, 5, u'Сумма без учета коэффицента на администрирование', green_style)
    sheet.write_merge(1, header_height, 6, 6, u'Профинансировано министерством', green_style)
    sheet.write_merge(1, header_height, 7, 7, u'Кассовый расход', green_style)
    sheet.write_merge(1, header_height, 8, 8, u'% исполнения по кассовому расходу', green_style)
    sheet.write_merge(1, header_height, 9, 9, u'Остаток неосвоенных средств', green_style)

    # Федеральный бюджет
    sheet.write_merge(0, 0, 10, 16, u'Федеральный бюджет (по состоянию на %d.%d.%d %d:%d)' % \
                                  (now.day, now.month, now.year, now.hour, now.minute), style_bold)
    sheet.write_merge(1, header_height, 10, 10, u'Количество жилых помещений', blue_style)
    sheet.write_merge(1, header_height, 11, 11, u'Сумма с учетом коэффициента на администрирование', blue_style)
    sheet.write_merge(1, header_height, 12, 12, u'Сумма без учета коэффицента на администрирование', blue_style)
    sheet.write_merge(1, header_height, 13, 13, u'Профинансировано министерством', blue_style)
    sheet.write_merge(1, header_height, 14, 14, u'Кассовый расход', blue_style)
    sheet.write_merge(1, header_height, 15, 15, u'% исполнения по кассовому расходу', blue_style)
    sheet.write_merge(1, header_height, 16, 16, u'Остаток неосвоенных средств', blue_style)

    # Итого
    sheet.write_merge(0, 0, 17, 19, u'Итого федеральный и краевой бюджет', style_bold)
    sheet.write_merge(1, header_height, 17, 17, u'Количество жилых помещений', style_plain)
    sheet.write_merge(1, header_height, 18, 18, u'Сумма с учетом коэффициента на администрирование', style_plain)
    sheet.write_merge(1, header_height, 19, 19, u'Кассовый расход', style_plain)

    # Заключенные контракты
    sheet.write_merge(0, 0, 20, 25, u'Заключенные контракты', style_bold)
    sheet.write_merge(1, header_height, 20, 20, u'Количество жилых помещений', grey_style)
    sheet.write_merge(1, header_height, 21, 21, u'Сумма по заключенным контрактам (без учета средств МО)', grey_style)
    sheet.write_merge(1, header_height, 22, 22, u'Сумма муниципальных средств, включенных в сумму контракта', grey_style)
    sheet.write_merge(1, header_height, 23, 23, u'Сумма по заключенным контрактам (ИТОГО)', grey_style)
    sheet.write_merge(1, header_height, 24, 24, u'% исполнения от суммы предусмотренной субвенции', grey_style)
    sheet.write_merge(1, header_height, 25, 25, u'Экономия по результатам заключенных контрактов', grey_style)

    # fill table
    row = header_height + 1
    col = 0
    num = 1
    object_kwargs = {}
    payment_kwargs = {}
    agreement_kwargs = {}
    if hasattr(request.user, 'customuser') and request.user.customuser.get_user_date():
        from_dt = request.user.customuser.get_user_date()
        to_dt = datetime(from_dt.year + 1, 01, 01)
        agreement_kwargs.update({'date__gt': from_dt, 'date__lt': to_dt})
        payment_kwargs.update({'date__gt': from_dt, 'date__lt': to_dt})
        object_kwargs = {'start_year__lt': from_dt, 'finish_year__gt': from_dt}
    payment_kwargs.update({} )
    for mo in MO.objects.all():
        sheet.write(row, col, u"%s" % num)
        sheet.write(row, col + 1, mo.name)
        mo_createion_form_map = {
            u"Приобретение": u"П",
            u"Долевое строительство": u"ДС",
            U"Строительство": u"C",
            }
        sheet.write(row, col + 2, u", ".join([mo_createion_form_map[c[1]] for c in CREATION_FORM_CHOICES if mo.creation_form and unicode(c[0]) in mo.creation_form.split(',')]))

        ## Краевой бюджет
        # Количество жилых помещений
        query = mo.departamentagreement_set.filter(**agreement_kwargs)
        # should be only one subvention with budget for one year
        agreement = query.filter(agreement_type=0)[0] if query.filter(agreement_type=0).exists() else None
        reg_subvention_performance = agreement.subvention.reg_budget.subvention_performance if agreement and agreement.subvention.reg_budget else 0
        sheet.write(row, col + 3, reg_subvention_performance)

        # Краевой бюджет сумма с учетом коэф администрирования
        reg_sum_with_k = 0
        for arg in query.filter(agreement_type=0):
            if arg.subvention.reg_budget:
                if arg.subvention.reg_budget.sub_sum:
                    reg_sum_with_k += arg.subvention.reg_budget.sub_sum
                if arg.subvention.reg_budget.adm_coef:
                    reg_sum_with_k += arg.subvention.reg_budget.adm_coef
        # count additional agreements as part of reg budget
        for arg in query.exclude(agreement_type=0):
            if arg.subvention.amount:
                reg_sum_with_k += arg.subvention.amount
        sheet.write(row, col + 4, u"%s руб." % reg_sum_with_k)

        # Краевой бюджет сумма без учета коэф администрирования
        reg_sum_without_k = 0
        for arg in query.filter(agreement_type=0):
            if arg.subvention.reg_budget:
                if arg.subvention.reg_budget.adm_coef:
                    reg_sum_without_k = reg_sum_with_k - arg.subvention.reg_budget.adm_coef
        sheet.write(row, col + 5, u"%s руб." % reg_sum_without_k)

        # Профинансировано министерством ?

        # Краевой бюджет кассовый расход
        reg_spend_amount = sum([p.get("amount") for p in Payment.objects.filter(contract__budget=2, **payment_kwargs) \
            .filter(contract__mo=mo).values("amount")])
        sheet.write(row, col + 7, u"%s руб." % reg_spend_amount)

        # % исполнения по кассовому расходу
        percent_reg_rest_of_unspended = 0
        if reg_sum_with_k and reg_spend_amount:
            percent_reg_rest_of_unspended = (float(reg_spend_amount) / float(reg_sum_with_k)) * 100
        sheet.write(row, col + 8, u"%s " % percent_reg_rest_of_unspended + u"%")

        # Остаток неосвоенных средств
        reg_rest_of_unspended = reg_sum_with_k - reg_spend_amount
        sheet.write(row, col + 9, u"%s руб." % reg_rest_of_unspended)

        ## Федеральный бюджет
        # Количество жилых помещений
        # should be only one subvention with budget for one year
        agreement = query.filter(agreement_type=0)[0] if query.filter(agreement_type=0).exists() else None
        fed_subvention_performance = agreement.subvention.fed_budget.subvention_performance if agreement and agreement.subvention.fed_budget else 0
        sheet.write(row, col + 10, fed_subvention_performance)

        # Федеральный бюджет сумма с учетом коэф администрирования
        fed_sum_with_k = 0
        for arg in query.filter(agreement_type=0):
            if arg.subvention.fed_budget and arg.subvention.fed_budget.sub_sum:
                fed_sum_with_k += arg.subvention.fed_budget.sub_sum
                if arg.subvention.fed_budget.adm_coef:
                    fed_sum_with_k += arg.subvention.fed_budget.adm_coef
        sheet.write(row, col + 11, u"%s руб." % fed_sum_with_k)

        # Федеральный бюджет сумма без учета коэф администрирования
        fed_sum_without_k = 0
        for arg in query.filter(agreement_type=0):
            if arg.subvention.fed_budget:
                if arg.subvention.fed_budget.adm_coef:
                    fed_sum_without_k = fed_sum_with_k - arg.subvention.fed_budget.adm_coef
        sheet.write(row, col + 12, u"%s руб." % fed_sum_without_k)

        # Профинансировано министерством ?

        # Федеральный бюджет кассовый расход
        fed_spend_amount = sum([p.get("amount") for p in Payment.objects.filter(contract__budget=1, **payment_kwargs)\
            .filter(contract__mo=mo).values("amount")])
        sheet.write(row, col + 14, u"%s руб." % fed_spend_amount)

        # % исполнения по кассовому расходу
        percent_fed_rest_of_unspended = 0
        if fed_sum_with_k and fed_spend_amount:
            percent_fed_rest_of_unspended = (float(fed_spend_amount) / float(fed_sum_with_k)) * 100
        sheet.write(row, col + 15, u"%s " % percent_fed_rest_of_unspended + u"%")

        # Остаток неосвоенных средств
        fed_rest_of_unspended = fed_sum_with_k - fed_spend_amount
        sheet.write(row, col + 16, u"%s руб." % fed_rest_of_unspended)

        ## sums
        # Количество жилых пормещений
        sum_flats_amount = reg_subvention_performance + fed_subvention_performance
        sheet.write(row, col + 17, sum_flats_amount)
        # Сумма с учетом коэффицента администрирования
        sum_sum_with_k = reg_sum_with_k + fed_sum_with_k
        sheet.write(row, col + 18, u"%s руб." % sum_sum_with_k)
        # Кассовый расход
        sum_spend_amount = reg_spend_amount + fed_spend_amount
        sheet.write(row, col + 19, u"%s руб." % sum_spend_amount)

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
        sheet.write(row, col + 20, contracts_flats_amount)

        # Сумма по заключенным контрактам (без учета средств МО)
        sheet.write(row, col + 21, contracts_summ_without_mo_money)

        # Сумма муниципальных средств, включенных в сумму контракта
        sheet.write(row, col + 22, contracts_summ_mo_money)

        # Сумма по заключенным контрактам ИТОГО
        sheet.write(row, col + 23, contracts_summ)

        # % исполнения от суммы предусмотренной субвенции (сумма субвенций)
        percent_rest_of_unspended_contract = 0
        if reg_sum_with_k and fed_sum_with_k and reg_spend_amount:
            percent_rest_of_unspended_contract = (float(contracts_summ) / float(reg_sum_with_k + fed_spend_amount)) * 100
        sheet.write(row, col + 24, u"%s " % percent_rest_of_unspended_contract + u"%")

        # Экономия по результатам заключенных контрактов
        contracts_economy = 0
        spent = sum([int(contract.summa) for contract in mo.contract_set.filter(**object_kwargs) if contract.summa])
        contracts_economy = sum([int(auction.start_price) for auction in mo.auction_set.filter(**object_kwargs) if auction.start_price]) - spent
        sheet.write(row, col + 25, u"%s руб." % contracts_economy)


        row += 1
        num += 1

    end = time.time()
    print end - start

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=list.xls'
    book.save(response)
    return response
