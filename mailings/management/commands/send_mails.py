from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from mailings.models import Mailing, Attempt

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        mailings = get_object_or_404(Mailing)
        for mailing in mailings:
            for recipient in mailing.recipients.all():
                try:
                    mailing.status = "started"
                    send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.message,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[recipient.email],
                        fail_silently=False,
                    )
                    Attempt.objects.create(
                        attempt_mailing=timezone.now(),
                        status="status_ok",
                        response="Email отправлен",
                        mailing=mailing,
                    )
                    print(
                        f"Сообщение {mailing.message.subject} успешно отправлено на  {recipient.email}"
                    )
                except Exception as e:
                    Attempt.objects.create(
                        attempt_mailing=timezone.now(),
                        status="status_not",
                        response=str(e),
                        mailing=mailing,
                    )
                    print(str(e))
            mailing.save()
