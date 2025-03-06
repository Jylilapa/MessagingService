from django import forms
from django.db.models import BooleanField

from mailings.models import Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            else:
                fild.widget.attrs["class"] = "form-control"


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["message", "recipients"]


class MailingModeratorForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Mailing
        fields = ["message", "owner"]
