# -*- coding: utf-8 -*-

from datetime import datetime
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


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            request.session.delete_test_cookie()
            return HttpResponseRedirect(request.GET.get('next', reverse('main')))
    else:
        form = AuthenticationForm(request)
    request.session.set_test_cookie()
    return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def main(request):
    if not request.user.is_authenticated():
        return login(request)
    context = {'title': _(u'Мониторинг')}
    return render(request, 'base_site.html', context)


