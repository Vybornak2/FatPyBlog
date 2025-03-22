from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Profile


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """Display user profile details."""

    model = Profile
    template_name = "core/profile_detail.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        """Get the logged in user's profile."""
        return self.request.user.profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Update user profile."""

    model = Profile
    fields = ["bio", "avatar"]
    template_name = "core/profile_form.html"
    success_url = reverse_lazy("profile-detail")

    def get_object(self, queryset=None):
        """Get the logged in user's profile."""
        return self.request.user.profile
