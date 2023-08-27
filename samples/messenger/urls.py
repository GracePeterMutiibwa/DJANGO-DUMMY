from django.urls import path

from . import views

app_name = 'messenger'

urlpatterns = [
    path('', views.websiteHomePage, name='welcome'),
    path('login/', views.homePage, name='home'),
    path('signup/', views.registerPage, name='register'),
    path('about-us/', views.aboutPage, name='about'),
    path('venues/', views.venuePage, name='venue'),
    path('restaurant/', views.restaurantPage, name='restaurant'),
    path('blog/', views.blogPostPage, name='blog'),
    path('contact/', views.contactPage, name='contact'),
    path('logout/', views.logoutUser, name='logout-user'),
    
    
]