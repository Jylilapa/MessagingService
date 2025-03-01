from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from mailings.models import Mailing, Attempt
from mailings.services import send_mailings


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        send_mailings()
