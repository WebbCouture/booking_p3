from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),                             # Home page (also shows bookings)
    path('new/', views.booking_create, name='booking_create'),     # Create new booking
    path('<int:pk>/edit/', views.booking_update, name='booking_update'),  # Edit booking
    path('<int:pk>/delete/', views.booking_delete, name='booking_delete'),# Delete booking

    # Tools
     path('tools/', views.tools_list, name='tools_list'),

    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # API
    path('api/booked-dates/<int:tool_id>/', views.booked_dates_api, name='booked_dates_api'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
