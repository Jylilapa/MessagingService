from django.db import models


class Recipient(models.Model):
    email = models.CharField(max_length=50, unique=True, verbose_name="Адрес электронной почты")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    comments = models.TextField(null=True, blank=True, verbose_name="Комментарии")

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["email"]

    def __str__(self):
        return self.email


class Letter(models.Model):
    subject = models.CharField(max_length=200, verbose_name="Тема письма")
    message = models.TextField(verbose_name="Тело письма")

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"
        ordering = ["subject"]

    def __str__(self):
        return self.subject

