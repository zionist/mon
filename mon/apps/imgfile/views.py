# -*- coding: utf-8 -*-
import webodt
import mimetypes
from webodt.converters import converter

from django.http import HttpResponse, StreamingHttpResponse, \
    HttpResponseNotFound, HttpResponseBadRequest
from django.core.servers.basehttp import FileWrapper
from django.template import Context
from django.shortcuts import render_to_response

from apps.build.models import Building
from apps.cmp.models import Contract, Result, CompareData, Auction, MO
from apps.cmp.forms import ContractForm, ResultForm, CompareDataForm
from apps.core.forms import RoomShowForm, HallwayShowForm, WCShowForm, \
    KitchenShowForm
from apps.build.forms import BuildingForm, BuildingShowForm
from apps.core.views import get_fk_forms, get_fk_show_forms, split_form
from apps.core.models import WC, Room, Hallway, Kitchen, Developer
from apps.core.views import get_fk_forms, get_fk_show_forms, get_fk_cmp_forms
from apps.imgfile.forms import QuestionsListForm, SelectMoForm
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist



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
    if not request.method == "POST":
        return HttpResponseNotFound("Not found")
    if not request.POST.get("mo"):
        return HttpResponseBadRequest("No mo")
    try:
        mo = MO.objects.get(pk=request.POST['mo'])
    except ObjectDoesNotExist:
        return HttpResponseNotFound("Not found")
    template = 'qet_questions_list_form.html'
    context = {'title': u'Создать форму опроса'}
    form = QuestionsListForm(mo=mo)
    context.update({'form': form})
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


def get_questions_list(request):
    if not request.method == "POST":
        return HttpResponseNotFound("Not found")
    print "#" * 100
    print request.POST
    print "#" * 100
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

    if request.POST.get("contract"):
        contract = Contract.objects.get(pk=request.POST['contract'])
        contract_form = BuildingForm(instance=contract)
        additions["contract"] = contract
        additions["contract-form"] = contract_form
        cmp_form = CompareDataForm(contract_form.initial)
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=contract)
    # return HttpResponse("Ok")

    print hallway_f

    context.update({'result': result, 'form': form, 'cmp_form': cmp_form,
                    'formsets': [room_f, hallway_f, wc_f, kitchen_f],
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
        contract_form = BuildingForm(instance=contract)
        additions["contract"] = contract
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
