from django import forms
from django.forms import Textarea

from auth_app.models import Client
from main_app.models import Application


class ApplicationAddForm(forms.ModelForm):
    """Форма добавления заявки"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['worker'].queryset = Client.objects.filter(is_worker=True)

    class Meta:
        model = Application
        fields = ('client', 'worker', 'title', 'content', 'status')

        widgets = {
            'content': Textarea(),
        }
