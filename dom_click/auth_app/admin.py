from django.contrib import admin

from auth_app.models import User, Client

admin.site.register(User)
admin.site.register(Client)
