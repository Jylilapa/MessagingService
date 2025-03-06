from django.core.cache import cache

from config.settings import CACHE_ENABLED
from recipients.models import Recipient, Letter


def get_recipients_from_cache():
    if not CACHE_ENABLED:
        return Recipient.objects.all()
    key = "recipient_list"
    recipients = cache.get(key)
    if recipients is not None:
        return recipients
    recipients = Recipient.objects.all()
    cache.set(key, recipients)
    return recipients


def get_letters_from_cache():
    if not CACHE_ENABLED:
        return Letter.objects.all()
    key = "letter_list"
    letters = cache.get(key)
    if letters is not None:
        return letters
    letters = Letter.objects.all()
    cache.set(key, letters)
    return letters
