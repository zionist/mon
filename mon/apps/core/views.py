# -*- coding: utf-8 -*-
import os
import xlwt
from copy import deepcopy

from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_list_or_404, \
    get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory, formset_factory, modelformset_factory
from django.core.urlresolvers import reverse
from django.forms import Form as CustomForm
from django.forms.fields import CharField
from django.forms.widgets import Textarea
from django.http.request import QueryDict
from django.conf import settings
from django.contrib.auth.decorators import permission_required, login_required
from django.core.servers.basehttp import FileWrapper
from apps.core.templatetags.extras import get_choice_or_value

from .forms import RoomForm, HallwayForm, WCForm, KitchenForm,\
    ResultRoomForm, ResultHallwayForm, ResultWCForm, ResultKitchenForm, \
    ResultRoomShowForm, ResultHallwayShowForm, ResultWCShowForm, ResultKitchenShowForm, \
    RoomShowForm, HallwayShowForm, WCShowForm, KitchenShowForm, \
    AuctionRoomForm, AuctionHallwayForm, AuctionWCForm, AuctionKitchenForm, \
    AuctionRoomShowForm, AuctionHallwayShowForm, AuctionWCShowForm, AuctionKitchenShowForm


def main(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")
    if request.user.is_staff:
        return redirect("mos")
    else:
        return redirect("change-mo", pk=request.user.customuser.mo.pk)


def generate_fonts_css(request):
    return render_to_response('fonts.css', locals(),
                              context_instance=RequestContext(request))


def get_fk_forms(parent=None, request=None, multi=None, result=None):
    room_p, hallway_p, wc_p, kitchen_p = 'room_build', 'hallway_build', 'wc_build', 'kitchen_build'
    forms = [RoomForm, HallwayForm, WCForm, KitchenForm] if not multi else [AuctionRoomForm, AuctionHallwayForm, AuctionWCForm, AuctionKitchenForm]
    if result:
        forms = [ResultRoomForm, ResultHallwayForm, ResultWCForm, ResultKitchenForm]
    if not parent:
        if request and request.method == "POST":
            room_f = forms[0](request.POST, request.FILES, prefix=room_p)
            hallway_f = forms[1](request.POST, request.FILES, prefix=hallway_p)
            wc_f = forms[2](request.POST, request.FILES, prefix=wc_p)
            kitchen_f = forms[3](request.POST, request.FILES, prefix=kitchen_p)
        else:
            room_f = forms[0](prefix=room_p)
            hallway_f = forms[1](prefix=hallway_p)
            wc_f = forms[2](prefix=wc_p)
            kitchen_f = forms[3](prefix=kitchen_p)
    else:
        if request and request.method == "POST":
            room_f = forms[0](request.POST, request.FILES, prefix=room_p, instance=parent.room)
            hallway_f = forms[1](request.POST, request.FILES, prefix=hallway_p, instance=parent.hallway)
            wc_f = forms[2](request.POST, request.FILES, prefix=wc_p, instance=parent.wc)
            kitchen_f = forms[3](request.POST, request.FILES, prefix=kitchen_p, instance=parent.kitchen)
        else:
            room_f = forms[0](prefix=room_p, instance=parent.room)
            hallway_f = forms[1](prefix=hallway_p, instance=parent.hallway)
            wc_f = forms[2](prefix=wc_p, instance=parent.wc)
            kitchen_f = forms[3](prefix=kitchen_p, instance=parent.kitchen)
    return [room_f, hallway_f, wc_f, kitchen_f]


def get_fk_show_forms(parent=None, multi=None, result=None):
    room_p, hallway_p, wc_p, kitchen_p = 'room_build', 'hallway_build', 'wc_build', 'kitchen_build'
    forms = [RoomShowForm, HallwayShowForm, WCShowForm, KitchenShowForm] if not multi \
        else [AuctionRoomShowForm, AuctionHallwayShowForm, AuctionWCShowForm, AuctionKitchenShowForm]
    if result:
        forms = [ResultRoomShowForm, ResultHallwayShowForm, ResultWCShowForm, ResultKitchenShowForm]
    room_f = forms[0](prefix=room_p, instance=parent.room)
    hallway_f = forms[1](prefix=hallway_p, instance=parent.hallway)
    wc_f = forms[2](prefix=wc_p, instance=parent.wc)
    kitchen_f = forms[3](prefix=kitchen_p, instance=parent.kitchen)
    return [room_f, hallway_f, wc_f, kitchen_f]


def get_fk_cmp_forms(parent=None, cmp=None, multi=None):
    room_p, hallway_p, wc_p, kitchen_p = 'room_cmp', 'hallway_cmp', 'wc_cmp', 'kitchen_cmp'
    forms = [RoomShowForm, HallwayShowForm, WCShowForm, KitchenShowForm] if not multi \
        else [AuctionRoomShowForm, AuctionHallwayShowForm, AuctionWCShowForm, AuctionKitchenShowForm]
    room_f = forms[0](prefix=room_p, instance=parent.room, cmp_initial=cmp.room)
    hallway_f = forms[1](prefix=hallway_p, instance=parent.hallway, cmp_initial=cmp.hallway)
    wc_f = forms[2](prefix=wc_p, instance=parent.wc, cmp_initial=cmp.wc)
    kitchen_f = forms[3](prefix=kitchen_p, instance=parent.kitchen, cmp_initial=cmp.kitchen)
    return [room_f, hallway_f, wc_f, kitchen_f]


def split_form(form):
    """
    move text_area fields to another form
    :param form: forms.Form object
    :return: two forms. First form without fields with Textarea widget
        and second form which contains fields with Textarea widget
    """
    if form.instance.id and not form.is_bound:
        text_area_form = CustomForm()
        text_area_form.is_bound = False
        text_area_form.prefix = form.prefix
        text_area_form.initial = QueryDict({}).copy()
        data = form.initial.copy()
        for k, v in form.fields.iteritems():
            if isinstance(v, CharField) and isinstance(v.widget, Textarea):
                text_area_form.fields.update({k: form.fields.pop(k)})
                if data.get(k):
                    text_area_form.initial.update({k: data.get(k)})
                    del data[k]
        form.data = data
        return (form, text_area_form)
    if form.is_bound:
        text_area_form = CustomForm()
        text_area_form.is_bound = True
        text_area_form.prefix = form.prefix
        text_area_form.data = QueryDict({}).copy()
        data = form.data.copy()
        for k, v in form.fields.iteritems():
            if isinstance(v, CharField) and isinstance(v.widget, Textarea):
                text_area_form.fields.update({k: form.fields.pop(k)})
                k = "%s-%s" % (form.prefix, k)
                if data.get(k):
                    text_area_form.data.update({k: data.get(k)})
                    del data[k]
        form.data = data
        return (form, text_area_form)
    else:
        text_area_form = CustomForm()
        for k, v in form.fields.iteritems():
            if isinstance(v, CharField) and isinstance(v.widget, Textarea):
                text_area_form.fields.update({k: form.fields.pop(k)})
        text_area_form.prefix = form.prefix
        return (form, text_area_form)


def set_fields_equal(form1, form2):
    """
    Leave only common fields in both forms
    :param form1:
    :param form2:
    :return: form1, form2
    """
    for name, field in form1.fields.items():
        if name not in form2.fields:
            form1.fields.pop(name)
    for name, field in form2.fields.items():
        if name not in form1.fields:
            form2.fields.pop(name)
    return form1, form2


@login_required
def download_file(request, name):
    if os.path.isfile(os.path.join(settings.MEDIA_ROOT, name)):
        name = os.path.join(settings.MEDIA_ROOT, name)
    wrapper = FileWrapper(file(name))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Length'] = os.path.getsize(name)
    return response


def copy_object(obj):
    new_obj = deepcopy(obj)
    new_obj.id = None
    new_obj.pk = None
    return new_obj

# object instance: form for display
def to_xls(request, objects={}, fk_forms=True, multi=False):
    # create
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('untitled')

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


    # object fields should be same as form fields
    # get all types of objects

    if fk_forms:
        room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(request=request, multi=multi)
        fk_forms = {u'Санузел': wc_f, u'Прихожая': hallway_f,
                    u'Кухня': kitchen_f, u'Комната': room_f}
    else:
        fk_forms = {}
    row = 0
    for form, objs in objects.iteritems():
        if not objs:
            continue
            # make headers
        header_form = form()
        col = 0
        for field in header_form:
            sheet.write(row, col, field.label if field.label else field.name,
                        style_bold)
            col += 1
        for fk_name, fk_form in fk_forms.iteritems():
            for field in fk_form:
                sheet.write(row, col, u"%s %s" % (fk_name, field.label)
                if field.label else u"%s %s" % (fk_name, field.name), style_bold)
                col += 1
            # write values
        row += 1
        for obj in objs:
            col = 0
            obj_form = form(instance=obj)
            for field in obj_form:
                value = obj_form.initial.get(field.name)
                if isinstance(value, bool) and value:
                    value = u"Да"
                elif isinstance(value, bool) and not value:
                    value = u"Нет"
                elif not value:
                    value = u''
                else:
                    value = u"%s" % get_choice_or_value(obj_form, field.name)
                sheet.write(row, col, value)
                col += 1

            # write fk forms values
            if fk_forms:
                room_f, hallway_f, wc_f, kitchen_f = get_fk_forms(parent=obj, multi=multi)
                fk_forms = {u'Санузел': wc_f, u'Прихожая': hallway_f,
                            u'Кухня': kitchen_f, u'Комната': room_f}
            for fk_name, fk_form in fk_forms.iteritems():
                for field in fk_form:
                    value = fk_form.initial.get(field.name)
                    if isinstance(value, bool) and value:
                        value = u"Да"
                    elif isinstance(value, bool) and not value:
                        value = u"Нет"
                    elif not value:
                        value = u''
                    else:
                        value = u"%s" % get_choice_or_value(fk_form,
                                                            field.name)
                    sheet.write(row, col, value)
                    col += 1
            row += 1

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=list.xls'
    book.save(response)
    return response


