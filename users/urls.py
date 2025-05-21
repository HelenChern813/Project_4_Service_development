from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig

from .views import RegisterView

app_name = UsersConfig.name

urlpatterns = [
    path("", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="sending_messages:client_list"), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
]
