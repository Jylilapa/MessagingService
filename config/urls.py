from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("mailings.urls", namespace="mailings")),
    path("", include("recipients.urls", namespace="recipients")),
]
