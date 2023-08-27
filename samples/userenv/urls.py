from django.urls import path

from . import views

app_name = 'userenv'


urlpatterns = [
    path("", view=views.accountsHomePage, name='useraccount'),
]