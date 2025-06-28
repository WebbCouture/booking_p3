from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Home page (also shows bookings)
    path('', views.home, name='home'),

    # Create new booking
    path('new/', views.booking_create, name='booking_create'),

    # Edit booking
    path(
        '<int:pk>/edit/',
        views.booking_update,
        name='booking_update'
    ),

    # Delete booking
    path(
        '<int:pk>/delete/',
        views.booking_delete,
        name='booking_delete'
    ),

    # Tools
    path('tools/', views.tools_list, name='tools_list'),

    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # API
    path(
        'api/booked-dates/<int:tool_id>/',
        views.booked_dates_api,
        name='booked_dates_api'
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
