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
    if request.method == 'GET':
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
    context.update({'form': form})
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


def get_questions_list(request):
    if not request.POST.get("mo"):
        return HttpResponseBadRequest("No mo name")
    mo = MO.objects.filter(name=request.POST['mo'])[0]
    if not request.method == "POST":
        return HttpResponseNotFound("Not found")
    form = QuestionsListForm(mo, request.POST)
    if not form.is_valid():
        context = {'form': form}
        request.session['wrong_post'] = request.POST.copy()
        return HttpResponseRedirect(reverse('questions-list-form'))
    #HttpResponse("Ok")

    data = {}
    context = {'title': u'Бланк опроса'}
    data['mo'] = mo
    data['responsible_person'] = request.POST.get('responsible_person')
    data['persons_list'] = []
    for p in request.POST.getlist('persons_list'):
        data['persons_list'].append(Person.objects.get(pk=p))


    # empty result
    result = Result()
    form = ResultForm()
    cmp_form = CompareDataForm()
    room_f = RoomShowForm()
    hallway_f = HallwayShowForm()
    wc_f = WCShowForm()
    kitchen_f = KitchenShowForm()


    # auction always should be
    if request.POST.get("auction") != u"0":
        auction = Auction.objects.get(pk=request.POST['auction'])
        auction_form = AuctionForm(instance=auction)
        context["auction"] = auction
        context["auction_form"] = auction_form
        print(auction_form.fields)
        cmp_form = CompareDataForm(auction_form.initial)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=auction)
    if auction.contract:
        contract = auction.contract
        contract_form = ContractForm(instance=contract)
        data["contract"] = contract
        data["contract-form"] = contract_form
        context["contract"] = contract
        context["contract_form"] = contract_form
        cmp_form = CompareDataForm(contract_form.initial)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=contract)

    context.update({'result': result, 'form': form, 'cmp_form': cmp_form,
                    'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                    'data': data,
                    # 'mo': request.POST.get('mo'),
                    'titles': [
                        Room._meta.verbose_name,
                        Hallway._meta.verbose_name,
                        WC._meta.verbose_name,
                        Kitchen._meta.verbose_name,
                        ]})
    template = webodt.ODFTemplate('quest.odt')
    document = template.render(Context(context))
    conv = converter()
    rtf_file = conv.convert(document, format='rtf')
    document.close()
    response = StreamingHttpResponse(FileWrapper(rtf_file),
                                     content_type=mimetypes.guess_type(document.name)[0])
    response['Content-Disposition'] = 'attachment; filename=download.rtf'
    return response


def get_questions_list_old(request):
    if not request.method == "GET":
        return HttpResponseNotFound("Not found")
    additions = {}
    context = {'title': u'Бланк опроса'}

    # empty result
    result = Result()
    form = ResultForm()
    cmp_form = CompareDataForm()
    room_f = RoomShowForm()
    hallway_f = HallwayShowForm()
    wc_f = WCShowForm()
    kitchen_f = KitchenShowForm()

    if request.GET.get("contract"):
        contract = Contract.objects.get(pk=request.GET['contract'])
        contract_form = ContractForm(instance=contract)
        context["contract"] = contract
        additions["contract-form"] = contract_form
        cmp_form = CompareDataForm(contract_form.initial)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=contract)
    elif request.GET.get("auction"):
        pass
    elif request.GET.get("building"):
        building = Building.objects.get(pk=request.GET['building'])
        building_form = BuildingForm(instance=building)
        additions["building"] = building
        additions["building-form"] = building_form
        cmp_form = CompareDataForm(building_form.initial)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=building)

    context.update({'result': result, 'form': form, 'cmp_form': cmp_form,
                   'formsets': [room_f, hallway_f, wc_f, kitchen_f],
                   'additions': additions,
                   'titles': [
                       Room._meta.verbose_name,
                       Hallway._meta.verbose_name,
                       WC._meta.verbose_name,
                       Kitchen._meta.verbose_name,
                       ]})
    template = webodt.ODFTemplate('quest.odt')
    document = template.render(Context(context))
    conv = converter()
    rtf_file = conv.convert(document, format='rtf')
    document.close()
    response = StreamingHttpResponse(FileWrapper(rtf_file),
                                     content_type=mimetypes.guess_type(document.name)[0])
    response['Content-Disposition'] = 'attachment; filename=download.rtf'
    return response
