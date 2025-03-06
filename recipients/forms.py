from django import forms
from django.db.models import BooleanField

from recipients.models import Recipient, Letter


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            else:
                fild.widget.attrs["class"] = "form-control"


class RecipientsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ["email", "first_name", "last_name", "comments"]


class LetterForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Letter
        fields = ["subject", "message"]
