from django.urls import path

from auth_app.views import clients, workers, login, logout, clients_add, \
    clients_edit

app_name = "auth_app"

urlpatterns = [
    path('clients/', clients, name='clients'),
    path('clients_add/', clients_add, name='clients_add'),
    path('clients_edit/<int:pk>', clients_edit, name='clients_edit'),
    path('workers/', workers, name='workers'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]
