import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserModeratorForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение адреса электронной почты",
            message=f"Пройдите по ссылке для подтверждения адреса электронной почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/user_detail.html"


class UserListView(LoginRequiredMixin, ListView):
    model = User

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Менеджер").exists():
            return User.objects.all()
        return HttpResponseForbidden


class UserModeratorView(LoginRequiredMixin, View):
    model = User
    form_class = UserModeratorForm

    def post(self, request, pk):
        block_user = get_object_or_404(User, pk=pk)
        if not request.user.has_perm("users.can_block_user"):
            return HttpResponseForbidden("У вас нет прав для блокировки пользователя")

        else:
            block_user.is_active = False
            block_user.save()
            return redirect("users:user_list")
