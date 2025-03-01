from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone

from mailings.forms import MailingForm, MailingModeratorForm
from mailings.models import Mailing, Attempt
from mailings.services import get_mailings_from_cache, send_mailings


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailings/mailing_list.html"

    def get_queryset(self):
        return get_mailings_from_cache()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["count_mailing"] = Mailing.objects.count()
        context_data["active_mailings_count"] = Mailing.objects.filter(status="Запущена").count()
        return context_data


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailings/mailing_detail.html"


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def post(self, request, *args, **kwargs):
        send_mailings()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_form_class(self):
        user = self.request.owner
        if user == self.object.owner:
            return MailingForm
        raise PermissionDenied


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailings/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def get_form_class(self):
        user = self.request.owner
        if user == self.object.owner:
            return MailingForm
        raise PermissionDenied


class AttemptListView(LoginRequiredMixin, ListView):
    model = Attempt
    template_name = "mailings/attempt_list.html"


class MailingModeratorView(LoginRequiredMixin, View):
    model = Mailing
    form_class = MailingModeratorForm

    def post(self, request, pk):
        block_mailing = get_object_or_404(Mailing, pk=pk)
        if not request.mailing.has_perm("mailings.can_stop_mailings"):
            return HttpResponseForbidden("У вас нет прав для блокировки рассылки")

        else:
            block_mailing.is_active = False
            block_mailing.save()
            return redirect("mailings:mailing_list")
