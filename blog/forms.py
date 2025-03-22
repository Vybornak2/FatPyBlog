from django import forms
from .models import Post, Subscription


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter post title",
                    "required": True,
                }
            ),
        }


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

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            email = email.lower()
            if Subscription.objects.filter(email=email).exists():
                raise forms.ValidationError("This email is already subscribed.")
        return email
