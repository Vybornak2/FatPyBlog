"""
URL Configuration for FatPyWeb project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    # Add user authentication URLs - make sure these come before blog urls
    path("accounts/", include("django.contrib.auth.urls")),
    # Blog URLs - ensure the namespace is properly included
    path("", include("blog.urls", namespace="blog")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
