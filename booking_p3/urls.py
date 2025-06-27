from django.contrib import admin
from django.urls import path, include
from bookings import views  # import views for home, login, logout, register
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home page at root URL
    path('', views.home, name='home'),

    # Bookings app URLs
    path('bookings/', include('bookings.urls')),

    # Authentication URLs
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('accounts/register/', views.register, name='register'),
]

# ✅ Serve media files (tool images) locally during development
# ❗️ Heroku doesn't support local media – use S3 or Cloudinary in production
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
