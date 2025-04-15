from django.urls import path
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    # path("", include("catalog.urls", namespace="catalog")),
    # path("blogs/", include("blogs.urls", namespace="blogs")),
    # path("users/", include("users.urls", namespace="users")),
]