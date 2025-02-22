from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from mailings.models import Mailing, Attempt


class MailingListView(ListView):
    model = Mailing
    template_name = "mailings/mailing_list.html"


class MailingDetailView(DetailView):
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


class MailingCreateView(CreateView):
    model = Mailing
    template_name = "mailings/mailing_form.html"


class MailingUpdateView(UpdateView):
    model = Mailing
    template_name = "mailings/mailing_form.html"


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailings/mailing_confirm_delete.html"
