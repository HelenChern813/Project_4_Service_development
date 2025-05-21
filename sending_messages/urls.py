from django.urls import path

from sending_messages.apps import SendingMessagesConfig
from sending_messages.views import (ClientCreateView, ClientDeleteView, ClientDetailView, ClientListView,
                                    ClientUpdateView, MailingCreateView, MailingDeleteView, MailingDetailView,
                                    MailingListView, MailingUpdateView, MessageCreateView, MessageDeleteView,
                                    MessageDetailView, MessageListView, MessageUpdateView)

app_name = SendingMessagesConfig.name

urlpatterns = [
    path("client_create/", ClientCreateView.as_view(), name="create_client"),
    path("client_list/", ClientListView.as_view(), name="client_list"),
    path("client_detail/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("client_edit/<int:pk>/", ClientUpdateView.as_view(), name="client_edit"),
    path("client_delete/<int:pk>/", ClientDeleteView.as_view(), name="client_delete"),
    path("message_create/", MessageCreateView.as_view(), name="message_client"),
    path("message_list/", MessageListView.as_view(), name="message_list"),
    path("message_detail/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("message_edit/<int:pk>/", MessageUpdateView.as_view(), name="message_edit"),
    path("message_delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"),
    path("mailing_create/", MailingCreateView.as_view(), name="mailing_client"),
    path("mailing_list/", MailingListView.as_view(), name="mailing_list"),
    path("mailing_detail/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailing_edit/<int:pk>/", MailingUpdateView.as_view(), name="mailing_edit"),
    path("mailing_delete/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"),
]
