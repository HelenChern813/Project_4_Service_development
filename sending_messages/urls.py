from django.urls import path
from django.views.generic import TemplateView
from sending_messages.apps import SendingMessagesConfig
from sending_messages.views import base_view

app_name = SendingMessagesConfig.name

urlpatterns = [
    path('base/', base_view, name='base'),
]
