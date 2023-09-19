from django.urls import path

from . import views

app_name = 'admin_panel'


urlpatterns = [
    path("", view=views.adminHomePage, name='admin-home'),
    path('addcategory/', views.registerCategory, name='insert-category'),
    path('deletecategory/<int:categoryId>', views.deleteCategory, name='delete-category'),
]