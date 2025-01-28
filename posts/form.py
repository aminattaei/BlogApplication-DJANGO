# forms.py
from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={"placeholder": "نظر خود را بنویسید..."}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50, min_length=10, required=True)
    message = forms.CharField(
        min_length=50, required=True, widget=forms.Textarea
    )
