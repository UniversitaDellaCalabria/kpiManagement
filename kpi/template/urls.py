from django.urls import path
from .views import dashboard

app_name = 'template'

urlpatterns = [
    path('', dashboard, name='dashboard'),
]
