from django.urls import path
from main_app.views import main, applications, applications_add, \
    applications_edit

app_name = "main_app"

urlpatterns = [
    path('', main, name='main'),
    path('applications/', applications, name='applications'),
    path('applications_add/', applications_add, name='applications_add'),
    path('applications_edit/<int:pk>', applications_edit, name='applications_edit'),
]
