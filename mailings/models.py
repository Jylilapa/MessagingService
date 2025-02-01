from django.db import models
from django.db.models import SET_NULL

from recipients.models import Letter, Recipient


class Mailing(models.Model):
    first_sent = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время первой отправки")
    end_sent = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время окончания отправки")
    status = models.CharField(max_length=20, verbose_name="Статус отправки")
    message = models.ForeignKey(Letter, on_delete=SET_NULL, null=True, blank=True, verbose_name="Сообщение")
    recipients = models.ManyToManyField(Recipient, verbose_name="Получатели")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["status"]

    def __str__(self):
        return self.status


class Attempt(models.Model):
    attempt_mailing = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    status = models.BooleanField(verbose_name="Статус")
    response = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(Mailing, on_delete=SET_NULL, verbose_name="Рассылка")

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"
        ordering = ["status"]

    def __str__(self):
        return self.status
