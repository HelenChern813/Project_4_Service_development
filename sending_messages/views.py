from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import MailingForm
from .models import Client, Mailing, MailingStatus, Message
from .services import launch_mailing


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


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "client_list.html"
    context_object_name = "clients"


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "client_detail.html"
    context_object_name = "client"


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "client_form.html"
    success_url = reverse_lazy("sending_messages:client_list")


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "client_confirm_delete.html"
    success_url = reverse_lazy("sending_messages:client_list")


class MessageCreateView(LoginRequiredMixin, CreateView):
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


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "message_list.html"
    context_object_name = "messages"


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "message_detail.html"
    context_object_name = "message"


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ["theme", "body_message"]
    template_name = "message_form.html"
    success_url = reverse_lazy("sending_messages:message_list")


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "message_confirm_delete.html"
    success_url = reverse_lazy("sending_messages:message_list")


class MailingCreateView(LoginRequiredMixin, CreateView):
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


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailing_list.html"
    context_object_name = "mailing"


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailing_detail.html"
    context_object_name = "mailing"


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing_form.html"
    success_url = reverse_lazy("sending_messages:mailing_list")


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailing_confirm_delete.html"
    success_url = reverse_lazy("sending_messages:mailing_list")


class LaunchMailingView(LoginRequiredMixin, View):

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, id=pk)
        launch_mailing(mailing)
        return redirect("sending_messages:mailing_list")


class MailingStatusListView(LoginRequiredMixin, ListView):
    model = MailingStatus
    template_name = "mailing_status_detail.html"
    context_object_name = "status"
