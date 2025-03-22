from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Post, Subscription, UserProfile, Tag
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter tags separated by commas (e.g., python, django, tutorial)",
            }
        ),
        label="Tags",
        help_text="Enter tags separated by commas",
    )

    class Meta:
        model = Post
        fields = ["title", "content", "tags_input"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter post title",
                    "required": True,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # If this is an existing post, populate tags_input with current tags
        if self.instance.pk:
            current_tags = self.instance.tags.all()
            if current_tags:
                self.fields["tags_input"].initial = ", ".join(
                    [tag.name for tag in current_tags]
                )

    def save(self, commit=True):
        post = super().save(commit=False)

        # Set author if provided and not already set
        if self.user and not post.author:
            post.author = self.user

        if commit:
            post.save()

            # Handle tags
            self.instance.tags.clear()  # Remove existing tags
            tags_input = self.cleaned_data.get("tags_input", "")

            if tags_input:
                tag_names = [
                    tag.strip() for tag in tags_input.split(",") if tag.strip()
                ]

                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name.lower())
                    self.instance.tags.add(tag)

        return post


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


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
                "required": True,
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "required": True,
            }
        )
    )


class RegisterForm(UserCreationForm):
    TITLE_CHOICES = [
        ("", "Select a title"),
        ("mr", "Mr."),
        ("mrs", "Mrs."),
        ("ms", "Ms."),
        ("miss", "Miss"),
        ("dr", "Dr."),
        ("prof", "Prof."),
        ("other", "Other"),
    ]

    title = forms.ChoiceField(
        choices=TITLE_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "required": False,
            }
        ),
    )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "First Name",
                "required": True,
            }
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Last Name",
                "required": True,
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email address",
                "required": True,
            }
        )
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
                "required": True,
            }
        )
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "required": True,
            }
        ),
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm Password",
                "required": True,
            }
        ),
    )

    subscribe = forms.BooleanField(
        required=False,
        initial=True,
        label="Subscribe to newsletter",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = User
        fields = [
            "title",
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

            # Save title to UserProfile
            if hasattr(user, "profile"):
                user.profile.title = self.cleaned_data.get("title", "")
                user.profile.name = f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}"
                user.profile.save()

        return user


class ProfileForm(forms.ModelForm):
    TITLE_CHOICES = [
        ("", "Select a title"),
        ("mr", "Mr."),
        ("mrs", "Mrs."),
        ("ms", "Ms."),
        ("miss", "Miss"),
        ("dr", "Dr."),
        ("prof", "Prof."),
        ("other", "Other"),
    ]

    title = forms.ChoiceField(
        choices=TITLE_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "required": False,
            }
        ),
    )

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "First Name",
                "required": True,
            }
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Last Name",
                "required": True,
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email",
                "required": True,
            }
        )
    )

    class Meta:
        model = UserProfile
        fields = ["title", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["email"].initial = self.user.email
            self.fields["first_name"].initial = self.user.first_name
            self.fields["last_name"].initial = self.user.last_name
            # Set name fields from the user model

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            # Update user email and name fields
            self.user.email = self.cleaned_data["email"]
            self.user.first_name = self.cleaned_data["first_name"]
            self.user.last_name = self.cleaned_data["last_name"]

            # Update profile
            profile.title = self.cleaned_data.get("title", "")
            profile.name = (
                f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}"
            )

            if commit:
                self.user.save()
                profile.save()
        return profile
