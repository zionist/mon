# -*- coding: utf-8 -*-
import webodt
import mimetypes
from webodt.converters import converter

from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.template import Context

from apps.build.models import Building
from apps.build.forms import BuildingForm, BuildingShowForm
from apps.core.views import get_fk_forms, get_fk_show_forms, split_form
from apps.core.models import WC, Room, Hallway, Kitchen, Developer


def get_questions_list(request, pk):
    context = {'title': u'Опросник'}
    build = Building.objects.get(pk=pk)
    form = BuildingForm(instance=build)
    room_f, hallway_f, wc_f, kitchen_f = get_fk_show_forms(parent=build)
    context.update({'object': build, 'form': form,
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
    response = HttpResponse(FileWrapper(rtf_file),
                            content_type=mimetypes.guess_type(document.name)[0])
    response['Content-Disposition'] = 'attachment; filename=download.rtf'
    return response
