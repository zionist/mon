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

from .models import MO, DepartamentAgreement, PeopleAmount, Subvention, FederalBudget, RegionalBudget
from .forms import MOForm, DepartamentAgreementForm, PeopleAmountForm, SubventionForm, FederalBudgetForm, \
    RegionalBudgetForm, MOShowForm, DepartamentAgreementShowForm, SubventionShowForm, FederalBudgetShowForm, RegionalBudgetShowForm
from apps.build.models import Building, Ground
from apps.cmp.models import Auction


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
            dep.subvention = sub
            dep.mo = form.save()
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
    template = 'mos.html'
    context = {'title': _(u'Муниципальные образования')}
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
        context.update({'mo_list': objects})
    return render(request, template, context, context_instance=RequestContext(request))


def get_mo(request, pk, extra=None):
    context = {'title': _(u'Муниципальное образование')}
    mo = MO.objects.get(pk=pk)
    dep_agreement = DepartamentAgreement.objects.get(mo=pk)
    sub = dep_agreement.subvention
    fed = sub.fed_budget
    reg = sub.reg_budget
    form = MOShowForm(instance=mo)
    dep_form = DepartamentAgreementShowForm(instance=dep_agreement)
    sub_form = SubventionShowForm(instance=sub)
    fed_form = FederalBudgetShowForm(instance=fed)
    reg_form = RegionalBudgetShowForm(instance=reg)
    context.update({'object': mo, 'form': form, 'dep_form': dep_form, 'sub_form': sub_form,
                    'formsets': [fed_form, reg_form], 'titles': [FederalBudget._meta.verbose_name, RegionalBudget._meta.verbose_name]})
    return render(request, 'mo.html', context, context_instance=RequestContext(request))


def update_mo(request, pk, extra=None):
    context = {'title': _(u'Параметры мниципального образования')}
    mo = MO.objects.get(pk=pk)
    dep_agreement = DepartamentAgreement.objects.get(mo=pk)
    sub = dep_agreement.subvention
    fed = sub.fed_budget
    reg = sub.reg_budget
    prefix, dep_prefix, sub_prefix, reg_prefix, fed_prefix = 'mo', 'dep_mo', 'sub_mo', 'reg_mo', 'fed_mo'
    if request.method == "POST":
        form = MOForm(request.POST, instance=mo, prefix=prefix)
        dep_form = DepartamentAgreementForm(request.POST, instance=dep_agreement, prefix=dep_prefix)
        sub_form = SubventionForm(request.POST, instance=sub, prefix=sub_prefix)
        fed_form = FederalBudgetForm(request.POST, instance=fed, prefix=fed_prefix)
        reg_form = RegionalBudgetForm(request.POST, instance=reg, prefix=reg_prefix)
        context.update({'object': mo, 'form': form, 'dep_form': dep_form, 'sub_form': sub_form,
                        'formsets': [fed_form, reg_form], 'titles': [FederalBudget._meta.verbose_name, RegionalBudget._meta.verbose_name],
                        'prefix': prefix})
        if form.is_valid() and dep_form.is_valid() and sub_form.is_valid() and fed_form.is_valid() and reg_form.is_valid():
            form.save()
            dep_form.save()
            fed_form.save()
            reg_form.save()
            sub_form.save()
            return redirect('mos')
        else:
            context.update({'object': mo, 'form': form, 'dep_form': dep_form, 'sub_form': sub_form,
                            'formsets': [fed_form, reg_form], 'titles': [FederalBudget._meta.verbose_name, RegionalBudget._meta.verbose_name],
                            'prefix': prefix})
            return render(request, 'mo_updating.html', context, context_instance=RequestContext(request))
    else:
        form = MOForm(instance=mo, prefix=prefix)
        dep_form = DepartamentAgreementForm(instance=dep_agreement, prefix=dep_prefix)
        sub_form = SubventionForm(instance=sub, prefix=sub_prefix)
        fed_form = FederalBudgetForm(instance=fed, prefix=fed_prefix)
        reg_form = RegionalBudgetForm(instance=reg, prefix=reg_prefix)
        context.update({'object': mo, 'form': form, 'dep_form': dep_form, 'sub_form': sub_form,
                        'formsets': [fed_form, reg_form], 'titles': [FederalBudget._meta.verbose_name, RegionalBudget._meta.verbose_name],
                        'prefix': prefix})
    return render(request, 'mo_updating.html', context, context_instance=RequestContext(request))


def pre_delete_mo(request, pk):
    context = {'title': _(u'Удаление муниципального образования')}
    mo = MO.objects.get(pk=pk)
    context.update({'object': mo})
    return render_to_response("mo_deleting.html", context, context_instance=RequestContext(request))


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
        objects = MO.objects.filter(contract__docs__count=0)
        template = '../../mo/templates/mos.html'
        context.update({'mo_list': objects})
    elif num == 19:
        # 19 МО, которые освоили выделенную субвенцию в полном объеме
        objects = MO.objects.filter(has_trouble=True)
        template = '../../payment/templates/payments.html'
        context.update({'payment_list': objects})
    elif num == 20:
        # 20 МО, которые предоставили жилые помещения детям-сиротам
        objects = MO.objects.filter(home_orphans__gt=0)
        template = '../../mo/templates/mos.html'
        context.update({'mo_list': objects})
    elif num == 21:
        # 21 МО, которые имеют перспективы освоения дополнительных денежных средств на текущий год.
        objects = MO.objects.filter(has_trouble=True)
        template = '../../mo/templates/mos.html'
        context.update({'mo_list': objects})
    if not objects:
        context.update({'errorlist': _(u'Объекты, соответствующие запросу, не найдены')})
    return render_to_response(template, context, context_instance=RequestContext(request))
