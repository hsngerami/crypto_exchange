from django.urls import path

from apps.accounts.apis.login import LoginAPI

urlpatterns = [
    path('login', LoginAPI.as_view(), name='login'),
]