from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django import forms


from .forms import CustomUserCreationForm


class RegisterUserAccount(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("ShopPage:home-page")
    template_name = "registration/signup.html"

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            logout(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
