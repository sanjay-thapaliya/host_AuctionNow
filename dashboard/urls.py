from django.urls import path

from dashboard.views import dashboard_home

urlpatterns = [
    path('dashboard/', dashboard_home, name='dashboard')
]