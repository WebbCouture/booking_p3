from django.contrib import admin
from django.urls import path, include
from bookings import views  # import views for login/logout/register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bookings.urls')),  # include app URLs
    
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),  # login
    path('accounts/logout/', views.CustomLogoutView.as_view(), name='logout'),  # logout
    path('accounts/register/', views.register, name='register'),  # registration
]
