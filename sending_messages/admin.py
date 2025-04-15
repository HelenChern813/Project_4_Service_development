from django.contrib import admin
from .models import Client, Message, Mailing, MailingStatus


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        'full_name',
        'comment',
        'owner'
    )
    list_filter = ("id", "email")
    search_fields = ("email",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "theme", "body_message", "owner")
    list_filter = ("theme",)
    search_fields = (
        "theme",
    )


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "start_sending", "owner")
    list_filter = ("status",)
    search_fields = (
        "start_sending",
    )


@admin.register(MailingStatus)
class MailingStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "mail_server_response")
    list_filter = ("status",)
