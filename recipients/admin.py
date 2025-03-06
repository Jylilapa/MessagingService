from django.contrib import admin

from recipients.models import Recipient, Letter


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "owner")
    search_fields = ("email", "first_name", "last_name")


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ("subject", "message", "owner")
    search_fields = ("subject",)
