from django.urls import path

from . import views

app_name = 'admin_panel'


urlpatterns = [
    path("", view=views.adminHomePage, name='admin-home'),
    path('uploads/', views.fileManagerPage, name='file-manager'),
]