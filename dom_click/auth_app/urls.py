from django.urls import path

from auth_app import views as auth_app

app_name = "auth_app"

urlpatterns = [
    path('clients/', auth_app.ClientListView.as_view(), name='clients'),
    path('clients_add/', auth_app.ClientCreateView.as_view(),
         name='clients_add'),
    path('clients_edit/<int:pk>/', auth_app.ClientUpdateView.as_view(),
         name='clients_edit'),
    path('clients_delete/<int:pk>/', auth_app.ClientDeleteView.as_view(),
         name='clients_delete'),
    path('workers/', auth_app.WorkerListView.as_view(), name='workers'),
    path('login/', auth_app.LoginAuthView.as_view(), name='login'),
    path('logout/', auth_app.LogoutView.as_view(), name='logout'),
]
