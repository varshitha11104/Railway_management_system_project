# railway/urls.py
'''
from django.urls import path
from . import views
from .views import admin_dashboard

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('login/', views.login_view, name='login'),  # Login page
    path('register/', views.register, name='register'),  # Registration page
    path('train_list/', views.train_list, name='train_list'),  # Train list page
    path('booking_list/', views.booking_list, name='booking_list'),  # Booking list page for users
    path('booking_history/', views.booking_history, name='booking_history'),  # Booking history page
    path('raise_query/', views.raise_query, name='raise_query'),  # Raise a query form
    path('query_list/', views.query_list, name='query_list'),  # List of user queries
    path('logout/', views.logout_view, name='logout'),  # Logout page
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('accounts/login/', views.login_view, name='login'),  # Custom login view for accounts
]
'''
from django.urls import path
from . import views
from .views import (
    home, register, login_view, logout_view, raise_query, query_list, booking_view, booking_success
)
from .views import login_view  # Import the login_view function

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', login_view, name='login'),  # Login page
    path('logout/', logout_view, name='logout'),  # Logout page
    path('booking/', booking_view, name='booking'),  # Booking page
    path('raise_query/', raise_query, name='raise_query'),  # Raise a query form
    path('query_list/', query_list, name='query_list'),  # List of user queries
    #path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('submit_query/', views.submit_query, name='submit_query'),
    path('query_success/', views.query_success, name='query_success'),
    path('search/', views.search_trains, name='search_trains'),
    path('add/', views.add_train, name='add_train'),
    path('update/<int:train_id>/', views.update_train, name='update_train'),
    path('list/', views.list_trains, name='list_trains'),
    path('re_authenticate/', views.re_authenticate, name='re_authenticate'),
    path('admin_home_page/', views.admin_home_page, name='admin_home_page'),
    path('administration/login/', views.administration_login, name='administration_login'),
    path('passenger/login/', views.passenger_login, name='passenger_login'),
    path('support/login/', views.customer_support_login, name='customer_support_login'),
    path('profile/', views.profile, name='profile'),
    path('support/home/', views.support_home, name='support_home'),
    path('administration/home/', views.administration_home, name='administration_home'),
    path('logout/', views.logout_view, name='logout'),
    path('success/', views.booking_success, name='booking_success'),
    path('history/', views.user_booking_history, name='booking_history'),
    path('details/<int:booking_id>/', views.booking_details, name='booking_details'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('admin_home_page/all_bookings/', views.all_bookings, name='all_bookings'),
    path('queries/', views.view_queries, name='view_queries'),
    path('solve_query/<int:query_id>/', views.solve_query, name='solve_query'),
    path('user_queries/', views.user_queries, name='user_queries'),
    #path('payment/', views.payment_view, name='payment'),  # Payment page (optional, if you want a dedicated payment page)
    path('ticket/<str:reference_number>/', views.ticket_view, name='ticket_view'),  # Display ticket details after successful booking and payment
  #  path('payment/<int:booking_id>/', views.payment_view, name='payment_page'),
    #path('payment/', views.payment_view, name='payment'), 
    path('ticket/<str:reference_number>/', views.ticket_view, name='ticket_view'), 
    path('payment/<int:booking_id>/', views.payment_view, name='payment_view'),
    path('payment-success/<int:booking_id>/', views.payment_success, name='payment_success'),# Correct path for ticket view

    path('find-trains/', views.find_trains, name='find_trains'),
    path('booking/', views.booking_view, name='booking_view'),
]

