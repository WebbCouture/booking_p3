from django.contrib import admin
from django.urls import path, include
from bookings import views  # import views for login/logout/register and home

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.home, name='home'),  # <-- Add home page at root
    
    path('bookings/', include('bookings.urls')),  # <-- Move bookings URLs here
    
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),  # login
    path('accounts/logout/', views.CustomLogoutView.as_view(), name='logout'),  # logout
    path('accounts/register/', views.register, name='register'),  # registration
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
