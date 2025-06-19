from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),                             # Home page (also shows bookings)
    path('new/', views.booking_create, name='booking_create'),     # Create new booking
    path('<int:pk>/edit/', views.booking_update, name='booking_update'),  # Edit booking
    path('<int:pk>/delete/', views.booking_delete, name='booking_delete'),# Delete booking

    # Tools
    path('tools/', views.tool_list, name='tool_list'),

    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # API
    path('api/booked-dates/<int:tool_id>/', views.booked_dates_api, name='booked_dates_api'),
]
