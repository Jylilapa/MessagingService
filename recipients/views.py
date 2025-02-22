from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from recipients.forms import RecipientsForm, LetterForm
from recipients.models import Recipient, Letter


class RecipientListView(ListView):
    model = Recipient


class RecipientDetailView(DetailView):
    model = Recipient
    template_name = "recipients/recipient_detail.html"


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientsForm
    template_name = "recipients/recipient_form.html"
    success_url = reverse_lazy("recipients:recipient_list")


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientsForm
    template_name = "recipients/recipient_form.html"
    success_url = reverse_lazy("recipients:recipient_list")


class RecipientDeleteView(DeleteView):
    model = Recipient
    success_url = reverse_lazy("recipients:recipient_list")


class LetterListView(ListView):
    model = Letter
    template_name = "recipients/letter_list.html"


class LetterDetailView(DetailView):
    model = Letter
    template_name = "recipients/letter_detail.html"


class LetterCreateView(CreateView):
    model = Letter
    form_class = LetterForm
    template_name = "recipients/letter_form.html"
    success_url = reverse_lazy("recipients:letter_list")


class LetterUpdateView(UpdateView):
    model = Letter
    form_class = LetterForm
    template_name = "recipients/letter_form.html"
    success_url = reverse_lazy("recipients:letter_list")


class LetterDeleteView(DeleteView):
    model = Letter
    success_url = reverse_lazy("recipients:letter_list")