from django.urls import reverse_lazy
from django.views.generic.edit import FormView


class RegisterView(FormView):
    template_name = "register.html"
    success_url = reverse_lazy("sending_messages:message_list")
