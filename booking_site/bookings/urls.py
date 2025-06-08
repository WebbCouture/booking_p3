from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_list, name='booking_list'),  # root of bookings app
    path('new/', views.booking_create, name='booking_create'),
    path('<int:pk>/edit/', views.booking_update, name='booking_update'),
    path('<int:pk>/delete/', views.booking_delete, name='booking_delete'),
]