from django.urls import path
from .views import FileUploadView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("upload/", FileUploadView.as_view(), name="file-upload"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
