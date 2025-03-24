from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse
from blog.utils.icon_paths import get_icon_path

register = template.Library()


@register.inclusion_tag("blog/partials/_button.html")
def render_button(url, text, type="primary", size=None, icon=None, args=None):
    """Render a styled button with optional icon

    Args:
        url: The button's destination URL
        text: The button's label text
        type: Button type (primary, outline, danger)
        size: Button size (sm, lg)
        icon: Bootstrap icon name
        args: Arguments for URL reversing (optional)
    """
    icon_path = get_icon_path(icon) if icon else ""

    # Process URL with args if provided
    if args is not None:
        if isinstance(args, (list, tuple)):
            url = reverse(url, args=args)
        else:
            url = reverse(url, args=[args])

    return {
        "url": url,
        "text": text,
        "type": type,
        "size": size,
        "icon": icon,
        "icon_path": icon_path,
    }


@register.inclusion_tag("blog/partials/_alert.html")
def render_alert(message, type="info", heading=None):
    """Render an alert box

    Args:
        message: The alert message
        type: Alert type (success, error, warning, info)
        heading: Optional alert heading
    """
    return {
        "message": message,
        "type": type,
        "heading": heading,
    }


@register.inclusion_tag("blog/partials/_tag.html")
def render_tag(tag_name):
    """Render a tag

    Args:
        tag_name: The tag text
    """
    return {"tag_name": tag_name}


@register.inclusion_tag("blog/partials/_content_card.html")
def render_content_card(title, body, footer=None, card_class=None):
    """Render a content card

    Args:
        title: Card title
        body: Card body content (HTML safe)
        footer: Optional card footer content (HTML safe)
        card_class: Optional CSS class for the card
    """
    return {
        "title": title,
        "body": body,
        "footer": footer,
        "card_class": card_class,
    }


@register.inclusion_tag("blog/partials/_empty_state.html")
def render_empty_state(title, message, action_content=None, icon=None):
    """Render an empty state placeholder

    Args:
        title: Main title text
        message: Descriptive message
        action_content: Optional HTML content for action buttons
        icon: Bootstrap icon class
    """
    icon_path = get_icon_path(icon) if icon else ""

    return {
        "title": title,
        "message": message,
        "action_content": action_content,
        "icon": icon,
        "icon_path": icon_path,
    }


@register.inclusion_tag("blog/partials/_feature_item.html")
def render_feature_item(title, description, icon_class):
    """Render a feature item with icon

    Args:
        title: Feature title
        description: Feature description
        icon_class: Bootstrap icon class
    """
    icon_path = get_icon_path(icon_class) if icon_class else ""

    return {
        "title": title,
        "description": description,
        "icon_class": icon_class,
        "icon_path": icon_path,
    }


@register.inclusion_tag("blog/partials/_link_card.html")
def render_link_card(url, text, icon_class, new_tab=True):
    """Render a link card with icon

    Args:
        url: Link destination
        text: Link text
        icon_class: Bootstrap icon class
        new_tab: Whether to open in new tab (default True)
    """
    icon_path = get_icon_path(icon_class) if icon_class else ""

    return {
        "url": url,
        "text": text,
        "icon_class": icon_class,
        "icon_path": icon_path,
        "new_tab": new_tab,
    }


@register.inclusion_tag("blog/partials/_post_item.html")
def render_post_item(post):
    """Render a post list item

    Args:
        post: The Post object to display
    """
    return {
        "post": post,
    }


@register.inclusion_tag("blog/partials/_post_actions.html")
def render_post_actions(post, request):
    """Render post action buttons

    Args:
        post: The Post object
        request: The request object for user permission checks
    """
    return {
        "post": post,
        "request": request,
    }


@register.inclusion_tag("blog/partials/_related_posts.html")
def render_related_posts(related_posts):
    """Render related posts section

    Args:
        related_posts: List of related Post objects
    """
    return {
        "related_posts": related_posts,
    }


@register.inclusion_tag("blog/partials/_nav_menu.html")
def render_nav_menu(request):
    """Render navigation menu dropdown

    Args:
        request: The request object
    """
    return {
        "request": request,
    }


@register.inclusion_tag("blog/partials/_account_menu.html")
def render_account_menu(user):
    """Render account menu dropdown

    Args:
        user: The current user object
    """
    return {
        "user": user,
    }


@register.inclusion_tag("blog/partials/_search_form.html")
def render_search_form(request):
    """Render search form

    Args:
        request: The request object
    """
    return {
        "request": request,
    }
