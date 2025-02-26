from django.urls import path
from django.views.decorators.cache import cache_page

from recipients.apps import RecipientsConfig
from recipients.views import RecipientListView, RecipientDetailView, RecipientCreateView, RecipientUpdateView, \
    RecipientDeleteView, LetterDetailView, LetterListView, LetterCreateView, LetterUpdateView, LetterDeleteView

app_name = RecipientsConfig.name

urlpatterns = [
    path("", RecipientListView.as_view(), name="recipient_list"),
    path("recipients/<int:pk>/", cache_page(60)(RecipientDetailView.as_view()), name="recipient_detail"),
    path("recipients/create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("recipients/<int:pk>/update/", RecipientUpdateView.as_view(), name="recipient_update"),
    path("recipients/<int:pk>/delete/", RecipientDeleteView.as_view(), name="recipient_delete"),
    path("letter/", LetterListView.as_view(), name="letter_list"),
    path("letter/<int:pk>/", cache_page(60)(LetterDetailView.as_view()), name="letter_detail"),
    path("letter/create/", LetterCreateView.as_view(), name="letter_create"),
    path("letter/<int:pk>/update/", LetterUpdateView.as_view(), name="letter_update"),
    path("letter/<int:pk>/delete/", LetterDeleteView.as_view(), name="letter_delete"),
]
