from django import forms

from .models import Mailing, Message, Client


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['message', 'clients']
        exclude = [
            "owner",
        ]
        widgets = {
            "clients": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # Получаем текущего пользователя
        super().__init__(*args, **kwargs)

        if user:
            # Фильтруем только те recipients, которые принадлежат текущему пользователю
            self.fields["clients"].queryset = Client.objects.filter(owner=user)
            self.fields["message"].queryset = Message.objects.filter(owner=user)
