from django.urls import path
from main_app import views as main_app

app_name = "main_app"

urlpatterns = [
    path('', main_app.IndexView.as_view(), name='main'),

    path('applications/', main_app.ApplicationListView.as_view(),
         name='applications'),

    path('applications_add/', main_app.ApplicationCreateView.as_view(),
         name='applications_add'),

    path('applications_edit/<int:pk>/',
         main_app.ApplicationUpdateView.as_view(), name='applications_edit'),

    path('applications_delete/<int:pk>/',
         main_app.ApplicationDeleteView.as_view(), name='applications_delete'),
]
