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
    RegionalBudgetForm, MOShowForm, DepartamentAgreementShowForm


def add_mo(request):
    template = 'mo_creation.html'
    context = {'title': _(u'Добавление муниципального образования')}
    prefix, dep_prefix = 'mo', 'dep_mo'
    if request.method == "POST":
        form = MOForm(request.POST, prefix=prefix)
        dep_form = DepartamentAgreementForm(request.POST, prefix=dep_prefix)
        if form.is_valid() and dep_form.is_valid():
            dep = dep_form.save()
            dep.mo = form.save()
            dep.save(update_fields=['mo'])
            return redirect('mos')
    else:
        form = MOForm(prefix=prefix)
        dep_form = DepartamentAgreementForm(prefix=dep_prefix)
    context.update({'form': form, 'dep_form': dep_form, 'prefix': prefix})
    return render_to_response(template, context, context_instance=RequestContext(request))


@login_required
def get_mos(request, pk=None):
    template = 'mos.html'
    context = {'title': _(u'Муниципальные образовнаиия')}
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
    prefix, dep_prefix = 'mo', 'dep_mo'
    if request.method == "POST":
        form = MOShowForm(request.POST, instance=mo, prefix=prefix)
        dep_form = DepartamentAgreementShowForm(request.POST, instance=dep_agreement, prefix=dep_prefix)
        context.update({'form': form, 'dep_form': dep_form})
    else:
        form = MOShowForm(instance=mo, prefix=prefix)
        dep_form = DepartamentAgreementShowForm(instance=dep_agreement, prefix=dep_prefix)
        context.update({'form': form, 'dep_form': dep_form})
    context.update({'object': mo})
    return render(request, 'mo.html', context, context_instance=RequestContext(request))


def update_mo(request, pk, extra=None):
    context = {'title': _(u'Параметры мниципального образования')}
    mo = MO.objects.get(pk=pk)
    dep_agreement = DepartamentAgreement.objects.get(mo=pk)
    prefix, dep_prefix = 'mo', 'dep_mo'
    if request.method == "POST":
        form = MOForm(request.POST, instance=mo, prefix=prefix)
        dep_form = DepartamentAgreementForm(request.POST, instance=dep_agreement, prefix=dep_prefix)
        context.update({'object': mo, 'form': form, 'dep_form': dep_form, 'prefix': prefix})
        if form.is_valid() and dep_form.is_valid():
            form.save()
            dep_form.save()
            return redirect('mos')
        else:
            context.update({'object': mo, 'form': form, 'dep_form': dep_form, 'prefix': prefix})
            return render(request, 'mo_updating.html', context, context_instance=RequestContext(request))
    else:
        form = MOForm(instance=mo, prefix=prefix)
        dep_form = DepartamentAgreementForm(instance=dep_agreement, prefix=dep_prefix)
        context.update({'object': mo, 'form': form, 'dep_form': dep_form, 'prefix': prefix})
    return render(request, 'mo_updating.html', context, context_instance=RequestContext(request))


def pre_delete_mo(request, pk):
    context = {'title': _(u'Удаление муниципального образования')}
    mo = MO.objects.get(pk=pk)
    context.update({'object': mo})
    return render_to_response("mo_deleting.html", context, context_instance=RequestContext(request))


def delete_mo(request, pk):
    context = {'title': _(u'Удаление осмотра')}
    mo = MO.objects.get(pk=pk)
    if mo and 'delete' in request.POST:
        dep_agreement = DepartamentAgreement.objects.get(mo=pk)
        mo.delete()
        dep_agreement.delete()
        return redirect('mos')
    elif 'cancel' in request.POST:
        return redirect('mos')
    else:
        context.update({'error': _(u'Возникла ошибка при удалении муниципального образования!')})
    return render_to_response("mo_deleting.html", context, context_instance=RequestContext(request))

