from .import views
from django.urls import path, include
from .views import usersignup, userlogin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.contrib import admin



urlpatterns=[
    path("index/",views.index,name="index"),
    path("adminhome/",views.adminhome,name="adminhome"),
    path("adminlogin/",views.adminlogin,name="adminlogin"),
    path("adminlogout/",views.adminlogout,name="adminlogout"),
    path('adminchangepassword/', views.adminchangepassword, name='adminchangepassword'),
    path('usersignup/', views.usersignup, name='usersignup'),
    path('userlogin/', views.userlogin, name='userlogin'),
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='your_login_template.html'), name='login'),
    path('accounts/login/', LoginView.as_view(template_name='Autocareapp/userlogin.html'), name='login'),

    path('Autocareapp/userlogin/', views.userlogin, name='userlogin'),
    path('userlogout/', views.userlogout, name='userlogout'),
    path('userhomepage/', views.userhomepage, name='userhomepage'),
    path('services/', views.services, name='services'),

    path('about/', views.about, name='about'),
    path('adminvehicle/', views.adminvehicle, name='adminvehicle'), 

    path('vehicle/', views.my_vehicle, name='my_vehicle'),
    path('ad_vehicle/', views.ad_vehicle, name='ad_vehicle'),
    path('vehicle/edit/<int:vehicle_id>/', views.edit_vehicle, name='edit_vehicle'),
    path('vehicle/delete/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
    
    path('book_service/', views.book_service, name='book_service'),
    
     path('managebookings/', views.managebookings, name='managebookings'),
     path('accept_booking/<int:booking_id>/', views.accept_booking, name='accept_booking'),
     path('inprogress_booking/<int:booking_id>/', views.inprogress_booking, name='inprogress_booking'),
     path('complete_booking/<int:booking_id>/', views.complete_booking, name='complete_booking'),
     path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
     
     path('service_status/', views.service_status, name='service_status'),
     path('service_status_page/', views.service_status_page, name='service_status_page'),

    
    path('land/', views.land, name='land'),
    path('abouut/', views.abouut, name='abouut'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
]



