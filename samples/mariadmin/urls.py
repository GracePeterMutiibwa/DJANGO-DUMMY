from django.urls import path

from . import views

app_name = 'admin_panel'


urlpatterns = [
    path("", view=views.adminHomePage, name='admin-home'),
]