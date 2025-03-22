from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from threading import Thread
import logging
import markdown
import re

logger = logging.getLogger(__name__)


# Add markdown processing function directly here to avoid circular import
def process_markdown_for_email(content):
    """Process markdown content with enhanced image handling for emails"""
    # First convert with standard extensions
    html_content = markdown.markdown(
        content, extensions=["fenced_code", "tables", "nl2br"]
    )

    # Post-process to ensure images have proper classes and attributes
    pattern = re.compile(r"<img([^>]*)>")

    def add_class_to_img(match):
        attributes = match.group(1)
        if "class=" in attributes:
            attributes = re.sub(
                r'class=(["\'])(.*?)(["\'])',
                r"class=\1\2 email-image\3",
                attributes,
            )
        else:
            attributes += ' class="email-image"'

        return f"<img{attributes}>"

    html_content = re.sub(pattern, add_class_to_img, html_content)
    return html_content


def send_async_email(email_message):
    """Send email in a separate thread to avoid blocking the request."""
    try:
        # Simple, compact debug output
        print(
            f"📧 SENDING EMAIL TO: {email_message.to} | SUBJECT: {email_message.subject}"
        )
        email_message.send()
        logger.info(f"Email sent successfully to {email_message.to}")
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")


def send_welcome_email(email):
    """Send welcome email to new subscribers."""
    subject = "Welcome to FatPyBlog Newsletter!"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = email

    # Create HTML content from template
    html_content = render_to_string(
        "blog/emails/welcome_email.html",
        {
            "site_name": "FatPyBlog",
            "site_url": settings.SITE_URL,
            "unsubscribe_url": f"{settings.SITE_URL}/unsubscribe/",
        },
    )
    text_content = strip_tags(html_content)  # Plain text version

    # Create email message
    email_message = EmailMultiAlternatives(
        subject, text_content, from_email, [to_email]
    )
    email_message.attach_alternative(html_content, "text/html")

    # Send email asynchronously if configured
    if settings.SEND_EMAILS_ASYNC:
        print(f"📧 QUEUING WELCOME EMAIL TO: {to_email}")
        Thread(target=send_async_email, args=(email_message,)).start()
    else:
        try:
            print(f"📧 SENDING WELCOME EMAIL TO: {to_email}")
            email_message.send()
            logger.info(f"Welcome email sent to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send welcome email: {str(e)}")
            return False


def send_new_post_notification(post, subscribers):
    """Send notification about new post to all subscribers."""
    subject = f"New Post on FatPyBlog: {post.title}"
    from_email = settings.DEFAULT_FROM_EMAIL

    # Process the post content with markdown to HTML
    rendered_content = process_markdown_for_email(post.content)

    # Create context for email template
    context = {
        "post_title": post.title,
        "post_summary": post.content[:200] + "..."
        if len(post.content) > 200
        else post.content,
        "post_content": rendered_content,  # Add the fully rendered content
        "post_url": f"{settings.SITE_URL}/post/{post.pk}/",
        "site_name": "FatPyBlog",
        "unsubscribe_url": f"{settings.SITE_URL}/unsubscribe/",
    }

    # Process all subscribers
    success_count = 0
    failed_count = 0

    # Simple header for post notification emails
    print(
        f"📨 SENDING POST NOTIFICATION | TITLE: {post.title} | TO: {subscribers.count()} SUBSCRIBERS"
    )

    for subscriber in subscribers:
        # Create HTML content from template
        html_content = render_to_string(
            "blog/emails/new_post_notification.html",
            {**context, "subscriber_email": subscriber.email},
        )
        text_content = strip_tags(html_content)

        # Create email message
        email_message = EmailMultiAlternatives(
            subject, text_content, from_email, [subscriber.email]
        )
        email_message.attach_alternative(html_content, "text/html")

        # Send email asynchronously if configured
        if settings.SEND_EMAILS_ASYNC:
            Thread(target=send_async_email, args=(email_message,)).start()
            success_count += 1
        else:
            try:
                email_message.send()
                success_count += 1
            except Exception as e:
                logger.error(
                    f"Failed to send notification to {subscriber.email}: {str(e)}"
                )
                failed_count += 1

    logger.info(
        f"New post notifications sent: {success_count} succeeded, {failed_count} failed"
    )
    return success_count, failed_count
