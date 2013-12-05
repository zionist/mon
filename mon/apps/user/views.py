# -*- coding: utf-8 -*-
from django.shortcuts import redirect, render, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import permission_required, \
    login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from .forms import UserCustomCreationForm, UserCustomChangeForm


@user_passes_test(lambda u: u.is_superuser)
def add_user(request):
    template = 'user_creation.html'
    context = {'title': _(u'Добавление пользователя')}
    if request.method == "POST":
        form = UserCustomCreationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            if form.cleaned_data.get('is_staff'):
                instance.is_staff = True
                instance.save(update_fields=['is_staff'])
            return redirect('users')
    else:
        form = UserCustomCreationForm()
    context.update({'form': form, })
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_superuser)
def update_user(request, pk):
    context = {'title': _(u'Редактирование пользователя')}
    user = User.objects.get(pk=pk)
    if request.method == "POST":
        form = UserCustomChangeForm(request.POST, instance=user)
        context.update({'object': user, 'form': form, })
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form = UserCustomChangeForm(instance=user)
    context.update({'object': user, 'form': form, })
    return render(request, 'user_updating.html', context,
                  context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_superuser)
def get_users(request):
    context = {'title': _(u'Пользователи')}
    objects = User.objects.all()
    page = request.GET.get('page', '1')
    paginator = Paginator(objects, 50)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    context.update({'user_list': objects})
    return render(request, 'users.html', context,
                  context_instance=RequestContext(request))


def pre_delete_user(request, pk):
    context = {'title': _(u'Удаление пользователя')}
    user =User.objects.get(pk=pk)
    context.update({'object': user})
    return render_to_response("user_deleting.html", context,
                              context_instance=RequestContext(request))


def delete_user(request, pk):
    context = {'title': _(u'Удаление пользователя')}
    user = User.objects.get(pk=pk)
    if user and 'delete' in request.POST:
        user.delete()
        return redirect('users')
    elif 'cancel' in request.POST:
        return redirect('users')
    else:
        context.update({'error': _(u'Возникла ошибка при удалении пользователя!')})
    return render_to_response("user_deleting.html", context,
                              context_instance=RequestContext(request))
