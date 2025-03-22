from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides
    self-updating created and modified fields.
    """

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        abstract = True


class Profile(TimeStampedModel):
    """User profile model."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.TextField(_("Biography"), blank=True)
    avatar = models.ImageField(_("Avatar"), upload_to="avatars/", blank=True, null=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return f"Profile for {self.user.username}"
