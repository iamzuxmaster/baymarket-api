from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from control import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/mobile/", include('mobile.urls')),
    path("control/", include("control.urls")),
    path("moderators/", include("moderators.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
