import smtplib

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from sending_messages.models import Mailing, MailingStatus


def launch_mailing(mailing):
    mailing.status = Mailing.RUNNING
    if mailing.start_sending is None:
        mailing.start_sending = timezone.now()
        mailing.save()

    attempt = MailingStatus.objects.create(mailing=mailing)
    try:
        message = mailing.message
        subject = message.theme
        body = message.body_message
        for client in mailing.clients.all():
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [client.email], fail_silently=False)

        attempt.status = True
        mailing.status = Mailing.COMPLETED
    except smtplib.SMTPException as e:
        attempt.mail_server_response = f"Ошибка SMTP: {str(e)}"
    except Exception as e:
        attempt.mail_server_response = f"Системная ошибка: {str(e)}"
    finally:
        attempt.save()
        mailing.stop_sending = timezone.now()
        mailing.save()
