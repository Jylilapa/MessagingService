from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from recipients.forms import RecipientsForm, LetterForm
from recipients.models import Recipient, Letter
from recipients.services import get_recipients_from_cache, get_letters_from_cache


class RecipientListView(ListView):
    model = Recipient

    def get_queryset(self):
        return get_recipients_from_cache()


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = "recipients/recipient_detail.html"


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientsForm
    template_name = "recipients/recipient_form.html"
    success_url = reverse_lazy("recipients:recipient_list")

    def form_valid(self, form):
        recipient = form.save()
        user = self.request.user
        recipient.owner = user
        recipient.save()
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientsForm
    template_name = "recipients/recipient_form.html"
    success_url = reverse_lazy("recipients:recipient_list")

    def get_form_class(self):
        user = self.request.owner
        if user == self.object.owner:
            return RecipientsForm
        raise PermissionDenied


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy("recipients:recipient_list")


class LetterListView(LoginRequiredMixin, ListView):
    model = Letter
    template_name = "recipients/letter_list.html"

    def get_queryset(self):
        return get_letters_from_cache()


class LetterDetailView(LoginRequiredMixin, DetailView):
    model = Letter
    template_name = "recipients/letter_detail.html"


class LetterCreateView(LoginRequiredMixin, CreateView):
    model = Letter
    form_class = LetterForm
    template_name = "recipients/letter_form.html"
    success_url = reverse_lazy("recipients:letter_list")

    def form_valid(self, form):
        letter = form.save()
        user = self.request.user
        letter.owner = user
        letter.save()
        return super().form_valid(form)


class LetterUpdateView(LoginRequiredMixin, UpdateView):
    model = Letter
    form_class = LetterForm
    template_name = "recipients/letter_form.html"
    success_url = reverse_lazy("recipients:letter_list")

    def get_form_class(self):
        user = self.request.owner
        if user == self.object.owner:
            return LetterForm
        raise PermissionDenied


class LetterDeleteView(LoginRequiredMixin, DeleteView):
    model = Letter
    success_url = reverse_lazy("recipients:letter_list")