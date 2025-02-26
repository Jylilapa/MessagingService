from django.urls import path
from django.views.decorators.cache import cache_page

from mailings.apps import MailingsConfig
from mailings.views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView, \
    AttemptListView

app_name = MailingsConfig.name

urlpatterns = [
    path("mailings/", MailingListView.as_view(), name="mailing_list"),
    path("mailings/<int:pk>/",cache_page(60)(MailingDetailView.as_view()), name="mailing_detail"),
    path("mailings/create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailings/<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailings/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("mailings/attempt/", AttemptListView.as_view(), name="attempt_list"),
]
