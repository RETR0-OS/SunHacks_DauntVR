from django.urls import path, include
from .views import api_login, web_login, web_register

urlpatterns = [
    path('login', api_login, name="api_login"),
    path('web/login', web_login, name="web_login"),
    path('web/register', web_register, name="web_register")
]
