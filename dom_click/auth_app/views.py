from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from auth_app.forms import UserLoginForm, ClientAddForm
from auth_app.models import Client


def client_edit(data, user):
    """Редактирование клиента в базе"""
    if data.get('is_worker'):
        user.update(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone_number=data.get('phone_number'),
            email=data.get('email'),
            is_worker=True
        )
    else:
        user.update(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone_number=data.get('phone_number'),
            email=data.get('email'),
            is_worker=False
        )


def clients(request):
    """Клиенты"""
    if request.user.is_staff:
        client = Client.objects.filter(is_active=True, is_worker=False)
        content = {
            'title': 'клиенты',
            'clients': client
        }
        return render(request, 'auth_app/clients.html', content)
    return HttpResponseRedirect(reverse('auth:login'))


@login_required
def clients_add(request):
    """Добавление клиентов"""
    form = ClientAddForm()
    if request.method == 'POST':
        form = ClientAddForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.session['next_url'])

    next_url = request.META.get('HTTP_REFERER')
    request.session['next_url'] = next_url

    content = {
        'title': 'добавление клиента',
        'form': form
    }

    return render(request, 'auth_app/add_client.html', content)


@login_required
def clients_edit(request, pk):
    """Изменение и удаление клиентов"""
    user = Client.objects.filter(id=pk, is_active=True, )
    form = ClientAddForm(instance=user.first())

    if request.method == 'POST':
        form = ClientAddForm(data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            if form.data.get('save'):
                client_edit(form.data, user)
            elif form.data.get('delete'):
                user.update(is_active=False)
            return HttpResponseRedirect(request.session['next_url'])

    next_url = request.META.get('HTTP_REFERER')
    request.session['next_url'] = next_url

    content = {
        'pk': pk,
        'user_delete': user.first(),
        'title': 'редактирование клиента',
        'form': form
    }

    return render(request, 'auth_app/edit_client.html', content)


def workers(request):
    """Сотрудники"""
    if request.user.is_staff:
        client = Client.objects.filter(is_active=True, is_worker=True)
        content = {
            'title': 'сотрудники',
            'clients': client
        }
        return render(request, 'auth_app/clients.html', content)
    return HttpResponseRedirect(reverse('auth:login'))


def login(request):
    """Авторизация"""
    login_form = UserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active and user.is_staff:
            auth.login(request, user)
        return HttpResponseRedirect(reverse('main:main'))

    content = {
        'title': 'авторизация',
        'login_form': login_form
    }

    return render(request, 'auth_app/login.html', content)


def logout(request):
    """Выход"""
    auth.logout(request)
    return HttpResponseRedirect(reverse('auth:login'))
