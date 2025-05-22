from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from users.models import CustomUser
from .forms import MailingForm
from .models import Client, Mailing, Message
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


class LaunchMailingView(View):

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, id=pk)
        launch_mailing(mailing)
        return redirect('sending_messages:mailing_list')


class HomePageView(DetailView):
    '''Главная страница'''
    model = CustomUser
    template_name = "home_page.html"

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)

        true_status = Mailing.objects.filter(status=Mailing.RUNNING).count()
        count_mailing = Mailing.objects.all().count()
        all_clients = Client.objects.all().count()

        contex['true_status'] = true_status
        contex['count_mailing'] = count_mailing
        contex['all_clients'] = all_clients
        return contex
