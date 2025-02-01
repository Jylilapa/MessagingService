from django.urls import path
from recipients.apps import RecipientsConfig

app_name = RecipientsConfig.name

urlpatterns = [
    path("", ),
]
