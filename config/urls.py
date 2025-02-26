from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("mailings.urls", "mailings")),
    path("", include("recipients.urls", "recipients")),
    path("users/", include("users.urls", "users"))
]
