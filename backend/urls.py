from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.serve_frontend_page, name="frontend-home"),
    path("support.html", views.serve_frontend_page, {"filename": "support.html"}, name="frontend-support"),
    path("<str:filename>", views.serve_frontend_file, name="frontend-file"),
    path("admin/", admin.site.urls),
    path("api/", include("portfolio.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
