from django.contrib.auth.forms import AuthenticationForm
from django import forms

from auth_app.models import User, Client


class UserLoginForm(AuthenticationForm):
    """Форма для аутентификации"""

    class Meta:
        model = User
        fields = ('email', 'password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''


class ClientAddForm(forms.ModelForm):
    """Форма добавления клиентов"""

    class Meta:
        model = Client
        fields = (
            'first_name', 'last_name', 'phone_number', 'email', 'is_worker')

