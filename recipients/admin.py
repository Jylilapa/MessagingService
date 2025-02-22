from django.contrib import admin

from recipients.models import Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name")
    search_fields = ("email", "first_name", "last_name")
