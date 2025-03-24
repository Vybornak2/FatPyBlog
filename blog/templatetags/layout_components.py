from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag("blog/layouts/_page_header.html")
def render_page_header(title, subtitle=None, actions=None):
    """Render a standard page header with optional actions

    Args:
        title: Page title
        subtitle: Optional subtitle
        actions: Optional HTML for action buttons
    """
    return {
        "title": title,
        "subtitle": subtitle,
        "actions": actions,
    }


@register.inclusion_tag("blog/layouts/_page_section.html")
def render_page_section(title=None, body=None, css_class=None, id=None):
    """Render a page section

    Args:
        title: Section title (optional)
        body: Section content (HTML)
        css_class: Additional CSS classes
        id: HTML ID for the section
    """
    return {
        "title": title,
        "body": body,
        "css_class": css_class,
        "id": id,
    }
