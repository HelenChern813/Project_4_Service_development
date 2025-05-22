from django.conf import settings
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import DetailView

from sending_messages.models import MailingStatus
from users.forms import CustomUserCreationForm
from users.models import CustomUser


class RegisterView(CreateView):
    model = CustomUser
    template_name = "register.html"
    success_url = reverse_lazy("sending_messages:message_list")
    form_class = CustomUserCreationForm


class UsersReportView(DetailView):
    '''отчет о рассылках'''

    model = CustomUser
    template_name = "report_detail.html"

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        user = self.object
        true_status = MailingStatus.objects.filter(mailing__owner=user, status=True).count()
        false_status = MailingStatus.objects.filter(mailing__owner=user, status=False).count()
        count_mailing = true_status + false_status
        contex['True'] = true_status
        contex['False'] = false_status
        contex['count'] = count_mailing
        return contex


class PasswordResetUserView(PasswordResetView):
    '''Восстановление пароля'''

    template_name = 'reset_password.html'
    email_template_name = 'password_reset_email.html'
    from_email = settings.DEFAULT_FROM_EMAIL
    success_url = reverse_lazy("users:password_reset_done")
    subject_template_name = 'password_reset_subject.txt'
