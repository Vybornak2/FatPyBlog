from django import forms
from .models import Post, Subscription


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]


class SubscriptionForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email address",
                "required": True,
                "aria-label": "Email address for subscription",
            }
        )
    )

    class Meta:
        model = Subscription
        fields = ["email"]
