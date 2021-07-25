from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from auth_app.forms import UserLoginForm, ClientAddForm
from auth_app.models import Client


class ClientListView(ListView):
    """Клиенты"""
    model = Client
    template_name = 'auth_app/clients.html'
    queryset = Client.objects.filter(is_active=True, is_worker=False)

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'клиенты'
        return context


class ClientCreateView(CreateView):
    """Добавление клиентов"""
    model = Client
    template_name = 'auth_app/add_client.html'
    form_class = ClientAddForm

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next_url = self.request.META.get('HTTP_REFERER')
        self.request.session['next_url'] = next_url
        context['title'] = 'добавление клиента'
        return context

    def form_valid(self, form):
        self.success_url = self.request.session['next_url']
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    """Изменение клиентов"""
    model = Client
    template_name = 'auth_app/edit_client.html'
    form_class = ClientAddForm

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next_url = self.request.META.get('HTTP_REFERER')
        self.request.session['next_url'] = next_url
        context['title'] = 'редактирование клиента'
        context['pk'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        self.success_url = self.request.session['next_url']
        return super().form_valid(form)


class ClientDeleteView(DeleteView):
    """Удаление клиентов"""
    model = Client
    template_name = 'auth_app/edit_client.html'

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
            self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next_url = self.request.META.get('HTTP_REFERER')
        self.request.session['next_url'] = next_url
        return context

    def get_success_url(self):
        self.success_url = self.request.session['next_url']
        return self.success_url


class WorkerListView(ListView):
    """Сотрудники"""
    model = Client
    template_name = 'auth_app/clients.html'
    queryset = Client.objects.filter(is_active=True, is_worker=True)

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'сотрудники'
        return context


class LogoutView(View):
    """Выход"""
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('auth:login'))


class LoginAuthView(LoginView):
    """Авторизация"""
    template_name = 'auth_app/login.html'
    form_class = UserLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'авторизация'
        return context

    def get_success_url(self):
        self.success_url = reverse('main:main')
        return self.success_url
