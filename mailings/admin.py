from django.contrib import admin

from mailings.models import Attempt, Mailing


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "message", "owner")
    search_fields = ("status", "message")


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "attempt_mailing", "status", "response", "mailing", "owner")
    search_fields = ("status", "mailing")
