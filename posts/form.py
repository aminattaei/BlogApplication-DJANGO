from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری خود را وارد کنید...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل خود را وارد کنید...'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور خود را وارد کنید...'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تکرار رمز عبور'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={
                "placeholder": "نظر خود را بنویسید...",
                "rows": 4,
                "class": "form-control",  # کلاس Bootstrap برای استایل بهتر
            }),
        }

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=50, 
        min_length=10, 
        required=True, 
        label="نام شما",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "نام خود را وارد کنید...",
        })
    )
    message = forms.CharField(
        min_length=50, 
        required=True, 
        label="پیام شما",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "پیام خود را اینجا بنویسید...",
            "rows": 5
        })
    )
