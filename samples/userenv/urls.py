from django.urls import path

from . import views

app_name = 'userenv'


urlpatterns = [
    path("", view=views.accountsHomePage, name='useraccount'),
    path('register-booking/', views.registerNewBooking, name='register-booking'),
    path('delete-request/<int:bookingId>/', views.cancelBooking, name='delete-request'),
    path('find-request-details/', views.fetchFullRequestDetails, name='full-request-details'),
    path('issue-payment-link/', views.issuePaymentLink, name='issue-link'),
]