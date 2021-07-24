from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from main_app.forms import ApplicationAddForm
from main_app.models import Application


def application_edit(data, application):
    """Редактирование заявки в базе"""
    application.update(
        client=data.get('client'),
        worker=data.get('worker'),
        title=data.get('title'),
        content=data.get('content'),
        status=data.get('status')
    )


def main(request):
    """Главная страница"""
    if request.user.is_staff:
        content = {
            'title': 'главная страница',
        }
        return render(request, 'main_app/index.html', content)
    return HttpResponseRedirect(reverse('auth:login'))


def applications(request):
    """Заявки - список"""
    if request.user.is_staff:
        form = ApplicationAddForm(request.POST, use_required_attribute=False)

        application = Application.objects.filter(
            is_active=True)

        content = {
            'title': 'заявки',
            'applications': application,
            'form': form
        }

        if request.method == 'POST':
            date_gte = request.POST.get('date_gte')
            if date_gte:
                date__gte = datetime.strptime(date_gte, '%Y-%m-%d').date()
                application = application.filter(created__gte=date__gte)

            date_lte = request.POST.get('date_lte')
            if date_lte:
                date__lte = datetime.strptime(date_lte, '%Y-%m-%d').date()
                application = application.filter(created__lte=date__lte)

            application = application.filter(
                title__contains=request.POST.get('title'),
                status__contains=request.POST.get('status'),
            )

            content['applications'] = application
            content['date_gte'] = date_gte
            content['date_lte'] = date_lte

            return render(request, 'main_app/applications.html', content)

        return render(request, 'main_app/applications.html', content)
    return HttpResponseRedirect(reverse('auth:login'))


@login_required
def applications_add(request):
    """Добавление заявки"""
    form = ApplicationAddForm()
    if request.method == 'POST':
        form = ApplicationAddForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('main:applications'))

    content = {
        'title': 'добавление заявки',
        'form': form
    }

    return render(request, 'main_app/applications_add.html', content)


@login_required
def applications_edit(request, pk):
    """Редактирование и удаление заявки"""
    application = Application.objects.filter(is_active=True, id=pk)
    form = ApplicationAddForm(instance=application.first())

    if request.method == 'POST':
        form = ApplicationAddForm(data=request.POST)
        if form.is_valid():
            form.save(commit=False)
            if form.data.get('save'):
                application_edit(form.data, application)
            elif form.data.get('delete'):
                application.update(is_active=False)
            return HttpResponseRedirect(request.session['next_url'])

    next_url = request.META.get('HTTP_REFERER')
    request.session['next_url'] = next_url

    content = {
        'pk': pk,
        'application': application.first(),
        'title': 'редактирование заявки',
        'form': form
    }

    return render(request, 'main_app/edit_application.html', content)
