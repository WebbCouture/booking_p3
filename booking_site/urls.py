from django.contrib import admin
from django.urls import path, include
from bookings import views  # import views for home, login, logout, register

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home page at root URL, shows bookings
    path('', views.home, name='home'),

    # Bookings app URLs
    path('bookings/', include('bookings.urls')),

    # Authentication URLs under /accounts/
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('accounts/register/', views.register, name='register'),
]

# Serve media files during development
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
