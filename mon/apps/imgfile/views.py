# -*- coding: utf-8 -*-
from datetime import datetime
import webodt
import mimetypes
from webodt.converters import converter

from django.http import HttpResponse, StreamingHttpResponse, \
    HttpResponseNotFound, HttpResponseBadRequest, HttpResponseRedirect
from django.core.servers.basehttp import FileWrapper
from django.template import Context
from django.shortcuts import render_to_response

from apps.build.models import Building
from apps.cmp.models import Contract, Result, CompareData, Auction, MO, \
    Person
from apps.payment.models import Payment
from apps.cmp.forms import ContractForm, ResultForm, CompareDataForm, \
    AuctionForm, ContractShowForm, CompareDataShowForm
from apps.core.forms import RoomShowForm, HallwayShowForm, WCShowForm, \
    KitchenShowForm
from apps.build.forms import BuildingForm, BuildingShowForm
from apps.core.views import get_fk_forms, get_fk_show_forms, split_form
from apps.core.models import WC, Room, Hallway, Kitchen, Developer
from apps.core.views import get_fk_forms, get_fk_show_forms, get_fk_cmp_forms
from apps.imgfile.forms import QuestionsListForm, SelectMoForm, QuestionsListFormSimple
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse



def get_select_mo_form(request):
    if not request.method == "GET":
        return HttpResponseNotFound("Not found")
    template = 'get_select_mo_form.html'
    context = {'title': u'Выбрать муниципальное образование'}
    form = SelectMoForm()
    context.update({'form': form})
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


def get_questions_list_form(request):
    context = {'title': u'Создать форму опроса'}
    template = 'qet_questions_list_form.html'
    # form from get_questions_list was wrong
    if request.method == 'GET' and request.session.get('wrong_post'):
        wrong_post = request.session.get('wrong_post')
        mo = MO.objects.filter(name=wrong_post['mo'])[0]
        form = QuestionsListForm(mo, request.session['wrong_post'])
    # generate new print form for MO
    elif request.method == 'POST':
        if not request.POST.get("mo"):
            return HttpResponseBadRequest("No mo")
        try:
            mo = MO.objects.get(pk=request.POST['mo'])
        except ObjectDoesNotExist:
            return HttpResponseNotFound("Not found")
        form = QuestionsListForm(mo=mo)
    else:
        return HttpResponseNotFound("Not found")
    context.update({'form': form})
    print context
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


def get_questions_list_form_simple(request):
    context = {'title': u'Создать форму опроса'}
    template = 'qet_questions_list_form.html'
    # form from get_questions_list was wrong
    if request.method == 'GET':
        mo = MO.objects.get(pk=request.GET.get('mo'))
        if not mo:
            return HttpResponseBadRequest(u"Не указано МО")
        form = QuestionsListFormSimple(mo)
    # generate new print form for MO
    elif request.method == 'POST':
        mo = MO.objects.get(name=request.POST.get("mo"))
        if not mo:
            return HttpResponseBadRequest(u"Не указано МО")
        form = QuestionsListFormSimple(mo=mo, data=request.POST)
        if form.is_valid():
            context = {'title': u'Бланк опроса'}
            auction = Auction.objects.get(pk=form.cleaned_data.get('auction'))
            context.update({'auction': auction})
            template = 'questions_list.html'
            data = form.cleaned_data.copy()
            data['auction'] = auction.num
            form.data = data
            context.update({'common_form': form})
            contract_form = ContractShowForm(instance=auction.contract)
            context.update({'contract_form': contract_form})
            build_forms = {}
            for obj in auction.contract.building_set.all():
                formset = get_fk_show_forms(parent=obj)
                build_forms[BuildingForm(instance=obj)] = formset
            context.update({'building_forms': build_forms})
            return render_to_response(template, context,
                                      context_instance=RequestContext(request))
    else:
        return HttpResponseNotFound("Not found")
    context.update({'form': form})
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


