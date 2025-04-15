from django.db import models
from users.models import CustomUser
from datetime import datetime


class Client(models.Model):
    ''' Модель «Получатель рассылки» '''

    email = models.EmailField(unique=True, verbose_name='Email', help_text='Введите почту получателя')
    full_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Полное имя получателя',
                                 help_text='Введите полное имя получателя')
    comment = models.TextField(verbose_name='Комментарий', help_text='Введите комментарий о получателе', blank=True,
                               null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name="recipients_owner", verbose_name="Владелец")

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ['id', 'email']


class Message(models.Model):
    ''' Модель сообщений '''

    theme = models.CharField(max_length=100, verbose_name='Тема письма', help_text='Введите тему письма')
    body_message = models.TextField(verbose_name='Текст сообщений', help_text='Введите текст сообщения')
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages_owner",
        verbose_name="Владелец",
    )

    def __str__(self):
        return f'{self.body_message}'

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['id', 'theme']


class Mailing(models.Model):
    ''' Модель рассылки сообщений'''

    COMPLETED = "completed"
    CREATED = "created"
    RUNNING = "running"

    STATUS_CHOICES = [
        (COMPLETED, "Завершена"),
        (CREATED, "Создана"),
        (RUNNING, "Запущена"),
    ]

    start_sending = models.DateTimeField(
        default=datetime.now(),
        verbose_name="Дата и время первой отправки",
    )

    stop_sending = models.DateTimeField(
        default=datetime.now(),
        verbose_name="Дата и время окончания отправки",
    )

    status = models.CharField(
        max_length=9,
        choices=STATUS_CHOICES,
        default=CREATED,
        verbose_name="Статус автоматической рассылки",
    )

    message = models.ForeignKey(
        Message,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mailing",
        verbose_name="Сообщение",
    )

    clients = models.ManyToManyField(
        Client,
        related_name="mailing",
        verbose_name="Получатели",
    )

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mailing_owner",
        verbose_name="Владелец",
    )

    def __str__(self):
        topic = self.message.theme
        client = self.clients
        return f"Тема рассылки- {topic}, получатели: {client}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["id", ]
        permissions = [
            ("can_cancel_mailing", "Can cancel mailing"),
        ]


class MailingStatus(models.Model):
    """Модель «Попытка рассылки»"""

    attempted_at = models.DateTimeField(
        verbose_name="Дата и время попытки отправки",
    )

    status = models.BooleanField(default=False, verbose_name="Статус рассылки", help_text="Статус рассылки")

    mail_server_response = models.TextField(
        null=True,
        blank=True,
        verbose_name="Ответ почтового сервера",
    )

    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="Рассылка",
    )

    def __str__(self):
        return f"{self.pk} - {self.mailing}. Статус: {self.status}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = [
            "id",
        ]
