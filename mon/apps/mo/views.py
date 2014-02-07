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
            if hasattr(sub, 'subvention_performance'):
                mo.home_orphans = int(mo.home_orphans) + int(sub.subvention_performance)
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
    if MO.objects.all().exists():
        objects = MO.objects.all().order_by('name')
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
    if request.user.is_staff:
        if selected_users:
            return HttpResponseForbidden(u"МО %s уже выбрано у пользователя %s" % (mo, selected_users[0]))
    user = CustomUser.objects.get(pk=request.user.pk)
    user.mo = mo
    user.save()
    context.update({'object': mo, 'form': form, 'agreement': True})
    dep_agreements = mo.departamentagreement_set.all()
    context.update({'hide_menu': True, 'agreements': dep_agreements})
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
    context.update({'object': dep_agreement, 'agreement': True, 'prefix': prefix})
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
    context = {'title': _(u'Соглашение с министерством')}
    dep_agreement = DepartamentAgreement.objects.get(pk=pk)
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
        objects = MO.objects.filter(pk__in=[mo.pk for mo in MO.objects.filter(departamentagreement__subvention_performance__gt=0)])
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
                mo.home_orphans = sum([int(dep.subvention_performance) for dep in mo.departamentagreement_set.all()
                                       if dep.subvention_performance])
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
    # create
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('untitled')

    # custom colors
    xlwt.add_palette_colour("c_light_grey", 0x21)
    book.set_colour_RGB(0x21, 216, 216, 216)

    # styles
    style_plain = xlwt.easyxf("align: vertical center, horizontal center;")
    style_bold = xlwt.easyxf(
        "font: bold 1;"
        "align: vertical center, horizontal center;"
    )

    date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')
    green_style = xlwt.easyxf("pattern: pattern solid, fore_colour c_light_grey;")

    # make sheet
    sheet.write_merge(0,0,1,6, u'Численность', style_bold)
    sheet.write_merge(0,5,0,0, u'№', style_bold)

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=list.xls'
    book.save(response)
    return response
