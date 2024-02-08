from django.urls import path

from .views import account_detail


urlpatterns = [
    path('profile/', account_detail, name='account_detail'),
]
