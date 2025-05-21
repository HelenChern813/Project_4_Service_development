from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import MailingForm
from .models import Client, Mailing, Message


class ClientCreateView(CreateView):
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "client_form.html"
    success_url = reverse_lazy("sending_messages:client_list")

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientListView(ListView):
    model = Client
    template_name = "client_list.html"
    context_object_name = "clients"


class ClientDetailView(DetailView):
    model = Client
    template_name = "client_detail.html"
    context_object_name = "client"


class ClientUpdateView(UpdateView):
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "client_form.html"
    success_url = reverse_lazy("sending_messages:client_list")


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "client_confirm_delete.html"
    success_url = reverse_lazy("sending_messages:client_list")


class MessageCreateView(CreateView):
    model = Message
    fields = ["theme", "body_message"]
    template_name = "message_form.html"
    success_url = reverse_lazy("sending_messages:message_list")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageListView(ListView):
    model = Message
    template_name = "message_list.html"
    context_object_name = "messages"


class MessageDetailView(DetailView):
    model = Message
    template_name = "message_detail.html"
    context_object_name = "message"


class MessageUpdateView(UpdateView):
    model = Message
    fields = ["theme", "body_message"]
    template_name = "message_form.html"
    success_url = reverse_lazy("sending_messages:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "message_confirm_delete.html"
    success_url = reverse_lazy("sending_messages:message_list")


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing_form.html"
    success_url = reverse_lazy("sending_messages:mailing_list")

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # Передаем текущего пользователя
        return kwargs


class MailingListView(ListView):
    model = Mailing
    template_name = "mailing_list.html"
    context_object_name = "mailings"


class MailingDetailView(DetailView):
    model = Mailing
    template_name = "mailing_detail.html"
    context_object_name = "mailing"


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing_form.html"
    success_url = reverse_lazy("sending_messages:mailing_list")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailing_confirm_delete.html"
    success_url = reverse_lazy("sending_messages:mailing_list")
