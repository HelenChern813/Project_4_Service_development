from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from sending_messages.models import Mailing


class Command(BaseCommand):
    """Кастомная команда запуска рассылки"""

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int)

    def handle(self, *args, **kwargs):

        mailing_id = kwargs["mailing_id"]
        try:
            mailing = Mailing.objects.get(id=mailing_id)
            mailing.status = Mailing.RUNNING
            if mailing.start_sending is None:
                mailing.start_sending = timezone.now()
                mailing.save()
            message = mailing.message
            subject = message.theme
            body = message.body_message
            for client in mailing.clients.all():
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [client.email], fail_silently=False)

            mailing.status = Mailing.COMPLETED
            mailing.stop_sending = timezone.now()
            mailing.save()
            self.stdout.write(self.style.SUCCESS(f"Рассылка успешно отправлена"))
        except Mailing.DoesNotExist:
            self.stderr.write(self.style.ERROR("Рассылка не найдена."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Ошибка: {str(e)}"))
