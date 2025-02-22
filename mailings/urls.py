from django.urls import path
from mailings.apps import MailingsConfig
from mailings.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView

app_name = MailingsConfig.name

urlpatterns = [
    path("mailings/", MailingListView.as_view(), name="mailing_list"),
    path("mailings/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailings/create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailings/<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailings/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"),
]
