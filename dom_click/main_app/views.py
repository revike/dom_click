from datetime import datetime

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView, UpdateView, \
    DeleteView, ListView

from main_app.forms import ApplicationAddForm
from main_app.models import Application


class IndexView(TemplateView):
    """Главная страница"""
    template_name = 'main_app/index.html'

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'главная страница'
        return context


class ApplicationListView(ListView):
    """Заявки - список"""
    model = Application
    template_name = 'main_app/applications.html'

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = ApplicationAddForm(
            data=self.request.GET, use_required_attribute=False)

        context['form'] = form
        context['title'] = 'заявки'
        context['date_gte'] = self.request.GET.get('date_gte')
        context['date_lte'] = self.request.GET.get('date_lte')
        return context

    def get_queryset(self):
        queryset = self.model.objects.filter(is_active=True)

        title = self.request.GET.get('title')
        if title:
            queryset = queryset.filter(title=title)

        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        date_gte = self.request.GET.get('date_gte')
        if date_gte:
            date__gte = datetime.strptime(date_gte, '%Y-%m-%d').date()
            queryset = queryset.filter(created__gte=date__gte)

        date_lte = self.request.GET.get('date_lte')
        if date_lte:
            date__lte = datetime.strptime(date_lte, '%Y-%m-%d').date()
            queryset = queryset.filter(created__lte=date__lte)

        return queryset


class ApplicationCreateView(CreateView):
    """Добавление заявки"""
    model = Application
    template_name = 'main_app/applications_add.html'
    form_class = ApplicationAddForm
    success_url = reverse_lazy('main:applications')

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'добавление заявки'
        return context


class ApplicationUpdateView(UpdateView):
    """Редактирование заявки"""
    model = Application
    template_name = 'main_app/edit_application.html'
    form_class = ApplicationAddForm
    success_url = reverse_lazy('main:applications')

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'редактирование заявки'
        context['pk'] = self.kwargs['pk']
        return context


class ApplicationDeleteView(DeleteView):
    """Удаление заявки"""
    model = Application
    template_name = 'main_app/edit_application.html'
    success_url = reverse_lazy('main:applications')

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
            self.object.save()
        return HttpResponseRedirect(self.get_success_url())
