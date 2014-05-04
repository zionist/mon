# -*- coding: utf-8 -*-
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
from apps.cmp.forms import ContractForm, ResultForm, CompareDataForm, \
    AuctionForm
from apps.core.forms import RoomShowForm, HallwayShowForm, WCShowForm, \
    KitchenShowForm
from apps.build.forms import BuildingForm, BuildingShowForm
from apps.core.views import get_fk_forms, get_fk_show_forms, split_form
from apps.core.models import WC, Room, Hallway, Kitchen, Developer
from apps.core.views import get_fk_forms, get_fk_show_forms, get_fk_cmp_forms
from apps.imgfile.forms import QuestionsListForm, SelectMoForm
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
