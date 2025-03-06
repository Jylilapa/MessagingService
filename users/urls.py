from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, UserDetailView, UserListView, UserModeratorView

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("", UserListView.as_view(), name="user_list"),
    path("block/<int:pk>/", UserModeratorView.as_view(), name="user_moderator_form"),
]
