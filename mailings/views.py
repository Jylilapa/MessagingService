from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from mailings.forms import MailingForm
from mailings.models import Mailing, Attempt
from mailings.services import get_mailings_from_cache


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailings/mailing_list.html"

    def get_queryset(self):
        return get_mailings_from_cache()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["count_mailing"] = Mailing.objects.count()
        context_data["active_mailings_count"] = Mailing.objects.filter(
            status="Запущена"
        ).count()
        return context_data


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailings/mailing_detail.html"

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        subject = self.object.message.letter.subject
        message = self.object.message.letter.message
        from_email = EMAIL_HOST_USER
        recipient_list = [recipient.email for recipient in self.object.recipients.all()]

        for recipient in recipient_list:
            try:
                send_mail(subject, message, from_email, [recipient])
                response = f"{subject} Успешно отправлено на {recipient.email}"
                Attempt.objects.create(attempt_mailing=timezone.now(), status="Успешно",
                                              response=response,
                                              mailing=self.object)
            except Exception as e:
                response = f"{recipient}: Ошибка: {e}"
                Attempt.objects.create(attempt_mailing=timezone.now(), status="Не отправлено",
                                              response=response,
                                              mailing=self.object)
        return redirect("mailings:mailing_list")


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        subject = self.object.message.letter.subject
        message = self.object.message.letter.message
        from_email = EMAIL_HOST_USER
        recipient_list = [recipient.email for recipient in self.object.recipients.all()]

        for recipient in recipient_list:
            try:
                send_mail(subject, message, from_email, [recipient])
                response = f"{subject} Успешно отправлено на {recipient.email}"
                Attempt.objects.create(attempt_mailing=timezone.now(), status="Успешно",
                                              response=response,
                                              mailing=self.object)
            except Exception as e:
                response = f"{recipient}: Ошибка: {e}"
                Attempt.objects.create(attempt_mailing=timezone.now(), status="Не отправлено",
                                              response=response,
                                              mailing=self.object)
        return redirect("mailings:mailing_list")


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
