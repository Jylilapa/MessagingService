from django.db import models
from django.db.models import SET_NULL

from recipients.models import Letter, Recipient
from users.models import User


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    first_sent = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время первой отправки")
    end_sent = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время окончания отправки")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created', verbose_name="Статус отправки")
    message = models.ForeignKey(Letter, on_delete=SET_NULL, null=True, blank=True, verbose_name="Сообщение")
    recipients = models.ManyToManyField(Recipient, verbose_name="Получатели")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Владелец")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["status"]
        permissions = [
            ("can_view_list_mailings", "Can view list mailings"),
        ]

    def __str__(self):
        return self.status


class Attempt(models.Model):
    STATUS_CHOICES = [
        ("status_ok", "Успешно"),
        ("status_not", "Не успешно"),
    ]

    attempt_mailing = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Статус")
    response = models.TextField(verbose_name="Ответ почтового сервера")
    mailing = models.ForeignKey(Mailing, on_delete=SET_NULL, null=True, blank=True, verbose_name="Рассылка")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Владелец")

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"
        ordering = ["status"]

    def __str__(self):
        return self.status
