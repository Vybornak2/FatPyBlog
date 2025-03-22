from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"


class Subscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["-subscribed_at"]
        verbose_name = "Email Subscription"
        verbose_name_plural = "Email Subscriptions"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=10, blank=True)
    
    def __str__(self):
        if self.title:
            return f"{self.title}. {self.user.username}'s Profile"
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile when a User is created"""
    if created:
        # Only create if UserProfile model table exists
        try:
            UserProfile.objects.create(user=instance)
        except Exception:
            # Handle the case where the table might not exist yet (during migrations)
            pass


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when User is saved"""
    try:
        # Check if profile exists before saving
        if hasattr(instance, 'profile'):
            instance.profile.save()
    except Exception:
        # Handle the case where the profile might not exist or table isn't created
        pass
