from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Post, Subscription
from .email_utils import send_new_post_notification
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Post)
def notify_subscribers_of_new_post(sender, instance, created, **kwargs):
    """Send email notifications when a new post is created."""
    if created and settings.ENABLE_EMAIL_NOTIFICATIONS:
        try:
            subscribers = Subscription.objects.all()
            if subscribers.exists():
                logger.info(
                    f"Sending notifications for new post '{instance.title}' to {subscribers.count()} subscribers"
                )
                success, failed = send_new_post_notification(instance, subscribers)
                logger.info(
                    f"New post notification stats: {success} sent successfully, {failed} failed"
                )
            else:
                logger.info("No subscribers to notify about new post")
        except Exception as e:
            logger.error(f"Error sending post notifications: {str(e)}")
