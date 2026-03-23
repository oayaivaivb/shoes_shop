from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

urlpatterns = [
    path('', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('auth/logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', include('shoes.urls')),
    path('admin/', admin.site.urls),
    # path('auth/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
