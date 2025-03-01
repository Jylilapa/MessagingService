from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone

from config.settings import CACHE_ENABLED, EMAIL_HOST_USER
from mailings.models import Mailing, Attempt


def get_mailings_from_cache():
    if not CACHE_ENABLED:
        return Mailing.objects.all()
    key = "mailing_list"
    mailings = cache.get(key)
    if mailings is not None:
        return mailings
    mailings = Mailing.objects.all()
    cache.set(key, mailings)
    return mailings


def send_mailings():
    mailings = Mailing.objects.filter(status="started")
    for mailing in mailings:
        for recipient in mailing.recipients.all():
            try:
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
                print(f"Сообщение {mailing.message.subject} успешно отправлено на  {recipient.email}")
            except Exception as e:
                Attempt.objects.create(
                    attempt_mailing=timezone.now(),
                    status="status_not",
                    response=str(e),
                    mailing=mailing,
                )
                print(str(e))
