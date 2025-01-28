from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django import forms
from .models import CustomUser

from .forms import CustomUserChangeForm,CustomUserCreationForm
class RegisterUserAccount(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy(
        "ShopPage:home-page"
    )  # بعد از ثبت‌نام به صفحه خانه هدایت می‌شود.
    template_name = "registration/signup.html"

    def dispatch(self, request, *args, **kwargs):
        # اگر کاربر وارد حسابی شده است، او را خارج می‌کنیم
        if request.user.is_authenticated:
            logout(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # ثبت‌نام کاربر و ورود خودکار
        response = super().form_valid(form)
        user = form.save()  # ذخیره کاربر
        login(self.request, user)  # ورود خودکار
        return response


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