def get_monitoring_info(request, pk=None):
    context = {'title': u'Информация о проведенном мониторинге'}
    template = 'monitoring_info.html'
    result = Result.objects.get(pk=pk)
    if not result:
        return HttpResponseNotFound(u"Not found")
    context.update({'result': result})

    user_year = datetime.today().year
    mo = result.mo
    payment_kwargs = {}
    agreement_kwargs = {}
    user_year = request.user.customuser.get_user_date().year
    from_dt = datetime(user_year, 01, 01)
    to_dt = datetime(user_year, 12, 31)
    agreement_kwargs.update({'date__gt': from_dt, 'date__lt': to_dt})
    payment_kwargs.update({'date__gt': from_dt, 'date__lt': to_dt,
                           'payment_state': 1})
    object_kwargs = {'start_year__lt': request.user.customuser.get_user_date(),
                     'finish_year__gt': request.user.customuser.get_user_date()}
    query = mo.departamentagreement_set.filter(**agreement_kwargs)

    # Бюджет сумма с учетом коэф администрирования
    reg_sum_with_k = 0
    fed_sum_with_k = 0
    for arg in query.all():
        if arg.subvention.reg_budget:
            if arg.subvention.reg_budget.sub_sum:
                reg_sum_with_k += arg.subvention.reg_budget.sub_sum
            if arg.subvention.reg_budget.adm_coef:
                reg_sum_with_k += arg.subvention.reg_budget.adm_coef
            if arg.subvention.fed_budget.sub_sum:
                fed_sum_with_k += arg.subvention.fed_budget.sub_sum
            if arg.subvention.fed_budget.adm_coef:
                fed_sum_with_k += arg.subvention.fed_budget.adm_coef
    context.update({'reg_sum_with_k': reg_sum_with_k, 'fed_sum_with_k': fed_sum_with_k})
    sum_with_k = reg_sum_with_k + fed_sum_with_k

    # Показатель результативности
    subvention_performance = 0
    reg_subvention_performance = sum([agr.subvention.reg_budget.subvention_performance or 0 for agr in query.all() if agr.subvention and agr.subvention.reg_budget])
    fed_subvention_performance = sum([agr.subvention.fed_budget.subvention_performance or 0 for agr in query.all() if agr.subvention and agr.subvention.fed_budget])
    subvention_performance = reg_subvention_performance + fed_subvention_performance
    context.update({'subvention_performance': subvention_performance})

    # Кассовый расход по освоению субвенций
    spend_amount = sum([p.get("amount") or 0 for p in Payment.objects.filter(**payment_kwargs).values("amount")])
    context.update({'spend_amount': spend_amount})

    # Отношение сумм субвенций к кассовому расходу (%)
    if not sum_with_k:
        percent_of_sum_with_k_and_spend_amount = 0
    else:
        percent_of_sum_with_k_and_spend_amount = spend_amount / sum_with_k * 100
    context.update({'percent_of_sum_with_k_and_spend_amount': percent_of_sum_with_k_and_spend_amount})

    return render_to_response(template, context,
                              context_instance=RequestContext(request))



def get_questions_list(request):
    if not request.method == "POST":
        return HttpResponseNotFound("Not found")
    if not request.POST.get("mo"):
        return HttpResponseBadRequest("No mo name")
    context = {'title': u'Бланк опроса'}
    mo = MO.objects.filter(name=request.POST['mo'])[0]
    context['mo'] = mo
    form = QuestionsListForm(mo, request.POST)
    if not form.is_valid():
        request.session['wrong_post'] = request.POST.copy()
        return HttpResponseRedirect(reverse('questions-list-form'))

    context['responsible_person'] = request.POST.get('responsible_person')
    context['list_sent_to_mo'] = request.POST.get('list_sent_to_mo')
    context['objects_equal'] = request.POST.get('objects_equal')
    context['persons_list'] = []
    context['building_forms'] = []
    for p in request.POST.getlist('persons_list'):
        context['persons_list'].append(Person.objects.get(pk=p))

    # is there a building with payment perpective
    is_perspective = [p for p in Building.objects.all().values("payment_perspective" ,) if p.get("payment_perspective") != 2]
    context['perspective'] = 0
    if is_perspective:
        context['perspective'] = 1

    context['perspective_forms'] = []
    context['contract_cmp_data'] = []
    context['perspective_cmp_data'] = []
    # pass forms and formsts for perspective buildings to template via dicts in array
    for building in Building.objects.filter(mo=mo, payment_perspective=1):
        object_form = BuildingForm(instance=building)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=building)
        object_formsets = [room_f, hallway_f, wc_f, kitchen_f]
        context['perspective_forms'].append({object_form: object_formsets})
        # get only last cmp form for displaying
        if building.result_set:
            if building.result_set.order_by('cmp_data__cmp_date'):
                last_cmp = building.result_set.order_by('cmp_data__cmp_date')[0]
                last_cmp_form = ResultForm(instance=last_cmp)
                context['perspective_cmp_data'].append({building.pk: last_cmp_form})

    # auction always should be
    auction = Auction.objects.get(pk=request.POST['auction'])
    auction_form = AuctionForm(instance=auction)
    context["auction"] = auction
    context["auction_form"] = auction_form
    room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=auction)
    if auction.contract:
        contract = auction.contract
        contract_form = ContractForm(instance=contract)
        # pass forms and formsts for contract building to template via dicts in array
        for building in Building.objects.filter(contract=contract):
            object_form = BuildingForm(instance=building)
            room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=building)
            object_formsets = [room_f, hallway_f, wc_f, kitchen_f]
            context['building_forms'].append({object_form: object_formsets})
            print context['building_forms']
            # get only last cmp form for displaying
            if building.result_set:
                if building.result_set.order_by('cmp_data__cmp_date'):
                    last_cmp = building.result_set.order_by('cmp_data__cmp_date')[0]
                    last_cmp_form = ResultForm(instance=last_cmp)
                    context['contract_cmp_data'].append({building.pk: last_cmp_form})
        context["contract"] = contract
        context["contract_form"] = contract_form
        # room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=contract)

    #context.update({'formsets': [room_f, hallway_f, wc_f, kitchen_f],
    #                'titles': [
    #                    Room._meta.verbose_name,
    #                    Hallway._meta.verbose_name,
    #                    WC._meta.verbose_name,
    #                    Kitchen._meta.verbose_name,
    #                    ]})
    template = webodt.ODFTemplate('quest.odt')
    document = template.render(Context(context))
    conv = converter()
    rtf_file = conv.convert(document, format='rtf')
    document.close()
    response = StreamingHttpResponse(FileWrapper(rtf_file),
                                     content_type=mimetypes.guess_type(document.name)[0])
    response['Content-Disposition'] = 'attachment; filename=download.rtf'
    return response
