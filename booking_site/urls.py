from django.contrib import admin
from django.urls import path, include
from bookings import views  # Import views for home, login, logout, register

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),  # Home page at root URL

    path('bookings/', include('bookings.urls')),  # Bookings app URLs

    # Authentication URLs grouped under /accounts/
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('accounts/register/', views.register, name='register'),
]

# Serve media files during development
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
