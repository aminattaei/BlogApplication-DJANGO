from django.urls import path
from .views import RegisterUserAccount, SignUpView


urlpatterns = [
    path("register/", RegisterUserAccount.as_view(), name="register"),
    path("add/", SignUpView.as_view(), name="signup"),
]
